import sys
import os
import json
import io
import traceback
from pathlib import Path
from typing import List, Optional
from dotenv import load_dotenv

# Garante encoding UTF-8 na saída padrão (Windows)
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# Load environment variables
load_dotenv()

# Validate imports early
try:
    from agents import Create_Crew
    from functions import MultiLanguageCodeAnalyzer
except ImportError as e:
    print(json.dumps({
        "error": f"Erro ao importar módulos necessários: {str(e)}",
        "error_type": "ImportError",
        "error_message": "Instale as dependências com: pip install -r requirements.txt"
    }), file=sys.stderr)
    sys.exit(1)

EXTENSIONS_PERMITIDAS = ('.py', '.js', '.ts', '.jsx', '.tsx', '.java')
IGNORED_DIRS = {'node_modules', '.git', 'dist', 'build', '__pycache__', '.venv', 'out', '.idea', '.vscode',
                '.next', '.swc'}  # Next.js: pasta de build e cache do compilador


def print_error(error_type: str, message: str, details: Optional[str] = None, suggestions: Optional[List[str]] = None):
    """Print structured error message as JSON"""
    error_data = {
        "error": message,
        "error_type": error_type,
        "error_message": message
    }

    if details:
        error_data["details"] = details

    if suggestions:
        error_data["suggestions"] = suggestions

    print(json.dumps(error_data, ensure_ascii=False), file=sys.stderr)


def validate_environment():
    """Validate Ollama environment (offline mode)"""
    print("🔍 Validando ambiente Ollama (Modo Offline)...", file=sys.stderr)

    # Check Ollama configuration
    ollama_url = os.getenv('OLLAMA_BASE_URL', 'http://localhost:11434')
    ollama_model = os.getenv('OLLAMA_MODEL', 'deepseek-coder:6.7b')

    print(f"   Ollama URL: {ollama_url}", file=sys.stderr)
    print(f"   Modelo: {ollama_model}", file=sys.stderr)

    # Verify Ollama is running
    try:
        import requests
        response = requests.get(f"{ollama_url}/api/tags", timeout=5)
        if response.status_code == 200:
            print(f"✅ Ollama está rodando", file=sys.stderr)

            # Check if required models are available
            models_data = response.json()
            available_models = [m['name'] for m in models_data.get('models', [])]

            required_models = ['deepseek-coder:6.7b', 'llama3:8b']
            missing_models = [m for m in required_models if m not in available_models]

            if missing_models:
                print_error(
                    "ConfigurationError",
                    f"Modelos Ollama ausentes: {', '.join(missing_models)}",
                    "Os modelos obrigatórios não estão instalados no Ollama",
                    [
                        f"Instale os modelos faltantes:",
                        f"   ollama pull deepseek-coder:6.7b",
                        f"   ollama pull llama3:8b"
                    ]
                )
                return False

            print(f"✅ Modelos Ollama disponíveis: {', '.join(required_models)}", file=sys.stderr)
            return True
        else:
            raise Exception(f"Status code: {response.status_code}")

    except Exception as e:
        print_error(
            "ConnectionError",
            "Não foi possível conectar ao Ollama",
            f"Erro: {str(e)}",
            [
                "Verifique se o Ollama está instalado: https://ollama.com/download",
                "Inicie o Ollama: ollama serve",
                "Instale os modelos necessários:",
                "   ollama pull deepseek-coder:6.7b",
                "   ollama pull llama3:8b"
            ]
        )
        return False


def find_package_json_path(search_path: str) -> Optional[str]:
    """Find package.json in project directory"""
    print(f"🔍 Procurando package.json em: {search_path}", file=sys.stderr)

    for root, dirs, files in os.walk(search_path):
        # Remove ignored directories from search
        dirs[:] = [d for d in dirs if d not in IGNORED_DIRS]

        if 'package.json' in files:
            path = os.path.join(root, 'package.json')
            print(f"✅ Encontrado: {path}", file=sys.stderr)
            return path

    print("⚠️  package.json não encontrado", file=sys.stderr)
    return None


