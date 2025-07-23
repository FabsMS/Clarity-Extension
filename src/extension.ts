import * as vscode from 'vscode';
import { spawn } from 'child_process';
import * as path from 'path';

export function activate(context: vscode.ExtensionContext) {
	const disposable = vscode.commands.registerCommand('fabsms-clarity.helloWorld', () => {
		const workspaceFolders = vscode.workspace.workspaceFolders;
		if (!workspaceFolders) {
			vscode.window.showErrorMessage('Nenhuma pasta aberta no VSCode.');
			return;
		}
		const projectPath = workspaceFolders[0].uri.fsPath;

		const pythonScript = path.join(context.extensionPath, 'python', 'main.py');
		
		console.log(`Executando: python "${pythonScript}" "${projectPath}"`);

		const pythonProcess = spawn('python', [pythonScript, projectPath]);

		let stdout = '';
		let stderr = '';

		pythonProcess.stdout.on('data', (data) => {
			stdout += data.toString();
		});

		pythonProcess.stderr.on('data', (data) => {
			stderr += data.toString();
		});

		pythonProcess.on('error', (err) => {
			console.error('--- ERRO AO INICIAR SCRIPT PYTHON ---');
			console.error('Erro (objeto):', err);
			console.error('--- FIM DO RELATÓRIO DE ERRO ---');
			vscode.window.showErrorMessage(`Falha ao iniciar o script Python: ${err.message}. Veja o 'Debug Console' (Ctrl+Shift+Y) para detalhes.`);
		});

		pythonProcess.on('close', (code) => {
			if (code !== 0) {
				console.error('--- ERRO AO EXECUTAR SCRIPT PYTHON ---');
				console.error('Código de saída:', code);
				console.error('Saída de erro (stderr):', stderr);
				console.error('--- FIM DO RELATÓRIO DE ERRO ---');
				vscode.window.showErrorMessage(`Erro ao executar script (código de saída: ${code}). Veja o 'Debug Console' (Ctrl+Shift+Y) para detalhes.`);
				return;
			}

			if (stderr) {
				console.warn('--- AVISO (STDERR) DO SCRIPT PYTHON ---');
				console.warn(stderr);
				console.warn('--- FIM DO AVISO ---');
			}
			
			vscode.window.showInformationMessage('Script Python executado com sucesso!');
			console.log('Saída (stdout):', stdout);
		});
	});

	context.subscriptions.push(disposable);
}