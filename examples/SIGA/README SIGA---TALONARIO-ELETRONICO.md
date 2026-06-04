<p align="center">
    <img src="https://raw.githubusercontent.com/PKief/vscode-material-icon-theme/ec559a9f6bfd399b82bb44393651661b08aaf7ba/icons/folder-markdown-open.svg" align="center" width="30%">
</p>
<p align="center"><h1 align="center">SIGA---TALONARIO-ELETRONICO</h1></p>
<p align="center">
	<em><code>❯ REPLACE-ME</code></em>
</p>
<p align="center">
	<img src="https://img.shields.io/github/license/FabsMS/SIGA---Talonario-Eletronico?style=default&logo=opensourceinitiative&logoColor=white&color=0080ff" alt="license">
	<img src="https://img.shields.io/github/last-commit/FabsMS/SIGA---Talonario-Eletronico?style=default&logo=git&logoColor=white&color=0080ff" alt="last-commit">
	<img src="https://img.shields.io/github/languages/top/FabsMS/SIGA---Talonario-Eletronico?style=default&color=0080ff" alt="repo-top-language">
	<img src="https://img.shields.io/github/languages/count/FabsMS/SIGA---Talonario-Eletronico?style=default&color=0080ff" alt="repo-language-count">
</p>
<p align="center"><!-- default option, no dependency badges. -->
</p>
<p align="center">
	<!-- default option, no dependency badges. -->
</p>
<br>

##  Table of Contents

