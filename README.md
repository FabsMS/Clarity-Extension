# 🤖 Clarity - AI-Powered Documentation Generator

![Version](https://img.shields.io/badge/version-0.0.1-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Python](https://img.shields.io/badge/python-3.11+-blue.svg)
![Node](https://img.shields.io/badge/node-20.x-green.svg)
![VS Code](https://img.shields.io/badge/VS%20Code-Extension-007ACC.svg)

**Clarity** é uma extensão inteligente para **Visual Studio Code** que utiliza **IA (Inteligência Artificial)** para analisar automaticamente seu código-fonte e gerar documentação técnica completa e estruturada (README.md).

**Desenvolvido como Trabalho de Conclusão de Curso (TCC)**

---

## ✨ Características

- 🤖 **Análise com IA**: Usa modelos de linguagem (LLMs) para entender seu código
- 🔍 **Multi-linguagem**: Suporta Python, JavaScript, TypeScript, JSX, TSX e Java
- ⚡ **Rápido e fácil**: Um comando gera toda a documentação
- 🎯 **Inteligente**: Detecta automaticamente tipo de projeto (React, Flask, Spring, etc.)
- 🔧 **Configurável**: Suporte para múltiplos provedores de IA (Gemini, Groq, OpenAI, etc.)
- 📦 **Integrado**: Funciona direto no VS Code
- 🆓 **Gratuito**: Usa APIs gratuitas de IA por padrão

---

## 🚀 Início Rápido

### 1. Pré-requisitos

Certifique-se de ter instalado:

- **[Python 3.11+](https://www.python.org/downloads/)**
- **[Node.js 20.x](https://nodejs.org/)**
- **[Visual Studio Code](https://code.visualstudio.com/)**

### 2. Instalação

```bash
# Clone o repositório
git clone https://github.com/FabsMS/fabsms-clarity.git
cd fabsms-clarity

# Instale dependências Node.js
npm install

# Crie ambiente virtual Python
python -m venv .venv

# Ative o ambiente virtual
# Windows:
.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate

# Instale dependências Python
pip install -r requirements.txt
```

### 3. Configurar API Key

```bash
# Copie o arquivo de exemplo
cp .env.example .env

# Edite .env e adicione sua chave de API
# Recomendado: Groq (grátis e rápido)
# Obtenha em: https://console.groq.com
```

**Exemplo de `.env`:**
```env
GROQ_API_KEY=sua_chave_groq_aqui
LLM_PROVIDER=groq
LLM_MODEL=llama-3.3-70b-versatile
```

📖 **[Guia completo de API Keys](docs/API_KEYS_GUIDE.md)** - Como obter chaves gratuitas

### 4. Executar

1. Abra o projeto no VS Code
2. Pressione `F5` para abrir janela de debug
3. Na nova janela, abra seu projeto
4. Pressione `Ctrl+Shift+P` (ou `Cmd+Shift+P` no Mac)
5. Digite: **"Gerar Documentação com Clarity"**
6. Aguarde enquanto a IA analisa seu código
7. README-CLARITY.md será gerado automaticamente!

---

## 🎯 Como Funciona

```
┌─────────────────────────────────────────────────────────┐
│  1. Usuário executa comando no VS Code                 │
└─────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────┐
│  2. Extensão coleta arquivos do projeto                │
│     • Python: Análise AST                               │
│     • JS/TS/Java: Análise Regex                         │
│     • Extrai: funções, classes, imports, deps          │
└─────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────┐
│  3. Sistema Multi-Agente (CrewAI)                       │
│     • Analyzer Agent: Entende contexto                  │
│     • Writer Agent: Gera README                         │
└─────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────┐
│  4. LLM processa e gera documentação                    │
│     • Gemini / Groq / OpenAI / etc                      │
│     • Temperatura: 0.1 (mais determinístico)            │
└─────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────┐
│  5. README-CLARITY.md salvo no projeto                  │
│     • Seções: Descrição, Instalação, Uso, API          │
│     • Formatação Markdown profissional                  │
└─────────────────────────────────────────────────────────┘
```

---

## 🛠️ Tecnologias

### Frontend (Extensão VS Code)
- **TypeScript 5.8.3** - Linguagem principal
- **VS Code Extension API** - Integração com editor
- **Node.js 20.x** - Runtime

### Backend (Motor de IA)
- **Python 3.11** - Linguagem backend
- **CrewAI 0.159.0** - Framework multi-agente
- **LangChain 0.3.27** - Framework LLM
- **ChromaDB 0.5.23** - Banco de dados vetorial
- **BeautifulSoup4** - Parsing HTML/XML

### LLMs Suportados
- ✅ **Groq** (Llama 3.3, Llama 3.1, Mixtral) - Grátis, muito rápido
- ✅ **Google Gemini** 1.5 Flash/Pro - Grátis
- ✅ **OpenAI** GPT-4/3.5 - Pago
- ✅ **Hugging Face** (modelos opensource) - Grátis
- ✅ **Ollama** (local) - Grátis, offline
- ✅ **Anthropic Claude** - Pago

---

## 📋 Linguagens Suportadas

| Linguagem | Método de Análise | Status |
|-----------|-------------------|--------|
| Python | AST (Abstract Syntax Tree) | ✅ Completo |
| JavaScript | Regex avançado | ✅ Completo |
| TypeScript | Regex avançado | ✅ Completo |
| JSX/TSX | Regex avançado | ✅ Completo |
| Java | Regex avançado | ✅ Completo |

**Detecta automaticamente:**
- Flask API, Django, FastAPI, Streamlit (Python)
- React, Vue, Angular, Node.js API (JavaScript/TypeScript)
- Spring Boot, Java Application (Java)

---

## 🎨 Exemplo de Output

```markdown
# Meu Projeto Incrível

**Uma API REST construída com Flask para gerenciar usuários**

## Características

- Autenticação JWT
- CRUD de usuários
- Validação de dados
- Documentação automática

## Instalação

...
```

---

## 📂 Estrutura do Projeto

```
fabsms-clarity/
├── .github/workflows/     # CI/CD (GitHub Actions)
│   ├── ci.yml            # Testes, lint, validações
│   └── build.yml         # Build e packaging
├── .vscode/              # Configurações VS Code
├── docs/                 # Documentação
│   └── API_KEYS_GUIDE.md # Guia de API keys
├── python/               # Backend Python
│   ├── agents.py         # Sistema multi-agente (CrewAI)
│   ├── functions.py      # Analisadores de código
│   └── main.py           # Script principal
├── src/                  # Frontend TypeScript
│   └── extension.ts      # Implementação extensão
├── .env.example          # Exemplo de configuração
├── .gitignore
├── package.json          # Dependências Node.js
├── requirements.txt      # Dependências Python (completo)
├── requirements-core.txt # Dependências principais
├── tsconfig.json         # Config TypeScript
└── README.md             # Este arquivo
```

---

## ⚙️ Configuração Avançada

### Opções do `.env`

```env
# Provedor de LLM (gemini, groq, openai, huggingface)
LLM_PROVIDER=groq

# Provedor de fallback (opcional)
LLM_FALLBACK_PROVIDER=gemini

# Modelo específico (opcional)
LLM_MODEL=llama-3.3-70b-versatile

# Temperatura (0.0-1.0, padrão: 0.1)
LLM_TEMPERATURE=0.1

# Logging verboso
VERBOSE_LOGGING=false

# Nome do arquivo de saída
OUTPUT_README_NAME=README-CLARITY.md

# Ollama (local)
USE_OLLAMA=false
OLLAMA_API_URL=http://localhost:11434
OLLAMA_MODEL=llama3.1
```

---

## 🔧 Desenvolvimento

### Estrutura de Commits

```bash
# Faça alterações
git add .
git commit -m "feat: adiciona suporte para C++"
git push
```

### Executar Testes

```bash
# Testes TypeScript
npm test

# Lint
npm run lint

# Compilar
npm run compile
```

### CI/CD

O projeto inclui workflows completos do GitHub Actions:
- ✅ Validação de estrutura de arquivos
- ✅ Linting e compilação TypeScript
- ✅ Validação de dependências Python
- ✅ Testes automatizados
- ✅ Security scan
- ✅ Build e packaging

---

## 🐛 Solução de Problemas

### Erro: "Model has been decommissioned" (Groq)
**Problema:** O modelo `llama-3.1-70b-versatile` foi descontinuado pela Groq.

**Solução:** Atualize para o novo modelo no seu `.env`:
```env
LLM_MODEL=llama-3.3-70b-versatile
```
O código já foi atualizado para usar o modelo correto por padrão.

### Erro: "API key not found"
**Solução:** Configure o arquivo `.env` com sua chave de API.
📖 [Ver guia completo](docs/API_KEYS_GUIDE.md)

### Erro: "Module not found"
**Solução:**
```bash
pip install -r requirements.txt
```

### Erro: "Python not found"
**Solução:** Certifique-se que o ambiente virtual está ativo:
```bash
# Windows
.venv\Scripts\activate

# Linux/Mac
source .venv/bin/activate
```

### Extensão não aparece no VS Code
**Solução:** Pressione `F5` no VS Code com o projeto aberto.

---

## 🤝 Contribuindo

Contribuições são bem-vindas! Por favor:

1. Fork o projeto
2. Crie uma branch (`git checkout -b feature/MinhaFeature`)
3. Commit suas mudanças (`git commit -m 'feat: adiciona MinhaFeature'`)
4. Push para a branch (`git push origin feature/MinhaFeature`)
5. Abra um Pull Request

---

## 📝 Roadmap

- [ ] Suporte para mais linguagens (Go, Rust, C#)
- [ ] Interface de configuração visual no VS Code
- [ ] Cache de análise para projetos grandes
- [ ] Geração incremental (atualizar README existente)
- [ ] Suporte para documentação de APIs (OpenAPI/Swagger)
- [ ] Publicação no VS Code Marketplace
- [ ] Telemetria e analytics
- [ ] Modo interativo (escolher seções do README)

---

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para detalhes.

---

## 👥 Autores

**FabsMS** - Desenvolvedor Principal
- GitHub: [@FabsMS](https://github.com/FabsMS)

**Projeto TCC** - Trabalho de Conclusão de Curso

---

## 🙏 Agradecimentos

- [CrewAI](https://github.com/joaomdmoura/crewAI) - Framework multi-agente
- [LangChain](https://www.langchain.com/) - Framework LLM
- [Groq](https://groq.com/) - API de IA rápida e gratuita
- [Google Gemini](https://ai.google.dev/) - API de IA do Google
- Comunidade VS Code Extension Development

---

## 📚 Links Úteis

- **Documentação:** [docs/API_KEYS_GUIDE.md](docs/API_KEYS_GUIDE.md)
- **Issues:** https://github.com/FabsMS/fabsms-clarity/issues
- **Discussões:** https://github.com/FabsMS/fabsms-clarity/discussions

---

## 📊 Status do Projeto

**Versão:** 0.0.1 (Beta)
**Status:** 🟢 Em desenvolvimento ativo
**Última atualização:** Janeiro 2026

---

<div align="center">

**⭐ Se este projeto foi útil, considere dar uma estrela no GitHub!**

**Made with ❤️ and 🤖 AI**

</div>
