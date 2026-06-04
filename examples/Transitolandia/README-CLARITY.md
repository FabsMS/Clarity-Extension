README:

<!--
  ⚠️  ATENÇÃO — README gerado automaticamente pelo CLARITY
  Antes de publicar, revise e preencha todos os campos marcados com TODO.
  Remova este bloco de comentário quando o README estiver pronto.
-->

# **ADMIN-TRANSITOLANDIA-FRONT**

> **⚠️ Aviso:** Este README foi gerado automaticamente. Revise as informações e
> preencha os campos marcados com `<!-- TODO -->` antes de publicar.

> **Desenvolvendo memória e conhecimento para a Transitolandia!**

![Licença](https://img.shields.io/badge/licen%C3%A7a-MIT-blue)
![Linguagem](https://img.shields.io/badge/linguagem-JavaScript-informational)
![Status](https://img.shields.io/badge/status-em%20desenvolvimento-yellow)

## 📋 Índice

- [Sobre](#sobre)
- [Funcionalidades](#funcionalidades)
- [Tecnologias](#tecnologias)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Pré-requisitos](#pre-requisitos)
- [Instalação](#instalacao)
- [Como Usar](#como-usar)
- [Variáveis de Ambiente](#variaveis-de-ambiente)
- [Contribuição](#contribuicao)
- [Licença](#licenca)

---

## <a id="sobre"></a>📖 Sobre

O projeto admin-transitolandia-front é uma aplicação web desenvolvida em JavaScript utilizando o framework React e a ferramenta Vite. O objetivo do sistema é fornecer uma plataforma para que os usuários possam gerenciar perguntas, jogos de memória e simulados, além de realizar login e cadastro.

O sistema resolve o problema de falta de uma plataforma unificada para a Transitolandia, permitindo que os usuários tenham acesso a conteúdo educacional e divertido de forma fácil e escalável. Além disso, o sistema é projetado para ser escalável e flexível, permitindo que novas funcionalidades sejam adicionadas facilmente.

## <a id="funcionalidades"></a>✨ Funcionalidades

- ✅ Cadastro e edição de perguntas
- ✅ Gerenciamento de jogos de memória
- ✅ Simulados para avaliação de conhecimento
- ✅ Login e cadastro de usuários
- ✅ Visualização de conteúdo educacional

## <a id="tecnologias"></a>🛠 Tecnologias

**Linguagem principal:** JavaScript

**Frameworks e Ferramentas:**

- **React** — um framework para construir interfaces de usuário
- **Vite** — uma ferramenta para desenvolvimento rápido e escalável

**Dependências principais:**

- `@emotion/styled`
- `@eslint/js`
- `@mui/icons-material`
- `@mui/material`
- `@types/react`
- `@types/react-dom`
- `@vitejs/plugin-react`
- `axios`
- `eslint`
- `eslint-plugin-react-hooks`
- `eslint-plugin-react-refresh`
- `globals`
- `js-cookie`
- `jwt-decode`
- `react`

## <a id="estrutura-do-projeto"></a>📁 Estrutura do Projeto

```
admin-transitolandia-front/
├── Notification/
│   └── (1 arquivo)
├── PrivateRoute/
│   └── (1 arquivo)
├── Sidebar/
│   └── (1 arquivo)
├── Topbar/
│   └── (1 arquivo)
├── Transitolandia/
│   ├── eslint.config.js
│   └── vite.config.js
├── contexts/
│   └── (1 arquivo)
├── hooks/
│   └── (1 arquivo)
├── pages/
│   ├── AddQuestionQuiz.jsx
│   ├── AddQuestionSimulado.jsx
│   ├── Initial.jsx
│   ├── SignIn.jsx
│   ├── UpdateQuestionQuiz.jsx
│   └── ... e mais 5 arquivo(s)
├── routes/
│   └── (1 arquivo)
├── services/
│   ├── HttpService.js
│   ├── JogoMemoriaService.js
│   ├── QuizService.js
│   └── ... e mais 2 arquivo(s)
├── src/
│   └── (1 arquivo)
└── utils/
    └── (1 arquivo)
```

**Descrição das pastas:**

- `Notification`: responsável por notificar os usuários sobre novos conteúdos ou atualizações
- `PrivateRoute`: define rotas privadas para usuários autenticados
- `Sidebar`: gerencia a navegação lateral do sistema
- `Topbar`: gerencia a navegação superior do sistema
- `Transitolandia`: contém arquivos de configuração para o sistema

## <a id="pre-requisitos"></a>⚙️ Pré-requisitos

Antes de começar, instale as seguintes ferramentas:

- [Node.js](https://nodejs.org/) v18 ou superior
- npm v9+

## <a id="instalacao"></a>🚀 Instalação

```bash
# 1. Clone o repositório
git clone https://github.com/<SEU-USUARIO>/admin-transitolandia-front.git
cd admin-transitolandia-front

# 2. Instale as dependências
npm install
# ou: yarn install
```

> Ajuste a URL do seu projeto no github.

## <a id="como-usar"></a>💻 Como Usar

**Desenvolvimento:**

```bash
npm run dev
```

**Produção:**

```bash
npm run build
npm run preview
```

## <a id="variaveis-de-ambiente"></a>🔧 Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis:

```env
# <!-- TODO: liste aqui as variáveis de ambiente necessárias -->
# Exemplo:
# API_URL=http://localhost:3000
# SECRET_KEY=sua_chave_secreta
```

> Configure as variáveis de ambiente com as variáveis necessárias.

## <a id="contribuicao"></a>🤝 Contribuição

Contribuições são bem-vindas! Siga os passos abaixo:

1. Faça um **fork** do projeto
2. Crie uma branch para sua feature:
```bash
git checkout -b feature/minha-feature
```
3. Commit suas alterações:
```bash
git commit -m 'feat: adiciona minha feature'
```
4. Push para a branch:
```bash
git push origin feature/minha-feature
```
5. Abra um **Pull Request**

## <a id="licenca"></a>📄 Licença

Este projeto está sob a licença **MIT**. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

---

<p align="center">
  Gerado com ❤️ por <a href="https://github.com/FabsMS/Clarity-Extension">CLARITY</a>
</p>