def get_all_relevant_files(project_path: str) -> List[str]:
    """Get all relevant code files from project"""
    print(f"📂 Coletando arquivos de código em: {project_path}", file=sys.stderr)
    print(f"📝 Extensões suportadas: {', '.join(EXTENSIONS_PERMITIDAS)}", file=sys.stderr)
    print(f"🚫 Diretórios ignorados: {', '.join(IGNORED_DIRS)}", file=sys.stderr)

    arquivos = []
    total_files_scanned = 0
    dirs_scanned = 0

    for root, dirs, files in os.walk(project_path):
        dirs_scanned += 1
        # Remove ignored directories
        original_dirs = dirs.copy()
        dirs[:] = [d for d in dirs if d not in IGNORED_DIRS]
        removed_dirs = set(original_dirs) - set(dirs)
        if removed_dirs:
            print(f"   Ignorando pastas em {root}: {', '.join(removed_dirs)}", file=sys.stderr)

        for file in files:
            total_files_scanned += 1
            if file.endswith(EXTENSIONS_PERMITIDAS):
                file_path = os.path.join(root, file)
                arquivos.append(file_path)
                print(f"   ✓ {file_path}", file=sys.stderr)

    print(f"\n📊 Estatísticas:", file=sys.stderr)
    print(f"   Total de pastas escaneadas: {dirs_scanned}", file=sys.stderr)
    print(f"   Total de arquivos escaneados: {total_files_scanned}", file=sys.stderr)
    print(f"✅ Encontrados {len(arquivos)} arquivos de código válidos", file=sys.stderr)

    # Show file breakdown by extension
    if arquivos:
        from collections import Counter
        extensions = Counter(Path(f).suffix for f in arquivos)
        print(f"\n📋 Arquivos por extensão:", file=sys.stderr)
        for ext, count in extensions.most_common():
            print(f"   {ext}: {count} arquivo(s)", file=sys.stderr)
    else:
        print(f"\n⚠️  AVISO: Nenhum arquivo válido encontrado!", file=sys.stderr)
        print(f"   Certifique-se de que o projeto contém arquivos com extensões suportadas", file=sys.stderr)

    return arquivos


