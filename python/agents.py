
from crewai import Agent, Task, Crew, Process
from functions import PythonAnalyzer, JavaScriptAnalyzer, JavaAnalyzer, MultiLanguageCodeAnalyzer


# Criação do agente
def create_multi_language_analyzer_agent():
    """Cria o agente analisador multilinguagem"""
    
    analyzer_tool = MultiLanguageCodeAnalyzer()
    
    agent = Agent(
        role="Analista de Código Multilinguagem",
        goal="Analisar código em diferentes linguagens e extrair informações estruturadas",
        backstory="""Você é um especialista em análise de código com conhecimento profundo 
        em múltiplas linguagens de programação (Python, JavaScript, Java, TypeScript, etc.). 
        Sua especialidade é extrair informações estruturadas de código fonte, identificando 
        padrões, dependências, complexidade e arquitetura. Você adapta sua análise conforme 
        as convenções e características específicas de cada linguagem.""",
        tools=[analyzer_tool],
        verbose=True,
        memory=True,
        allow_delegation=False
    )
    
    return agent
# teste execução e criação de agente, tarefa e crew
if __name__ == "__main__":
    # Criar o agente
    analyzer = create_multi_language_analyzer_agent()
    
    # Definir tarefa
    analysis_task = Task(
        description="""Analise o arquivo de código fornecido e extraia:
        1. Linguagem de programação detectada
        2. Estrutura geral (classes, funções, imports)
        3. Namespace/package se aplicável
        4. Ponto de entrada da aplicação
        5. Dependências externas
        6. Complexidade e propósito do código
        7. Padrões arquiteturais identificados
        
        Adapte a análise conforme as convenções da linguagem detectada.""",
        expected_output="Análise completa e estruturada do código com informações específicas da linguagem",
        agent=analyzer
    )
    
    # Criar crew
    crew = Crew(
        agents=[analyzer],
        tasks=[analysis_task],
        process=Process.sequential,
        verbose=True
    )
    
analyzer_tool = MultiLanguageCodeAnalyzer()

# teste
result = analyzer_tool._run("src/extension.ts")
print(result)
