from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

# Carrega as variáveis de ambiente (seu GOOGLE_API_KEY)
load_dotenv()

print("Iniciando teste de conexão com a API do Gemini...")

try:
    # Tenta inicializar e usar o modelo com um nome conhecido e estável
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash-latest") # Usando 'gemini-pro' para o teste

    print("Modelo inicializado com sucesso. Enviando um prompt simples...")

    # Envia uma pergunta simples para o modelo
    response = llm.invoke("Olá! Qual é a capital do Brasil?")

    print("\n✅ Conexão bem-sucedida!")
    print("\nResposta do Gemini:")
    print(response.content)

except Exception as e:
    print("\n❌ Ocorreu um erro durante o teste:")
    print(f"\nTipo de Erro: {type(e).__name__}")
    print(f"\nMensagem de Erro Detalhada:\n{e}")