- [ Overview](#-overview)
- [ Features](#-features)
- [ Project Structure](#-project-structure)
  - [ Project Index](#-project-index)
- [ Getting Started](#-getting-started)
  - [ Prerequisites](#-prerequisites)
  - [ Installation](#-installation)
  - [ Usage](#-usage)
  - [ Testing](#-testing)
- [ Project Roadmap](#-project-roadmap)
- [ Contributing](#-contributing)
- [ License](#-license)
- [ Acknowledgments](#-acknowledgments)

---

##  Overview

<code>❯ REPLACE-ME</code>

---

##  Features

<code>❯ REPLACE-ME</code>

---

##  Project Structure

```sh
└── SIGA---Talonario-Eletronico/
    ├── README.md
    ├── app
    │   ├── (private)
    │   │   ├── consultas
    │   │   │   ├── (components)
    │   │   │   │   ├── ConsultasOpcaoCard.tsx
    │   │   │   │   └── index.ts
    │   │   │   ├── condutores-detran
    │   │   │   │   ├── (components)
    │   │   │   │   └── page.tsx
    │   │   │   ├── page.tsx
    │   │   │   └── veiculos-detran
    │   │   │       ├── (components)
    │   │   │       └── page.tsx
    │   │   ├── infracoes
    │   │   │   ├── (components)
    │   │   │   │   ├── InfracoesFiltro.tsx
    │   │   │   │   ├── InfracoesOpcaoCard.tsx
    │   │   │   │   ├── InfracoesTableOperacoes.tsx
    │   │   │   │   └── index.ts
    │   │   │   ├── [id]
    │   │   │   │   ├── (components)
    │   │   │   │   └── page.tsx
    │   │   │   ├── novo
    │   │   │   │   ├── (components)
    │   │   │   │   └── page.tsx
    │   │   │   └── page.tsx
    │   │   ├── layout.tsx
    │   │   ├── lotes
    │   │   │   ├── (components)
    │   │   │   │   ├── LotesFiltro.tsx
    │   │   │   │   ├── LotesOpcaoCard.tsx
    │   │   │   │   ├── LotesOperacoes.tsx
    │   │   │   │   └── index.ts
    │   │   │   ├── [id]
    │   │   │   │   ├── (components)
    │   │   │   │   └── page.tsx
    │   │   │   ├── impressao-nas
    │   │   │   │   ├── (components)
    │   │   │   │   └── ImpressaoNAsContent.tsx
    │   │   │   ├── impressao-nps
    │   │   │   │   ├── (components)
    │   │   │   │   └── ImpressaoNPsContent.tsx
    │   │   │   ├── page.tsx
    │   │   │   └── validacao
    │   │   │       └── ValidacaoContent.tsx
    │   │   ├── processos
    │   │   │   └── page.tsx
    │   │   ├── transportes
    │   │   │   ├── (components)
    │   │   │   │   ├── TransportesOpcaoCard.tsx
    │   │   │   │   └── index.ts
    │   │   │   ├── infracoes-transporte
    │   │   │   │   ├── (components)
    │   │   │   │   └── InfracoesTransporteContent.tsx
    │   │   │   └── page.tsx
    │   │   └── usuarios
    │   │       ├── (components)
    │   │       │   ├── UsuariosFiltro.tsx
    │   │       │   ├── UsuariosTableOperacoes.tsx
    │   │       │   └── index.ts
    │   │       ├── [id]
    │   │       │   ├── (components)
    │   │       │   └── page.tsx
    │   │       ├── novo
    │   │       │   ├── (components)
    │   │       │   └── page.tsx
    │   │       └── page.tsx
    │   ├── (public)
    │   │   ├── layout.tsx
    │   │   └── login
    │   │       ├── (components)
    │   │       │   ├── LoginForm.tsx
    │   │       │   ├── LoginVisualPanel.tsx
    │   │       │   └── index.ts
    │   │       └── page.tsx
    │   ├── api
    │   │   ├── ait
    │   │   │   ├── createNa
    │   │   │   │   └── route.ts
    │   │   │   ├── getByAIT
    │   │   │   │   └── [ait]
    │   │   │   └── put
    │   │   │       └── [ait]
    │   │   ├── consulta
    │   │   │   ├── chassi
    │   │   │   │   └── [chassi]
    │   │   │   ├── cnh
    │   │   │   │   └── [cnh]
    │   │   │   ├── cpf
    │   │   │   │   └── [cpf]
    │   │   │   └── placa
    │   │   │       └── [placa]
    │   │   ├── infracao
    │   │   │   ├── create
    │   │   │   │   └── route.ts
    │   │   │   ├── delete
    │   │   │   │   └── [id]
    │   │   │   ├── getAll
    │   │   │   │   └── route.ts
    │   │   │   ├── getByCod
    │   │   │   │   └── [cod]
    │   │   │   ├── getById
    │   │   │   │   └── [id]
    │   │   │   └── put
    │   │   │       └── [id]
    │   │   ├── login
    │   │   │   └── route.ts
    │   │   ├── lote
    │   │   │   ├── close
    │   │   │   │   └── [id]
    │   │   │   ├── create
    │   │   │   │   └── route.ts
    │   │   │   ├── getAll
    │   │   │   │   └── route.ts
    │   │   │   ├── getById
    │   │   │   │   └── [id]
    │   │   │   └── put
    │   │   │       └── [id]
    │   │   └── usuario
    │   │       ├── create
    │   │       │   └── route.ts
    │   │       ├── createAdmin
    │   │       │   └── route.ts
    │   │       ├── delete
    │   │       │   └── [id]
    │   │       ├── getAll
    │   │       │   └── route.ts
    │   │       ├── getBy
    │   │       │   ├── cpf
    │   │       │   ├── funcao
    │   │       │   ├── id
    │   │       │   └── matricula
    │   │       └── put
    │   │           └── [id]
    │   ├── favicon.ico
    │   ├── globals.css
    │   ├── layout.tsx
    │   └── page.tsx
    ├── components
    │   ├── DataTable
    │   │   ├── DataTable.tsx
    │   │   └── index.ts
    │   ├── ProgressBar
    │   │   ├── ProgressBar.tsx
    │   │   └── index.ts
    │   └── Sidebar
    │       ├── NavLink.tsx
    │       ├── NavLinkClient.tsx
    │       ├── Sidebar.tsx
    │       ├── Sidebar.tsx.bak
    │       ├── UserMenu.tsx
    │       └── index.ts
    ├── eslint.config.mjs
    ├── lib
    │   └── api.ts
    ├── mock
    │   ├── ait
    │   │   └── index.ts
    │   ├── auth
    │   │   └── index.ts
    │   ├── condutores
    │   │   └── index.ts
    │   ├── index.ts
    │   ├── infracoes
    │   │   └── index.ts
    │   ├── lotes
    │   │   ├── impressao-nas
    │   │   │   └── index.ts
    │   │   ├── impressao-nps
    │   │   │   └── index.ts
    │   │   ├── index.ts
    │   │   ├── infracoes
    │   │   │   └── index.ts
    │   │   └── validacao
    │   │       └── index.ts
    │   ├── transportes
    │   │   └── index.ts
    │   ├── usuarios
    │   │   └── index.ts
    │   └── veiculos
    │       └── index.ts
    ├── next.config.ts
    ├── package-lock.json
    ├── package.json
    ├── postcss.config.mjs
    ├── public
    │   ├── Desenho CNH.svg
    │   ├── Desenho de Caminhão.svg
    │   ├── Desenho de Carreta.svg
    │   ├── Desenho de Carro.svg
    │   ├── Desenho de Moto.svg
    │   ├── Desenho de Van.svg
    │   ├── Icon CNH.svg
    │   ├── Icon CPF.svg
    │   ├── Icon Chassi.svg
    │   ├── Icon Placa.svg
    │   ├── file.svg
    │   ├── fotocarro1.webp
    │   ├── fotocarro2.jpg
    │   ├── globe.svg
    │   ├── logo.png
    │   ├── logo.svg
    │   ├── next.svg
    │   ├── vercel.svg
    │   └── window.svg
    ├── temp_sidebar.txt
    ├── tsconfig.json
    └── types
        ├── ait.ts
        ├── auth.ts
        ├── condutores.ts
        ├── consultas.ts
        ├── index.ts
        ├── infracoes.ts
        ├── lotes.ts
        ├── navigation.ts
        ├── table.ts
        ├── transportes.ts
        ├── usuarios.ts
        └── veiculos.ts
```


###  Project Index
<details open>
	<summary><b><code>SIGA---TALONARIO-ELETRONICO/</code></b></summary>
	<details> <!-- __root__ Submodule -->
		<summary><b>__root__</b></summary>
		<blockquote>
			<table>
			<tr>
				<td><b><a href='https://github.com/FabsMS/SIGA---Talonario-Eletronico/blob/master/package-lock.json'>package-lock.json</a></b></td>
				<td><code>❯ REPLACE-ME</code></td>
			</tr>
			<tr>
				<td><b><a href='https://github.com/FabsMS/SIGA---Talonario-Eletronico/blob/master/eslint.config.mjs'>eslint.config.mjs</a></b></td>
				<td><code>❯ REPLACE-ME</code></td>
			</tr>
			<tr>
				<td><b><a href='https://github.com/FabsMS/SIGA---Talonario-Eletronico/blob/master/temp_sidebar.txt'>temp_sidebar.txt</a></b></td>
				<td><code>❯ REPLACE-ME</code></td>
			</tr>
			<tr>
				<td><b><a href='https://github.com/FabsMS/SIGA---Talonario-Eletronico/blob/master/postcss.config.mjs'>postcss.config.mjs</a></b></td>
				<td><code>❯ REPLACE-ME</code></td>
			</tr>
			<tr>
				<td><b><a href='https://github.com/FabsMS/SIGA---Talonario-Eletronico/blob/master/next.config.ts'>next.config.ts</a></b></td>
				<td><code>❯ REPLACE-ME</code></td>
			</tr>
			<tr>
				<td><b><a href='https://github.com/FabsMS/SIGA---Talonario-Eletronico/blob/master/tsconfig.json'>tsconfig.json</a></b></td>
				<td><code>❯ REPLACE-ME</code></td>
			</tr>
			<tr>
				<td><b><a href='https://github.com/FabsMS/SIGA---Talonario-Eletronico/blob/master/package.json'>package.json</a></b></td>
				<td><code>❯ REPLACE-ME</code></td>
			</tr>
			</table>
		</blockquote>
	</details>
	<details> <!-- app Submodule -->
		<summary><b>app</b></summary>
		<blockquote>
			<table>
			<tr>
				<td><b><a href='https://github.com/FabsMS/SIGA---Talonario-Eletronico/blob/master/app/layout.tsx'>layout.tsx</a></b></td>
				<td><code>❯ REPLACE-ME</code></td>
			</tr>
			<tr>
				<td><b><a href='https://github.com/FabsMS/SIGA---Talonario-Eletronico/blob/master/app/page.tsx'>page.tsx</a></b></td>
				<td><code>❯ REPLACE-ME</code></td>
			</tr>
			<tr>
				<td><b><a href='https://github.com/FabsMS/SIGA---Talonario-Eletronico/blob/master/app/globals.css'>globals.css</a></b></td>
				<td><code>❯ REPLACE-ME</code></td>
			</tr>
			</table>
			<details>
				<summary><b>(public)</b></summary>
				<blockquote>
					<table>
					<tr>
						<td><b><a href='https://github.com/FabsMS/SIGA---Talonario-Eletronico/blob/master/app/(public)/layout.tsx'>layout.tsx</a></b></td>
						<td><code>❯ REPLACE-ME</code></td>
					</tr>
					</table>
					<details>
						<summary><b>login</b></summary>
						<blockquote>
							<table>
							<tr>
								<td><b><a href='https://github.com/FabsMS/SIGA---Talonario-Eletronico/blob/master/app/(public)/login/page.tsx'>page.tsx</a></b></td>
								<td><code>❯ REPLACE-ME</code></td>
							</tr>
							</table>
							<details>
								<summary><b>(components)</b></summary>
								<blockquote>
									<table>
									<tr>
										<td><b><a href='https://github.com/FabsMS/SIGA---Talonario-Eletronico/blob/master/app/(public)/login/(components)/index.ts'>index.ts</a></b></td>
										<td><code>❯ REPLACE-ME</code></td>
									</tr>
									<tr>
										<td><b><a href='https://github.com/FabsMS/SIGA---Talonario-Eletronico/blob/master/app/(public)/login/(components)/LoginVisualPanel.tsx'>LoginVisualPanel.tsx</a></b></td>
										<td><code>❯ REPLACE-ME</code></td>
									</tr>
									<tr>
										<td><b><a href='https://github.com/FabsMS/SIGA---Talonario-Eletronico/blob/master/app/(public)/login/(components)/LoginForm.tsx'>LoginForm.tsx</a></b></td>
										<td><code>❯ REPLACE-ME</code></td>
									</tr>
									</table>
								</blockquote>
							</details>
						</blockquote>
					</details>
				</blockquote>
			</details>
			<details>
				<summary><b>api</b></summary>
				<blockquote>
					<details>
						<summary><b>login</b></summary>
						<blockquote>
							<table>
							<tr>
								<td><b><a href='https://github.com/FabsMS/SIGA---Talonario-Eletronico/blob/master/app/api/login/route.ts'>route.ts</a></b></td>
								<td><code>❯ REPLACE-ME</code></td>
							</tr>
							</table>
						</blockquote>
					</details>
					<details>
						<summary><b>consulta</b></summary>
						<blockquote>
							<details>
								<summary><b>placa</b></summary>
								<blockquote>
									<details>
										<summary><b>[placa]</b></summary>
										<blockquote>
											<table>
											<tr>
												<td><b><a href='https://github.com/FabsMS/SIGA---Talonario-Eletronico/blob/master/app/api/consulta/placa/[placa]/route.ts'>route.ts</a></b></td>
												<td><code>❯ REPLACE-ME</code></td>
											</tr>
											</table>
										</blockquote>
									</details>
								</blockquote>
							</details>
							<details>
								<summary><b>cpf</b></summary>
								<blockquote>
									<details>
										<summary><b>[cpf]</b></summary>
										<blockquote>
											<table>
											<tr>
												<td><b><a href='https://github.com/FabsMS/SIGA---Talonario-Eletronico/blob/master/app/api/consulta/cpf/[cpf]/route.ts'>route.ts</a></b></td>
												<td><code>❯ REPLACE-ME</code></td>
											</tr>
											</table>
										</blockquote>
									</details>
								</blockquote>
							</details>
							<details>
								<summary><b>chassi</b></summary>
								<blockquote>
									<details>
										<summary><b>[chassi]</b></summary>
										<blockquote>
											<table>
											<tr>
												<td><b><a href='https://github.com/FabsMS/SIGA---Talonario-Eletronico/blob/master/app/api/consulta/chassi/[chassi]/route.ts'>route.ts</a></b></td>
												<td><code>❯ REPLACE-ME</code></td>
											</tr>
											</table>
										</blockquote>
									</details>
								</blockquote>
							</details>
							<details>
								<summary><b>cnh</b></summary>
								<blockquote>
									<details>
										<summary><b>[cnh]</b></summary>
										<blockquote>
											<table>
											<tr>
												<td><b><a href='https://github.com/FabsMS/SIGA---Talonario-Eletronico/blob/master/app/api/consulta/cnh/[cnh]/route.ts'>route.ts</a></b></td>
												<td><code>❯ REPLACE-ME</code></td>
											</tr>
											</table>
										</blockquote>
									</details>
								</blockquote>
							</details>
						</blockquote>
					</details>
					<details>
						<summary><b>lote</b></summary>
						<blockquote>
							<details>
								<summary><b>put</b></summary>
								<blockquote>
									<details>
										<summary><b>[id]</b></summary>
										<blockquote>
											<table>
											<tr>
												<td><b><a href='https://github.com/FabsMS/SIGA---Talonario-Eletronico/blob/master/app/api/lote/put/[id]/route.ts'>route.ts</a></b></td>
												<td><code>❯ REPLACE-ME</code></td>
											</tr>
											</table>
										</blockquote>
									</details>
								</blockquote>
							</details>
							<details>
								<summary><b>create</b></summary>
								<blockquote>
									<table>
									<tr>
										<td><b><a href='https://github.com/FabsMS/SIGA---Talonario-Eletronico/blob/master/app/api/lote/create/route.ts'>route.ts</a></b></td>
										<td><code>❯ REPLACE-ME</code></td>
									</tr>
									</table>
								</blockquote>
							</details>
							<details>
								<summary><b>close</b></summary>
								<blockquote>
									<details>
										<summary><b>[id]</b></summary>
										<blockquote>
											<table>
											<tr>
												<td><b><a href='https://github.com/FabsMS/SIGA---Talonario-Eletronico/blob/master/app/api/lote/close/[id]/route.ts'>route.ts</a></b></td>
												<td><code>❯ REPLACE-ME</code></td>
											</tr>
											</table>
										</blockquote>
									</details>
								</blockquote>
							</details>
							<details>
								<summary><b>getAll</b></summary>
								<blockquote>
									<table>
									<tr>
										<td><b><a href='https://github.com/FabsMS/SIGA---Talonario-Eletronico/blob/master/app/api/lote/getAll/route.ts'>route.ts</a></b></td>
										<td><code>❯ REPLACE-ME</code></td>
									</tr>
									</table>
								</blockquote>
							</details>
							<details>
								<summary><b>getById</b></summary>
								<blockquote>
									<details>
										<summary><b>[id]</b></summary>
										<blockquote>
											<table>
											<tr>
												<td><b><a href='https://github.com/FabsMS/SIGA---Talonario-Eletronico/blob/master/app/api/lote/getById/[id]/route.ts'>route.ts</a></b></td>
												<td><code>❯ REPLACE-ME</code></td>
											</tr>
											</table>
										</blockquote>
									</details>
								</blockquote>
							</details>
						</blockquote>
					</details>
					<details>
						<summary><b>infracao</b></summary>
						<blockquote>
							<details>
								<summary><b>put</b></summary>
								<blockquote>
									<details>
										<summary><b>[id]</b></summary>
										<blockquote>
											<table>
											<tr>
												<td><b><a href='https://github.com/FabsMS/SIGA---Talonario-Eletronico/blob/master/app/api/infracao/put/[id]/route.ts'>route.ts</a></b></td>
												<td><code>❯ REPLACE-ME</code></td>
											</tr>
											</table>
										</blockquote>
									</details>
								</blockquote>
							</details>
							<details>
								<summary><b>create</b></summary>
								<blockquote>
									<table>
									<tr>
										<td><b><a href='https://github.com/FabsMS/SIGA---Talonario-Eletronico/blob/master/app/api/infracao/create/route.ts'>route.ts</a></b></td>
										<td><code>❯ REPLACE-ME</code></td>
									</tr>
									</table>
								</blockquote>
							</details>
							<details>
								<summary><b>getByCod</b></summary>
								<blockquote>
									<details>
										<summary><b>[cod]</b></summary>
										<blockquote>
											<table>
											<tr>
												<td><b><a href='https://github.com/FabsMS/SIGA---Talonario-Eletronico/blob/master/app/api/infracao/getByCod/[cod]/route.ts'>route.ts</a></b></td>
												<td><code>❯ REPLACE-ME</code></td>
											</tr>
											</table>
										</blockquote>
									</details>
								</blockquote>
							</details>
							<details>
								<summary><b>delete</b></summary>
								<blockquote>
									<details>
										<summary><b>[id]</b></summary>
										<blockquote>
											<table>
											<tr>
												<td><b><a href='https://github.com/FabsMS/SIGA---Talonario-Eletronico/blob/master/app/api/infracao/delete/[id]/route.ts'>route.ts</a></b></td>
												<td><code>❯ REPLACE-ME</code></td>
											</tr>
											</table>
										</blockquote>
									</details>
								</blockquote>
							</details>
							<details>
								<summary><b>getAll</b></summary>
								<blockquote>
									<table>
									<tr>
										<td><b><a href='https://github.com/FabsMS/SIGA---Talonario-Eletronico/blob/master/app/api/infracao/getAll/route.ts'>route.ts</a></b></td>
										<td><code>❯ REPLACE-ME</code></td>
									</tr>
									</table>
								</blockquote>
							</details>
							<details>
								<summary><b>getById</b></summary>
								<blockquote>
									<details>
										<summary><b>[id]</b></summary>
										<blockquote>
											<table>
											<tr>
												<td><b><a href='https://github.com/FabsMS/SIGA---Talonario-Eletronico/blob/master/app/api/infracao/getById/[id]/route.ts'>route.ts</a></b></td>
												<td><code>❯ REPLACE-ME</code></td>
											</tr>
											</table>
										</blockquote>
									</details>
								</blockquote>
							</details>
						</blockquote>
					</details>
					<details>
						<summary><b>ait</b></summary>
						<blockquote>
							<details>
								<summary><b>put</b></summary>
								<blockquote>
									<details>
										<summary><b>[ait]</b></summary>
										<blockquote>
											<table>
											<tr>
												<td><b><a href='https://github.com/FabsMS/SIGA---Talonario-Eletronico/blob/master/app/api/ait/put/[ait]/route.ts'>route.ts</a></b></td>
												<td><code>❯ REPLACE-ME</code></td>
											</tr>
											</table>
										</blockquote>
									</details>
								</blockquote>
							</details>
							<details>
								<summary><b>createNa</b></summary>
								<blockquote>
									<table>
									<tr>
										<td><b><a href='https://github.com/FabsMS/SIGA---Talonario-Eletronico/blob/master/app/api/ait/createNa/route.ts'>route.ts</a></b></td>
										<td><code>❯ REPLACE-ME</code></td>
									</tr>
									</table>
								</blockquote>
							</details>
							<details>
								<summary><b>getByAIT</b></summary>
								<blockquote>
									<details>
										<summary><b>[ait]</b></summary>
										<blockquote>
											<table>
											<tr>
												<td><b><a href='https://github.com/FabsMS/SIGA---Talonario-Eletronico/blob/master/app/api/ait/getByAIT/[ait]/route.ts'>route.ts</a></b></td>
												<td><code>❯ REPLACE-ME</code></td>
											</tr>
											</table>
										</blockquote>
									</details>
								</blockquote>
							</details>
						</blockquote>
					</details>
					<details>
						<summary><b>usuario</b></summary>
						<blockquote>
							<details>
								<summary><b>put</b></summary>
								<blockquote>
									<details>
										<summary><b>[id]</b></summary>
										<blockquote>
											<table>
											<tr>
												<td><b><a href='https://github.com/FabsMS/SIGA---Talonario-Eletronico/blob/master/app/api/usuario/put/[id]/route.ts'>route.ts</a></b></td>
												<td><code>❯ REPLACE-ME</code></td>
											</tr>
											</table>
										</blockquote>
									</details>
								</blockquote>
							</details>
							<details>
								<summary><b>create</b></summary>
								<blockquote>
									<table>
									<tr>
										<td><b><a href='https://github.com/FabsMS/SIGA---Talonario-Eletronico/blob/master/app/api/usuario/create/route.ts'>route.ts</a></b></td>
										<td><code>❯ REPLACE-ME</code></td>
									</tr>
									</table>
								</blockquote>
							</details>
							<details>
								<summary><b>getBy</b></summary>
								<blockquote>
									<details>
										<summary><b>id</b></summary>
										<blockquote>
											<details>
												<summary><b>[id]</b></summary>
												<blockquote>
													<table>
													<tr>
														<td><b><a href='https://github.com/FabsMS/SIGA---Talonario-Eletronico/blob/master/app/api/usuario/getBy/id/[id]/route.ts'>route.ts</a></b></td>
														<td><code>❯ REPLACE-ME</code></td>
													</tr>
													</table>
												</blockquote>
											</details>
										</blockquote>
									</details>
									<details>
										<summary><b>funcao</b></summary>
										<blockquote>
											<details>
												<summary><b>[funcao]</b></summary>
												<blockquote>
													<table>
													<tr>
														<td><b><a href='https://github.com/FabsMS/SIGA---Talonario-Eletronico/blob/master/app/api/usuario/getBy/funcao/[funcao]/route.ts'>route.ts</a></b></td>
														<td><code>❯ REPLACE-ME</code></td>
													</tr>
													</table>
												</blockquote>
											</details>
										</blockquote>
									</details>
									<details>
										<summary><b>cpf</b></summary>
										<blockquote>
											<details>
												<summary><b>[cpf]</b></summary>
												<blockquote>
													<table>
													<tr>
														<td><b><a href='https://github.com/FabsMS/SIGA---Talonario-Eletronico/blob/master/app/api/usuario/getBy/cpf/[cpf]/route.ts'>route.ts</a></b></td>
														<td><code>❯ REPLACE-ME</code></td>
													</tr>
													</table>
												</blockquote>
											</details>
										</blockquote>
									</details>
									<details>
										<summary><b>matricula</b></summary>
										<blockquote>
											<details>
												<summary><b>[matricula]</b></summary>
												<blockquote>
													<table>
													<tr>
														<td><b><a href='https://github.com/FabsMS/SIGA---Talonario-Eletronico/blob/master/app/api/usuario/getBy/matricula/[matricula]/route.ts'>route.ts</a></b></td>
														<td><code>❯ REPLACE-ME</code></td>
													</tr>
													</table>
												</blockquote>
											</details>
										</blockquote>
									</details>
								</blockquote>
							</details>
							<details>
								<summary><b>delete</b></summary>
								<blockquote>
									<details>
										<summary><b>[id]</b></summary>
										<blockquote>
											<table>
											<tr>
												<td><b><a href='https://github.com/FabsMS/SIGA---Talonario-Eletronico/blob/master/app/api/usuario/delete/[id]/route.ts'>route.ts</a></b></td>
												<td><code>❯ REPLACE-ME</code></td>
											</tr>
											</table>
										</blockquote>
									</details>
								</blockquote>
							</details>
							<details>
								<summary><b>getAll</b></summary>
								<blockquote>
									<table>
									<tr>
										<td><b><a href='https://github.com/FabsMS/SIGA---Talonario-Eletronico/blob/master/app/api/usuario/getAll/route.ts'>route.ts</a></b></td>
										<td><code>❯ REPLACE-ME</code></td>
									</tr>
									</table>
								</blockquote>
							</details>
							<details>
								<summary><b>createAdmin</b></summary>
								<blockquote>
									<table>
									<tr>
										<td><b><a href='https://github.com/FabsMS/SIGA---Talonario-Eletronico/blob/master/app/api/usuario/createAdmin/route.ts'>route.ts</a></b></td>
										<td><code>❯ REPLACE-ME</code></td>
									</tr>
									</table>
								</blockquote>
							</details>
						</blockquote>
					</details>
				</blockquote>
			</details>
			<details>
				<summary><b>(private)</b></summary>
				<blockquote>
					<table>
					<tr>
						<td><b><a href='https://github.com/FabsMS/SIGA---Talonario-Eletronico/blob/master/app/(private)/layout.tsx'>layout.tsx</a></b></td>
						<td><code>❯ REPLACE-ME</code></td>
					</tr>
					</table>
					<details>
						<summary><b>infracoes</b></summary>
						<blockquote>
							<table>
							<tr>
								<td><b><a href='https://github.com/FabsMS/SIGA---Talonario-Eletronico/blob/master/app/(private)/infracoes/page.tsx'>page.tsx</a></b></td>
								<td><code>❯ REPLACE-ME</code></td>
							</tr>
							</table>
							<details>
								<summary><b>[id]</b></summary>
								<blockquote>
									<table>
									<tr>
										<td><b><a href='https://github.com/FabsMS/SIGA---Talonario-Eletronico/blob/master/app/(private)/infracoes/[id]/page.tsx'>page.tsx</a></b></td>
										<td><code>❯ REPLACE-ME</code></td>
									</tr>
									</table>
									<details>
										<summary><b>(components)</b></summary>
										<blockquote>
											<table>
											<tr>
												<td><b><a href='https://github.com/FabsMS/SIGA---Talonario-Eletronico/blob/master/app/(private)/infracoes/[id]/(components)/index.ts'>index.ts</a></b></td>
												<td><code>❯ REPLACE-ME</code></td>
											</tr>
											<tr>
												<td><b><a href='https://github.com/FabsMS/SIGA---Talonario-Eletronico/blob/master/app/(private)/infracoes/[id]/(components)/DetalhesAutoInfracao.tsx'>DetalhesAutoInfracao.tsx</a></b></td>
												<td><code>❯ REPLACE-ME</code></td>
											</tr>
											<tr>
												<td><b><a href='https://github.com/FabsMS/SIGA---Talonario-Eletronico/blob/master/app/(private)/infracoes/[id]/(components)/DetalhesPagamento.tsx'>DetalhesPagamento.tsx</a></b></td>
												<td><code>❯ REPLACE-ME</code></td>
											</tr>
											<tr>
												<td><b><a href='https://github.com/FabsMS/SIGA---Talonario-Eletronico/blob/master/app/(private)/infracoes/[id]/(components)/DetalhesCometimento.tsx'>DetalhesCometimento.tsx</a></b></td>
												<td><code>❯ REPLACE-ME</code></td>
											</tr>
											<tr>
												<td><b><a href='https://github.com/FabsMS/SIGA---Talonario-Eletronico/blob/master/app/(private)/infracoes/[id]/(components)/DetalhesTipoInfracao.tsx'>DetalhesTipoInfracao.tsx</a></b></td>
												<td><code>❯ REPLACE-ME</code></td>
											</tr>
											<tr>
												<td><b><a href='https://github.com/FabsMS/SIGA---Talonario-Eletronico/blob/master/app/(private)/infracoes/[id]/(components)/DetalhesProprietario.tsx'>DetalhesProprietario.tsx</a></b></td>
												<td><code>❯ REPLACE-ME</code></td>
											</tr>
											<tr>
												<td><b><a href='https://github.com/FabsMS/SIGA---Talonario-Eletronico/blob/master/app/(private)/infracoes/[id]/(components)/DetalhesSNE.tsx'>DetalhesSNE.tsx</a></b></td>
												<td><code>❯ REPLACE-ME</code></td>
											</tr>
											<tr>
												<td><b><a href='https://github.com/FabsMS/SIGA---Talonario-Eletronico/blob/master/app/(private)/infracoes/[id]/(components)/DetalhesMedicoes.tsx'>DetalhesMedicoes.tsx</a></b></td>
												<td><code>❯ REPLACE-ME</code></td>
											</tr>
											<tr>
												<td><b><a href='https://github.com/FabsMS/SIGA---Talonario-Eletronico/blob/master/app/(private)/infracoes/[id]/(components)/DetalhesVeiculo.tsx'>DetalhesVeiculo.tsx</a></b></td>
												<td><code>❯ REPLACE-ME</code></td>
											</tr>
											</table>
										</blockquote>
									</details>
								</blockquote>
							</details>
							<details>
								<summary><b>novo</b></summary>
								<blockquote>
									<table>
									<tr>
										<td><b><a href='https://github.com/FabsMS/SIGA---Talonario-Eletronico/blob/master/app/(private)/infracoes/novo/page.tsx'>page.tsx</a></b></td>
										<td><code>❯ REPLACE-ME</code></td>
									</tr>
									</table>
									<details>
										<summary><b>(components)</b></summary>
										<blockquote>
											<table>
											<tr>
												<td><b><a href='https://github.com/FabsMS/SIGA---Talonario-Eletronico/blob/master/app/(private)/infracoes/novo/(components)/index.ts'>index.ts</a></b></td>
												<td><code>❯ REPLACE-ME</code></td>
											</tr>
											<tr>
												<td><b><a href='https://github.com/FabsMS/SIGA---Talonario-Eletronico/blob/master/app/(private)/infracoes/novo/(components)/DadosVeiculoForm.tsx'>DadosVeiculoForm.tsx</a></b></td>
												<td><code>❯ REPLACE-ME</code></td>
											</tr>
											<tr>
												<td><b><a href='https://github.com/FabsMS/SIGA---Talonario-Eletronico/blob/master/app/(private)/infracoes/novo/(components)/DadosInfracaoForm.tsx'>DadosInfracaoForm.tsx</a></b></td>
												<td><code>❯ REPLACE-ME</code></td>
											</tr>
											</table>
										</blockquote>
									</details>
								</blockquote>
							</details>
							<details>
								<summary><b>(components)</b></summary>
								<blockquote>
									<table>
									<tr>
										<td><b><a href='https://github.com/FabsMS/SIGA---Talonario-Eletronico/blob/master/app/(private)/infracoes/(components)/index.ts'>index.ts</a></b></td>
										<td><code>❯ REPLACE-ME</code></td>
									</tr>
									<tr>
										<td><b><a href='https://github.com/FabsMS/SIGA---Talonario-Eletronico/blob/master/app/(private)/infracoes/(components)/InfracoesOpcaoCard.tsx'>InfracoesOpcaoCard.tsx</a></b></td>
										<td><code>❯ REPLACE-ME</code></td>
									</tr>
									<tr>
										<td><b><a href='https://github.com/FabsMS/SIGA---Talonario-Eletronico/blob/master/app/(private)/infracoes/(components)/InfracoesTableOperacoes.tsx'>InfracoesTableOperacoes.tsx</a></b></td>
										<td><code>❯ REPLACE-ME</code></td>
									</tr>
									<tr>
										<td><b><a href='https://github.com/FabsMS/SIGA---Talonario-Eletronico/blob/master/app/(private)/infracoes/(components)/InfracoesFiltro.tsx'>InfracoesFiltro.tsx</a></b></td>
										<td><code>❯ REPLACE-ME</code></td>
									</tr>
									</table>
								</blockquote>
							</details>
						</blockquote>
					</details>
					<details>
						<summary><b>processos</b></summary>
						<blockquote>
							<table>
							<tr>
								<td><b><a href='https://github.com/FabsMS/SIGA---Talonario-Eletronico/blob/master/app/(private)/processos/page.tsx'>page.tsx</a></b></td>
								<td><code>❯ REPLACE-ME</code></td>
							</tr>
							</table>
						</blockquote>
					</details>
					<details>
						<summary><b>transportes</b></summary>
						<blockquote>
							<table>
							<tr>
								<td><b><a href='https://github.com/FabsMS/SIGA---Talonario-Eletronico/blob/master/app/(private)/transportes/page.tsx'>page.tsx</a></b></td>
								<td><code>❯ REPLACE-ME</code></td>
							</tr>
							</table>
							<details>
								<summary><b>infracoes-transporte</b></summary>
								<blockquote>
									<table>
									<tr>
										<td><b><a href='https://github.com/FabsMS/SIGA---Talonario-Eletronico/blob/master/app/(private)/transportes/infracoes-transporte/InfracoesTransporteContent.tsx'>InfracoesTransporteContent.tsx</a></b></td>
										<td><code>❯ REPLACE-ME</code></td>
									</tr>
									</table>
									<details>
										<summary><b>(components)</b></summary>
										<blockquote>
											<table>
											<tr>
												<td><b><a href='https://github.com/FabsMS/SIGA---Talonario-Eletronico/blob/master/app/(private)/transportes/infracoes-transporte/(components)/index.ts'>index.ts</a></b></td>
												<td><code>❯ REPLACE-ME</code></td>
											</tr>
											<tr>
												<td><b><a href='https://github.com/FabsMS/SIGA---Talonario-Eletronico/blob/master/app/(private)/transportes/infracoes-transporte/(components)/InfracoesTransporteFiltro.tsx'>InfracoesTransporteFiltro.tsx</a></b></td>
												<td><code>❯ REPLACE-ME</code></td>
											</tr>
											<tr>
												<td><b><a href='https://github.com/FabsMS/SIGA---Talonario-Eletronico/blob/master/app/(private)/transportes/infracoes-transporte/(components)/InfracoesTransporteOperacoes.tsx'>InfracoesTransporteOperacoes.tsx</a></b></td>
												<td><code>❯ REPLACE-ME</code></td>
											</tr>
											</table>
										</blockquote>
									</details>
								</blockquote>
							</details>
							<details>
								<summary><b>(components)</b></summary>
								<blockquote>
									<table>
									<tr>
										<td><b><a href='https://github.com/FabsMS/SIGA---Talonario-Eletronico/blob/master/app/(private)/transportes/(components)/index.ts'>index.ts</a></b></td>
										<td><code>❯ REPLACE-ME</code></td>
									</tr>
									<tr>
										<td><b><a href='https://github.com/FabsMS/SIGA---Talonario-Eletronico/blob/master/app/(private)/transportes/(components)/TransportesOpcaoCard.tsx'>TransportesOpcaoCard.tsx</a></b></td>
										<td><code>❯ REPLACE-ME</code></td>
									</tr>
									</table>
								</blockquote>
							</details>
						</blockquote>
					</details>
					<details>
						<summary><b>consultas</b></summary>
						<blockquote>
							<table>
							<tr>
								<td><b><a href='https://github.com/FabsMS/SIGA---Talonario-Eletronico/blob/master/app/(private)/consultas/page.tsx'>page.tsx</a></b></td>
								<td><code>❯ REPLACE-ME</code></td>
							</tr>
							</table>
							<details>
								<summary><b>condutores-detran</b></summary>
								<blockquote>
									<table>
									<tr>
										<td><b><a href='https://github.com/FabsMS/SIGA---Talonario-Eletronico/blob/master/app/(private)/consultas/condutores-detran/page.tsx'>page.tsx</a></b></td>
										<td><code>❯ REPLACE-ME</code></td>
									</tr>
									</table>
									<details>
										<summary><b>(components)</b></summary>
										<blockquote>
											<table>
											<tr>
												<td><b><a href='https://github.com/FabsMS/SIGA---Talonario-Eletronico/blob/master/app/(private)/consultas/condutores-detran/(components)/index.ts'>index.ts</a></b></td>
												<td><code>❯ REPLACE-ME</code></td>
											</tr>
											<tr>
												<td><b><a href='https://github.com/FabsMS/SIGA---Talonario-Eletronico/blob/master/app/(private)/consultas/condutores-detran/(components)/ConsultaCondutoresForm.tsx'>ConsultaCondutoresForm.tsx</a></b></td>
												<td><code>❯ REPLACE-ME</code></td>
											</tr>
											<tr>
												<td><b><a href='https://github.com/FabsMS/SIGA---Talonario-Eletronico/blob/master/app/(private)/consultas/condutores-detran/(components)/CondutorResultado.tsx'>CondutorResultado.tsx</a></b></td>
												<td><code>❯ REPLACE-ME</code></td>
											</tr>
											</table>
										</blockquote>
									</details>
								</blockquote>
							</details>
							<details>
								<summary><b>veiculos-detran</b></summary>
								<blockquote>
									<table>
									<tr>
										<td><b><a href='https://github.com/FabsMS/SIGA---Talonario-Eletronico/blob/master/app/(private)/consultas/veiculos-detran/page.tsx'>page.tsx</a></b></td>
										<td><code>❯ REPLACE-ME</code></td>
									</tr>
									</table>
									<details>
										<summary><b>(components)</b></summary>
										<blockquote>
											<table>
											<tr>
												<td><b><a href='https://github.com/FabsMS/SIGA---Talonario-Eletronico/blob/master/app/(private)/consultas/veiculos-detran/(components)/index.ts'>index.ts</a></b></td>
												<td><code>❯ REPLACE-ME</code></td>
											</tr>
											<tr>
												<td><b><a href='https://github.com/FabsMS/SIGA---Talonario-Eletronico/blob/master/app/(private)/consultas/veiculos-detran/(components)/VeiculoResultado.tsx'>VeiculoResultado.tsx</a></b></td>
												<td><code>❯ REPLACE-ME</code></td>
											</tr>
											</table>
										</blockquote>
									</details>
								</blockquote>
							</details>
							<details>
								<summary><b>(components)</b></summary>
								<blockquote>
									<table>
									<tr>
										<td><b><a href='https://github.com/FabsMS/SIGA---Talonario-Eletronico/blob/master/app/(private)/consultas/(components)/index.ts'>index.ts</a></b></td>
										<td><code>❯ REPLACE-ME</code></td>
									</tr>
									<tr>
										<td><b><a href='https://github.com/FabsMS/SIGA---Talonario-Eletronico/blob/master/app/(private)/consultas/(components)/ConsultasOpcaoCard.tsx'>ConsultasOpcaoCard.tsx</a></b></td>
										<td><code>❯ REPLACE-ME</code></td>
									</tr>
									</table>
								</blockquote>
							</details>
						</blockquote>
					</details>
					<details>
						<summary><b>lotes</b></summary>
						<blockquote>
							<table>
							<tr>
								<td><b><a href='https://github.com/FabsMS/SIGA---Talonario-Eletronico/blob/master/app/(private)/lotes/page.tsx'>page.tsx</a></b></td>
								<td><code>❯ REPLACE-ME</code></td>
							</tr>
							</table>
							<details>
								<summary><b>impressao-nps</b></summary>
								<blockquote>
									<table>
									<tr>
										<td><b><a href='https://github.com/FabsMS/SIGA---Talonario-Eletronico/blob/master/app/(private)/lotes/impressao-nps/ImpressaoNPsContent.tsx'>ImpressaoNPsContent.tsx</a></b></td>
										<td><code>❯ REPLACE-ME</code></td>
									</tr>
									</table>
									<details>
										<summary><b>(components)</b></summary>
										<blockquote>
											<table>
											<tr>
												<td><b><a href='https://github.com/FabsMS/SIGA---Talonario-Eletronico/blob/master/app/(private)/lotes/impressao-nps/(components)/index.ts'>index.ts</a></b></td>
												<td><code>❯ REPLACE-ME</code></td>
											</tr>
											<tr>
												<td><b><a href='https://github.com/FabsMS/SIGA---Talonario-Eletronico/blob/master/app/(private)/lotes/impressao-nps/(components)/ImpressaoNPsOperacoes.tsx'>ImpressaoNPsOperacoes.tsx</a></b></td>
												<td><code>❯ REPLACE-ME</code></td>
											</tr>
											<tr>
												<td><b><a href='https://github.com/FabsMS/SIGA---Talonario-Eletronico/blob/master/app/(private)/lotes/impressao-nps/(components)/ImpressaoNPsFiltro.tsx'>ImpressaoNPsFiltro.tsx</a></b></td>
												<td><code>❯ REPLACE-ME</code></td>
											</tr>
											</table>
										</blockquote>
									</details>
								</blockquote>
							</details>
							<details>
								<summary><b>[id]</b></summary>
								<blockquote>
									<table>
									<tr>
										<td><b><a href='https://github.com/FabsMS/SIGA---Talonario-Eletronico/blob/master/app/(private)/lotes/[id]/page.tsx'>page.tsx</a></b></td>
										<td><code>❯ REPLACE-ME</code></td>
									</tr>
									</table>
									<details>
										<summary><b>(components)</b></summary>
										<blockquote>
											<table>
											<tr>
												<td><b><a href='https://github.com/FabsMS/SIGA---Talonario-Eletronico/blob/master/app/(private)/lotes/[id]/(components)/index.ts'>index.ts</a></b></td>
												<td><code>❯ REPLACE-ME</code></td>
											</tr>
											<tr>
												<td><b><a href='https://github.com/FabsMS/SIGA---Talonario-Eletronico/blob/master/app/(private)/lotes/[id]/(components)/InfracoesOperacoes.tsx'>InfracoesOperacoes.tsx</a></b></td>
												<td><code>❯ REPLACE-ME</code></td>
											</tr>
											<tr>
												<td><b><a href='https://github.com/FabsMS/SIGA---Talonario-Eletronico/blob/master/app/(private)/lotes/[id]/(components)/InfracoesFiltro.tsx'>InfracoesFiltro.tsx</a></b></td>
												<td><code>❯ REPLACE-ME</code></td>
											</tr>
											</table>
										</blockquote>
									</details>
								</blockquote>
							</details>
							<details>
								<summary><b>impressao-nas</b></summary>
								<blockquote>
									<table>
									<tr>
										<td><b><a href='https://github.com/FabsMS/SIGA---Talonario-Eletronico/blob/master/app/(private)/lotes/impressao-nas/ImpressaoNAsContent.tsx'>ImpressaoNAsContent.tsx</a></b></td>
										<td><code>❯ REPLACE-ME</code></td>
									</tr>
									</table>
									<details>
										<summary><b>(components)</b></summary>
										<blockquote>
											<table>
											<tr>
												<td><b><a href='https://github.com/FabsMS/SIGA---Talonario-Eletronico/blob/master/app/(private)/lotes/impressao-nas/(components)/index.ts'>index.ts</a></b></td>
												<td><code>❯ REPLACE-ME</code></td>
											</tr>
											<tr>
												<td><b><a href='https://github.com/FabsMS/SIGA---Talonario-Eletronico/blob/master/app/(private)/lotes/impressao-nas/(components)/ImpressaoNAsFiltro.tsx'>ImpressaoNAsFiltro.tsx</a></b></td>
												<td><code>❯ REPLACE-ME</code></td>
											</tr>
											<tr>
												<td><b><a href='https://github.com/FabsMS/SIGA---Talonario-Eletronico/blob/master/app/(private)/lotes/impressao-nas/(components)/ImpressaoNAsOperacoes.tsx'>ImpressaoNAsOperacoes.tsx</a></b></td>
												<td><code>❯ REPLACE-ME</code></td>
											</tr>
											</table>
										</blockquote>
									</details>
								</blockquote>
							</details>
							<details>
								<summary><b>validacao</b></summary>
								<blockquote>
									<table>
									<tr>
										<td><b><a href='https://github.com/FabsMS/SIGA---Talonario-Eletronico/blob/master/app/(private)/lotes/validacao/ValidacaoContent.tsx'>ValidacaoContent.tsx</a></b></td>
										<td><code>❯ REPLACE-ME</code></td>
									</tr>
									</table>
								</blockquote>
							</details>
							<details>
								<summary><b>(components)</b></summary>
								<blockquote>
									<table>
									<tr>
										<td><b><a href='https://github.com/FabsMS/SIGA---Talonario-Eletronico/blob/master/app/(private)/lotes/(components)/LotesOpcaoCard.tsx'>LotesOpcaoCard.tsx</a></b></td>
										<td><code>❯ REPLACE-ME</code></td>
									</tr>
									<tr>
										<td><b><a href='https://github.com/FabsMS/SIGA---Talonario-Eletronico/blob/master/app/(private)/lotes/(components)/index.ts'>index.ts</a></b></td>
										<td><code>❯ REPLACE-ME</code></td>
									</tr>
									<tr>
										<td><b><a href='https://github.com/FabsMS/SIGA---Talonario-Eletronico/blob/master/app/(private)/lotes/(components)/LotesFiltro.tsx'>LotesFiltro.tsx</a></b></td>
										<td><code>❯ REPLACE-ME</code></td>
									</tr>
									<tr>
										<td><b><a href='https://github.com/FabsMS/SIGA---Talonario-Eletronico/blob/master/app/(private)/lotes/(components)/LotesOperacoes.tsx'>LotesOperacoes.tsx</a></b></td>
										<td><code>❯ REPLACE-ME</code></td>
									</tr>
									</table>
								</blockquote>
							</details>
						</blockquote>
					</details>
					<details>
						<summary><b>usuarios</b></summary>
						<blockquote>
							<table>
							<tr>
								<td><b><a href='https://github.com/FabsMS/SIGA---Talonario-Eletronico/blob/master/app/(private)/usuarios/page.tsx'>page.tsx</a></b></td>
								<td><code>❯ REPLACE-ME</code></td>
							</tr>
							</table>
							<details>
								<summary><b>[id]</b></summary>
								<blockquote>
									<table>
									<tr>
										<td><b><a href='https://github.com/FabsMS/SIGA---Talonario-Eletronico/blob/master/app/(private)/usuarios/[id]/page.tsx'>page.tsx</a></b></td>
										<td><code>❯ REPLACE-ME</code></td>
									</tr>
									</table>
									<details>
										<summary><b>(components)</b></summary>
										<blockquote>
											<table>
											<tr>
												<td><b><a href='https://github.com/FabsMS/SIGA---Talonario-Eletronico/blob/master/app/(private)/usuarios/[id]/(components)/index.ts'>index.ts</a></b></td>
												<td><code>❯ REPLACE-ME</code></td>
											</tr>
											<tr>
												<td><b><a href='https://github.com/FabsMS/SIGA---Talonario-Eletronico/blob/master/app/(private)/usuarios/[id]/(components)/EditarUsuarioForm.tsx'>EditarUsuarioForm.tsx</a></b></td>
												<td><code>❯ REPLACE-ME</code></td>
											</tr>
											<tr>
												<td><b><a href='https://github.com/FabsMS/SIGA---Talonario-Eletronico/blob/master/app/(private)/usuarios/[id]/(components)/PermissoesCard.tsx'>PermissoesCard.tsx</a></b></td>
												<td><code>❯ REPLACE-ME</code></td>
											</tr>
											</table>
										</blockquote>
									</details>
								</blockquote>
							</details>
							<details>
								<summary><b>novo</b></summary>
								<blockquote>
									<table>
									<tr>
										<td><b><a href='https://github.com/FabsMS/SIGA---Talonario-Eletronico/blob/master/app/(private)/usuarios/novo/page.tsx'>page.tsx</a></b></td>
										<td><code>❯ REPLACE-ME</code></td>
									</tr>
									</table>
									<details>
										<summary><b>(components)</b></summary>
										<blockquote>
											<table>
											<tr>
												<td><b><a href='https://github.com/FabsMS/SIGA---Talonario-Eletronico/blob/master/app/(private)/usuarios/novo/(components)/index.ts'>index.ts</a></b></td>
												<td><code>❯ REPLACE-ME</code></td>
											</tr>
											<tr>
												<td><b><a href='https://github.com/FabsMS/SIGA---Talonario-Eletronico/blob/master/app/(private)/usuarios/novo/(components)/NovoUsuarioForm.tsx'>NovoUsuarioForm.tsx</a></b></td>
												<td><code>❯ REPLACE-ME</code></td>
											</tr>
											</table>
										</blockquote>
									</details>
								</blockquote>
							</details>
							<details>
								<summary><b>(components)</b></summary>
								<blockquote>
									<table>
									<tr>
										<td><b><a href='https://github.com/FabsMS/SIGA---Talonario-Eletronico/blob/master/app/(private)/usuarios/(components)/UsuariosFiltro.tsx'>UsuariosFiltro.tsx</a></b></td>
										<td><code>❯ REPLACE-ME</code></td>
									</tr>
									<tr>
										<td><b><a href='https://github.com/FabsMS/SIGA---Talonario-Eletronico/blob/master/app/(private)/usuarios/(components)/index.ts'>index.ts</a></b></td>
										<td><code>❯ REPLACE-ME</code></td>
									</tr>
									<tr>
										<td><b><a href='https://github.com/FabsMS/SIGA---Talonario-Eletronico/blob/master/app/(private)/usuarios/(components)/UsuariosTableOperacoes.tsx'>UsuariosTableOperacoes.tsx</a></b></td>
										<td><code>❯ REPLACE-ME</code></td>
									</tr>
									</table>
								</blockquote>
							</details>
						</blockquote>
					</details>
				</blockquote>
			</details>
		</blockquote>
	</details>
	<details> <!-- mock Submodule -->
		<summary><b>mock</b></summary>
		<blockquote>
			<table>
			<tr>
				<td><b><a href='https://github.com/FabsMS/SIGA---Talonario-Eletronico/blob/master/mock/index.ts'>index.ts</a></b></td>
				<td><code>❯ REPLACE-ME</code></td>
			</tr>
			</table>
			<details>
				<summary><b>infracoes</b></summary>
				<blockquote>
					<table>
					<tr>
						<td><b><a href='https://github.com/FabsMS/SIGA---Talonario-Eletronico/blob/master/mock/infracoes/index.ts'>index.ts</a></b></td>
						<td><code>❯ REPLACE-ME</code></td>
					</tr>
					</table>
				</blockquote>
			</details>
			<details>
				<summary><b>veiculos</b></summary>
				<blockquote>
					<table>
					<tr>
						<td><b><a href='https://github.com/FabsMS/SIGA---Talonario-Eletronico/blob/master/mock/veiculos/index.ts'>index.ts</a></b></td>
						<td><code>❯ REPLACE-ME</code></td>
					</tr>
					</table>
				</blockquote>
			</details>
			<details>
				<summary><b>transportes</b></summary>
				<blockquote>
					<table>
					<tr>
						<td><b><a href='https://github.com/FabsMS/SIGA---Talonario-Eletronico/blob/master/mock/transportes/index.ts'>index.ts</a></b></td>
						<td><code>❯ REPLACE-ME</code></td>
					</tr>
					</table>
				</blockquote>
			</details>
			<details>
				<summary><b>condutores</b></summary>
				<blockquote>
					<table>
					<tr>
						<td><b><a href='https://github.com/FabsMS/SIGA---Talonario-Eletronico/blob/master/mock/condutores/index.ts'>index.ts</a></b></td>
						<td><code>❯ REPLACE-ME</code></td>
					</tr>
					</table>
				</blockquote>
			</details>
			<details>
				<summary><b>ait</b></summary>
				<blockquote>
					<table>
					<tr>
						<td><b><a href='https://github.com/FabsMS/SIGA---Talonario-Eletronico/blob/master/mock/ait/index.ts'>index.ts</a></b></td>
						<td><code>❯ REPLACE-ME</code></td>
					</tr>
					</table>
				</blockquote>
			</details>
			<details>
				<summary><b>lotes</b></summary>
				<blockquote>
					<table>
					<tr>
						<td><b><a href='https://github.com/FabsMS/SIGA---Talonario-Eletronico/blob/master/mock/lotes/index.ts'>index.ts</a></b></td>
						<td><code>❯ REPLACE-ME</code></td>
					</tr>
					</table>
					<details>
						<summary><b>impressao-nps</b></summary>
						<blockquote>
							<table>
							<tr>
								<td><b><a href='https://github.com/FabsMS/SIGA---Talonario-Eletronico/blob/master/mock/lotes/impressao-nps/index.ts'>index.ts</a></b></td>
								<td><code>❯ REPLACE-ME</code></td>
							</tr>
							</table>
						</blockquote>
					</details>
					<details>
						<summary><b>impressao-nas</b></summary>
						<blockquote>
							<table>
							<tr>
								<td><b><a href='https://github.com/FabsMS/SIGA---Talonario-Eletronico/blob/master/mock/lotes/impressao-nas/index.ts'>index.ts</a></b></td>
								<td><code>❯ REPLACE-ME</code></td>
							</tr>
							</table>
						</blockquote>
					</details>
					<details>
						<summary><b>infracoes</b></summary>
						<blockquote>
							<table>
							<tr>
								<td><b><a href='https://github.com/FabsMS/SIGA---Talonario-Eletronico/blob/master/mock/lotes/infracoes/index.ts'>index.ts</a></b></td>
								<td><code>❯ REPLACE-ME</code></td>
							</tr>
							</table>
						</blockquote>
					</details>
					<details>
						<summary><b>validacao</b></summary>
						<blockquote>
							<table>
							<tr>
								<td><b><a href='https://github.com/FabsMS/SIGA---Talonario-Eletronico/blob/master/mock/lotes/validacao/index.ts'>index.ts</a></b></td>
								<td><code>❯ REPLACE-ME</code></td>
							</tr>
							</table>
						</blockquote>
					</details>
				</blockquote>
			</details>
			<details>
				<summary><b>auth</b></summary>
				<blockquote>
					<table>
					<tr>
						<td><b><a href='https://github.com/FabsMS/SIGA---Talonario-Eletronico/blob/master/mock/auth/index.ts'>index.ts</a></b></td>
						<td><code>❯ REPLACE-ME</code></td>
					</tr>
					</table>
				</blockquote>
			</details>
			<details>
				<summary><b>usuarios</b></summary>
				<blockquote>
					<table>
					<tr>
						<td><b><a href='https://github.com/FabsMS/SIGA---Talonario-Eletronico/blob/master/mock/usuarios/index.ts'>index.ts</a></b></td>
						<td><code>❯ REPLACE-ME</code></td>
					</tr>
					</table>
				</blockquote>
			</details>
		</blockquote>
	</details>
	<details> <!-- components Submodule -->
		<summary><b>components</b></summary>
		<blockquote>
			<details>
				<summary><b>DataTable</b></summary>
				<blockquote>
					<table>
					<tr>
						<td><b><a href='https://github.com/FabsMS/SIGA---Talonario-Eletronico/blob/master/components/DataTable/index.ts'>index.ts</a></b></td>
						<td><code>❯ REPLACE-ME</code></td>
					</tr>
					<tr>
						<td><b><a href='https://github.com/FabsMS/SIGA---Talonario-Eletronico/blob/master/components/DataTable/DataTable.tsx'>DataTable.tsx</a></b></td>
						<td><code>❯ REPLACE-ME</code></td>
					</tr>
					</table>
				</blockquote>
			</details>
			<details>
				<summary><b>ProgressBar</b></summary>
				<blockquote>
					<table>
					<tr>
						<td><b><a href='https://github.com/FabsMS/SIGA---Talonario-Eletronico/blob/master/components/ProgressBar/index.ts'>index.ts</a></b></td>
						<td><code>❯ REPLACE-ME</code></td>
					</tr>
					<tr>
						<td><b><a href='https://github.com/FabsMS/SIGA---Talonario-Eletronico/blob/master/components/ProgressBar/ProgressBar.tsx'>ProgressBar.tsx</a></b></td>
						<td><code>❯ REPLACE-ME</code></td>
					</tr>
					</table>
				</blockquote>
			</details>
			<details>
				<summary><b>Sidebar</b></summary>
				<blockquote>
					<table>
					<tr>
						<td><b><a href='https://github.com/FabsMS/SIGA---Talonario-Eletronico/blob/master/components/Sidebar/NavLink.tsx'>NavLink.tsx</a></b></td>
						<td><code>❯ REPLACE-ME</code></td>
					</tr>
					<tr>
						<td><b><a href='https://github.com/FabsMS/SIGA---Talonario-Eletronico/blob/master/components/Sidebar/index.ts'>index.ts</a></b></td>
						<td><code>❯ REPLACE-ME</code></td>
					</tr>
					<tr>
						<td><b><a href='https://github.com/FabsMS/SIGA---Talonario-Eletronico/blob/master/components/Sidebar/Sidebar.tsx'>Sidebar.tsx</a></b></td>
						<td><code>❯ REPLACE-ME</code></td>
					</tr>
					<tr>
						<td><b><a href='https://github.com/FabsMS/SIGA---Talonario-Eletronico/blob/master/components/Sidebar/NavLinkClient.tsx'>NavLinkClient.tsx</a></b></td>
						<td><code>❯ REPLACE-ME</code></td>
					</tr>
					<tr>
						<td><b><a href='https://github.com/FabsMS/SIGA---Talonario-Eletronico/blob/master/components/Sidebar/UserMenu.tsx'>UserMenu.tsx</a></b></td>
						<td><code>❯ REPLACE-ME</code></td>
					</tr>
					</table>
				</blockquote>
			</details>
		</blockquote>
	</details>
	<details> <!-- types Submodule -->
		<summary><b>types</b></summary>
		<blockquote>
			<table>
			<tr>
				<td><b><a href='https://github.com/FabsMS/SIGA---Talonario-Eletronico/blob/master/types/transportes.ts'>transportes.ts</a></b></td>
				<td><code>❯ REPLACE-ME</code></td>
			</tr>
			<tr>
				<td><b><a href='https://github.com/FabsMS/SIGA---Talonario-Eletronico/blob/master/types/index.ts'>index.ts</a></b></td>
				<td><code>❯ REPLACE-ME</code></td>
			</tr>
			<tr>
				<td><b><a href='https://github.com/FabsMS/SIGA---Talonario-Eletronico/blob/master/types/table.ts'>table.ts</a></b></td>
				<td><code>❯ REPLACE-ME</code></td>
			</tr>
			<tr>
				<td><b><a href='https://github.com/FabsMS/SIGA---Talonario-Eletronico/blob/master/types/ait.ts'>ait.ts</a></b></td>
				<td><code>❯ REPLACE-ME</code></td>
			</tr>
			<tr>
				<td><b><a href='https://github.com/FabsMS/SIGA---Talonario-Eletronico/blob/master/types/veiculos.ts'>veiculos.ts</a></b></td>
				<td><code>❯ REPLACE-ME</code></td>
			</tr>
			<tr>
				<td><b><a href='https://github.com/FabsMS/SIGA---Talonario-Eletronico/blob/master/types/condutores.ts'>condutores.ts</a></b></td>
				<td><code>❯ REPLACE-ME</code></td>
			</tr>
			<tr>
				<td><b><a href='https://github.com/FabsMS/SIGA---Talonario-Eletronico/blob/master/types/lotes.ts'>lotes.ts</a></b></td>
				<td><code>❯ REPLACE-ME</code></td>
			</tr>
			<tr>
				<td><b><a href='https://github.com/FabsMS/SIGA---Talonario-Eletronico/blob/master/types/auth.ts'>auth.ts</a></b></td>
				<td><code>❯ REPLACE-ME</code></td>
			</tr>
			<tr>
				<td><b><a href='https://github.com/FabsMS/SIGA---Talonario-Eletronico/blob/master/types/usuarios.ts'>usuarios.ts</a></b></td>
				<td><code>❯ REPLACE-ME</code></td>
			</tr>
			<tr>
				<td><b><a href='https://github.com/FabsMS/SIGA---Talonario-Eletronico/blob/master/types/consultas.ts'>consultas.ts</a></b></td>
				<td><code>❯ REPLACE-ME</code></td>
			</tr>
			<tr>
				<td><b><a href='https://github.com/FabsMS/SIGA---Talonario-Eletronico/blob/master/types/infracoes.ts'>infracoes.ts</a></b></td>
				<td><code>❯ REPLACE-ME</code></td>
			</tr>
			<tr>
				<td><b><a href='https://github.com/FabsMS/SIGA---Talonario-Eletronico/blob/master/types/navigation.ts'>navigation.ts</a></b></td>
				<td><code>❯ REPLACE-ME</code></td>
			</tr>
			</table>
		</blockquote>
	</details>
	<details> <!-- lib Submodule -->
		<summary><b>lib</b></summary>
		<blockquote>
			<table>
			<tr>
				<td><b><a href='https://github.com/FabsMS/SIGA---Talonario-Eletronico/blob/master/lib/api.ts'>api.ts</a></b></td>
				<td><code>❯ REPLACE-ME</code></td>
			</tr>
			</table>
		</blockquote>
	</details>
</details>

---
##  Getting Started

###  Prerequisites

Before getting started with SIGA---Talonario-Eletronico, ensure your runtime environment meets the following requirements:

- **Programming Language:** TypeScript
- **Package Manager:** Npm


###  Installation

Install SIGA---Talonario-Eletronico using one of the following methods:

**Build from source:**

1. Clone the SIGA---Talonario-Eletronico repository:
```sh
❯ git clone https://github.com/FabsMS/SIGA---Talonario-Eletronico
```

2. Navigate to the project directory:
```sh
❯ cd SIGA---Talonario-Eletronico
```

3. Install the project dependencies:


**Using `npm`** &nbsp; [<img align="center" src="https://img.shields.io/badge/npm-CB3837.svg?style={badge_style}&logo=npm&logoColor=white" />](https://www.npmjs.com/)

```sh
❯ npm install
```




###  Usage
Run SIGA---Talonario-Eletronico using the following command:
**Using `npm`** &nbsp; [<img align="center" src="https://img.shields.io/badge/npm-CB3837.svg?style={badge_style}&logo=npm&logoColor=white" />](https://www.npmjs.com/)

```sh
❯ npm start
```


###  Testing
Run the test suite using the following command:
**Using `npm`** &nbsp; [<img align="center" src="https://img.shields.io/badge/npm-CB3837.svg?style={badge_style}&logo=npm&logoColor=white" />](https://www.npmjs.com/)

```sh
❯ npm test
```


---
##  Project Roadmap

- [X] **`Task 1`**: <strike>Implement feature one.</strike>
- [ ] **`Task 2`**: Implement feature two.
- [ ] **`Task 3`**: Implement feature three.

---

##  Contributing

- **💬 [Join the Discussions](https://github.com/FabsMS/SIGA---Talonario-Eletronico/discussions)**: Share your insights, provide feedback, or ask questions.
- **🐛 [Report Issues](https://github.com/FabsMS/SIGA---Talonario-Eletronico/issues)**: Submit bugs found or log feature requests for the `SIGA---Talonario-Eletronico` project.
- **💡 [Submit Pull Requests](https://github.com/FabsMS/SIGA---Talonario-Eletronico/blob/main/CONTRIBUTING.md)**: Review open PRs, and submit your own PRs.

<details closed>
<summary>Contributing Guidelines</summary>

1. **Fork the Repository**: Start by forking the project repository to your github account.
2. **Clone Locally**: Clone the forked repository to your local machine using a git client.
   ```sh
   git clone https://github.com/FabsMS/SIGA---Talonario-Eletronico
   ```
3. **Create a New Branch**: Always work on a new branch, giving it a descriptive name.
   ```sh
   git checkout -b new-feature-x
   ```
4. **Make Your Changes**: Develop and test your changes locally.
5. **Commit Your Changes**: Commit with a clear message describing your updates.
   ```sh
   git commit -m 'Implemented new feature x.'
   ```
6. **Push to github**: Push the changes to your forked repository.
   ```sh
   git push origin new-feature-x
   ```
7. **Submit a Pull Request**: Create a PR against the original project repository. Clearly describe the changes and their motivations.
8. **Review**: Once your PR is reviewed and approved, it will be merged into the main branch. Congratulations on your contribution!
</details>

<details closed>
<summary>Contributor Graph</summary>
<br>
<p align="left">
   <a href="https://github.com{/FabsMS/SIGA---Talonario-Eletronico/}graphs/contributors">
      <img src="https://contrib.rocks/image?repo=FabsMS/SIGA---Talonario-Eletronico">
   </a>
</p>
</details>

---

##  License

This project is protected under the [SELECT-A-LICENSE](https://choosealicense.com/licenses) License. For more details, refer to the [LICENSE](https://choosealicense.com/licenses/) file.

---

##  Acknowledgments

- List any resources, contributors, inspiration, etc. here.

---
