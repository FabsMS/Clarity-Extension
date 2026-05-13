"""
============================================
CLARITY - LLM Configuration Module (100% Offline)
============================================
Módulo centralizado para inicialização e validação dos LLMs locais via Ollama.

Arquitetura Multi-Modelo:
- Analyst LLM: deepseek-coder:6.7b (T=0.1) -> Análise técnica precisa
- Writer LLM: llama3:8b (T=0.4) -> Documentação criativa e clara

Este módulo garante que:
1. O Ollama está ativo e acessível
2. Os modelos obrigatórios estão instalados
3. Nenhuma chamada externa é realizada (100% offline)
4. Mensagens de erro são claras e acionáveis
"""

import os
import sys
import requests
from typing import Optional, Dict, List
from crewai import LLM
from dotenv import load_dotenv

load_dotenv()

# ============================================
# CONFIGURAÇÕES HARDCODED (NÃO EDITÁVEL VIA .ENV)
# ============================================
ANALYST_MODEL = "deepseek-coder:6.7b"
ANALYST_TEMPERATURE = 0.1

WRITER_MODEL = "llama3:8b"
WRITER_TEMPERATURE = 0.1  # Reduzido para 0.1 para eliminar criatividade e invenção

REQUIRED_MODELS = [ANALYST_MODEL, WRITER_MODEL]


class OllamaConnectionError(Exception):
    """Exceção customizada para erros de conexão com Ollama"""
    pass


class OllamaModelMissingError(Exception):
    """Exceção customizada para modelos ausentes no Ollama"""
    pass


def check_ollama_availability() -> Dict[str, any]:
    """
    Verifica se o Ollama está ativo e acessível.

    Returns:
        dict: Informações sobre status do Ollama e modelos disponíveis

    Raises:
        OllamaConnectionError: Se não conseguir conectar ao Ollama
    """
    ollama_base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

    print(f"🔍 Verificando disponibilidade do Ollama...", file=sys.stderr, flush=True)
    print(f"   URL: {ollama_base_url}", file=sys.stderr, flush=True)

    try:
        response = requests.get(f"{ollama_base_url}/api/tags", timeout=5)

        if response.status_code != 200:
            raise OllamaConnectionError(
                f"Ollama respondeu com status {response.status_code}. "
                f"Verifique se o serviço está funcionando corretamente."
            )

        models_data = response.json()
        available_models = [m['name'] for m in models_data.get('models', [])]

        print(f"✅ Ollama está ativo e acessível", file=sys.stderr, flush=True)
        print(f"   Modelos disponíveis: {len(available_models)}", file=sys.stderr, flush=True)

        return {
            "status": "online",
            "base_url": ollama_base_url,
            "available_models": available_models
        }

    except requests.exceptions.ConnectionError:
        raise OllamaConnectionError(
            "❌ Não foi possível conectar ao Ollama.\n"
            "\n"
            "Soluções:\n"
            "  1. Verifique se o Ollama está instalado: https://ollama.com/download\n"
            "  2. Inicie o serviço Ollama: ollama serve\n"
            "  3. Verifique se a porta 11434 está livre\n"
            "  4. Confirme OLLAMA_BASE_URL no arquivo .env\n"
        )

    except requests.exceptions.Timeout:
        raise OllamaConnectionError(
            "❌ Timeout ao tentar conectar ao Ollama.\n"
            "\n"
            "Soluções:\n"
            "  1. Verifique se o Ollama está rodando: ollama list\n"
            "  2. Reinicie o Ollama: ollama serve\n"
            "  3. Verifique sua conexão de rede local\n"
        )

    except Exception as e:
        raise OllamaConnectionError(
            f"❌ Erro inesperado ao verificar Ollama: {str(e)}\n"
            "\n"
            "Soluções:\n"
            "  1. Reinstale o Ollama: https://ollama.com/download\n"
            "  2. Verifique logs do Ollama\n"
            "  3. Reporte o erro: https://github.com/FabsMS/Clarity-Extension/issues\n"
        )


def verify_required_models(available_models: List[str]) -> None:
    """
    Verifica se os modelos obrigatórios estão instalados.

    Args:
        available_models: Lista de modelos disponíveis no Ollama

    Raises:
        OllamaModelMissingError: Se algum modelo obrigatório estiver ausente
    """
    print(f"\n🔍 Verificando modelos obrigatórios...", file=sys.stderr, flush=True)

    missing_models = [m for m in REQUIRED_MODELS if m not in available_models]

    if missing_models:
        error_msg = (
            f"❌ Modelos obrigatórios ausentes: {', '.join(missing_models)}\n"
            f"\n"
            f"Para instalar os modelos faltantes, execute:\n"
        )

        for model in missing_models:
            error_msg += f"  ollama pull {model}\n"

        error_msg += (
            f"\n"
            f"Modelos disponíveis atualmente:\n"
            f"  {', '.join(available_models) if available_models else 'Nenhum'}\n"
        )

        raise OllamaModelMissingError(error_msg)

    print(f"✅ Todos os modelos obrigatórios estão instalados:", file=sys.stderr, flush=True)
    for model in REQUIRED_MODELS:
        print(f"   ✓ {model}", file=sys.stderr, flush=True)


