"""
Script para testar o sistema de rotação de chaves do Groq
"""
import sys
import os
from pathlib import Path

# Adiciona o diretório python ao path
sys.path.insert(0, str(Path(__file__).parent / "python"))

from dotenv import load_dotenv
load_dotenv()

# Importa o gerenciador de chaves
from agents import key_manager

def test_key_rotation():
    """Testa a rotação de chaves"""
    print("=" * 60)
    print("[TEST] TESTE DE ROTACAO DE CHAVES")
    print("=" * 60)

    # Mostra chaves carregadas
    print(f"\n[INFO] Chaves carregadas: {len(key_manager.api_keys)}")
    for i, (name, key, model) in enumerate(key_manager.api_keys):
        masked_key = key[:10] + "..." + key[-4:] if len(key) > 14 else key
        print(f"   {i + 1}. {name}: {masked_key} (modelo: {model})")

    # Testa rotação
    print(f"\n[TEST] Testando rotacao de chaves...")
    print(f"   Chave inicial: {key_manager.get_current_key()[0]}")

    for i in range(len(key_manager.api_keys) + 1):
        success = key_manager.rotate_key()
        current_name, _, current_model = key_manager.get_current_key()
        print(f"   Rotacao {i + 1}: {current_name} + {current_model} (sucesso: {success})")

    print(f"\n[OK] Teste de rotacao concluido!")

    # Simula cenário de rate limit
    print(f"\n[TEST] Simulando cenario de rate limit...")
    key_manager.current_key_index = 0  # Reset para primeira chave

    for attempt in range(len(key_manager.api_keys)):
        key_name, _, model_name = key_manager.get_current_key()
        print(f"   Tentativa {attempt + 1}: Usando chave {key_name} + modelo {model_name}")

        # Simula erro de rate limit
        print(f"      [WARN] Rate limit na chave {key_name} (modelo {model_name})")

        if key_manager.has_more_keys():
            key_manager.rotate_key()
            print(f"      [RETRY] Rotacionando para proxima chave...")
        else:
            print(f"      [FAIL] Sem mais chaves disponiveis")
            break

    print(f"\n[OK] Simulacao concluida!")

if __name__ == "__main__":
    try:
        test_key_rotation()
    except Exception as e:
        print(f"\n[ERROR] Erro no teste: {str(e)}")
        sys.exit(1)