if __name__ == "__main__":
    try:
        print("=" * 60, file=sys.stderr)
        print("🤖 CLARITY - AI Documentation Generator", file=sys.stderr)
        print("=" * 60, file=sys.stderr)

        # ============================================
        # STEP 1: Validate arguments
        # ============================================
        if len(sys.argv) <= 1:
            print_error(
                "ArgumentError",
                "Nenhum caminho de projeto foi fornecido",
                "O script requer o caminho do projeto como argumento",
                ["Uso: python main.py <caminho_do_projeto>"]
            )
            sys.exit(1)

        project_path_arg = sys.argv[1]
        print(f"📁 Projeto: {project_path_arg}", file=sys.stderr)

        # ============================================
        # STEP 2: Validate project path
        # ============================================
        if not os.path.exists(project_path_arg):
            print_error(
                "FileNotFoundError",
                f"Caminho não existe: {project_path_arg}",
                "O caminho fornecido não foi encontrado no sistema de arquivos",
                [
                    "Verifique se o caminho está correto",
                    "Verifique se você tem permissão para acessar o diretório"
                ]
            )
            sys.exit(1)

        if not os.path.isdir(project_path_arg):
            print_error(
                "NotADirectoryError",
                f"O caminho não é um diretório: {project_path_arg}",
                "O script requer um diretório de projeto, não um arquivo",
                ["Forneça o caminho para a pasta raiz do seu projeto"]
            )
            sys.exit(1)

        # ============================================
        # STEP 3: Validate environment
        # ============================================
        if not validate_environment():
            sys.exit(1)

        # ============================================
        # STEP 4: Find project root
        # ============================================
        package_json_path = find_package_json_path(project_path_arg)
        actual_project_path = os.path.dirname(package_json_path) if package_json_path else project_path_arg
        print(f"🎯 Raiz do projeto: {actual_project_path}", file=sys.stderr)

        # ============================================
        # STEP 5: Collect files
        # ============================================
        arquivos_para_analisar = get_all_relevant_files(actual_project_path)

        if not arquivos_para_analisar:
            print_error(
                "NoFilesFoundError",
                "Nenhum arquivo de código encontrado",
                f"Não foram encontrados arquivos com extensões suportadas: {', '.join(EXTENSIONS_PERMITIDAS)}",
                [
                    "Verifique se o projeto contém código-fonte",
                    f"Extensões suportadas: {', '.join(EXTENSIONS_PERMITIDAS)}",
                    "O projeto pode estar vazio ou em um formato não suportado"
                ]
            )
            sys.exit(1)

        # ============================================
        # STEP 6: Generate documentation with AI
        # ============================================
        print(f"\n{'─' * 60}", file=sys.stderr)
        print("🤖 Gerando documentação com IA...", file=sys.stderr)
        print(f"📋 Analisando {len(arquivos_para_analisar)} arquivos...", file=sys.stderr)

        try:
            crew_manager = Create_Crew()
            # Pass the list of files to analyze, not a summary string
            agent_result = crew_manager.generate_documentation(arquivos_para_analisar)

            # Extrai o conteúdo do README
            if hasattr(agent_result, 'output'):
                readme_content = agent_result.output
            elif isinstance(agent_result, dict):
                readme_content = agent_result.get("output") or str(agent_result)
            elif hasattr(agent_result, "to_json"):
                readme_content = agent_result.to_json()
            elif hasattr(agent_result, "dict"):
                readme_content = agent_result.dict().get("result")
            else:
                readme_content = str(agent_result)

            if not readme_content or len(readme_content.strip()) < 100:
                raise ValueError("Conteúdo gerado está vazio ou muito curto")

            print(f"✅ Documentação gerada ({len(readme_content)} caracteres)", file=sys.stderr)

        except Exception as e:
            error_message = str(e).lower()

            if 'connection' in error_message or 'ollama' in error_message:
                print_error(
                    "OllamaConnectionError",
                    "Não foi possível conectar ao Ollama",
                    str(e),
                    [
                        "Verifique se o Ollama está rodando: ollama serve",
                        "Verifique se os modelos estão instalados:",
                        "   ollama pull deepseek-coder:6.7b",
                        "   ollama pull llama3:8b"
                    ]
                )
            elif 'timeout' in error_message:
                print_error(
                    "TimeoutError",
                    "Tempo limite excedido ao processar com Ollama",
                    str(e),
                    [
                        "O modelo pode estar sobrecarregado, tente novamente",
                        "Verifique se o Ollama está funcionando: ollama list",
                        "Reinicie o Ollama: ollama serve"
                    ]
                )
            else:
                print_error(
                    "AIGenerationError",
                    "Erro ao gerar documentação com IA",
                    str(e),
                    [
                        "Verifique os logs acima para detalhes",
                        "Tente executar novamente",
                        f"Stack trace: {traceback.format_exc()}"
                    ]
                )

            sys.exit(1)

        # ============================================
        # STEP 8: Save README
        # ============================================
        print(f"\n{'─' * 60}", file=sys.stderr)
        print("💾 Salvando README...", file=sys.stderr)

        try:
            output_filename = os.getenv('OUTPUT_README_NAME', 'README-CLARITY.md')
            readme_file_path = os.path.join(actual_project_path, output_filename)

            with open(readme_file_path, 'w', encoding='utf-8') as f:
                f.write(readme_content)

            # Verify file was written
            if not os.path.exists(readme_file_path):
                raise FileNotFoundError("Arquivo não foi criado")

            file_size = os.path.getsize(readme_file_path)
            print(f"✅ README salvo ({file_size} bytes)", file=sys.stderr)
            print(f"📄 {readme_file_path}", file=sys.stderr)

        except Exception as e:
            print_error(
                "FileWriteError",
                "Erro ao salvar arquivo README",
                str(e),
                [
                    f"Verifique permissões de escrita em: {actual_project_path}",
                    "Verifique se há espaço em disco",
                    "Tente executar com privilégios de administrador"
                ]
            )
            sys.exit(1)

        # ============================================
        # STEP 9: Success response
        # ============================================
        print(f"\n{'=' * 60}", file=sys.stderr)
        print("✅ SUCESSO!", file=sys.stderr)
        print(f"{'=' * 60}\n", file=sys.stderr)

        # IMPORTANT: This is the ONLY stdout output (JSON for VS Code)
        print(json.dumps({
            "success": True,
            "message": f"README gerado com sucesso!",
            "readme_path": readme_file_path,
            "stats": {
                "files_analyzed": len(arquivos_para_analisar),
                "readme_size": file_size,
                "project_path": actual_project_path
            }
        }, ensure_ascii=False))

    except KeyboardInterrupt:
        print_error(
            "InterruptedError",
            "Execução interrompida pelo usuário",
            "O processo foi cancelado manualmente",
            []
        )
        sys.exit(130)

    except Exception as e:
        print(f"\n{'=' * 60}", file=sys.stderr)
        print("❌ ERRO INESPERADO", file=sys.stderr)
        print(f"{'=' * 60}", file=sys.stderr)
        print(f"Tipo: {type(e).__name__}", file=sys.stderr)
        print(f"Mensagem: {str(e)}", file=sys.stderr)
        print(f"\n{traceback.format_exc()}", file=sys.stderr)

        print_error(
            type(e).__name__,
            "Erro inesperado ao executar o script",
            str(e),
            [
                "Veja os logs acima para detalhes completos",
                "Verifique se todas as dependências estão instaladas",
                "Reporte o erro em: https://github.com/FabsMS/Clarity-Extension/issues",
                f"Stack trace completo impresso no stderr"
            ]
        )
        sys.exit(1)
