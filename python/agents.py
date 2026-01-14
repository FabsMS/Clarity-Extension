import os, json, sys, time
from pathlib import Path
from typing import Iterable

from crewai import Agent, Task, Crew, Process, LLM
from dotenv import load_dotenv
from functions import MultiLanguageCodeAnalyzer, ReadmeGeneratorTool

load_dotenv()

# Global para gerenciar rotação de chaves
class GroqKeyManager:
    def __init__(self):
        self.api_keys = []  # Lista de tuplas: (nome, chave, modelo)
        self.current_key_index = 0
        self.load_keys()

    def load_keys(self):
        """Carrega todas as chaves disponíveis do .env com seus modelos específicos"""
        # Modelos Groq PRODUCTION ATIVOS (verificados 2025-01-13 - documentação oficial)
        # APENAS 2 modelos de geração de texto estão ativos:
        # - llama-3.1-8b-instant: 250K TPM, 1K RPM
        # - llama-3.3-70b-versatile: 300K TPM, 1K RPM
        # Estratégia: Alternar entre os 2 modelos disponíveis
        # DESCONTINUADOS: llama-3.1-70b-versatile, mixtral-8x7b-32768, gemma2-9b-it
        available_models = [
            "llama-3.1-8b-instant",        # Primary: mais rápido (560 T/sec)
            "llama-3.3-70b-versatile",     # Fallback 1: mais poderoso (280 T/sec)
            "llama-3.1-8b-instant",        # Fallback 2: volta ao rápido (chave diferente = rate limit diferente)
        ]

        primary_key = os.getenv("GROQ_API_KEY")
        primary_model = os.getenv("LLM_MODEL") or os.getenv("GROQ_MODEL_PRIMARY") or available_models[0]
        if primary_key:
            self.api_keys.append(("primary", primary_key, primary_model))

        fallback1 = os.getenv("GROQ_API_KEY_FALLBACK_1")
        fallback1_model = os.getenv("GROQ_MODEL_FALLBACK_1") or available_models[1]
        if fallback1:
            self.api_keys.append(("fallback_1", fallback1, fallback1_model))

        fallback2 = os.getenv("GROQ_API_KEY_FALLBACK_2")
        fallback2_model = os.getenv("GROQ_MODEL_FALLBACK_2") or available_models[2]
        if fallback2:
            self.api_keys.append(("fallback_2", fallback2, fallback2_model))

        if not self.api_keys:
            raise ValueError("Nenhuma GROQ_API_KEY encontrada no .env")

        print(f"[INFO] Carregadas {len(self.api_keys)} chaves Groq com modelos:", file=sys.stderr, flush=True)
        for name, _, model in self.api_keys:
            print(f"       - {name}: {model}", file=sys.stderr, flush=True)

    def get_current_key(self):
        """Retorna a chave e modelo atual"""
        if not self.api_keys:
            return None, None, None
        return self.api_keys[self.current_key_index]

    def rotate_key(self):
        """Rotaciona para a próxima chave"""
        if len(self.api_keys) <= 1:
            return False

        old_index = self.current_key_index
        self.current_key_index = (self.current_key_index + 1) % len(self.api_keys)

        old_name = self.api_keys[old_index][0]
        new_name = self.api_keys[self.current_key_index][0]

        print(f"[ROTATE] Rotacionando chave: {old_name} -> {new_name}", file=sys.stderr, flush=True)
        return True

    def has_more_keys(self):
        """Verifica se ainda há chaves para tentar"""
        return len(self.api_keys) > 1

# Instância global do gerenciador de chaves
key_manager = GroqKeyManager()


