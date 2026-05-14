# 🤖 Clarity - AI-Powered Documentation Generator

![Version](https://img.shields.io/badge/version-0.0.5-blue.svg)
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
- 🔧 **100% Offline**: Funciona localmente com Ollama, sem necessidade de APIs externas
- 📦 **Integrado**: Funciona direto no VS Code
- 🆓 **Gratuito**: Totalmente gratuito e privado, seus dados não saem da sua máquina

## 🏗️ Arquitetura Multi-Modelo

O Clarity utiliza uma arquitetura avançada com **dois modelos especializados**:

### 1. **Analyst LLM** - `deepseek-coder:6.7b`
- 🎯 **Responsabilidade**: Análise técnica precisa do código
- 🌡️ **Temperatura**: 0.1 (preciso e determinístico)
- 💡 **Especialização**: Identificação de padrões arquiteturais, estrutura do código e detalhes técnicos
- ⚙️ **Função**: Gerar análise estruturada do projeto

### 2. **Writer LLM** - `llama3:8b`
- 📝 **Responsabilidade**: Geração do README final
- 🌡️ **Temperatura**: 0.4 (criativo e fluido)
- 💡 **Especialização**: Linguagem natural, documentação clara e envolvente
- ⚙️ **Função**: Transformar análise técnica em documentação profissional

**Benefícios da arquitetura multi-modelo:**
- ✅ Análise técnica mais precisa com modelo especializado em código
- ✅ Documentação mais clara e legível com modelo especializado em escrita
- ✅ Separação de responsabilidades para melhor qualidade final
- ✅ Funcionamento 100% offline sem dependências externas

## 🔄 Fluxo de Processamento Otimizado

O Clarity implementa um **fluxo inteligente com chunking** para lidar com projetos de qualquer tamanho:

```
📦 PROJETO
    ↓
[FASE 1] Coleta e Chunking
    ├─ Divide arquivos em blocos (chunks)
    ├─ Máx: 15 arquivos por chunk
    └─ Máx: 5000 linhas por chunk
    ↓
[FASE 2] Análise com Analyst LLM (deepseek-coder:6.7b)
    ├─ Processa cada chunk separadamente
    ├─ Gera análise intermediária estruturada
    └─ Temperatura: 0.1 (análise precisa)
    ↓
[FASE 3] Consolidação
    ├─ Mescla análises de todos os chunks
    ├─ Deduplica informações
    └─ Otimiza dados para contexto
    ↓
[FASE 4] Relatório Técnico Estruturado
    ├─ Cria relatório JSON otimizado
    ├─ Limita tamanho para evitar estouro de contexto
    └─ Foca em informações mais relevantes
    ↓
[FASE 5] Geração de README com Writer LLM (llama3:8b)
    ├─ Recebe relatório técnico consolidado
    ├─ Gera documentação profissional
    └─ Temperatura: 0.4 (escrita criativa)
    ↓
📄 README-CLARITY.md
```

### Vantagens do Fluxo Otimizado:

🚀 **Escalabilidade**: Processa projetos de qualquer tamanho sem estouro de memória
🎯 **Precisão**: Cada chunk recebe atenção focada do Analyst LLM
🧩 **Consolidação Inteligente**: Mescla informações preservando o essencial
⚡ **Performance**: Processamento eficiente mesmo em projetos grandes
🛡️ **Controle de Contexto**: Previne erros por limite de tokens excedido

## 📊 Status do Projeto

**Versão:** 0.0.5 (Beta)
**Status:** 🟢 Em desenvolvimento ativo
**Última atualização:** Maio 2026

---

<div align="center">

**⭐ Se este projeto foi útil, considere dar uma estrela no GitHub!**

</div>
