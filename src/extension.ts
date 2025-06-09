import * as vscode from 'vscode';
import { exec } from 'child_process';
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
		const command = `python "${pythonScript}" "${projectPath}"`;

		exec(command, (err, stdout, stderr) => {
			if (err) {
				vscode.window.showErrorMessage(`Erro: ${stderr}`);
			} else {
				vscode.window.showInformationMessage('Script Python executado com sucesso!');
				console.log(stdout);
			}
		});
	});

	context.subscriptions.push(disposable);
}