def get_llm():
    """
    Get LLM instance based on configuration in .env
    Supports: Groq, Gemini, OpenAI, and more
    """
    provider = os.getenv("LLM_PROVIDER", "groq").lower()
    temperature = float(os.getenv("LLM_TEMPERATURE", "0.1"))

    print(f"[LLM] Configurando LLM: {provider}", file=sys.stderr, flush=True)

    try:
        if provider == "groq":
            # Groq (Fast & Free) com rotação automática de chaves E MODELOS
            # IMPORTANTE: Cada chave usa um modelo diferente para ter rate limits independentes

            # Tenta todas as chaves disponíveis
            max_retries = len(key_manager.api_keys)
            last_error = None

            for attempt in range(max_retries):
                key_name, api_key, model_name = key_manager.get_current_key()

                try:
                    print(f"   [KEY] Tentando chave Groq: {key_name} (tentativa {attempt + 1}/{max_retries})", file=sys.stderr, flush=True)
                    print(f"   [MODEL] Modelo: groq/{model_name}", file=sys.stderr, flush=True)

                    llm_instance = LLM(
                        model=f"groq/{model_name}",
                        api_key=api_key,
                        temperature=temperature
                    )

                    print(f"   [OK] Chave {key_name} com modelo {model_name} configurada com sucesso", file=sys.stderr, flush=True)
                    return llm_instance

                except Exception as e:
                    error_msg = str(e).lower()
                    print(f"   [ERROR] Erro ao configurar chave {key_name}: {str(e)[:100]}", file=sys.stderr, flush=True)

                    if 'rate limit' in error_msg or 'quota' in error_msg:
                        print(f"   [WARN] Chave {key_name} (modelo {model_name}) atingiu rate limit", file=sys.stderr, flush=True)
                        last_error = e

                        # Tenta próxima chave se houver
                        if key_manager.rotate_key():
                            print(f"   [RETRY] Tentando proxima chave com modelo diferente...", file=sys.stderr, flush=True)
                            continue
                        else:
                            break
                    else:
                        # Erro não relacionado a rate limit, re-raise
                        raise

            # Se chegou aqui, todas as chaves falharam
            raise Exception(f"Todas as chaves Groq atingiram o rate limit. Aguarde 1 minuto. Erro: {last_error}")

        elif provider == "gemini":
            # Google Gemini
            api_key = os.getenv("GEMINI_API_KEY")
            if not api_key:
                raise ValueError("GEMINI_API_KEY não encontrada no .env")

            model_name = os.getenv("LLM_MODEL") or "gemini-1.5-flash"
            print(f"   Modelo: gemini/{model_name}", flush=True)

            return LLM(
                model=f"gemini/{model_name}",
                api_key=api_key,
                temperature=temperature
            )

        elif provider == "openai":
            # OpenAI
            api_key = os.getenv("OPENAI_API_KEY")
            if not api_key:
                raise ValueError("OPENAI_API_KEY não encontrada no .env")

            model_name = os.getenv("LLM_MODEL") or "gpt-3.5-turbo"
            print(f"   Modelo: {model_name}", flush=True)

            return LLM(
                model=model_name,
                api_key=api_key,
                temperature=temperature
            )

        else:
            raise ValueError(f"Provedor não suportado: {provider}")

    except Exception as e:
        print(f"⚠️  Erro ao configurar {provider}: {str(e)}", flush=True)

        # Try fallback provider
        fallback_provider = os.getenv("LLM_FALLBACK_PROVIDER", "").lower()

        if fallback_provider and fallback_provider != provider:
            print(f"🔄 Tentando fallback: {fallback_provider}", flush=True)

            try:
                if fallback_provider == "gemini":
                    api_key = os.getenv("GEMINI_API_KEY")
                    if api_key:
                        return LLM(
                            model="gemini/gemini-1.5-flash",
                            api_key=api_key,
                            temperature=temperature
                        )

                elif fallback_provider == "groq":
                    api_key = os.getenv("GROQ_API_KEY")
                    if api_key:
                        return LLM(
                            model="groq/llama-3.3-70b-versatile",
                            api_key=api_key,
                            temperature=temperature
                        )

            except Exception as fallback_error:
                print(f"❌ Fallback também falhou: {str(fallback_error)}", flush=True)

        # Re-raise original error if no fallback works
        raise


# Initialize LLM
llm = get_llm()
print(f"[OK] LLM configurado com sucesso\n", file=sys.stderr, flush=True)