def get_analyst_llm() -> LLM:
    """
    Cria instância do Analyst LLM com validação prévia.

    Modelo: deepseek-coder:6.7b
    Temperatura: 0.1 (mais preciso e determinístico)
    Responsabilidade: Análise técnica detalhada do código

    Returns:
        LLM: Instância configurada do Analyst LLM

    Raises:
        OllamaConnectionError: Se não conseguir conectar ao Ollama
        OllamaModelMissingError: Se o modelo não estiver instalado
        ValueError: Se houver erro na configuração do LLM
    """
    ollama_base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

    print(f"\n{'─'*60}", file=sys.stderr, flush=True)
    print(f"[ANALYST LLM] Configurando modelo de análise técnica", file=sys.stderr, flush=True)
    print(f"{'─'*60}", file=sys.stderr, flush=True)
    print(f"   Base URL: {ollama_base_url}", file=sys.stderr, flush=True)
    print(f"   Modelo: {ANALYST_MODEL}", file=sys.stderr, flush=True)
    print(f"   Temperatura: {ANALYST_TEMPERATURE} (análise precisa)", file=sys.stderr, flush=True)

    try:
        llm_instance = LLM(
            model=f"ollama/{ANALYST_MODEL}",
            base_url=ollama_base_url,
            temperature=ANALYST_TEMPERATURE
        )

        print(f"✅ Analyst LLM configurado com sucesso", file=sys.stderr, flush=True)
        return llm_instance

    except Exception as e:
        error_msg = (
            f"❌ Erro ao configurar Analyst LLM: {str(e)}\n"
            f"\n"
            f"Soluções:\n"
            f"  1. Verifique se o Ollama está rodando: ollama serve\n"
            f"  2. Verifique se o modelo está instalado: ollama pull {ANALYST_MODEL}\n"
            f"  3. Teste o modelo manualmente: ollama run {ANALYST_MODEL}\n"
        )
        print(error_msg, file=sys.stderr, flush=True)
        raise ValueError(f"Falha ao conectar Analyst LLM com Ollama: {str(e)}")


def get_writer_llm() -> LLM:
    """
    Cria instância do Writer LLM com validação prévia.

    Modelo: llama3:8b
    Temperatura: 0.4 (mais criativo e fluido)
    Responsabilidade: Geração do README final com linguagem natural

    Returns:
        LLM: Instância configurada do Writer LLM

    Raises:
        OllamaConnectionError: Se não conseguir conectar ao Ollama
        OllamaModelMissingError: Se o modelo não estiver instalado
        ValueError: Se houver erro na configuração do LLM
    """
    ollama_base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

    print(f"\n{'─'*60}", file=sys.stderr, flush=True)
    print(f"[WRITER LLM] Configurando modelo de escrita de documentação", file=sys.stderr, flush=True)
    print(f"{'─'*60}", file=sys.stderr, flush=True)
    print(f"   Base URL: {ollama_base_url}", file=sys.stderr, flush=True)
    print(f"   Modelo: {WRITER_MODEL}", file=sys.stderr, flush=True)
    print(f"   Temperatura: {WRITER_TEMPERATURE} (escrita criativa)", file=sys.stderr, flush=True)

    try:
        llm_instance = LLM(
            model=f"ollama/{WRITER_MODEL}",
            base_url=ollama_base_url,
            temperature=WRITER_TEMPERATURE
        )

        print(f"✅ Writer LLM configurado com sucesso", file=sys.stderr, flush=True)
        return llm_instance

    except Exception as e:
        error_msg = (
            f"❌ Erro ao configurar Writer LLM: {str(e)}\n"
            f"\n"
            f"Soluções:\n"
            f"  1. Verifique se o Ollama está rodando: ollama serve\n"
            f"  2. Verifique se o modelo está instalado: ollama pull {WRITER_MODEL}\n"
            f"  3. Teste o modelo manualmente: ollama run {WRITER_MODEL}\n"
        )
        print(error_msg, file=sys.stderr, flush=True)
        raise ValueError(f"Falha ao conectar Writer LLM com Ollama: {str(e)}")


def initialize_llms() -> Dict[str, LLM]:
    """
    Inicializa ambos os LLMs com validação completa.

    Este é o ponto de entrada principal para configuração dos LLMs.
    Realiza todas as verificações necessárias antes de criar as instâncias.

    Returns:
        dict: Dicionário com 'analyst' e 'writer' LLM instances

    Raises:
        OllamaConnectionError: Se não conseguir conectar ao Ollama
        OllamaModelMissingError: Se algum modelo estiver ausente
        ValueError: Se houver erro na configuração dos LLMs
    """
    print(f"\n{'='*60}", file=sys.stderr, flush=True)
    print(f"🤖 INICIALIZANDO ARQUITETURA MULTI-MODELO", file=sys.stderr, flush=True)
    print(f"{'='*60}\n", file=sys.stderr, flush=True)

    # PASSO 1: Verificar disponibilidade do Ollama
    try:
        ollama_info = check_ollama_availability()
    except OllamaConnectionError as e:
        print(str(e), file=sys.stderr, flush=True)
        raise

    # PASSO 2: Verificar modelos obrigatórios
    try:
        verify_required_models(ollama_info["available_models"])
    except OllamaModelMissingError as e:
        print(str(e), file=sys.stderr, flush=True)
        raise

    # PASSO 3: Inicializar Analyst LLM
    try:
        analyst_llm = get_analyst_llm()
    except ValueError as e:
        print(f"❌ Falha ao inicializar Analyst LLM", file=sys.stderr, flush=True)
        raise

    # PASSO 4: Inicializar Writer LLM
    try:
        writer_llm = get_writer_llm()
    except ValueError as e:
        print(f"❌ Falha ao inicializar Writer LLM", file=sys.stderr, flush=True)
        raise

    print(f"\n{'='*60}", file=sys.stderr, flush=True)
    print(f"✅ ARQUITETURA MULTI-MODELO CONFIGURADA COM SUCESSO!", file=sys.stderr, flush=True)
    print(f"{'='*60}\n", file=sys.stderr, flush=True)

    return {
        "analyst": analyst_llm,
        "writer": writer_llm
    }
