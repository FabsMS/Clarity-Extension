#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test script to validate Clarity setup
Run this to check if everything is configured correctly
"""

import sys
import os
import io
from pathlib import Path

# Force UTF-8 encoding on Windows
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# Colors for terminal output
RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'


def print_header(text):
    print(f"\n{BLUE}{'=' * 60}{RESET}")
    print(f"{BLUE}{text}{RESET}")
    print(f"{BLUE}{'=' * 60}{RESET}\n")


def print_success(text):
    print(f"{GREEN}✅ {text}{RESET}")


def print_error(text):
    print(f"{RED}❌ {text}{RESET}")


def print_warning(text):
    print(f"{YELLOW}⚠️  {text}{RESET}")


def print_info(text):
    print(f"{BLUE}ℹ️  {text}{RESET}")


def test_python_version():
    """Test Python version"""
    print_info("Testando versão do Python...")

    version = sys.version_info
    version_str = f"{version.major}.{version.minor}.{version.micro}"

    if version.major == 3 and version.minor >= 11:
        print_success(f"Python {version_str} ✓")
        return True
    else:
        print_error(f"Python {version_str} (requer 3.11+)")
        return False


def test_imports():
    """Test required imports"""
    print_info("Testando imports necessários...")

    required_modules = [
        ('crewai', 'CrewAI'),
        ('langchain', 'LangChain'),
        ('dotenv', 'python-dotenv'),
        ('bs4', 'BeautifulSoup4'),
        ('chromadb', 'ChromaDB'),
        ('ollama', 'Ollama'),
    ]

    all_ok = True

    for module_name, display_name in required_modules:
        try:
            __import__(module_name)
            print_success(f"{display_name}")
        except ImportError:
            print_error(f"{display_name} - Execute: pip install {module_name}")
            all_ok = False

    return all_ok


def test_env_file():
    """Test .env file"""
    print_info("Testando arquivo .env...")

    env_path = Path('.env')

    if not env_path.exists():
        print_error("Arquivo .env não encontrado")
        print_warning("Crie o arquivo .env na raiz do projeto")
        return False

    print_success("Arquivo .env existe")

    # Load .env
    from dotenv import load_dotenv
    load_dotenv()

    # Check Ollama configuration
    ollama_url = os.getenv('OLLAMA_BASE_URL', 'http://localhost:11434')
    ollama_model = os.getenv('OLLAMA_MODEL', 'deepseek-coder:6.7b')

    print_success(f"OLLAMA_BASE_URL: {ollama_url}")
    print_success(f"OLLAMA_MODEL: {ollama_model}")

    return True


def test_llm_config():
    """Test Ollama configuration"""
    print_info("Testando configuração do Ollama...")

    from dotenv import load_dotenv
    load_dotenv()

    ollama_url = os.getenv('OLLAMA_BASE_URL', 'http://localhost:11434')
    model = os.getenv('OLLAMA_MODEL', 'deepseek-coder:6.7b')
    temperature = os.getenv('LLM_TEMPERATURE', '0.1')

    print_success(f"Ollama URL: {ollama_url}")
    print_success(f"Modelo: {model}")
    print_success(f"Temperatura: {temperature}")

    # Test Ollama connection
    try:
        import requests
        response = requests.get(f"{ollama_url}/api/tags", timeout=5)
        if response.status_code == 200:
            print_success("Ollama está rodando")

            models_data = response.json()
            available_models = [m['name'] for m in models_data.get('models', [])]

            if 'deepseek-coder:6.7b' in available_models:
                print_success("Modelo deepseek-coder:6.7b disponível")
            else:
                print_warning("Modelo deepseek-coder:6.7b não encontrado")

            if 'llama3:8b' in available_models:
                print_success("Modelo llama3:8b disponível")
            else:
                print_warning("Modelo llama3:8b não encontrado")

            return True
        else:
            print_error(f"Ollama retornou status {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Não foi possível conectar ao Ollama: {str(e)}")
        print_warning("Execute: ollama serve")
        return False


def test_project_structure():
    """Test project structure"""
    print_info("Testando estrutura do projeto...")

    required_files = [
        'python/main.py',
        'python/agents.py',
        'python/functions.py',
        'src/extension.ts',
        'package.json',
        'tsconfig.json',
        'requirements.txt',
    ]

    all_ok = True

    for file_path in required_files:
        if Path(file_path).exists():
            print_success(file_path)
        else:
            print_error(f"{file_path} - Arquivo não encontrado")
            all_ok = False

    return all_ok


def test_agents_module():
    """Test if agents module can be imported"""
    print_info("Testando módulo agents...")

    try:
        sys.path.insert(0, str(Path('python').absolute()))
        from agents import get_llm, Create_Crew

        print_success("Importação de agents.py")

        # Try to initialize LLM
        try:
            llm = get_llm()
            print_success("LLM inicializado com sucesso")
            return True
        except Exception as e:
            print_error(f"Erro ao inicializar LLM: {str(e)}")
            print_warning("Verifique suas chaves de API no .env")
            return False

    except ImportError as e:
        print_error(f"Erro ao importar agents: {str(e)}")
        return False


def main():
    """Main test function"""
    print_header("🧪 CLARITY - Teste de Configuração")

    tests = [
        ("Python Version", test_python_version),
        ("Imports", test_imports),
        ("Arquivo .env", test_env_file),
        ("Configuração LLM", test_llm_config),
        ("Estrutura do Projeto", test_project_structure),
        ("Módulo Agents", test_agents_module),
    ]

    results = []

    for test_name, test_func in tests:
        print(f"\n{'-' * 60}")
        result = test_func()
        results.append((test_name, result))

    # Summary
    print_header("📊 Resumo dos Testes")

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for test_name, result in results:
        if result:
            print_success(f"{test_name}")
        else:
            print_error(f"{test_name}")

    print(f"\n{'-' * 60}")

    if passed == total:
        print_success(f"Todos os testes passaram! ({passed}/{total})")
        print_info("\n🚀 Você está pronto para usar o Clarity!")
        print_info("Execute no VS Code: F5 → Ctrl+Shift+P → 'Gerar Documentação com Clarity'\n")
        return 0
    else:
        print_error(f"Alguns testes falharam ({passed}/{total})")
        print_warning("\n⚠️  Corrija os problemas acima antes de usar o Clarity")
        print_info("Veja QUICKSTART.md para mais detalhes\n")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
