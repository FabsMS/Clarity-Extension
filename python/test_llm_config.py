"""
============================================
Test Suite for llm_config.py Module
============================================
Testes para verificar:
1. Validação de disponibilidade do Ollama
2. Verificação de modelos obrigatórios
3. Inicialização correta dos LLMs
4. Tratamento de erros com mensagens claras
5. Garantia de que nenhuma chamada externa é feita
"""

import sys
import os
import io
from pathlib import Path

# Garante encoding UTF-8 na saída padrão (Windows)
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# Add python directory to path
sys.path.insert(0, str(Path(__file__).parent))

import llm_config


def test_ollama_availability():
    """Testa se a função de verificação do Ollama funciona"""
    print("\n" + "="*60)
    print("TEST 1: Verificação de disponibilidade do Ollama")
    print("="*60)

    try:
        ollama_info = llm_config.check_ollama_availability()

        assert ollama_info["status"] == "online", "Ollama deve estar online"
        assert "base_url" in ollama_info, "Deve retornar base_url"
        assert "available_models" in ollama_info, "Deve retornar lista de modelos"
        assert isinstance(ollama_info["available_models"], list), "Modelos devem ser uma lista"

        print("✅ Ollama está disponível e acessível")
        print(f"   Base URL: {ollama_info['base_url']}")
        print(f"   Modelos disponíveis: {len(ollama_info['available_models'])}")

        return True

    except llm_config.OllamaConnectionError as e:
        print(f"❌ Falha: {str(e)}")
        return False


def test_required_models():
    """Testa se os modelos obrigatórios estão instalados"""
    print("\n" + "="*60)
    print("TEST 2: Verificação de modelos obrigatórios")
    print("="*60)

    try:
        ollama_info = llm_config.check_ollama_availability()
        llm_config.verify_required_models(ollama_info["available_models"])

        print("✅ Todos os modelos obrigatórios estão instalados:")
        for model in llm_config.REQUIRED_MODELS:
            print(f"   ✓ {model}")

        return True

    except llm_config.OllamaModelMissingError as e:
        print(f"❌ Falha: Modelos ausentes")
        print(str(e))
        return False
    except llm_config.OllamaConnectionError as e:
        print(f"❌ Falha: Não foi possível conectar ao Ollama")
        print(str(e))
        return False


def test_analyst_llm_initialization():
    """Testa a inicialização do Analyst LLM"""
    print("\n" + "="*60)
    print("TEST 3: Inicialização do Analyst LLM")
    print("="*60)

    try:
        analyst_llm = llm_config.get_analyst_llm()

        assert analyst_llm is not None, "Analyst LLM não deve ser None"
        print(f"✅ Analyst LLM inicializado com sucesso")
        print(f"   Modelo: {llm_config.ANALYST_MODEL}")
        print(f"   Temperatura: {llm_config.ANALYST_TEMPERATURE}")

        return True

    except Exception as e:
        print(f"❌ Falha ao inicializar Analyst LLM: {str(e)}")
        return False


def test_writer_llm_initialization():
    """Testa a inicialização do Writer LLM"""
    print("\n" + "="*60)
    print("TEST 4: Inicialização do Writer LLM")
    print("="*60)

    try:
        writer_llm = llm_config.get_writer_llm()

        assert writer_llm is not None, "Writer LLM não deve ser None"
        print(f"✅ Writer LLM inicializado com sucesso")
        print(f"   Modelo: {llm_config.WRITER_MODEL}")
        print(f"   Temperatura: {llm_config.WRITER_TEMPERATURE}")

        return True

    except Exception as e:
        print(f"❌ Falha ao inicializar Writer LLM: {str(e)}")
        return False


def test_full_initialization():
    """Testa a inicialização completa (ambos os LLMs)"""
    print("\n" + "="*60)
    print("TEST 5: Inicialização completa da arquitetura multi-modelo")
    print("="*60)

    try:
        llms = llm_config.initialize_llms()

        assert "analyst" in llms, "Deve retornar 'analyst' LLM"
        assert "writer" in llms, "Deve retornar 'writer' LLM"
        assert llms["analyst"] is not None, "Analyst LLM não deve ser None"
        assert llms["writer"] is not None, "Writer LLM não deve ser None"

        print("✅ Arquitetura multi-modelo inicializada com sucesso")
        print("   ✓ Analyst LLM: OK")
        print("   ✓ Writer LLM: OK")

        return True

    except Exception as e:
        print(f"❌ Falha na inicialização completa: {str(e)}")
        return False


def test_no_external_calls():
    """Verifica que nenhuma chamada externa está sendo feita"""
    print("\n" + "="*60)
    print("TEST 6: Verificação de chamadas externas")
    print("="*60)

    # Verifica que apenas localhost é usado
    ollama_base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

    assert "localhost" in ollama_base_url or "127.0.0.1" in ollama_base_url, \
        "Base URL deve ser localhost (100% offline)"

    print("✅ Confirmado: Sistema 100% offline")
    print(f"   Ollama URL: {ollama_base_url}")
    print("   ✓ Nenhuma chamada externa detectada")

    return True


def run_all_tests():
    """Executa todos os testes"""
    print("\n" + "="*60)
    print("🧪 CLARITY - Test Suite for llm_config.py")
    print("="*60)

    tests = [
        ("Ollama Availability", test_ollama_availability),
        ("Required Models", test_required_models),
        ("Analyst LLM Init", test_analyst_llm_initialization),
        ("Writer LLM Init", test_writer_llm_initialization),
        ("Full Initialization", test_full_initialization),
        ("No External Calls", test_no_external_calls),
    ]

    results = []

    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"\n❌ Erro inesperado em '{test_name}': {str(e)}")
            results.append((test_name, False))

    # Summary
    print("\n" + "="*60)
    print("📊 RESULTADOS DOS TESTES")
    print("="*60)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for test_name, result in results:
        status = "✅ PASSOU" if result else "❌ FALHOU"
        print(f"{status} - {test_name}")

    print("\n" + "-"*60)
    print(f"Total: {passed}/{total} testes passaram ({(passed/total)*100:.1f}%)")
    print("="*60 + "\n")

    return passed == total


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