class Create_Crew:
    def __init__(self):
        self.analyzer_agent = self.create_multi_language_analyzer_agent()
        self.writer_agent   = self.create_readme_writer_agent()
        self.analysis_task  = None
        self.readme_task    = None
        self.crew           = None

    def create_multi_language_analyzer_agent(self):
        return Agent(
            role="Analista de Código Multilinguagem",
            goal="Analisar todos os arquivos de um projeto e extrair informações estruturadas",
            backstory=("Você é um especialista em análise de código com domínio em várias linguagens. "
                       "Gere uma visão abrangente da estrutura e lógica do sistema."),
            tools=[MultiLanguageCodeAnalyzer()],
            verbose=True,
            allow_delegation=False,
            llm=llm
        )

    def create_readme_writer_agent(self):
        return Agent(
            role="Senior Technical Writer & Documentation Architect",
            goal=(
                "Criar documentação README.md de nível enterprise, seguindo os mais altos padrões "
                "de empresas como Google, Microsoft, Meta, Netflix e AWS. O README deve ser "
                "extremamente profissional, detalhado, acessível e servir como referência da indústria."
            ),
            backstory=(
                "Você é um Technical Writer sênior com 15+ anos de experiência documentando "
                "projetos open-source e enterprise de empresas Fortune 500. Seus READMEs são "
                "conhecidos por serem excepcionalmente claros, completos e profissionais. "
                "Você tem expertise em comunicação técnica, arquitetura de software, UX writing "
                "e conhece profundamente as melhores práticas de documentação da indústria. "
                "Seus READMEs são frequentemente usados como referência e modelo para outras equipes."
            ),
            tools=[ReadmeGeneratorTool()],
            verbose=True,
            allow_delegation=False,
            llm=llm
        )

    # --- normaliza entrada (lista de arquivos, arquivo único ou diretório) ---
    def _expand_files(self, files_or_dir):
        if isinstance(files_or_dir, str):
            p = Path(files_or_dir)
            if p.is_dir():
                analyzer = MultiLanguageCodeAnalyzer()
                return analyzer._collect_files(p)
            if p.is_file():
                return [str(p)]
            return []
        if isinstance(files_or_dir, Iterable):
            return [str(Path(x)) for x in files_or_dir if str(x).strip()]
        return []

    # --- gera a análise determinística + resumo e JSON para o redator ---
    def _build_analysis_and_summary(self, files):
        analyzer = MultiLanguageCodeAnalyzer()
        analysis_dict = analyzer._run(files)                 # dados reais
        summary_text  = analyzer.summarize_analysis(analysis_dict, max_files=10)
        analysis_json = json.dumps(analysis_dict, ensure_ascii=False)
        return analysis_dict, analysis_json, summary_text

    def create_analysis_task(self, summary_text: str):
        # apenas fornece contexto; output curto e direto
        return Task(
            description=(
                "Contexto técnico da análise do projeto (não gere README aqui):\n\n"
                f"{summary_text}\n\n"
                "Responda apenas: 'Contexto entendido.'"
            ),
            expected_output="Contexto entendido.",
            agent=self.analyzer_agent,
            return_direct=True
        )

    def create_readme_task(self, analysis_json: str):
        return Task(
            description=(
                "# MISSÃO: Criar um README.md de Nível Enterprise\n\n"
                "Crie um README.md EXCEPCIONAL que seria aprovado pelas equipes de documentação do "
                "Google, Microsoft, Meta, Netflix e AWS. Use EXCLUSIVAMENTE os dados JSON fornecidos abaixo.\n\n"

                "## REGRAS CRÍTICAS:\n"
                "❌ PROIBIDO inventar informações não presentes no JSON\n"
                "❌ PROIBIDO usar URLs ou links externos fictícios\n"
                "✅ Use APENAS informações reais extraídas do código\n"
                "✅ Seja EXTREMAMENTE descritivo e profissional\n"
                "✅ Escreva parágrafos completos e bem elaborados\n\n"

                "## DADOS DO PROJETO:\n```json\n" + analysis_json + "\n```\n\n"

                "## ESTRUTURA OBRIGATÓRIA (Markdown profissional):\n\n"

                "### 1. CABEÇALHO (Header)\n"
                "- Logo/Banner (use emoji se não houver logo): 🏥 para saúde, 📱 para mobile, 💼 para business, etc.\n"
                "- Nome do projeto em H1\n"
                "- Tagline/slogan impactante (1-2 frases que capturam a essência)\n"
                "- Badges relevantes e profissionais (linguagens, build status, licença, etc.)\n"
                "- Descrição executiva (2-3 parágrafos): O QUE é, POR QUE existe, PARA QUEM é\n\n"

                "### 2. HIGHLIGHTS (Destaques)\n"
                "- Seção '✨ Key Features' ou '🎯 Highlights'\n"
                "- 4-6 features principais com descrições de 1-2 linhas cada\n"
                "- Use emojis apropriados para cada feature\n\n"

                "### 3. ÍNDICE (Table of Contents)\n"
                "- Links para todas as seções principais\n"
                "- Bem organizado e fácil de navegar\n\n"

                "### 4. SOBRE O PROJETO (About)\n"
                "- Seção '📖 About' ou '🎯 Overview'\n"
                "- 3-5 parágrafos explicando:\n"
                "  * Contexto e motivação\n"
                "  * Problema que resolve\n"
                "  * Como funciona (visão geral)\n"
                "  * Público-alvo\n"
                "  * Diferenciais\n\n"

                "### 5. DEMO/SCREENSHOTS (se aplicável)\n"
                "- Seção '🎬 Demo' ou '📸 Screenshots'\n"
                "- Mencione onde encontrar demos/screenshots\n\n"

                "### 6. TECNOLOGIAS (Tech Stack)\n"
                "- Seção '🛠️ Built With' ou '⚡ Tech Stack'\n"
                "- Liste TODAS as linguagens detectadas\n"
                "- Frameworks e bibliotecas principais identificados\n"
                "- Ferramentas e tecnologias\n"
                "- Inclua breve explicação do porquê de cada escolha (quando óbvio)\n\n"

                "### 7. ARQUITETURA (Architecture)\n"
                "- Seção '🏗️ Architecture' ou '📐 System Design'\n"
                "- Explicação detalhada da estrutura do projeto\n"
                "- Padrões arquiteturais identificados\n"
                "- Fluxo de dados (se identificável)\n"
                "- Componentes principais e suas responsabilidades\n"
                "- Diagramas em texto/Mermaid se necessário\n\n"

                "### 8. ESTRUTURA DE PASTAS (Project Structure)\n"
                "- Seção '📁 Project Structure'\n"
                "- Árvore de diretórios formatada\n"
                "- Explicação detalhada de cada pasta/arquivo importante\n"
                "- Convenções de organização usadas\n\n"

                "### 9. PRIMEIROS PASSOS (Getting Started)\n"
                "- Seção '🚀 Getting Started'\n"
                "- Subseções detalhadas:\n"
                "  * **Prerequisites** (requisitos de sistema, ferramentas, versões)\n"
                "  * **Installation** (passo a passo completo e claro)\n"
                "  * **Configuration** (variáveis de ambiente, configs)\n"
                "  * **Running** (como executar dev, build, prod)\n\n"

                "### 10. USO (Usage)\n"
                "- Seção '💻 Usage' ou '📚 How to Use'\n"
                "- Exemplos práticos e detalhados\n"
                "- Casos de uso comuns\n"
                "- Snippets de código (quando relevante)\n"
                "- Explicações passo a passo\n\n"

                "### 11. API/COMPONENTES (se aplicável)\n"
                "- Seção '📡 API Documentation' ou '🧩 Components'\n"
                "- Documentação dos principais endpoints/componentes\n"
                "- Parâmetros, retornos, exemplos\n\n"

                "### 12. DESENVOLVIMENTO (Development)\n"
                "- Seção '👨‍💻 Development'\n"
                "- Como configurar ambiente de desenvolvimento\n"
                "- Scripts disponíveis\n"
                "- Convenções de código\n"
                "- Como debugar\n\n"

                "### 13. TESTES (Testing)\n"
                "- Seção '🧪 Testing'\n"
                "- Estratégia de testes\n"
                "- Como rodar testes\n"
                "- Cobertura de testes\n\n"

                "### 14. DEPLOYMENT (se aplicável)\n"
                "- Seção '🚢 Deployment'\n"
                "- Como fazer deploy\n"
                "- Ambientes disponíveis\n"
                "- CI/CD pipeline\n\n"

                "### 15. CONTRIBUINDO (Contributing)\n"
                "- Seção '🤝 Contributing'\n"
                "- Guidelines claros para contribuidores\n"
                "- Processo de PR\n"
                "- Code of Conduct\n"
                "- Como reportar bugs\n\n"

                "### 16. ROADMAP (se aplicável)\n"
                "- Seção '🗺️ Roadmap'\n"
                "- Features planejadas\n"
                "- Melhorias futuras\n\n"

                "### 17. FAQ\n"
                "- Seção '❓ FAQ' ou '💡 Troubleshooting'\n"
                "- Problemas comuns e soluções\n"
                "- Dicas e truques\n\n"

                "### 18. LICENÇA (License)\n"
                "- Seção '📄 License'\n"
                "- Tipo de licença (inferir do projeto ou usar MIT por padrão)\n\n"

                "### 19. CONTATO/SUPORTE (Contact)\n"
                "- Seção '📞 Support' ou '💬 Contact'\n"
                "- Canais de comunicação\n"
                "- Links relevantes\n\n"

                "### 20. AGRADECIMENTOS (Acknowledgments)\n"
                "- Seção '🙏 Acknowledgments'\n"
                "- Créditos e agradecimentos\n"
                "- Inspirações\n\n"

                "## DIRETRIZES DE ESTILO:\n"
                "1. **Tom Profissional**: Claro, direto, confiante mas acessível\n"
                "2. **Parágrafos Completos**: Mínimo 3-4 linhas por seção importante\n"
                "3. **Detalhamento**: Seja MUITO descritivo, não economize em explicações\n"
                "4. **Formatação**: Use negrito, itálico, listas, code blocks apropriadamente\n"
                "5. **Emojis**: Use com moderação e profissionalismo (apenas em títulos)\n"
                "6. **Clareza**: Escreva para que até iniciantes entendam\n"
                "7. **Completude**: Não deixe seções importantes vazias\n"
                "8. **Engajamento**: Faça o leitor querer usar o projeto\n\n"

                "## EXEMPLOS DE REFERÊNCIA:\n"
                "Inspire-se em READMEs de:\n"
                "- React.js (facebook/react)\n"
                "- TensorFlow (tensorflow/tensorflow)\n"
                "- VS Code (microsoft/vscode)\n"
                "- Node.js (nodejs/node)\n"
                "- Kubernetes (kubernetes/kubernetes)\n\n"

                "## OUTPUT FINAL:\n"
                "Retorne SOMENTE o conteúdo Markdown do README, sem explicações adicionais.\n"
                "O README deve ter NO MÍNIMO 400 linhas de conteúdo rico e profissional."
            ),
            expected_output=(
                "Um README.md excepcional, completo e profissional com no mínimo 400 linhas, "
                "seguindo os mais altos padrões da indústria, extremamente detalhado e bem estruturado."
            ),
            agent=self.writer_agent,
            return_direct=True
        )

    def _create_crew(self):
        return Crew(
            agents=[self.analyzer_agent, self.writer_agent],
            tasks=[self.analysis_task, self.readme_task],
            process=Process.sequential,
            verbose=True,
            llm=llm
        )

    # --- extração robusta do resultado do Crew ---
    def _extract_output(self, result):
        if result is None:
            return None
        if isinstance(result, str):
            return result
        for attr in ("output", "raw", "result", "final_output"):
            if hasattr(result, attr):
                val = getattr(result, attr)
                if val:
                    return val
        if isinstance(result, dict):
            return result.get("output") or result.get("result")
        return str(result)

    def generate_documentation(self, files_or_dir) -> dict:
        files = self._expand_files(files_or_dir)
        analysis_dict, analysis_json, summary_text = self._build_analysis_and_summary(files)

        # monta tasks
        self.analysis_task = self.create_analysis_task(summary_text)
        self.readme_task   = self.create_readme_task(analysis_json)
        self.crew          = self._create_crew()

        # executa com retry automático em caso de rate limit
        max_retries = len(key_manager.api_keys)
        max_retry_cycles = 3  # Tenta até 3 ciclos completos de todas as chaves
        last_error = None
        cycle = 0

        while cycle < max_retry_cycles:
            for attempt in range(max_retries):
                try:
                    key_name, _, model_name = key_manager.get_current_key()
                    cycle_info = f"ciclo {cycle + 1}/{max_retry_cycles}, " if max_retry_cycles > 1 else ""
                    print(f"\n[EXEC] Executando documentacao com chave: {key_name} + modelo: {model_name} ({cycle_info}tentativa {attempt + 1}/{max_retries})", file=sys.stderr, flush=True)

                    result = self.crew.kickoff()
                    readme_markdown = self._extract_output(result)

                    # Se sucesso, sai do loop
                    print(f"[SUCCESS] Documentacao gerada com sucesso usando chave: {key_name}", file=sys.stderr, flush=True)

                    # Fallback: se vier vazio ou incoerente, gera deterministicamente pela tool
                    if (not readme_markdown) or str(readme_markdown).strip() in {"None", "null", ""}:
                        readme_markdown = ReadmeGeneratorTool().run(analysis_json)

                    # Se o modelo disser "Sem Código" mas há linhas > 0, força correção via tool
                    if "Projeto Sem Código" in (readme_markdown or "") and analysis_dict.get("total_linhas", 0) > 0:
                        readme_markdown = ReadmeGeneratorTool().run(analysis_json)

                    return {
                        "status": "success",
                        "arquivos_analisados": files,
                        "analise_resumida": summary_text,
                        "output": readme_markdown
                    }

                except Exception as e:
                    error_msg = str(e).lower()
                    last_error = e

                    print(f"[ERROR] Erro durante execucao: {str(e)[:200]}", file=sys.stderr, flush=True)

                    # Verifica se é erro de rate limit
                    if 'rate limit' in error_msg or 'quota' in error_msg or 'ratelimit' in error_msg:
                        print(f"[WARN] Rate limit detectado na chave {key_name}", file=sys.stderr, flush=True)

                        # Tenta rotacionar para próxima chave
                        if attempt < max_retries - 1:
                            if key_manager.rotate_key():
                                print(f"[RETRY] Tentando novamente com proxima chave...", file=sys.stderr, flush=True)

                                # Recria o crew com a nova chave
                                global llm
                                llm = get_llm()
                                self.analyzer_agent = self.create_multi_language_analyzer_agent()
                                self.writer_agent = self.create_readme_writer_agent()
                                self.analysis_task = self.create_analysis_task(summary_text)
                                self.readme_task = self.create_readme_task(analysis_json)
                                self.crew = self._create_crew()

                                continue
                        else:
                            # Todas as chaves do ciclo atual falharam
                            if cycle < max_retry_cycles - 1:
                                wait_time = 65  # 65 segundos para garantir que o rate limit resetou
                                print(f"[WAIT] Todas as chaves atingiram rate limit. Aguardando {wait_time}s antes do proximo ciclo...", file=sys.stderr, flush=True)

                                # Mostra contador de espera
                                for remaining in range(wait_time, 0, -5):
                                    print(f"[WAIT] Aguardando... {remaining}s restantes", file=sys.stderr, flush=True)
                                    time.sleep(5)

                                print(f"[RETRY] Iniciando novo ciclo de tentativas...", file=sys.stderr, flush=True)

                                # Reset para primeira chave
                                key_manager.current_key_index = 0

                                # Recria o crew com a primeira chave
                                llm = get_llm()
                                self.analyzer_agent = self.create_multi_language_analyzer_agent()
                                self.writer_agent = self.create_readme_writer_agent()
                                self.analysis_task = self.create_analysis_task(summary_text)
                                self.readme_task = self.create_readme_task(analysis_json)
                                self.crew = self._create_crew()

                                break  # Sai do for para incrementar o ciclo
                            else:
                                print(f"[FAIL] Todas as tentativas foram esgotadas", file=sys.stderr, flush=True)
                                raise Exception(f"Todas as chaves atingiram rate limit apos {max_retry_cycles} ciclos: {last_error}")
                    else:
                        # Erro não é rate limit, re-raise imediatamente
                        print(f"[FAIL] Erro nao relacionado a rate limit, abortando", file=sys.stderr, flush=True)
                        raise

            # Incrementa o ciclo apenas se saiu do loop por break (todas chaves falharam)
            if last_error and ('rate limit' in str(last_error).lower() or 'quota' in str(last_error).lower()):
                cycle += 1
            else:
                break

        # Se chegou aqui sem retornar, todas as tentativas falharam
        raise Exception(f"Falha apos {max_retry_cycles} ciclos completos: {last_error}")
