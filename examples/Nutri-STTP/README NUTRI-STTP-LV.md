<p align="center">
    <img src="https://raw.githubusercontent.com/PKief/vscode-material-icon-theme/ec559a9f6bfd399b82bb44393651661b08aaf7ba/icons/folder-markdown-open.svg" align="center" width="30%">
</p>
<p align="center"><h1 align="center">NUTRI-STTP-LV</h1></p>
<p align="center">
	<em><code>❯ REPLACE-ME</code></em>
</p>
<p align="center">
	<img src="https://img.shields.io/github/license/FabsMS/Nutri-STTP-LV?style=default&logo=opensourceinitiative&logoColor=white&color=0080ff" alt="license">
	<img src="https://img.shields.io/github/last-commit/FabsMS/Nutri-STTP-LV?style=default&logo=git&logoColor=white&color=0080ff" alt="last-commit">
	<img src="https://img.shields.io/github/languages/top/FabsMS/Nutri-STTP-LV?style=default&color=0080ff" alt="repo-top-language">
	<img src="https://img.shields.io/github/languages/count/FabsMS/Nutri-STTP-LV?style=default&color=0080ff" alt="repo-language-count">
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
└── Nutri-STTP-LV/
    ├── Dockerfile
    ├── README.md
    ├── dist
    │   ├── ArchivesAnimations
    │   │   └── JSON-Loader.json
    │   ├── assets
    │   │   ├── index-C_UZkWuT.css
    │   │   └── index-DCotEvNg.js
    │   ├── img
    │   │   ├── Logo Nutri STTP.png
    │   │   ├── Logo-Vetorizada.svg
    │   │   ├── background.png
    │   │   ├── background2.png
    │   │   ├── home-removebg-preview.png
    │   │   ├── home.png
    │   │   ├── icon-nutri-azul.png
    │   │   ├── icon-nutri.png
    │   │   ├── icon-paciente-verde.png
    │   │   ├── icon-paciente.png
    │   │   ├── icon-user-group-solid.svg
    │   │   ├── icon-user-solid.svg
    │   │   ├── imagem-home.png
    │   │   ├── logo-campina-grande.png
    │   │   └── logo-sttp-preto2.png
    │   └── index.html
    ├── index.html
    ├── package-lock.json
    ├── package.json
    ├── public
    │   ├── ArchivesAnimations
    │   │   └── JSON-Loader.json
    │   └── img
    │       ├── Logo Nutri STTP.png
    │       ├── Logo-Vetorizada.svg
    │       ├── background.png
    │       ├── background2.png
    │       ├── home-removebg-preview.png
    │       ├── home.png
    │       ├── icon-nutri-azul.png
    │       ├── icon-nutri.png
    │       ├── icon-paciente-verde.png
    │       ├── icon-paciente.png
    │       ├── icon-user-group-solid.svg
    │       ├── icon-user-solid.svg
    │       ├── imagem-home.png
    │       ├── logo-campina-grande.png
    │       └── logo-sttp-preto2.png
    ├── services
    │   ├── ConsultaService.js
    │   ├── HttpService.js
    │   └── UserService.js
    ├── src
    │   ├── Animations
    │   │   └── Loader.jsx
    │   ├── App.jsx
    │   ├── assets
    │   │   └── react.svg
    │   ├── components
    │   │   ├── BlocoDeConsulta
    │   │   │   └── index.jsx
    │   │   ├── BlocoDeConsultaMarcada
    │   │   │   └── index.jsx
    │   │   ├── Button
    │   │   │   └── TypeSignup.jsx
    │   │   ├── CalendarioAgendamento
    │   │   │   └── index.jsx
    │   │   ├── CalendarioMarcacao
    │   │   │   └── index.jsx
    │   │   ├── Filtro
    │   │   │   └── index.jsx
    │   │   ├── Form
    │   │   │   ├── Input.jsx
    │   │   │   ├── Password.jsx
    │   │   │   └── Select.jsx
    │   │   ├── FormAnamnese
    │   │   │   ├── InpuData.jsx
    │   │   │   ├── InputAlimentos.jsx
    │   │   │   ├── InputDados.jsx
    │   │   │   ├── InputIMC.jsx
    │   │   │   ├── InputImagem.jsx
    │   │   │   ├── InputMultiline.jsx
    │   │   │   ├── SelectPacientes.jsx
    │   │   │   └── Timer.jsx
    │   │   ├── FormCadastroDependente
    │   │   │   └── index.jsx
    │   │   ├── FormPerfilNutricionista
    │   │   │   └── index.jsx
    │   │   ├── FormPerfilPaciente
    │   │   │   ├── graficoArea.jsx
    │   │   │   ├── graficoLinhas.jsx
    │   │   │   └── index.jsx
    │   │   ├── HeaderNutricionista
    │   │   │   └── index.jsx
    │   │   ├── HeaderPaciente
    │   │   │   └── index.jsx
    │   │   ├── Modais
    │   │   │   ├── ModalCadastramento
    │   │   │   │   └── index.jsx
    │   │   │   ├── ModalDetalhePaciente
    │   │   │   │   └── index.jsx
    │   │   │   └── ModalEdicaoServidor
    │   │   │       └── index.jsx
    │   │   ├── Stepper
    │   │   │   └── index.jsx
    │   │   ├── StepperGerenciamentoDatas
    │   │   │   └── index.jsx
    │   │   └── TabelaServidores
    │   │       └── index.jsx
    │   ├── contexts
    │   │   ├── CpfChecado.jsx
    │   │   └── ListaPacientes.jsx
    │   ├── index.css
    │   ├── main.jsx
    │   ├── pages
    │   │   ├── Anamnese
    │   │   │   └── index.jsx
    │   │   ├── CadastroDependente
    │   │   │   └── index.jsx
    │   │   ├── ChecagemCPF
    │   │   │   └── index.jsx
    │   │   ├── ConsultasMarcadas
    │   │   │   └── index.jsx
    │   │   ├── ForgotPassword
    │   │   │   └── index.jsx
    │   │   ├── HomeNutricionista
    │   │   │   └── index.jsx
    │   │   ├── HomePaciente
    │   │   │   └── index.jsx
    │   │   ├── ListaServidores
    │   │   │   └── index.jsx
    │   │   ├── MarcarConsultaNutricionista
    │   │   │   └── index.jsx
    │   │   ├── MarcarConsultaPaciente
    │   │   │   └── index.jsx
    │   │   ├── NewPassword
    │   │   │   └── index.jsx
    │   │   ├── PerfilNutricionista
    │   │   │   └── index.jsx
    │   │   ├── PerfilPaciente
    │   │   │   └── index.jsx
    │   │   ├── SignupNutricionista
    │   │   │   └── index.jsx
    │   │   ├── SignupPaciente
    │   │   │   └── index.jsx
    │   │   ├── Singin
    │   │   │   └── index.jsx
    │   │   └── TypeSignup
    │   │       └── index.jsx
    │   └── routes
    │       └── index.jsx
    └── vite.config.js
