import sys
import os
import json
from pathlib import Path
from agents import Agent, Crew, Process, Create_Crew
crew = Create_Crew()
file_path='src/extension.ts'

try:
    resultado = crew. generate_documentation(file_path)
    print("Execução concluída com sucesso!")
    print(resultado)

except Exception as e:
    print("!!!!!!!!!!!!!!!!!!!!")
    print(type(e).__name__)
    print(f"Mensagem Erro: {e}")
   

