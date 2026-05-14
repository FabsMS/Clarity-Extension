import * as vscode from 'vscode';
import { spawn, exec } from 'child_process';
import * as path from 'path';
import * as fs from 'fs';
import * as os from 'os';

// ============================================================
// UTILITÁRIOS
// ============================================================

function fileExists(filePath: string): boolean {
	try { return fs.existsSync(filePath); } catch { return false; }
}

function getPythonVenvPath(extensionPath: string): string {
	return os.platform() === 'win32'
		? path.join(extensionPath, '.venv', 'Scripts', 'python.exe')
		: path.join(extensionPath, '.venv', 'bin', 'python');
}


function runShellCommand(command: string): Promise<string> {
	return new Promise((resolve, reject) => {
		exec(command, { encoding: 'utf8' }, (error, stdout, stderr) => {
			if (error) { reject(new Error(stderr || error.message)); }
			else { resolve((stdout || stderr).trim()); }
		});
	});
}

function runProcess(executable: string, args: string[], cwd?: string): Promise<void> {
	return new Promise((resolve, reject) => {
		const proc = spawn(executable, args, {
			cwd,
			env: { ...process.env, PYTHONIOENCODING: 'utf-8' },
			shell: os.platform() === 'win32'
		});
		let stderr = '';
		proc.stderr?.on('data', (d) => { stderr += d.toString(); });
		proc.stdout?.on('data', () => {});
		proc.on('error', reject);
		proc.on('close', (code) => {
			if (code === 0) { resolve(); }
			else { reject(new Error(stderr || `Exit code ${code}`)); }
		});
	});
}

async function findSystemPython(): Promise<{ cmd: string | null; tooNew: boolean }> {
	// Tenta versões específicas antes das genéricas (útil quando 3.14 é o padrão)
	const candidates = os.platform() === 'win32'
		? ['py -3.13', 'py -3.12', 'py -3.11', 'py', 'python', 'python3']
		: ['python3.13', 'python3.12', 'python3.11', 'python3', 'python'];

	let tooNew = false;
	for (const cmd of candidates) {
		try {
			const output = await runShellCommand(`${cmd} --version`);
			const match = output.match(/Python (\d+)\.(\d+)/);
			if (match) {
				const major = parseInt(match[1]);
				const minor = parseInt(match[2]);
				if (major === 3 && minor >= 11 && minor <= 13) { return { cmd, tooNew: false }; }
				if (major === 3 && minor >= 14) { tooNew = true; }
			}
		} catch { /* não encontrado, tenta próximo */ }
	}
	return { cmd: null, tooNew };
}

function formatErrorMessage(title: string, details: string, suggestions: string[]): string {
	let msg = `${title}\n\n${details}`;
	if (suggestions.length > 0) {
		msg += '\n\nPossíveis soluções:\n';
		suggestions.forEach((s, i) => { msg += `${i + 1}. ${s}\n`; });
	}
	return msg;
}

// ============================================================
// SETUP DO AMBIENTE PYTHON
// ============================================================

