import * as vscode from 'vscode';
import { spawn } from 'child_process';
import * as path from 'path';
import * as fs from 'fs';
import * as os from 'os';

// Helper function to check if file exists
function fileExists(filePath: string): boolean {
	try {
		return fs.existsSync(filePath);
	} catch {
		return false;
	}
}

// Helper function to get Python path based on OS
function getPythonPath(extensionPath: string): string {
	const isWindows = os.platform() === 'win32';

	if (isWindows) {
		return path.join(extensionPath, '.venv', 'Scripts', 'python.exe');
	} else {
		return path.join(extensionPath, '.venv', 'bin', 'python');
	}
}

// Helper function to format error messages
function formatErrorMessage(title: string, details: string, suggestions: string[]): string {
	let message = `${title}\n\n${details}`;

	if (suggestions.length > 0) {
		message += '\n\nPossíveis soluções:\n';
		suggestions.forEach((suggestion, index) => {
			message += `${index + 1}. ${suggestion}\n`;
		});
	}

	return message;
}

export function activate(context: vscode.ExtensionContext) {
	const disposable = vscode.commands.registerCommand('fabsms-clarity.generateDocumentation', async () => {
		// ============================================
		// STEP 1: Validate workspace
		// ============================================
		const workspaceFolders = vscode.workspace.workspaceFolders;
		if (!workspaceFolders) {
			vscode.window.showErrorMessage(
				'❌ Nenhuma pasta aberta no VSCode.\n\n' +
				'Por favor, abra uma pasta do seu projeto antes de gerar documentação.'
			);
			return;
		}
		const projectPath = workspaceFolders[0].uri.fsPath;

		// ============================================
		// STEP 2: Validate Python environment
		// ============================================
		const pythonScript = path.join(context.extensionPath, 'python', 'main.py');
		const pythonPath = getPythonPath(context.extensionPath);
		const envPath = path.join(context.extensionPath, '.venv');
		const envFile = path.join(context.extensionPath, '.env');

		// Check if Python script exists
		if (!fileExists(pythonScript)) {
			const errorMsg = formatErrorMessage(
				'❌ Script Python não encontrado',
				`O arquivo main.py não foi encontrado em:\n${pythonScript}`,
				[
					'Verifique se a extensão foi instalada corretamente',
					'Reinstale a extensão',
					'Entre em contato com o desenvolvedor'
				]
			);
			vscode.window.showErrorMessage(errorMsg);
			return;
		}

		// Check if Python virtual environment exists
		if (!fileExists(pythonPath)) {
			const errorMsg = formatErrorMessage(
				'❌ Ambiente Python não encontrado',
				`O ambiente virtual Python não foi encontrado em:\n${envPath}`,
				[
					'Execute: python -m venv .venv',
					'Ative o ambiente: .venv\\Scripts\\activate (Windows) ou source .venv/bin/activate (Linux/Mac)',
					'Instale as dependências: pip install -r requirements.txt',
					'Verifique o README.md para instruções detalhadas'
				]
			);
			vscode.window.showErrorMessage(errorMsg);
			return;
		}

		// Check if .env file exists
		if (!fileExists(envFile)) {
			const choice = await vscode.window.showWarningMessage(
				'⚠️ Arquivo .env não encontrado!\n\n' +
				'O arquivo .env contém as chaves de API necessárias para o funcionamento da extensão.\n\n' +
				'Você precisa criar um arquivo .env na raiz da extensão com suas chaves de API.',
				'Abrir Documentação',
				'Criar .env agora',
				'Continuar mesmo assim'
			);

			if (choice === 'Abrir Documentação') {
				const envExamplePath = path.join(context.extensionPath, '.env.example');
				if (fileExists(envExamplePath)) {
					const doc = await vscode.workspace.openTextDocument(envExamplePath);
					vscode.window.showTextDocument(doc);
				}
				return;
			} else if (choice === 'Criar .env agora') {
				const envExamplePath = path.join(context.extensionPath, '.env.example');
				if (fileExists(envExamplePath)) {
					const content = fs.readFileSync(envExamplePath, 'utf-8');
					fs.writeFileSync(envFile, content);
					const doc = await vscode.workspace.openTextDocument(envFile);
					vscode.window.showTextDocument(doc);
					vscode.window.showInformationMessage(
						'✅ Arquivo .env criado! Por favor, adicione suas chaves de API e execute o comando novamente.'
					);
				}
				return;
			}
			// If "Continue anyway", proceed but will likely fail
		}

		// ============================================
		// STEP 3: Execute Python script with progress
		// ============================================
		await vscode.window.withProgress({
			location: vscode.ProgressLocation.Notification,
			title: "🤖 Clarity: Gerando documentação com IA...",
			cancellable: false
		}, async (progress) => {
			return new Promise<void>((resolve, reject) => {
				progress.report({ message: 'Inicializando...' });
				console.log(`\n${'='.repeat(60)}`);
				console.log('🚀 CLARITY - AI Documentation Generator');
				console.log(`${'='.repeat(60)}`);
				console.log(`📁 Projeto: ${projectPath}`);
				console.log(`🐍 Python: ${pythonPath}`);
				console.log(`📜 Script: ${pythonScript}`);
				console.log(`${'-'.repeat(60)}\n`);

				const startTime = Date.now();
				const pythonProcess = spawn(pythonPath, [pythonScript, projectPath], {
					env: { ...process.env, PYTHONIOENCODING: 'utf-8' }
				});

				let stdout = '';
				let stderr = '';
				let lastProgressUpdate = Date.now();

				pythonProcess.stdout.on('data', (data) => {
					const chunk = data.toString();
					stdout += chunk;

					// Update progress every 2 seconds
					const now = Date.now();
					if (now - lastProgressUpdate > 2000) {
						progress.report({ message: 'Analisando código...' });
						lastProgressUpdate = now;
					}

					// Log progress indicators
					if (chunk.includes('Analisando') || chunk.includes('Analyzing')) {
						console.log(`🔍 ${chunk.trim()}`);
					}
				});

				pythonProcess.stderr.on('data', (data) => {
					const chunk = data.toString();
					stderr += chunk;

					// Log warnings but don't fail
					if (chunk.toLowerCase().includes('warning')) {
						console.warn(`⚠️  ${chunk.trim()}`);
					} else if (chunk.toLowerCase().includes('error')) {
						console.error(`❌ ${chunk.trim()}`);
					}
				});

				pythonProcess.on('error', (err) => {
					const elapsedTime = ((Date.now() - startTime) / 1000).toFixed(2);

					console.error('\n❌ ERRO AO INICIAR PROCESSO PYTHON');
					console.error(`⏱️  Tempo decorrido: ${elapsedTime}s`);
					console.error(`📋 Erro: ${err.message}`);
					console.error(`🔧 Código: ${err.name}`);

					let errorMessage = '❌ Falha ao iniciar o script Python\n\n';
					let suggestions: string[] = [];

					if (err.message.includes('ENOENT')) {
						errorMessage += 'O executável Python não foi encontrado.\n';
						suggestions = [
							'Verifique se o Python 3.11+ está instalado',
							'Crie o ambiente virtual: python -m venv .venv',
							'Ative o ambiente e instale dependências: pip install -r requirements.txt',
							'Verifique o caminho: ' + pythonPath
						];
					} else if (err.message.includes('EACCES')) {
						errorMessage += 'Sem permissão para executar o Python.\n';
						suggestions = [
							'Verifique as permissões do arquivo: ' + pythonPath,
							'No Linux/Mac, execute: chmod +x ' + pythonPath
						];
					} else {
						errorMessage += `Erro: ${err.message}\n`;
						suggestions = [
							'Verifique os logs no Console de Depuração (Ctrl+Shift+Y)',
							'Reinstale as dependências Python',
							'Entre em contato com o desenvolvedor'
						];
					}

					vscode.window.showErrorMessage(formatErrorMessage(
						'Erro ao iniciar Python',
						errorMessage,
						suggestions
					));

					reject(err);
				});

				pythonProcess.on('close', (code) => {
					const elapsedTime = ((Date.now() - startTime) / 1000).toFixed(2);

					console.log(`\n${'-'.repeat(60)}`);
					console.log(`⏱️  Tempo total de execução: ${elapsedTime}s`);
					console.log(`📊 Código de saída: ${code}`);
					console.log(`${'-'.repeat(60)}\n`);

					if (code !== 0) {
						console.error('❌ PROCESSO PYTHON FINALIZOU COM ERRO\n');
						console.error('📋 STDERR:');
						console.error(stderr || '(vazio)');
						console.error('\n📋 STDOUT:');
						console.error(stdout || '(vazio)');

						let errorMessage = `❌ Erro ao executar script Python (código: ${code})\n\n`;
						let suggestions: string[] = [];

						// Parse common Python errors
						if (stderr.includes('ModuleNotFoundError')) {
							const match = stderr.match(/ModuleNotFoundError: No module named '([^']+)'/);
							const moduleName = match ? match[1] : 'desconhecido';

							errorMessage += `Módulo Python não encontrado: ${moduleName}\n`;
							suggestions = [
								`Instale o módulo: pip install ${moduleName}`,
								'Ou instale todas as dependências: pip install -r requirements.txt',
								'Verifique se o ambiente virtual está ativo'
							];
						} else if (stderr.includes('ImportError')) {
							errorMessage += 'Erro ao importar módulos Python.\n';
							suggestions = [
								'Reinstale as dependências: pip install -r requirements.txt',
								'Verifique se o ambiente virtual está ativo',
								'Verifique se há conflitos de versão'
							];
						} else if (stderr.includes('API key') || stderr.includes('GEMINI_API_KEY') || stderr.includes('authentication')) {
							errorMessage += 'Problema com a chave de API.\n';
							suggestions = [
								'Verifique se o arquivo .env existe',
								'Verifique se a chave de API está correta no .env',
								'Obtenha uma nova chave em: https://aistudio.google.com/app/apikey',
								'Ou use Groq (grátis): https://console.groq.com'
							];
						} else if (stderr.includes('SyntaxError')) {
							errorMessage += 'Erro de sintaxe no código Python.\n';
							suggestions = [
								'Verifique se o código Python está correto',
								'Reinstale a extensão',
								'Reporte o erro no GitHub: https://github.com/FabsMS/fabsms-clarity/issues'
							];
						} else {
							errorMessage += 'Erro desconhecido durante a execução.\n';
							suggestions = [
								'Veja os detalhes completos no Console de Depuração (Ctrl+Shift+Y)',
								'Verifique o arquivo .env',
								'Reinstale as dependências Python'
							];
						}

						// Show first 500 chars of error
						if (stderr.length > 0) {
							const errorPreview = stderr.substring(0, 500);
							console.error('\n📋 Prévia do erro:');
							console.error(errorPreview);
						}

						vscode.window.showErrorMessage(formatErrorMessage(
							'Erro na execução Python',
							errorMessage,
							suggestions
						));

						return reject(new Error(`Python exited with code ${code}`));
					}

					// ============================================
					// STEP 4: Parse Python output
					// ============================================
					try {
						progress.report({ message: 'Processando resultado...' });

						console.log('📋 STDOUT completo:');
						console.log(stdout);

						// Try to find the last valid JSON in output
						// Look for JSON that starts with { and has "success" or "error" key
						let result = null;
						const lines = stdout.split('\n');

						// Try to find complete JSON from end to start
						for (let i = lines.length - 1; i >= 0; i--) {
							const line = lines[i].trim();
							if (line.startsWith('{') && (line.includes('"success"') || line.includes('"error"'))) {
								try {
									result = JSON.parse(line);
									console.log(`\n✅ JSON válido encontrado na linha ${i + 1}`);
									break;
								} catch {
									// Try to accumulate multiple lines if JSON spans multiple lines
									let jsonStr = line;
									for (let j = i + 1; j < lines.length; j++) {
										jsonStr += lines[j];
										try {
											result = JSON.parse(jsonStr);
											console.log(`\n✅ JSON válido encontrado (linhas ${i + 1}-${j + 1})`);
											break;
										} catch {
											// Continue accumulating
										}
									}
									if (result) break;
								}
							}
						}

						if (!result) {
							throw new Error(
								'Nenhum JSON válido encontrado na saída do script Python.\n\n' +
								'A saída do script pode estar incompleta ou corrompida.\n' +
								'Verifique o Console de Depuração para mais detalhes.'
							);
						}

						console.log('📊 Resultado parseado:');
						console.log(JSON.stringify(result, null, 2));

						// ============================================
						// STEP 5: Handle result
						// ============================================
						if (result.error) {
							console.error(`\n❌ Erro retornado pelo Python: ${result.error}`);

							vscode.window.showErrorMessage(
								`❌ ${result.error}\n\n` +
								'Verifique o Console de Depuração para mais detalhes.'
							);

							reject(new Error(result.error));
						} else if (result.success) {
							console.log(`\n✅ README gerado com sucesso!`);
							console.log(`📄 Caminho: ${result.readme_path}`);

							vscode.window.showInformationMessage(
								`✅ ${result.message}`,
								'Abrir README',
								'Copiar caminho'
							).then(async (selection) => {
								if (selection === 'Abrir README') {
									try {
										const readmeUri = vscode.Uri.file(result.readme_path);
										const doc = await vscode.workspace.openTextDocument(readmeUri);
										await vscode.window.showTextDocument(doc);
										console.log('📖 README aberto no editor');
									} catch (err) {
										const error = err as Error;
										vscode.window.showErrorMessage(
											`❌ Erro ao abrir README: ${error.message}\n\n` +
											`Caminho: ${result.readme_path}`
										);
									}
								} else if (selection === 'Copiar caminho') {
									vscode.env.clipboard.writeText(result.readme_path);
									vscode.window.showInformationMessage('📋 Caminho copiado!');
								}
							});

							resolve();
						} else {
							throw new Error('Resposta inválida do script Python (nem success nem error)');
						}

					} catch (e) {
						console.error('\n❌ ERRO AO PROCESSAR SAÍDA DO PYTHON');
						console.error('Tipo de erro:', e instanceof Error ? e.constructor.name : typeof e);
						console.error('Mensagem:', e instanceof Error ? e.message : String(e));
						console.error('\n📋 STDOUT recebido:');
						console.error(stdout || '(vazio)');

						let errorMessage = '❌ Falha ao processar a resposta do script Python\n\n';

						if (e instanceof SyntaxError) {
							errorMessage += 'A saída do script não é um JSON válido.\n';
						} else {
							errorMessage += `Erro: ${e instanceof Error ? e.message : String(e)}\n`;
						}

						vscode.window.showErrorMessage(formatErrorMessage(
							'Erro ao processar resultado',
							errorMessage,
							[
								'Verifique o Console de Depuração (Ctrl+Shift+Y) para ver a saída completa',
								'O script Python pode não ter executado corretamente',
								'Verifique se há erros no arquivo .env',
								'Tente executar novamente'
							]
						));

						reject(e);
					}
				});
			});
		});
	});

	context.subscriptions.push(disposable);
}
