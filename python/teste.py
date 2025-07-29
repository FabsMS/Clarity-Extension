import sys
import os
import json
from pathlib import Path
from agents import Agent, Crew, Process, Create_Crew
crew = Create_Crew()
file_path='src/extension.ts'
# result = crew.generate_documentation(file_path)
try:
    # Substitua "caminho/para/seu/arquivo.py" pelo arquivo real que você quer analisar
    resultado = crew .generate_documentation(file_path)
    print("Execução concluída com sucesso!")
    print(resultado)

except Exception as e:
    print("!!!!!!!!!!!!!!!!!!!!")
    print(type(e).__name__)
    print(f"Mensagem Erro: {e}")
   
# if result["status"] == "success":
#     readme_path = Path(output_dir) / "README.md"
    
#     # (assumindo que o resultado final contém o README)
#     readme_content = str(result["result"])
    
#     with open(readme_path, "w", encoding="utf-8") as f:
#         f.write(readme_content)
    
#     result["readme_saved"] = str(readme_path)