```


###  Project Index
<details open>
	<summary><b><code>NUTRI-STTP-LV/</code></b></summary>
	<details> <!-- __root__ Submodule -->
		<summary><b>__root__</b></summary>
		<blockquote>
			<table>
			<tr>
				<td><b><a href='https://github.com/FabsMS/Nutri-STTP-LV/blob/master/package-lock.json'>package-lock.json</a></b></td>
				<td><code>❯ REPLACE-ME</code></td>
			</tr>
			<tr>
				<td><b><a href='https://github.com/FabsMS/Nutri-STTP-LV/blob/master/vite.config.js'>vite.config.js</a></b></td>
				<td><code>❯ REPLACE-ME</code></td>
			</tr>
			<tr>
				<td><b><a href='https://github.com/FabsMS/Nutri-STTP-LV/blob/master/Dockerfile'>Dockerfile</a></b></td>
				<td><code>❯ REPLACE-ME</code></td>
			</tr>
			<tr>
				<td><b><a href='https://github.com/FabsMS/Nutri-STTP-LV/blob/master/index.html'>index.html</a></b></td>
				<td><code>❯ REPLACE-ME</code></td>
			</tr>
			<tr>
				<td><b><a href='https://github.com/FabsMS/Nutri-STTP-LV/blob/master/package.json'>package.json</a></b></td>
				<td><code>❯ REPLACE-ME</code></td>
			</tr>
			</table>
		</blockquote>
	</details>
	<details> <!-- services Submodule -->
		<summary><b>services</b></summary>
		<blockquote>
			<table>
			<tr>
				<td><b><a href='https://github.com/FabsMS/Nutri-STTP-LV/blob/master/services/UserService.js'>UserService.js</a></b></td>
				<td><code>❯ REPLACE-ME</code></td>
			</tr>
			<tr>
				<td><b><a href='https://github.com/FabsMS/Nutri-STTP-LV/blob/master/services/ConsultaService.js'>ConsultaService.js</a></b></td>
				<td><code>❯ REPLACE-ME</code></td>
			</tr>
			<tr>
				<td><b><a href='https://github.com/FabsMS/Nutri-STTP-LV/blob/master/services/HttpService.js'>HttpService.js</a></b></td>
				<td><code>❯ REPLACE-ME</code></td>
			</tr>
			</table>
		</blockquote>
	</details>
	<details> <!-- public Submodule -->
		<summary><b>public</b></summary>
		<blockquote>
			<details>
				<summary><b>ArchivesAnimations</b></summary>
				<blockquote>
					<table>
					<tr>
						<td><b><a href='https://github.com/FabsMS/Nutri-STTP-LV/blob/master/public/ArchivesAnimations/JSON-Loader.json'>JSON-Loader.json</a></b></td>
						<td><code>❯ REPLACE-ME</code></td>
					</tr>
					</table>
				</blockquote>
			</details>
		</blockquote>
	</details>
	<details> <!-- src Submodule -->
		<summary><b>src</b></summary>
		<blockquote>
			<table>
			<tr>
				<td><b><a href='https://github.com/FabsMS/Nutri-STTP-LV/blob/master/src/index.css'>index.css</a></b></td>
				<td><code>❯ REPLACE-ME</code></td>
			</tr>
			<tr>
				<td><b><a href='https://github.com/FabsMS/Nutri-STTP-LV/blob/master/src/App.jsx'>App.jsx</a></b></td>
				<td><code>❯ REPLACE-ME</code></td>
			</tr>
			<tr>
				<td><b><a href='https://github.com/FabsMS/Nutri-STTP-LV/blob/master/src/main.jsx'>main.jsx</a></b></td>
				<td><code>❯ REPLACE-ME</code></td>
			</tr>
			</table>
			<details>
				<summary><b>contexts</b></summary>
				<blockquote>
					<table>
					<tr>
						<td><b><a href='https://github.com/FabsMS/Nutri-STTP-LV/blob/master/src/contexts/CpfChecado.jsx'>CpfChecado.jsx</a></b></td>
						<td><code>❯ REPLACE-ME</code></td>
					</tr>
					<tr>
						<td><b><a href='https://github.com/FabsMS/Nutri-STTP-LV/blob/master/src/contexts/ListaPacientes.jsx'>ListaPacientes.jsx</a></b></td>
						<td><code>❯ REPLACE-ME</code></td>
					</tr>
					</table>
				</blockquote>
			</details>
			<details>
				<summary><b>components</b></summary>
				<blockquote>
					<details>
						<summary><b>BlocoDeConsultaMarcada</b></summary>
						<blockquote>
							<table>
							<tr>
								<td><b><a href='https://github.com/FabsMS/Nutri-STTP-LV/blob/master/src/components/BlocoDeConsultaMarcada/index.jsx'>index.jsx</a></b></td>
								<td><code>❯ REPLACE-ME</code></td>
							</tr>
							</table>
						</blockquote>
					</details>
					<details>
						<summary><b>BlocoDeConsulta</b></summary>
						<blockquote>
							<table>
							<tr>
								<td><b><a href='https://github.com/FabsMS/Nutri-STTP-LV/blob/master/src/components/BlocoDeConsulta/index.jsx'>index.jsx</a></b></td>
								<td><code>❯ REPLACE-ME</code></td>
							</tr>
							</table>
						</blockquote>
					</details>
					<details>
						<summary><b>Button</b></summary>
						<blockquote>
							<table>
							<tr>
								<td><b><a href='https://github.com/FabsMS/Nutri-STTP-LV/blob/master/src/components/Button/TypeSignup.jsx'>TypeSignup.jsx</a></b></td>
								<td><code>❯ REPLACE-ME</code></td>
							</tr>
							</table>
						</blockquote>
					</details>
					<details>
						<summary><b>FormCadastroDependente</b></summary>
						<blockquote>
							<table>
							<tr>
								<td><b><a href='https://github.com/FabsMS/Nutri-STTP-LV/blob/master/src/components/FormCadastroDependente/index.jsx'>index.jsx</a></b></td>
								<td><code>❯ REPLACE-ME</code></td>
							</tr>
							</table>
						</blockquote>
					</details>
					<details>
						<summary><b>CalendarioMarcacao</b></summary>
						<blockquote>
							<table>
							<tr>
								<td><b><a href='https://github.com/FabsMS/Nutri-STTP-LV/blob/master/src/components/CalendarioMarcacao/index.jsx'>index.jsx</a></b></td>
								<td><code>❯ REPLACE-ME</code></td>
							</tr>
							</table>
						</blockquote>
					</details>
					<details>
						<summary><b>TabelaServidores</b></summary>
						<blockquote>
							<table>
							<tr>
								<td><b><a href='https://github.com/FabsMS/Nutri-STTP-LV/blob/master/src/components/TabelaServidores/index.jsx'>index.jsx</a></b></td>
								<td><code>❯ REPLACE-ME</code></td>
							</tr>
							</table>
						</blockquote>
					</details>
					<details>
						<summary><b>Modais</b></summary>
						<blockquote>
							<details>
								<summary><b>ModalEdicaoServidor</b></summary>
								<blockquote>
									<table>
									<tr>
										<td><b><a href='https://github.com/FabsMS/Nutri-STTP-LV/blob/master/src/components/Modais/ModalEdicaoServidor/index.jsx'>index.jsx</a></b></td>
										<td><code>❯ REPLACE-ME</code></td>
									</tr>
									</table>
								</blockquote>
							</details>
							<details>
								<summary><b>ModalCadastramento</b></summary>
								<blockquote>
									<table>
									<tr>
										<td><b><a href='https://github.com/FabsMS/Nutri-STTP-LV/blob/master/src/components/Modais/ModalCadastramento/index.jsx'>index.jsx</a></b></td>
										<td><code>❯ REPLACE-ME</code></td>
									</tr>
									</table>
								</blockquote>
							</details>
							<details>
								<summary><b>ModalDetalhePaciente</b></summary>
								<blockquote>
									<table>
									<tr>
										<td><b><a href='https://github.com/FabsMS/Nutri-STTP-LV/blob/master/src/components/Modais/ModalDetalhePaciente/index.jsx'>index.jsx</a></b></td>
										<td><code>❯ REPLACE-ME</code></td>
									</tr>
									</table>
								</blockquote>
							</details>
						</blockquote>
					</details>
					<details>
						<summary><b>CalendarioAgendamento</b></summary>
						<blockquote>
							<table>
							<tr>
								<td><b><a href='https://github.com/FabsMS/Nutri-STTP-LV/blob/master/src/components/CalendarioAgendamento/index.jsx'>index.jsx</a></b></td>
								<td><code>❯ REPLACE-ME</code></td>
							</tr>
							</table>
						</blockquote>
					</details>
					<details>
						<summary><b>HeaderNutricionista</b></summary>
						<blockquote>
							<table>
							<tr>
								<td><b><a href='https://github.com/FabsMS/Nutri-STTP-LV/blob/master/src/components/HeaderNutricionista/index.jsx'>index.jsx</a></b></td>
								<td><code>❯ REPLACE-ME</code></td>
							</tr>
							</table>
						</blockquote>
					</details>
					<details>
						<summary><b>StepperGerenciamentoDatas</b></summary>
						<blockquote>
							<table>
							<tr>
								<td><b><a href='https://github.com/FabsMS/Nutri-STTP-LV/blob/master/src/components/StepperGerenciamentoDatas/index.jsx'>index.jsx</a></b></td>
								<td><code>❯ REPLACE-ME</code></td>
							</tr>
							</table>
						</blockquote>
					</details>
					<details>
						<summary><b>FormPerfilPaciente</b></summary>
						<blockquote>
							<table>
							<tr>
								<td><b><a href='https://github.com/FabsMS/Nutri-STTP-LV/blob/master/src/components/FormPerfilPaciente/index.jsx'>index.jsx</a></b></td>
								<td><code>❯ REPLACE-ME</code></td>
							</tr>
							<tr>
								<td><b><a href='https://github.com/FabsMS/Nutri-STTP-LV/blob/master/src/components/FormPerfilPaciente/graficoLinhas.jsx'>graficoLinhas.jsx</a></b></td>
								<td><code>❯ REPLACE-ME</code></td>
							</tr>
							<tr>
								<td><b><a href='https://github.com/FabsMS/Nutri-STTP-LV/blob/master/src/components/FormPerfilPaciente/graficoArea.jsx'>graficoArea.jsx</a></b></td>
								<td><code>❯ REPLACE-ME</code></td>
							</tr>
							</table>
						</blockquote>
					</details>
					<details>
						<summary><b>FormAnamnese</b></summary>
						<blockquote>
							<table>
							<tr>
								<td><b><a href='https://github.com/FabsMS/Nutri-STTP-LV/blob/master/src/components/FormAnamnese/InputAlimentos.jsx'>InputAlimentos.jsx</a></b></td>
								<td><code>❯ REPLACE-ME</code></td>
							</tr>
							<tr>
								<td><b><a href='https://github.com/FabsMS/Nutri-STTP-LV/blob/master/src/components/FormAnamnese/InputMultiline.jsx'>InputMultiline.jsx</a></b></td>
								<td><code>❯ REPLACE-ME</code></td>
							</tr>
							<tr>
								<td><b><a href='https://github.com/FabsMS/Nutri-STTP-LV/blob/master/src/components/FormAnamnese/InpuData.jsx'>InpuData.jsx</a></b></td>
								<td><code>❯ REPLACE-ME</code></td>
							</tr>
							<tr>
								<td><b><a href='https://github.com/FabsMS/Nutri-STTP-LV/blob/master/src/components/FormAnamnese/InputIMC.jsx'>InputIMC.jsx</a></b></td>
								<td><code>❯ REPLACE-ME</code></td>
							</tr>
							<tr>
								<td><b><a href='https://github.com/FabsMS/Nutri-STTP-LV/blob/master/src/components/FormAnamnese/SelectPacientes.jsx'>SelectPacientes.jsx</a></b></td>
								<td><code>❯ REPLACE-ME</code></td>
							</tr>
							<tr>
								<td><b><a href='https://github.com/FabsMS/Nutri-STTP-LV/blob/master/src/components/FormAnamnese/InputDados.jsx'>InputDados.jsx</a></b></td>
								<td><code>❯ REPLACE-ME</code></td>
							</tr>
							<tr>
								<td><b><a href='https://github.com/FabsMS/Nutri-STTP-LV/blob/master/src/components/FormAnamnese/Timer.jsx'>Timer.jsx</a></b></td>
								<td><code>❯ REPLACE-ME</code></td>
							</tr>
							<tr>
								<td><b><a href='https://github.com/FabsMS/Nutri-STTP-LV/blob/master/src/components/FormAnamnese/InputImagem.jsx'>InputImagem.jsx</a></b></td>
								<td><code>❯ REPLACE-ME</code></td>
							</tr>
							</table>
						</blockquote>
					</details>
					<details>
						<summary><b>HeaderPaciente</b></summary>
						<blockquote>
							<table>
							<tr>
								<td><b><a href='https://github.com/FabsMS/Nutri-STTP-LV/blob/master/src/components/HeaderPaciente/index.jsx'>index.jsx</a></b></td>
								<td><code>❯ REPLACE-ME</code></td>
							</tr>
							</table>
						</blockquote>
					</details>
					<details>
						<summary><b>Form</b></summary>
						<blockquote>
							<table>
							<tr>
								<td><b><a href='https://github.com/FabsMS/Nutri-STTP-LV/blob/master/src/components/Form/Input.jsx'>Input.jsx</a></b></td>
								<td><code>❯ REPLACE-ME</code></td>
							</tr>
							<tr>
								<td><b><a href='https://github.com/FabsMS/Nutri-STTP-LV/blob/master/src/components/Form/Select.jsx'>Select.jsx</a></b></td>
								<td><code>❯ REPLACE-ME</code></td>
							</tr>
							<tr>
								<td><b><a href='https://github.com/FabsMS/Nutri-STTP-LV/blob/master/src/components/Form/Password.jsx'>Password.jsx</a></b></td>
								<td><code>❯ REPLACE-ME</code></td>
							</tr>
							</table>
						</blockquote>
					</details>
					<details>
						<summary><b>FormPerfilNutricionista</b></summary>
						<blockquote>
							<table>
							<tr>
								<td><b><a href='https://github.com/FabsMS/Nutri-STTP-LV/blob/master/src/components/FormPerfilNutricionista/index.jsx'>index.jsx</a></b></td>
								<td><code>❯ REPLACE-ME</code></td>
							</tr>
							</table>
						</blockquote>
					</details>
					<details>
						<summary><b>Filtro</b></summary>
						<blockquote>
							<table>
							<tr>
								<td><b><a href='https://github.com/FabsMS/Nutri-STTP-LV/blob/master/src/components/Filtro/index.jsx'>index.jsx</a></b></td>
								<td><code>❯ REPLACE-ME</code></td>
							</tr>
							</table>
						</blockquote>
					</details>
					<details>
						<summary><b>Stepper</b></summary>
						<blockquote>
							<table>
							<tr>
								<td><b><a href='https://github.com/FabsMS/Nutri-STTP-LV/blob/master/src/components/Stepper/index.jsx'>index.jsx</a></b></td>
								<td><code>❯ REPLACE-ME</code></td>
							</tr>
							</table>
						</blockquote>
					</details>
				</blockquote>
			</details>
			<details>
				<summary><b>Animations</b></summary>
				<blockquote>
					<table>
					<tr>
						<td><b><a href='https://github.com/FabsMS/Nutri-STTP-LV/blob/master/src/Animations/Loader.jsx'>Loader.jsx</a></b></td>
						<td><code>❯ REPLACE-ME</code></td>
					</tr>
					</table>
				</blockquote>
			</details>
			<details>
				<summary><b>routes</b></summary>
				<blockquote>
					<table>
					<tr>
						<td><b><a href='https://github.com/FabsMS/Nutri-STTP-LV/blob/master/src/routes/index.jsx'>index.jsx</a></b></td>
						<td><code>❯ REPLACE-ME</code></td>
					</tr>
					</table>
				</blockquote>
			</details>
			<details>
				<summary><b>pages</b></summary>
				<blockquote>
					<details>
						<summary><b>CadastroDependente</b></summary>
						<blockquote>
							<table>
							<tr>
								<td><b><a href='https://github.com/FabsMS/Nutri-STTP-LV/blob/master/src/pages/CadastroDependente/index.jsx'>index.jsx</a></b></td>
								<td><code>❯ REPLACE-ME</code></td>
							</tr>
							</table>
						</blockquote>
					</details>
					<details>
						<summary><b>ForgotPassword</b></summary>
						<blockquote>
							<table>
							<tr>
								<td><b><a href='https://github.com/FabsMS/Nutri-STTP-LV/blob/master/src/pages/ForgotPassword/index.jsx'>index.jsx</a></b></td>
								<td><code>❯ REPLACE-ME</code></td>
							</tr>
							</table>
						</blockquote>
					</details>
					<details>
						<summary><b>Singin</b></summary>
						<blockquote>
							<table>
							<tr>
								<td><b><a href='https://github.com/FabsMS/Nutri-STTP-LV/blob/master/src/pages/Singin/index.jsx'>index.jsx</a></b></td>
								<td><code>❯ REPLACE-ME</code></td>
							</tr>
							</table>
						</blockquote>
					</details>
					<details>
						<summary><b>MarcarConsultaNutricionista</b></summary>
						<blockquote>
							<table>
							<tr>
								<td><b><a href='https://github.com/FabsMS/Nutri-STTP-LV/blob/master/src/pages/MarcarConsultaNutricionista/index.jsx'>index.jsx</a></b></td>
								<td><code>❯ REPLACE-ME</code></td>
							</tr>
							</table>
						</blockquote>
					</details>
					<details>
						<summary><b>NewPassword</b></summary>
						<blockquote>
							<table>
							<tr>
								<td><b><a href='https://github.com/FabsMS/Nutri-STTP-LV/blob/master/src/pages/NewPassword/index.jsx'>index.jsx</a></b></td>
								<td><code>❯ REPLACE-ME</code></td>
							</tr>
							</table>
						</blockquote>
					</details>
					<details>
						<summary><b>PerfilPaciente</b></summary>
						<blockquote>
							<table>
							<tr>
								<td><b><a href='https://github.com/FabsMS/Nutri-STTP-LV/blob/master/src/pages/PerfilPaciente/index.jsx'>index.jsx</a></b></td>
								<td><code>❯ REPLACE-ME</code></td>
							</tr>
							</table>
						</blockquote>
					</details>
					<details>
						<summary><b>TypeSignup</b></summary>
						<blockquote>
							<table>
							<tr>
								<td><b><a href='https://github.com/FabsMS/Nutri-STTP-LV/blob/master/src/pages/TypeSignup/index.jsx'>index.jsx</a></b></td>
								<td><code>❯ REPLACE-ME</code></td>
							</tr>
							</table>
						</blockquote>
					</details>
					<details>
						<summary><b>ListaServidores</b></summary>
						<blockquote>
							<table>
							<tr>
								<td><b><a href='https://github.com/FabsMS/Nutri-STTP-LV/blob/master/src/pages/ListaServidores/index.jsx'>index.jsx</a></b></td>
								<td><code>❯ REPLACE-ME</code></td>
							</tr>
							</table>
						</blockquote>
					</details>
					<details>
						<summary><b>Anamnese</b></summary>
						<blockquote>
							<table>
							<tr>
								<td><b><a href='https://github.com/FabsMS/Nutri-STTP-LV/blob/master/src/pages/Anamnese/index.jsx'>index.jsx</a></b></td>
								<td><code>❯ REPLACE-ME</code></td>
							</tr>
							</table>
						</blockquote>
					</details>
					<details>
						<summary><b>ConsultasMarcadas</b></summary>
						<blockquote>
							<table>
							<tr>
								<td><b><a href='https://github.com/FabsMS/Nutri-STTP-LV/blob/master/src/pages/ConsultasMarcadas/index.jsx'>index.jsx</a></b></td>
								<td><code>❯ REPLACE-ME</code></td>
							</tr>
							</table>
						</blockquote>
					</details>
					<details>
						<summary><b>MarcarConsultaPaciente</b></summary>
						<blockquote>
							<table>
							<tr>
								<td><b><a href='https://github.com/FabsMS/Nutri-STTP-LV/blob/master/src/pages/MarcarConsultaPaciente/index.jsx'>index.jsx</a></b></td>
								<td><code>❯ REPLACE-ME</code></td>
							</tr>
							</table>
						</blockquote>
					</details>
					<details>
						<summary><b>HomePaciente</b></summary>
						<blockquote>
							<table>
							<tr>
								<td><b><a href='https://github.com/FabsMS/Nutri-STTP-LV/blob/master/src/pages/HomePaciente/index.jsx'>index.jsx</a></b></td>
								<td><code>❯ REPLACE-ME</code></td>
							</tr>
							</table>
						</blockquote>
					</details>
					<details>
						<summary><b>SignupNutricionista</b></summary>
						<blockquote>
							<table>
							<tr>
								<td><b><a href='https://github.com/FabsMS/Nutri-STTP-LV/blob/master/src/pages/SignupNutricionista/index.jsx'>index.jsx</a></b></td>
								<td><code>❯ REPLACE-ME</code></td>
							</tr>
							</table>
						</blockquote>
					</details>
					<details>
						<summary><b>ChecagemCPF</b></summary>
						<blockquote>
							<table>
							<tr>
								<td><b><a href='https://github.com/FabsMS/Nutri-STTP-LV/blob/master/src/pages/ChecagemCPF/index.jsx'>index.jsx</a></b></td>
								<td><code>❯ REPLACE-ME</code></td>
							</tr>
							</table>
						</blockquote>
					</details>
					<details>
						<summary><b>HomeNutricionista</b></summary>
						<blockquote>
							<table>
							<tr>
								<td><b><a href='https://github.com/FabsMS/Nutri-STTP-LV/blob/master/src/pages/HomeNutricionista/index.jsx'>index.jsx</a></b></td>
								<td><code>❯ REPLACE-ME</code></td>
							</tr>
							</table>
						</blockquote>
					</details>
					<details>
						<summary><b>PerfilNutricionista</b></summary>
						<blockquote>
							<table>
							<tr>
								<td><b><a href='https://github.com/FabsMS/Nutri-STTP-LV/blob/master/src/pages/PerfilNutricionista/index.jsx'>index.jsx</a></b></td>
								<td><code>❯ REPLACE-ME</code></td>
							</tr>
							</table>
						</blockquote>
					</details>
					<details>
						<summary><b>SignupPaciente</b></summary>
						<blockquote>
							<table>
							<tr>
								<td><b><a href='https://github.com/FabsMS/Nutri-STTP-LV/blob/master/src/pages/SignupPaciente/index.jsx'>index.jsx</a></b></td>
								<td><code>❯ REPLACE-ME</code></td>
							</tr>
							</table>
						</blockquote>
					</details>
				</blockquote>
			</details>
		</blockquote>
	</details>
</details>

---
##  Getting Started

###  Prerequisites

Before getting started with Nutri-STTP-LV, ensure your runtime environment meets the following requirements:

- **Programming Language:** JavaScript
- **Package Manager:** Npm
- **Container Runtime:** Docker


###  Installation

Install Nutri-STTP-LV using one of the following methods:

**Build from source:**

1. Clone the Nutri-STTP-LV repository:
```sh
❯ git clone https://github.com/FabsMS/Nutri-STTP-LV
```

2. Navigate to the project directory:
```sh
❯ cd Nutri-STTP-LV
```

3. Install the project dependencies:


**Using `npm`** &nbsp; [<img align="center" src="https://img.shields.io/badge/npm-CB3837.svg?style={badge_style}&logo=npm&logoColor=white" />](https://www.npmjs.com/)

```sh
❯ npm install
```


**Using `docker`** &nbsp; [<img align="center" src="https://img.shields.io/badge/Docker-2CA5E0.svg?style={badge_style}&logo=docker&logoColor=white" />](https://www.docker.com/)

```sh
❯ docker build -t FabsMS/Nutri-STTP-LV .
```




###  Usage
Run Nutri-STTP-LV using the following command:
**Using `npm`** &nbsp; [<img align="center" src="https://img.shields.io/badge/npm-CB3837.svg?style={badge_style}&logo=npm&logoColor=white" />](https://www.npmjs.com/)

```sh
❯ npm start
```


**Using `docker`** &nbsp; [<img align="center" src="https://img.shields.io/badge/Docker-2CA5E0.svg?style={badge_style}&logo=docker&logoColor=white" />](https://www.docker.com/)

```sh
❯ docker run -it {image_name}
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

- **💬 [Join the Discussions](https://github.com/FabsMS/Nutri-STTP-LV/discussions)**: Share your insights, provide feedback, or ask questions.
- **🐛 [Report Issues](https://github.com/FabsMS/Nutri-STTP-LV/issues)**: Submit bugs found or log feature requests for the `Nutri-STTP-LV` project.
- **💡 [Submit Pull Requests](https://github.com/FabsMS/Nutri-STTP-LV/blob/main/CONTRIBUTING.md)**: Review open PRs, and submit your own PRs.

<details closed>
<summary>Contributing Guidelines</summary>

1. **Fork the Repository**: Start by forking the project repository to your github account.
2. **Clone Locally**: Clone the forked repository to your local machine using a git client.
   ```sh
   git clone https://github.com/FabsMS/Nutri-STTP-LV
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
   <a href="https://github.com{/FabsMS/Nutri-STTP-LV/}graphs/contributors">
      <img src="https://contrib.rocks/image?repo=FabsMS/Nutri-STTP-LV">
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
