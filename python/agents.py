import json, sys
from pathlib import Path
from typing import Iterable

from crewai import Agent, Task, Crew, Process
from dotenv import load_dotenv
from functions import MultiLanguageCodeAnalyzer
from llm_config import initialize_llms

load_dotenv()

# Initialize both LLMs with full validation
llms = initialize_llms()
analyst_llm = llms["analyst"]
writer_llm = llms["writer"]

class Create_Crew:
    # Configuração de chunking para controle de contexto
    MAX_FILES_PER_CHUNK = 15  # Máximo de arquivos por chunk
    MAX_LINES_PER_CHUNK = 5000  # Máximo de linhas por chunk
    MAX_CONTEXT_TOKENS = 8000  # Estimativa de tokens máximos (margem de segurança)

    def __init__(self):
        self.analyzer_agent = self.create_multi_language_analyzer_agent()
        self.writer_agent   = self.create_readme_writer_agent()
        self.analysis_task  = None
        self.readme_task    = None
        self.crew           = None
        self.intermediate_analyses = []  # Armazena análises intermediárias

    # ============================================
    # MÉTODOS DE CHUNKING E CONTROLE DE CONTEXTO
    # ============================================

    def _chunk_files(self, files: list) -> list:
        """
        Divide a lista de arquivos em chunks para evitar estouro de contexto

        Estratégias:
        1. Máximo de arquivos por chunk
        2. Máximo de linhas totais por chunk
        3. Agrupamento por diretório/módulo quando possível

        Returns:
            List[List[str]]: Lista de chunks, onde cada chunk é uma lista de arquivos
        """
        print(f"\n[CHUNKING] Dividindo {len(files)} arquivos em blocos...", file=sys.stderr, flush=True)

        chunks = []
        current_chunk = []
        current_lines = 0

        for file_path in files:
            try:
                # Conta linhas do arquivo
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    file_lines = sum(1 for _ in f)

                # Verifica se adicionar este arquivo excederia os limites
                would_exceed_files = len(current_chunk) >= self.MAX_FILES_PER_CHUNK
                would_exceed_lines = (current_lines + file_lines) > self.MAX_LINES_PER_CHUNK

                if would_exceed_files or would_exceed_lines:
                    # Salva chunk atual e inicia novo
                    if current_chunk:
                        chunks.append(current_chunk)
                        print(f"   Chunk {len(chunks)}: {len(current_chunk)} arquivos, ~{current_lines} linhas",
                              file=sys.stderr, flush=True)
                    current_chunk = [file_path]
                    current_lines = file_lines
                else:
                    current_chunk.append(file_path)
                    current_lines += file_lines

            except Exception as e:
                print(f"   [WARN] Erro ao processar {file_path}: {str(e)}", file=sys.stderr, flush=True)
                continue

        # Adiciona último chunk
        if current_chunk:
            chunks.append(current_chunk)
            print(f"   Chunk {len(chunks)}: {len(current_chunk)} arquivos, ~{current_lines} linhas",
                  file=sys.stderr, flush=True)

        print(f"[CHUNKING] Total: {len(chunks)} chunks criados\n", file=sys.stderr, flush=True)
        return chunks

    def _analyze_chunk(self, chunk_files: list, chunk_num: int, total_chunks: int) -> dict:
        """
        Analisa um chunk de arquivos e gera resumo intermediário

        Args:
            chunk_files: Lista de arquivos do chunk
            chunk_num: Número do chunk atual
            total_chunks: Total de chunks

        Returns:
            dict: Análise estruturada do chunk
        """
        print(f"\n[ANALYST] Processando chunk {chunk_num}/{total_chunks}...", file=sys.stderr, flush=True)

        analyzer = MultiLanguageCodeAnalyzer()
        chunk_analysis = analyzer._run(chunk_files)

        # Adiciona metadados do chunk
        chunk_analysis['_chunk_info'] = {
            'chunk_number': chunk_num,
            'total_chunks': total_chunks,
            'files_in_chunk': len(chunk_files),
            'files': [str(Path(f).name) for f in chunk_files]
        }

        print(f"[ANALYST] Chunk {chunk_num} analisado: "
              f"{chunk_analysis.get('total_linhas', 0)} linhas, "
              f"{len(chunk_analysis.get('detalhes', chunk_analysis.get('arquivos', [])))} arquivos",
              file=sys.stderr, flush=True)

        return chunk_analysis

    def _consolidate_analyses(self, chunk_analyses: list) -> dict:
        """
        Consolida múltiplas análises de chunks em uma análise unificada

        Args:
            chunk_analyses: Lista de análises de chunks

        Returns:
            dict: Análise consolidada e otimizada
        """
        print(f"\n[CONSOLIDATION] Consolidando {len(chunk_analyses)} chunks...", file=sys.stderr, flush=True)

        if not chunk_analyses:
            return {}

        if len(chunk_analyses) == 1:
            # Remove metadados de chunk se houver apenas um
            analysis = chunk_analyses[0].copy()
            if '_chunk_info' in analysis:
                del analysis['_chunk_info']
            return analysis

        # Consolida dados de todos os chunks
        from collections import defaultdict

        # Extrair metadados do primeiro chunk (nome do projeto vem do package.json)
        first_analysis = chunk_analyses[0]

        consolidated = {
            'projeto_nome': first_analysis.get('projeto_nome', first_analysis.get('projeto', None)),
            'projeto_descricao': first_analysis.get('projeto_descricao', None),
            'projeto_versao': first_analysis.get('projeto_versao', None),
            'projeto_scripts': first_analysis.get('projeto_scripts', {}),
            'total_arquivos': 0,
            'total_linhas': 0,
            'total_funcoes': 0,
            'total_classes': 0,
            'linguagens': set(),  # Será convertido para lista no final
            'arquivos': [],
            'estrutura_pastas': defaultdict(int),
            'dependencias': set(),
            'frameworks_detectados': set(),
            'padroes_arquiteturais': set(),
            'imports_principais': defaultdict(set),
            'arquivos_chave': []
        }

        # Consolida dados de cada chunk
        for analysis in chunk_analyses:
            # Total de arquivos, linhas, funções e classes
            consolidated['total_arquivos'] += analysis.get('quantidade_arquivos', 0)
            consolidated['total_linhas'] += analysis.get('total_linhas', 0)
            consolidated['total_funcoes'] += analysis.get('total_funcoes', 0)
            consolidated['total_classes'] += analysis.get('total_classes', 0)

            # Linguagens (pode ser lista ou dicionário)
            linguagens = analysis.get('linguagens', [])
            if isinstance(linguagens, list):
                consolidated['linguagens'].update(linguagens)
            elif isinstance(linguagens, dict):
                consolidated['linguagens'].update(linguagens.keys())

            # Arquivos (pode estar em 'detalhes' ou 'arquivos')
            chunk_files = analysis.get('detalhes', analysis.get('arquivos', []))
            if isinstance(chunk_files, list):
                # Limita a 5 arquivos mais importantes por chunk
                for file_info in chunk_files[:5]:
                    if isinstance(file_info, dict):
                        consolidated['arquivos'].append({
                            'caminho': file_info.get('arquivo', file_info.get('caminho', '')),
                            'linguagem': file_info.get('linguagem', ''),
                            'linhas': file_info.get('linhas', 0),
                            'funcoes': file_info.get('funcoes', 0),
                            'classes': file_info.get('classes', 0)
                        })

            # Estrutura de pastas
            if 'estrutura_pastas' in analysis:
                estrutura = analysis.get('estrutura_pastas', {})
                if isinstance(estrutura, dict):
                    for folder, count in estrutura.items():
                        consolidated['estrutura_pastas'][folder] += count

            # Dependências
            if 'dependencias' in analysis:
                deps = analysis.get('dependencias', [])
                if isinstance(deps, (list, set)):
                    consolidated['dependencias'].update(deps)

            # Frameworks
            if 'frameworks_detectados' in analysis:
                frameworks = analysis.get('frameworks_detectados', [])
                if isinstance(frameworks, (list, set)):
                    consolidated['frameworks_detectados'].update(frameworks)

            # Padrões arquiteturais
            if 'padroes_arquiteturais' in analysis:
                patterns = analysis.get('padroes_arquiteturais', [])
                if isinstance(patterns, (list, set)):
                    consolidated['padroes_arquiteturais'].update(patterns)

            # Imports principais
            if 'imports_principais' in analysis:
                imports = analysis.get('imports_principais', {})
                if isinstance(imports, dict):
                    for lang, imps in imports.items():
                        if isinstance(imps, (list, set)):
                            consolidated['imports_principais'][lang].update(imps)

            # Arquivos-chave
            if 'arquivos_chave' in analysis:
                chave = analysis.get('arquivos_chave', [])
                if isinstance(chave, list):
                    consolidated['arquivos_chave'].extend(chave)

        # Converte sets/defaultdicts para listas/dicts para JSON
        consolidated['linguagens'] = sorted(list(consolidated['linguagens']))
        consolidated['dependencias'] = sorted(list(consolidated['dependencias']))
        consolidated['frameworks_detectados'] = sorted(list(consolidated['frameworks_detectados']))
        consolidated['padroes_arquiteturais'] = sorted(list(consolidated['padroes_arquiteturais']))
        consolidated['estrutura_pastas'] = dict(consolidated['estrutura_pastas'])
        consolidated['imports_principais'] = {
            lang: sorted(list(imps))[:15]  # Top 15 por linguagem
            for lang, imps in consolidated['imports_principais'].items()
        }
        consolidated['arquivos_chave'] = list(set(consolidated['arquivos_chave']))[:10]  # Deduplica e limita

        print(f"[CONSOLIDATION] Análise consolidada: "
              f"{consolidated['total_arquivos']} arquivos, "
              f"{consolidated['total_linhas']} linhas, "
              f"{len(consolidated['linguagens'])} linguagens",
              file=sys.stderr, flush=True)

        return consolidated

    def _generate_technical_report(self, consolidated_analysis: dict) -> str:
        """
        Gera relatório técnico estruturado a partir da análise consolidada

        Este relatório é otimizado para o Writer LLM (llama3:8b)

        Returns:
            str: Relatório técnico formatado em JSON
        """
        print(f"\n[REPORT] Gerando relatório técnico estruturado...", file=sys.stderr, flush=True)

        # Processa linguagens (pode ser lista ou dicionário)
        linguagens = consolidated_analysis.get('linguagens', [])
        if isinstance(linguagens, list):
            linguagens_principais = linguagens[:5]  # Top 5 linguagens
        elif isinstance(linguagens, dict):
            linguagens_principais = dict(sorted(
                linguagens.items(),
                key=lambda x: x[1],
                reverse=True
            )[:5])
        else:
            linguagens_principais = []

        # Cria relatório otimizado focando nos aspectos mais importantes
        # Para chunk único, _run() retorna 'quantidade_arquivos' e 'detalhes'
        # Para multi-chunk, _consolidate_analyses() unifica em 'total_arquivos' e 'arquivos'
        total_arquivos = (
            consolidated_analysis.get('total_arquivos') or
            consolidated_analysis.get('quantidade_arquivos', 0)
        )
        detalhes_arquivos = (
            consolidated_analysis.get('arquivos') or
            consolidated_analysis.get('detalhes', [])
        )

        report = {
            'projeto_nome': consolidated_analysis.get('projeto_nome', consolidated_analysis.get('projeto', 'Projeto')),
            'projeto_descricao': consolidated_analysis.get('projeto_descricao', None),
            'projeto_versao': consolidated_analysis.get('projeto_versao', None),
            'projeto_scripts': consolidated_analysis.get('projeto_scripts', {}),
            'visao_geral': {
                'total_arquivos': total_arquivos,
                'total_linhas': consolidated_analysis.get('total_linhas', 0),
                'total_funcoes': consolidated_analysis.get('total_funcoes', 0),
                'total_classes': consolidated_analysis.get('total_classes', 0),
                'linguagens_principais': linguagens_principais
            },
            'tecnologias': {
                'frameworks': consolidated_analysis.get('frameworks_detectados', [])[:10],
                'dependencias_principais': consolidated_analysis.get('dependencias', [])[:20],
                'imports_principais': consolidated_analysis.get('imports_principais', {})
            },
            'arquitetura': {
                'padroes': consolidated_analysis.get('padroes_arquiteturais', []),
                'estrutura_pastas': consolidated_analysis.get('estrutura_pastas', {}),
                'arquivos_chave': consolidated_analysis.get('arquivos_chave', [])[:10]
            },
            'detalhes_arquivos': detalhes_arquivos[:15]
        }

        # Pre-build ASCII directory tree — incluído no prompt como bloco literal
        # para que o modelo copie diretamente, sem risco de reformatação errada
        report['arvore_diretorios'] = self._build_ascii_tree(
            str(report.get('projeto_nome') or 'projeto'),
            consolidated_analysis.get('estrutura_pastas', {}),
            detalhes_arquivos
        )

        report_json = json.dumps(report, ensure_ascii=False, indent=2)
        report_size  = len(report_json)
        estimated_tokens = report_size // 4

        print(f"[REPORT] Relatório gerado: {report_size} caracteres (~{estimated_tokens} tokens)",
              file=sys.stderr, flush=True)

        # DEBUG: Mostrar o JSON que será enviado ao Writer LLM
        print(f"\n[DEBUG] JSON ENVIADO AO WRITER LLM:", file=sys.stderr, flush=True)
        print(f"{report_json[:500]}..." if len(report_json) > 500 else report_json,
              file=sys.stderr, flush=True)
        print(f"", file=sys.stderr, flush=True)

        if estimated_tokens > self.MAX_CONTEXT_TOKENS:
            print(f"[WARN] Relatório pode ser grande para contexto. Considere otimização adicional.",
                  file=sys.stderr, flush=True)

        return report_json

    def _build_ascii_tree(self, nome_projeto: str, estrutura_pastas: dict, detalhes_arquivos: list) -> str:
        """
        Constrói uma árvore ASCII de diretórios a partir dos dados de análise.

        Usa os caminhos reais de `detalhes_arquivos` para mostrar arquivos dentro
        de cada pasta. Quando há mais arquivos do que os listados, exibe
        "... e mais N arquivo(s)".
        """
        from pathlib import Path

        nome_str = str(nome_projeto or "projeto")
        lines = [f"{nome_str}/"]

        # Mapeia pasta → arquivos reais vistos em detalhes_arquivos
        folder_files: dict = {}
        root_files: list = []

        for file_info in detalhes_arquivos:
            caminho = file_info.get('caminho', '')
            if not caminho:
                continue
            p = Path(caminho)
            parent = p.parent.name
            if parent == nome_str or parent == '':
                root_files.append(p.name)
            else:
                folder_files.setdefault(parent, []).append(p.name)

        # Une pastas com contagem (estrutura_pastas) e pastas com arquivos reais
        all_folders = sorted(set(list(estrutura_pastas.keys()) + list(folder_files.keys())))

        total_items = len(root_files) + len(all_folders)
        item_idx = 0

        for filename in root_files:
            item_idx += 1
            is_last = (item_idx == total_items)
            lines.append(f"{'└── ' if is_last else '├── '}{filename}")

        for folder in all_folders:
            item_idx += 1
            is_last_folder = (item_idx == total_items)
            f_prefix = "└── " if is_last_folder else "├── "
            c_prefix = "    " if is_last_folder else "│   "

            count = estrutura_pastas.get(folder, len(folder_files.get(folder, [])))
            files = sorted(folder_files.get(folder, []))

            lines.append(f"{f_prefix}{folder}/")

            if files:
                remaining = max(0, count - len(files))
                for j, fname in enumerate(files):
                    is_last_file = (j == len(files) - 1)
                    if is_last_file and remaining > 0:
                        lines.append(f"{c_prefix}├── {fname}")
                        lines.append(f"{c_prefix}└── ... e mais {remaining} arquivo(s)")
                    else:
                        lines.append(f"{c_prefix}{'└── ' if is_last_file else '├── '}{fname}")
            else:
                suffix = f"{count} arquivo{'s' if count != 1 else ''}"
                lines.append(f"{c_prefix}└── ({suffix})")

        return "\n".join(lines)

    # ============================================
    # MÉTODOS ORIGINAIS (AGENTES E TASKS)
    # ============================================

    def create_multi_language_analyzer_agent(self):
        """
        Cria o agente de análise usando deepseek-coder:6.7b

        Este agente é responsável por:
        - Receber o contexto da análise já realizada
        - Entender a estrutura do projeto
        - Passar informações para o próximo agente

        Nota: A análise real é feita ANTES pelo código Python diretamente,
        este agente apenas recebe e contextualiza os resultados.
        """
        return Agent(
            role="Analista de Código Multilinguagem",
            goal="Entender e contextualizar a análise do projeto",
            backstory=(
                "Você é um especialista em análise de código com domínio em várias linguagens. "
                "Você recebe análises técnicas detalhadas e as compreende completamente. "
                "Foque em precisão técnica e detalhes arquiteturais."
            ),
            tools=[],  # Sem ferramentas - análise já foi feita pelo código Python
            verbose=True,
            allow_delegation=False,
            llm=analyst_llm  # deepseek-coder:6.7b (temperatura 0.1)
        )

    def create_readme_writer_agent(self):
        """
        Cria o agente de escrita usando llama3:8b.
        Sem ferramentas (tools=[]) para evitar o loop ReAct do CrewAI,
        que chamaria o ReadmeGeneratorTool com o formato errado e geraria lixo.
        """
        return Agent(
            role="Escritor de Documentação Técnica",
            goal="Gerar um README.md completo em Português do Brasil usando APENAS os dados JSON fornecidos na tarefa.",
            backstory=(
                "Você é um escritor técnico especializado em documentação de software. "
                "Você transforma dados de análise de código em documentação clara e precisa. "
                "Você NUNCA inventa informações — usa somente o que está nos dados fornecidos."
            ),
            tools=[],  # SEM ferramentas — o modelo gera diretamente sem loop ReAct
            verbose=True,
            allow_delegation=False,
            llm=writer_llm
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
        """
        Pré-preenche em Python tudo que vem do JSON (nome, linguagem, frameworks,
        dependências, árvore, comandos, pré-requisitos) e deixa para o modelo
        APENAS as partes criativas: tagline, descrição, features e desc. de pastas.
        Isso evita que o modelo fique com [CAMPO] literais no output.
        """
        try:
            data = json.loads(analysis_json)
        except Exception:
            data = {}

        # ── Extrair campos do JSON ──────────────────────────────────────────
        nome       = data.get('projeto_nome') or 'Projeto'
        visao      = data.get('visao_geral', {})
        linguagens = visao.get('linguagens_principais', [])
        frameworks = data.get('tecnologias', {}).get('frameworks', [])
        deps       = data.get('tecnologias', {}).get('dependencias_principais', [])[:15]
        desc_orig  = data.get('projeto_descricao') or ''

        # Mapear extensão de arquivo → nome legível para badge e texto
        _lang_map = {
            'ts': 'TypeScript', 'tsx': 'TypeScript',
            'js': 'JavaScript', 'jsx': 'JavaScript',
            'py': 'Python', 'java': 'Java',
        }
        lang = _lang_map.get(linguagens[0].lower(), linguagens[0]) if linguagens else 'TypeScript'

        # ── Seções pré-montadas ─────────────────────────────────────────────
        frameworks_md = (
            '\n'.join(
                f'- **{f}** — [escreva uma linha sobre o papel deste framework]'
                for f in frameworks
            ) if frameworks else '- *(não detectados)*'
        )
        deps_md = (
            '\n'.join(f'- `{d}`' for d in deps) if deps else '- *(não detectadas)*'
        )

        # ── Inferir comandos e pré-requisitos ───────────────────────────────
        _is_python = any(l.lower() in ('py', 'python') for l in linguagens)
        _scripts   = data.get('projeto_scripts', {})  # scripts reais do package.json

        if _is_python:
            cmd_dev  = 'python main.py'
            cmd_prod = 'python main.py'
            prereq   = '- [Python](https://python.org/) 3.10 ou superior\n- pip'
        elif _scripts:
            # Usa os scripts reais do package.json
            _has_dev     = 'dev'     in _scripts
            _has_start   = 'start'   in _scripts
            _has_build   = 'build'   in _scripts
            _has_preview = 'preview' in _scripts
            _has_android = 'android' in _scripts  
            _has_ios     = 'ios'     in _scripts  

            # Comando de desenvolvimento
            if _has_dev:
                cmd_dev = 'npm run dev'
            elif _has_start:
                cmd_dev = 'npm start'
            else:
                cmd_dev = 'npm run dev'

            # Comando de produção/build
            if _has_build and _has_preview:
                cmd_prod = 'npm run build\nnpm run preview'
            elif _has_build and _has_start:
                cmd_prod = 'npm run build\nnpm start'
            elif _has_build:
                cmd_prod = 'npm run build'
            else:
                cmd_prod = cmd_dev  # fallback: mesmo comando

            # Se for Expo (tem android/ios ou "start" contém "expo")
            _start_val = _scripts.get('start', '')
            if _has_android or _has_ios or 'expo' in _start_val.lower():
                cmd_dev  = 'npm start'
                cmd_prod = (
                    'npm run android  # Android\n'
                    'npm run ios      # iOS\n'
                    'npm run web      # Web'
                ) if (_has_android and _has_ios) else cmd_prod

            prereq = '- [Node.js](https://nodejs.org/) v18 ou superior\n- npm v9+'
        elif 'Next.js' in frameworks:
            cmd_dev  = 'npm run dev'
            cmd_prod = 'npm run build\nnpm start'
            prereq   = '- [Node.js](https://nodejs.org/) v18 ou superior\n- npm v9+'
        elif 'Vite' in frameworks:
            cmd_dev  = 'npm run dev'
            cmd_prod = 'npm run build\nnpm run preview'
            prereq   = '- [Node.js](https://nodejs.org/) v18 ou superior\n- npm v9+'
        elif 'React' in frameworks:
            cmd_dev  = 'npm start'
            cmd_prod = 'npm run build'
            prereq   = '- [Node.js](https://nodejs.org/) v16 ou superior\n- npm v8+'
        elif 'Express' in frameworks:
            cmd_dev  = 'node index.js'
            cmd_prod = 'node index.js'
            prereq   = '- [Node.js](https://nodejs.org/) v18 ou superior\n- npm v9+'
        else:
            cmd_dev  = 'npm run dev'
            cmd_prod = 'npm run build'
            prereq   = '- [Node.js](https://nodejs.org/) v18 ou superior\n- npm v9+'

        # ── Árvore de diretórios (pré-computada) ────────────────────────────
        _arvore = data.get('arvore_diretorios', '')
        arvore_md = f'```\n{_arvore}\n```' if _arvore else '*(estrutura não detectada)*'

        # ── Extrair nomes de arquivos e imports para inferência de domínio ───
        _detalhes  = data.get('detalhes_arquivos', [])
        _arq_chave = data.get('arquitetura', {}).get('arquivos_chave', [])
        _imports   = data.get('tecnologias', {}).get('imports_principais', {})

        # Stems dos arquivos revelam o domínio (Login, Dashboard, Cart, Relatorio…)
        _GENERICOS = {
            'index', 'main', 'app', 'config', 'setup', '__init__', 'types',
            'utils', 'helpers', 'constants', 'globals', 'vite-env', 'env',
        }
        _stems: list[str] = []
        for _f in _detalhes:
            _stem = Path(_f.get('caminho', '')).stem
            if _stem and _stem.lower() not in _GENERICOS:
                _stems.append(_stem)
        for _f in _arq_chave:
            _stem = Path(_f).stem
            if _stem and _stem.lower() not in _GENERICOS and _stem not in _stems:
                _stems.append(_stem)

        # Imports externos únicos (sem relativos e sem escopos @)
        _ext_imports: set[str] = set()
        for _lang_imps in _imports.values():
            for _imp in _lang_imps[:15]:
                if not _imp.startswith('.') and not _imp.startswith('/'):
                    _ext_imports.add(_imp.split('/')[0])

        # Pastas do projeto
        _pastas = list(data.get('arquitetura', {}).get('estrutura_pastas', {}).keys())

        # ── Resumo rico para orientar o modelo nas partes criativas ──────────
        resumo = (
            f"Nome: {nome}\n"
            f"Linguagem: {lang}\n"
            f"Frameworks: {', '.join(frameworks) if frameworks else 'nenhum'}\n"
            f"Dependências: {', '.join(deps[:10]) if deps else 'nenhuma'}\n"
        )
        if _stems:
            resumo += f"Arquivos do projeto: {', '.join(_stems[:35])}\n"
        if _ext_imports:
            resumo += f"Imports externos: {', '.join(sorted(_ext_imports)[:15])}\n"
        if _pastas:
            resumo += f"Pastas: {', '.join(_pastas)}\n"
        if desc_orig:
            resumo += f"Descrição original: {desc_orig}\n"

        # ── Template pré-preenchido (modelo só toca nos campos [...]) ─────────
        template = (
            "<!--\n"
            "  ⚠️  ATENÇÃO — README gerado automaticamente pelo CLARITY\n"
            "  Antes de publicar, revise e preencha todos os campos marcados com TODO.\n"
            "  Remova este bloco de comentário quando o README estiver pronto.\n"
            "-->\n\n"
            f"# **{nome.upper()}**\n\n"
            "> **⚠️ Aviso:** Este README foi gerado automaticamente. Revise as informações e\n"
            "> preencha os campos marcados com `<!-- TODO -->` antes de publicar.\n\n"
            "> [TAGLINE]\n\n"
            f"![Licença](https://img.shields.io/badge/licen%C3%A7a-MIT-blue)\n"
            f"![Linguagem](https://img.shields.io/badge/linguagem-{lang}-informational)\n"
            f"![Status](https://img.shields.io/badge/status-em%20desenvolvimento-yellow)\n\n"
            "## 📋 Índice\n\n"
            "- [Sobre](#sobre)\n"
            "- [Funcionalidades](#funcionalidades)\n"
            "- [Tecnologias](#tecnologias)\n"
            "- [Estrutura do Projeto](#estrutura-do-projeto)\n"
            "- [Pré-requisitos](#pre-requisitos)\n"
            "- [Instalação](#instalacao)\n"
            "- [Como Usar](#como-usar)\n"
            "- [Variáveis de Ambiente](#variaveis-de-ambiente)\n"
            "- [Contribuição](#contribuicao)\n"
            "- [Licença](#licenca)\n\n"
            "---\n\n"
            "## <a id=\"sobre\"></a>📖 Sobre\n\n"
            "[DESCRICAO]\n\n"
            "## <a id=\"funcionalidades\"></a>✨ Funcionalidades\n\n"
            "[FUNCIONALIDADES]\n\n"
            "## <a id=\"tecnologias\"></a>🛠 Tecnologias\n\n"
            f"**Linguagem principal:** {lang}\n\n"
            "**Frameworks e Ferramentas:**\n\n"
            f"{frameworks_md}\n\n"
            "**Dependências principais:**\n\n"
            f"{deps_md}\n\n"
            "## <a id=\"estrutura-do-projeto\"></a>📁 Estrutura do Projeto\n\n"
            f"{arvore_md}\n\n"
            "[DESCRICAO_PASTAS]\n\n"
            "## <a id=\"pre-requisitos\"></a>⚙️ Pré-requisitos\n\n"
            "Antes de começar, instale as seguintes ferramentas:\n\n"
            f"{prereq}\n\n"
            "## <a id=\"instalacao\"></a>🚀 Instalação\n\n"
            "```bash\n"
            "# 1. Clone o repositório\n"
            f"git clone https://github.com/<SEU-USUARIO>/{nome}.git\n"
            f"cd {nome}\n\n"
            "# 2. Instale as dependências\n"
            "npm install\n"
            "# ou: yarn install\n"
            "```\n\n"
            "> Ajuste a URL do seu projeto no github.\n\n"
            "## <a id=\"como-usar\"></a>💻 Como Usar\n\n"
            "**Desenvolvimento:**\n\n"
            "```bash\n"
            f"{cmd_dev}\n"
            "```\n\n"
            "**Produção:**\n\n"
            "```bash\n"
            f"{cmd_prod}\n"
            "```\n\n"
            "## <a id=\"variaveis-de-ambiente\"></a>🔧 Variáveis de Ambiente\n\n"
            "Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis:\n\n"
            "```env\n"
            "# <!-- TODO: liste aqui as variáveis de ambiente necessárias -->\n"
            "# Exemplo:\n"
            "# API_URL=http://localhost:3000\n"
            "# SECRET_KEY=sua_chave_secreta\n"
            "```\n\n"
            "> Configure as variáveis de ambiente com as variáveis necessárias.\n\n"
            "## <a id=\"contribuicao\"></a>🤝 Contribuição\n\n"
            "Contribuições são bem-vindas! Siga os passos abaixo:\n\n"
            "1. Faça um **fork** do projeto\n"
            "2. Crie uma branch para sua feature:\n"
            "```bash\n"
            "git checkout -b feature/minha-feature\n"
            "```\n"
            "3. Commit suas alterações:\n"
            "```bash\n"
            "git commit -m 'feat: adiciona minha feature'\n"
            "```\n"
            "4. Push para a branch:\n"
            "```bash\n"
            "git push origin feature/minha-feature\n"
            "```\n"
            "5. Abra um **Pull Request**\n\n"
            "## <a id=\"licenca\"></a>📄 Licença\n\n"
            "Este projeto está sob a licença **MIT**. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.\n\n"
            "---\n\n"
            "<p align=\"center\">\n"
            "  Gerado com ❤️ por <a href=\"https://github.com/FabsMS/Clarity-Extension\">CLARITY</a>\n"
            "</p>\n"
        )

        return Task(
            description=(
                "Preencha os campos marcados com [...] no README abaixo. "
                "Escreva em Português do Brasil. "
                "Mantenha todo o resto EXATAMENTE como está — não altere nomes, URLs, badges, âncoras nem blocos de código.\n\n"
                "DADOS DO PROJETO (use para orientar o texto criativo):\n"
                + resumo + "\n"
                "CAMPOS A PREENCHER:\n"
                "- [TAGLINE]: frase curta e específica sobre ESTE projeto (máx. 15 palavras). Use o nome e os arquivos para inferir o domínio.\n"
                "- [DESCRICAO]: Escreva 3 parágrafos LONGOS e ESPECÍFICOS — cada um com pelo menos 3-4 frases completas:\n"
                "  Parágrafo 1 — Propósito: O que é o projeto e qual problema real ele resolve. "
                "Deduza pelo nome: 'admin-xxx' → painel de gestão; 'ecommerce' → loja virtual; 'transitolandia' → sistema de trânsito. "
                "Cite o nome do projeto e o contexto de negócio. Mínimo 3 frases.\n"
                "  Parágrafo 2 — Módulos e funcionalidades: Descreva de forma narrativa o que o sistema faz, "
                "baseando-se nos nomes dos arquivos fornecidos (Login, Dashboard, Relatorio, Cart, Pagamento, etc.). "
                "Cite os módulos específicos que você encontrou. Mínimo 4 frases.\n"
                "  Parágrafo 3 — Tecnologia e público-alvo: Para quem foi desenvolvido e como as tecnologias escolhidas "
                "beneficiam o usuário (performance, usabilidade, manutenibilidade). Mínimo 2 frases.\n"
                "  PROIBIDO usar: 'aplicação rápida e escalável', 'visa criar', 'resolve o problema de desenvolver', "
                "'facilidade e eficiência', qualquer frase genérica que sirva para qualquer projeto.\n"
                "- [FUNCIONALIDADES]: 5 a 7 funcionalidades ESPECÍFICAS e CONCRETAS deduzidas dos arquivos. "
                "Cada item deve descrever uma feature real do sistema, não uma tecnologia: "
                "ex. Login.tsx → '✅ Sistema de autenticação e controle de acesso'; "
                "Dashboard.tsx → '✅ Painel de controle com visão geral do sistema'; "
                "Relatorio.tsx → '✅ Geração e visualização de relatórios'; "
                "Cart.tsx → '✅ Carrinho de compras com persistência'. "
                "Formato: `- ✅ Descrição concreta da funcionalidade`\n"
                "- [DESCRICAO_PASTAS]: uma linha por pasta da árvore explicando sua finalidade\n"
                "- Nos Frameworks e Ferramentas: substitua `[escreva uma linha sobre o papel deste framework]` pela descrição real\n\n"
                "README:\n\n"
                + template
            ),
            expected_output="README.md completo com todos os campos [...] preenchidos e o resto inalterado.",
            agent=self.writer_agent,
            return_direct=True
        )

    def _create_crew(self):
        """
        Cria o Crew apenas com o Writer Agent (llama3:8b).

        O Analyst Agent foi removido do Crew porque:
        - A análise estática já é feita em Python antes desta etapa
        - O deepseek-coder rejeita tarefas em português, gerando "I'm sorry..."
        - Esse output de recusa vira contexto do escritor no modo sequencial,
          fazendo o writer ignorar o JSON e alucinar o README inteiro.
        """
        return Crew(
            agents=[self.writer_agent],
            tasks=[self.readme_task],
            process=Process.sequential,
            verbose=True
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
        """
        Gera documentação usando fluxo otimizado com chunking

        Fluxo:
        1. Projeto → Chunks
        2. Chunks → Analyst (DeepSeek) → Análises intermediárias
        3. Análises → Consolidação → Relatório técnico estruturado
        4. Relatório → Writer (Llama3) → README-CLARITY.md

        Returns:
            dict: Resultado da geração com status e output
        """
        print(f"\n{'='*60}", file=sys.stderr, flush=True)
        print(f"INICIANDO GERAÇÃO DE DOCUMENTAÇÃO COM FLUXO OTIMIZADO", file=sys.stderr, flush=True)
        print(f"{'='*60}\n", file=sys.stderr, flush=True)

        # FASE 1: Expansão e Chunking
        files = self._expand_files(files_or_dir)
        print(f"[FASE 1] Arquivos coletados: {len(files)}", file=sys.stderr, flush=True)

        if not files:
            raise ValueError("Nenhum arquivo encontrado para análise")

        # Divide em chunks se necessário
        if len(files) > self.MAX_FILES_PER_CHUNK:
            print(f"[FASE 1] Projeto grande detectado. Ativando modo chunking...", file=sys.stderr, flush=True)
            chunks = self._chunk_files(files)
        else:
            print(f"[FASE 1] Projeto pequeno. Processamento direto...", file=sys.stderr, flush=True)
            chunks = [files]

        # FASE 2: Análise com Analyst (DeepSeek)
        print(f"\n{'─'*60}", file=sys.stderr, flush=True)
        print(f"[FASE 2] ANÁLISE COM ANALYST LLM (deepseek-coder:6.7b)", file=sys.stderr, flush=True)
        print(f"{'─'*60}", file=sys.stderr, flush=True)

        chunk_analyses = []
        for i, chunk in enumerate(chunks, 1):
            chunk_analysis = self._analyze_chunk(chunk, i, len(chunks))
            chunk_analyses.append(chunk_analysis)

        # FASE 3: Consolidação
        print(f"\n{'─'*60}", file=sys.stderr, flush=True)
        print(f"[FASE 3] CONSOLIDAÇÃO DE ANÁLISES", file=sys.stderr, flush=True)
        print(f"{'─'*60}", file=sys.stderr, flush=True)

        consolidated_analysis = self._consolidate_analyses(chunk_analyses)

        # FASE 4: Geração de Relatório Técnico
        print(f"\n{'─'*60}", file=sys.stderr, flush=True)
        print(f"[FASE 4] GERAÇÃO DE RELATÓRIO TÉCNICO ESTRUTURADO", file=sys.stderr, flush=True)
        print(f"{'─'*60}", file=sys.stderr, flush=True)

        technical_report = self._generate_technical_report(consolidated_analysis)

        # FASE 5: Geração de README com Writer (Llama3)
        print(f"\n{'─'*60}", file=sys.stderr, flush=True)
        print(f"[FASE 5] GERAÇÃO DE README COM WRITER LLM (llama3:8b)", file=sys.stderr, flush=True)
        print(f"{'─'*60}\n", file=sys.stderr, flush=True)

        # Monta tasks (apenas o writer — a análise já foi feita em Python)
        self.readme_task = self.create_readme_task(technical_report)
        self.crew        = self._create_crew()

        # Executa geração final
        try:
            print(f"[WRITER] Processando relatório técnico e gerando README...", file=sys.stderr, flush=True)

            result = self.crew.kickoff()
            readme_markdown = self._extract_output(result)

            print(f"[SUCCESS] Documentação gerada com sucesso", file=sys.stderr, flush=True)

            # Remove wrapper ```markdown ... ``` que o modelo às vezes adiciona em volta do output
            if readme_markdown:
                stripped = readme_markdown.strip()
                if stripped.startswith("```"):
                    lines = stripped.splitlines()
                    # remove primeira linha (```markdown, ```md, ``` etc.)
                    lines = lines[1:]
                    # remove última linha se for ```
                    if lines and lines[-1].strip() == "```":
                        lines = lines[:-1]
                    readme_markdown = "\n".join(lines)

            print(f"\n{'='*60}", file=sys.stderr, flush=True)
            print(f"DOCUMENTAÇÃO GERADA COM SUCESSO", file=sys.stderr, flush=True)
            print(f"{'='*60}\n", file=sys.stderr, flush=True)

            return {
                "status": "success",
                "arquivos_analisados": files,
                "chunks_processados": len(chunks),
                "total_linhas": consolidated_analysis.get('total_linhas', 0),
                "output": readme_markdown
            }

        except Exception as e:
            print(f"\n[ERROR] Erro durante execução: {str(e)[:200]}", file=sys.stderr, flush=True)
            raise