async function setupPythonEnvironment(context: vscode.ExtensionContext): Promise<boolean> {
	const choice = await vscode.window.showInformationMessage(
		'⚙️ Configuração inicial do Clarity\n\nUm ambiente Python será criado com todas as dependências. Isso pode levar alguns minutos.',
		{ modal: true },
		'Configurar agora',
		'Cancelar'
	);
	if (choice !== 'Configurar agora') { return false; }

	return await vscode.window.withProgress({
		location: vscode.ProgressLocation.Notification,
		title: '⚙️ Clarity: Configurando ambiente Python...',
		cancellable: false
	}, async (progress) => {
		const ext = context.extensionPath;

		try {
			// Passo 1: Localiza Python 3.11–3.13 no sistema
			progress.report({ increment: 5, message: 'Procurando Python 3.11–3.13 no sistema...' });
			const { cmd: pythonCmd, tooNew } = await findSystemPython();
			if (!pythonCmd) {
				const msg = tooNew
					? '❌ Python 3.14+ não é suportado pelas dependências do Clarity.\n\nInstale o Python 3.12 ou 3.13 em https://python.org/downloads e tente novamente.'
					: '❌ Python 3.11, 3.12 ou 3.13 não encontrado no sistema.\n\nInstale o Python 3.12 em https://python.org/downloads e tente novamente.';
				vscode.window.showErrorMessage(msg, 'Baixar Python').then(sel => {
					if (sel === 'Baixar Python') {
						vscode.env.openExternal(vscode.Uri.parse('https://www.python.org/downloads/'));
					}
				});
				return false;
			}

			// Passo 2: Cria o ambiente virtual
			progress.report({ increment: 10, message: 'Criando ambiente virtual (.venv)...' });
			const venvDir = path.join(ext, '.venv');
			if (!fileExists(venvDir)) {
				await runProcess(pythonCmd, ['-m', 'venv', venvDir]);
			}

			// Passo 3: Atualiza pip via "python -m pip" (necessário no Windows)
			progress.report({ increment: 10, message: 'Atualizando pip...' });
			const pythonExe = getPythonVenvPath(ext);
			try {
				await runProcess(pythonExe, ['-m', 'pip', 'install', '--upgrade', 'pip', '--quiet']);
			} catch {
				// Falha no upgrade do pip não é fatal — continua com a versão atual
			}

			// Passo 4: Instala dependências via "python -m pip" (evita bug do pip.exe no Windows)
			progress.report({ increment: 10, message: 'Instalando dependências (5–10 minutos na primeira vez)...' });
			const req = path.join(ext, 'requirements.txt');
			await runProcess(pythonExe, ['-m', 'pip', 'install', '-r', req, '--quiet'], ext);

			// Passo 5: Cria .env a partir do exemplo, se ainda não existir
			progress.report({ increment: 60, message: 'Finalizando...' });
			const envFile    = path.join(ext, '.env');
			const envExample = path.join(ext, '.env.example');
			if (!fileExists(envFile) && fileExists(envExample)) {
				fs.copyFileSync(envExample, envFile);
			}

			vscode.window.showInformationMessage(
				'✅ Ambiente configurado!\n\nAgora instale os modelos Ollama para usar o Clarity.',
				'Instalar Ollama'
			).then(sel => {
				if (sel === 'Instalar Ollama') {
					vscode.env.openExternal(vscode.Uri.parse('https://ollama.com/download'));
				}
			});
			return true;

		} catch (err) {
			const error = err as Error;
			vscode.window.showErrorMessage(
				formatErrorMessage(
					'❌ Erro durante configuração',
					error.message,
					[
						'Verifique se o Python 3.11+ está instalado corretamente',
						'Tente manualmente: python -m venv .venv',
						'Depois: .venv\\Scripts\\pip install -r requirements.txt'
					]
				)
			);
			return false;
		}
	});
}

// ============================================================
// ATIVAÇÃO DA EXTENSÃO
// ============================================================

