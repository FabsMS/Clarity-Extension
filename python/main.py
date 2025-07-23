# Exemplo de main.py
import sys
import os
import json

def analyze_react_project(project_path):
    project_info = {
        "name": os.path.basename(project_path),
        "type": "unknown",
        "dependencies": {},
        "files": [],
        "components": [],
        "routes": []
    }

    package_json_path = os.path.join(project_path, 'package.json')
    if os.path.exists(package_json_path):
        project_info["type"] = "react" # Ou 'node'/'javascript'
        with open(package_json_path, 'r', encoding='utf-8') as f:
            pkg_data = json.load(f)
            project_info["dependencies"] = pkg_data.get("dependencies", {})
            # Adicione lógica para ler scripts, etc.

    # Percorrer arquivos
    for root, dirs, files in os.walk(project_path):
        for file in files:
            file_path = os.path.join(root, file)
            relative_path = os.path.relpath(file_path, project_path)
            project_info["files"].append(relative_path)
            # Adicione lógica para ler conteúdo de arquivos .jsx/.tsx e identificar componentes
            # Exemplo simplificado:
            if file.endswith(('.jsx', '.tsx')):
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if 'function' in content and 'export default' in content:
                        # Uma heurística muito simples para um componente
                        project_info["components"].append(relative_path)
                    # TODO: Lógica mais complexa para rotas (react-router-dom)

    return project_info

if __name__ == "__main__":
    try:
        if len(sys.argv) > 1:
            project_path = sys.argv[1]
            if not os.path.isdir(project_path):
                raise FileNotFoundError(f"O caminho fornecido não é um diretório válido: {project_path}")

            if os.path.exists(os.path.join(project_path, 'package.json')):
                analysis_results = analyze_react_project(project_path)
            else:
                analysis_results = {"error": "Tipo de projeto não suportado. Nenhum package.json encontrado."}
            
            print(json.dumps(analysis_results, indent=2))
        else:
            raise ValueError("Nenhum caminho de projeto foi fornecido como argumento.")

    except Exception as e:
        error_report = {
            "error": "Ocorreu um erro inesperado no script Python.",
            "error_type": type(e).__name__,
            "error_message": str(e),
        }
        print(json.dumps(error_report), file=sys.stderr)
        sys.exit(1)