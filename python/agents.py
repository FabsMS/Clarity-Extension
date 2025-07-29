
from crewai import Agent, Task, Crew, Process
from functions import PythonAnalyzer, JavaScriptAnalyzer, JavaAnalyzer, MultiLanguageCodeAnalyzer, ReadmeGeneratorTool

from dotenv import load_dotenv

load_dotenv()
#from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.chat_models.litellm import ChatLiteLLM

# llm = ChatGoogleGenerativeAI(
#     model="gemini/gemini-1.5-flash-latest",
#     temperature=0.7,
   
# )
llm = ChatLiteLLM(
    model="gemini/gemini-1.5-flash-latest",
    temperature=0.7,
    api_key="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx" ) 
# Criação do agente
class Create_Crew:
    def __init__(self):
        self.analyzer_agent = self.create_multi_language_analyzer_agent()
        self.writer_agent = self.create_readme_writer_agent()
        
        
        self.analysis_task = self.create_analysis_task()
        self.readme_task = self.create_readme_task()
        
        self.crew = self._create_crew()

    def create_multi_language_analyzer_agent(self):
        """Cria o agente analisador multilinguagem"""
        
        analyzer_tool = MultiLanguageCodeAnalyzer()
        
        return Agent(
            role="Analista de Código Multilinguagem",
            goal="Analisar código em diferentes linguagens e extrair informações estruturadas",
            backstory="""Você é um especialista em análise de código com conhecimento profundo 
            em múltiplas linguagens de programação (Python, JavaScript, Java, TypeScript, etc.). 
            Sua especialidade é extrair informações estruturadas de código fonte, identificando 
            padrões, dependências, complexidade e arquitetura. Você adapta sua análise conforme 
            as convenções e características específicas de cada linguagem.""",
            tools=[analyzer_tool],
            verbose=True,
            #emory=True,
            allow_delegation=False,
            llm=llm  # Usando o LLM configurado
        )
        

    def create_readme_writer_agent(self):
        """Cria o agente redator de README"""
        
        readme_tool = ReadmeGeneratorTool()
        
        return Agent(
            role="Redator de Documentação",
            goal="Criar documentação README.md clara, completa e profissional baseada na análise de código",
            backstory="""Você é um especialista em documentação técnica com vasta experiência 
            em criar READMEs que são informativos, bem estruturados e fáceis de seguir. 
            Você entende as necessidades de diferentes tipos de projetos e adapta a documentação 
            conforme o contexto, linguagem e propósito do software. Sua documentação segue as 
            melhores práticas da comunidade de desenvolvimento e é otimizada para facilitar 
            a adoção e contribuição ao projeto.""",
            tools=[readme_tool],
            verbose=True,
            #memory=True,
            allow_delegation=False,
            llm=llm  # Usando o LLM configurado
        )
        
        return agent
      # Definir tarefa
    def create_analysis_task(self):
        return Task(
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
            agent=self.analyzer_agent
        )
    def create_readme_task(self):
        return Task(

                description="""Com base na análise de código fornecida pela tarefa anterior, 
                crie um README.md completo e profissional que inclua:
                
                1. **Cabeçalho**: Título atrativo e descrição clara do projeto
                2. **Badges**: Apropriados para linguagem, framework e status do projeto
                3. **Índice**: Navegação clara e organizada
                4. **Instalação**: 
                - Pré-requisitos específicos da linguagem/framework
                - Comandos de instalação passo a passo
                - Configuração inicial se necessária
                5. **Uso**: 
                - Exemplos práticos baseados no tipo de projeto identificado
                - Comandos de execução específicos
                - URLs de acesso (para APIs/webapps)
                6. **API/Funcionalidades**: 
                - Documentação das principais classes e funções
                - Parâmetros, tipos de retorno e exemplos
                7. **Estrutura**: Layout organizado do projeto
                8. **Dependências**: Lista detalhada com propósito de cada uma
                9. **Contribuição**: Guia para novos contribuidores
                10. **Licença**: Informações de licenciamento
                
                **ADAPTE O CONTEÚDO** conforme o tipo de projeto:
                - APIs: Inclua endpoints, exemplos de requests/responses
                - Libraries: Foque em imports e uso das funções
                - Applications: Destaque funcionalidades e como executar
                - Scripts: Explique parâmetros e casos de uso
                
                **IMPORTANTE**: Use os dados EXATOS da análise anterior, não invente informações.""",
                expected_output="""README.md completo em formato Markdown com:
                - Conteúdo adaptado ao tipo específico de projeto
                - Exemplos práticos baseados no código analisado
                - Instruções precisas de instalação e uso
                - Documentação técnica das funcionalidades principais""",
                agent=self.writer_agent,
                context=[self.analysis_task]  # Esta tarefa depende da análise
            )
        
      
    
    def _create_crew(self):
        """Cria o crew com os agentes e tarefas"""
        return Crew(
            agents=[self.analyzer_agent, self.writer_agent],
            tasks=[self.analysis_task, self.readme_task],
            process=Process.sequential,  
            verbose=True,
            #memory=True,
            llm=llm  # Usando o LLM configurado
        )
    
    def generate_documentation(self, file_path: str) -> dict:
        """Gera documentação completa para um arquivo"""
        # Configurar o arquivo para análise
        self.analysis_task.description += f"\n\n**ARQUIVO PARA ANÁLISE**: {file_path}"
        
        # Executar o crew
        result = self.crew.kickoff()
        
        return {
            "status": "success",
            "file_analyzed": file_path,
            "result": result
        }

    

        
        
    # analyzer_tool = MultiLanguageCodeAnalyzer()


    # # teste
    # result = analyzer_tool._run("src/extension.ts")
    # print(result)