export function activate(context: vscode.ExtensionContext) {

	// ── Comando: Configurar ambiente ────────────────────────
	const setupCmd = vscode.commands.registerCommand('fabsms-clarity.setupEnvironment', async () => {
		await setupPythonEnvironment(context);
	});

	// ── Comando: Gerar documentação ─────────────────────────
	const generateCmd = vscode.commands.registerCommand('fabsms-clarity.generateDocumentation', async () => {

		// Valida workspace
		const workspaceFolders = vscode.workspace.workspaceFolders;
		if (!workspaceFolders) {
			vscode.window.showErrorMessage(
				'❌ Nenhuma pasta aberta.\n\nAbra a pasta do seu projeto antes de gerar documentação.'
			);
			return;
		}
		const projectPath  = workspaceFolders[0].uri.fsPath;
		const pythonScript = path.join(context.extensionPath, 'python', 'main.py');
		const pythonPath   = getPythonVenvPath(context.extensionPath);
		const envFile      = path.join(context.extensionPath, '.env');

		// Valida script Python
		if (!fileExists(pythonScript)) {
			vscode.window.showErrorMessage('❌ Script Python não encontrado. Reinstale a extensão.');
			return;
		}

		// Ambiente não configurado → oferece setup automático
		if (!fileExists(pythonPath)) {
			const sel = await vscode.window.showWarningMessage(
				'⚠️ Ambiente Python não configurado.\n\nO Clarity precisa instalar as dependências antes de usar.',
				'Configurar agora',
				'Cancelar'
			);
			if (sel === 'Configurar agora') {
				const ok = await setupPythonEnvironment(context);
				if (!ok) { return; }
			} else { return; }
		}

		// Arquivo .env ausente → oferece criação
		if (!fileExists(envFile)) {
			const sel = await vscode.window.showWarningMessage(
				'⚠️ Arquivo .env não encontrado.\n\nEle contém as configurações do Ollama.',
				'Criar .env agora',
				'Continuar mesmo assim'
			);
			if (sel === 'Criar .env agora') {
				const envExample = path.join(context.extensionPath, '.env.example');
				if (fileExists(envExample)) {
					fs.copyFileSync(envExample, envFile);
					const doc = await vscode.workspace.openTextDocument(envFile);
					await vscode.window.showTextDocument(doc);
					vscode.window.showInformationMessage('✅ .env criado! Execute o comando novamente após revisar.');
				}
				return;
			}
		}

		// ── Execução principal ───────────────────────────────
		await vscode.window.withProgress({
			location: vscode.ProgressLocation.Notification,
			title: '🤖 Clarity: Gerando documentação com IA...',
			cancellable: false
		}, async (progress) => {
			return new Promise<void>((resolve, reject) => {

				progress.report({ message: 'Inicializando...' });

				const startTime = Date.now();
				const TIMEOUT_MS = 15 * 60 * 1000; // 15 minutos

				const pythonProcess = spawn(pythonPath, [pythonScript, projectPath], {
					env: { ...process.env, PYTHONIOENCODING: 'utf-8' }
				});

				// Encerra automaticamente se demorar demais
				const timeoutHandle = setTimeout(() => {
					pythonProcess.kill();
					vscode.window.showErrorMessage(
						'⏱️ Tempo limite excedido (15 min).\n\n' +
						'Verifique se o Ollama está respondendo: ollama list'
					);
					reject(new Error('Timeout'));
				}, TIMEOUT_MS);

				// Mensagens progressivas para o usuário não achar que travou
				const progressSteps = [
					{ delay: 5_000,   msg: 'Analisando arquivos do projeto...' },
					{ delay: 20_000,  msg: 'Processando código...' },
					{ delay: 60_000,  msg: 'Gerando documentação (pode levar alguns minutos)...' },
					{ delay: 180_000, msg: 'Aguardando resposta do modelo de linguagem...' },
					{ delay: 360_000, msg: 'Ainda processando — projetos grandes demoram mais...' },
				];
				const stepTimers = progressSteps.map(({ delay, msg }) =>
					setTimeout(() => progress.report({ message: msg }), delay)
				);

				let stdout = '';
				let stderr = '';

				pythonProcess.stdout.on('data', (data) => { stdout += data.toString(); });
				pythonProcess.stderr.on('data', (data) => { stderr += data.toString(); });

				pythonProcess.on('error', (err) => {
					clearTimeout(timeoutHandle);
					stepTimers.forEach(clearTimeout);
					vscode.window.showErrorMessage(
						formatErrorMessage('❌ Erro ao iniciar Python', err.message, [
							'Verifique se o ambiente foi configurado: Clarity: Configurar Ambiente Python',
							'Caminho esperado: ' + pythonPath
						])
					);
					reject(err);
				});

				pythonProcess.on('close', (code) => {
					clearTimeout(timeoutHandle);
					stepTimers.forEach(clearTimeout);

					const elapsed = ((Date.now() - startTime) / 1000).toFixed(1);
					console.log(`[Clarity] Finalizado em ${elapsed}s — código ${code}`);

					if (code !== 0) {
						const combined = stdout + stderr;
						let errorMsg   = '❌ Erro ao gerar documentação.\n\n';
						let suggestions: string[] = [];

						if (combined.includes('ModuleNotFoundError')) {
							const m = combined.match(/No module named '([^']+)'/);
							errorMsg += `Módulo não encontrado: ${m ? m[1] : 'desconhecido'}`;
							suggestions = [
								'Execute: Clarity: Configurar Ambiente Python (Ctrl+Shift+P)',
								'Ou manualmente: .venv/Scripts/pip install -r requirements.txt'
							];
						} else if (
							combined.includes('OllamaModelMissing') ||
							combined.includes('ausentes')
						) {
							errorMsg += 'Modelos Ollama não instalados.';
							suggestions = [
								'ollama pull deepseek-coder:6.7b',
								'ollama pull llama3:8b'
							];
						} else if (
							combined.toLowerCase().includes('ollama') ||
							combined.includes('ConnectionError') ||
							combined.includes('11434')
						) {
							vscode.window.showErrorMessage(
								'❌ Clarity: Não foi possível conectar ao Ollama.\n\nVerifique se está instalado e em execução.',
								'Instalar Ollama',
								'Iniciar: ollama serve'
							).then(sel => {
								if (sel === 'Instalar Ollama') {
									vscode.env.openExternal(vscode.Uri.parse('https://ollama.com/download'));
								}
							});
							return reject(new Error('Ollama não disponível'));
						} else {
							errorMsg += 'Erro inesperado durante execução.';
							suggestions = [
								'Abra o Console de Depuração (Ctrl+Shift+Y) para ver os detalhes',
								'Verifique se o Ollama está ativo: ollama list'
							];
						}

						vscode.window.showErrorMessage(formatErrorMessage('Clarity', errorMsg, suggestions));
						return reject(new Error(`Python exit ${code}`));
					}

					// Extrai o JSON de sucesso do stdout (busca do fim para o início)
					try {
						let result: Record<string, unknown> | null = null;
						const lines = stdout.split('\n');
						for (let i = lines.length - 1; i >= 0; i--) {
							const line = lines[i].trim();
							if (line.startsWith('{') && line.includes('"success"')) {
								try { result = JSON.parse(line); break; } catch { /* continua */ }
							}
						}

						if (!result) {
							throw new Error('JSON de resposta não encontrado na saída do Python.');
						}

						if (result.success) {
							vscode.window.showInformationMessage(
								`✅ README gerado em ${elapsed}s!`,
								'Abrir README',
								'Copiar caminho'
							).then(async (sel) => {
								if (sel === 'Abrir README') {
									const doc = await vscode.workspace.openTextDocument(
										vscode.Uri.file(result!.readme_path as string)
									);
									vscode.window.showTextDocument(doc);
								} else if (sel === 'Copiar caminho') {
									vscode.env.clipboard.writeText(result!.readme_path as string);
									vscode.window.showInformationMessage('📋 Caminho copiado!');
								}
							});
							resolve();
						} else {
							throw new Error((result.error as string) || 'Resposta inválida do Python.');
						}

					} catch (e) {
						vscode.window.showErrorMessage(
							`❌ Erro ao processar resposta: ${e instanceof Error ? e.message : String(e)}`
						);
						reject(e);
					}
				});
			});
		});
	});

	context.subscriptions.push(setupCmd, generateCmd);

	// Avisa na primeira ativação se o ambiente não estiver configurado
	const pythonPath = getPythonVenvPath(context.extensionPath);
	if (!fileExists(pythonPath)) {
		vscode.window.showInformationMessage(
			'👋 Bem-vindo ao Clarity! Configure o ambiente Python para começar.',
			'Configurar agora',
			'Depois'
		).then(sel => {
			if (sel === 'Configurar agora') {
				vscode.commands.executeCommand('fabsms-clarity.setupEnvironment');
			}
		});
	}
}

export function deactivate() {}
