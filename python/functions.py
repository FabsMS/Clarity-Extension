import ast
import os
import re
import json
from dataclasses import dataclass
from pathlib import Path
from abc import ABC, abstractmethod
from crewai import Agent, Task, Crew, Process
from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Dict, List, Any, Optional
from pathlib import Path
# Estruturas de dados genéricas


@dataclass
class FunctionInfo:
    name: str
    docstring: Optional[str]
    parameters: List[str]
    return_type: Optional[str]
    visibility: str  # public, private, protected
    complexity: str
    line_number: int
    annotations: List[str]  # decorators, attributes, etc.

@dataclass
class ClassInfo:
    name: str
    docstring: Optional[str]
    methods: List[FunctionInfo]
    attributes: List[str]
    inheritance: List[str]
    interfaces: List[str]  # Para linguagens como Java/C#
    visibility: str
    is_abstract: bool
    line_number: int

@dataclass
class FileAnalysis:
    filepath: str
    language: str
    imports: List[str]
    functions: List[FunctionInfo]
    classes: List[ClassInfo]
    dependencies: List[str]
    main_purpose: str
    complexity_score: float
    package_namespace: Optional[str]
    entry_point: Optional[str]  # main function, etc.
@dataclass 
class ReadmeSection:
    title: str
    content: str
    order: int
    is_required: bool = True

@dataclass
class ReadmeTemplate:
    language: str
    sections: List[ReadmeSection]
    badges: List[str]
    installation_commands: List[str]
    usage_examples: List[str]


# Interface para analisadores de linguagem
class LanguageAnalyzer(ABC):
    @abstractmethod
    def analyze(self, content: str, filepath: str) -> FileAnalysis:
        pass
    
    @abstractmethod
    def get_file_extensions(self) -> List[str]:
        pass

# Analisador Python
class PythonAnalyzer(LanguageAnalyzer):
    def get_file_extensions(self) -> List[str]:
        return ['.py']
    
    def analyze(self, content: str, filepath: str) -> FileAnalysis:
        import ast
        
        try:
            tree = ast.parse(content)
            analysis = FileAnalysis(
                filepath=filepath,
                language="Python",
                imports=[],
                functions=[],
                classes=[],
                dependencies=[],
                main_purpose="",
                complexity_score=0.0,
                package_namespace=None,
                entry_point=None
            )
            
            self._analyze_ast(tree, analysis, content)
            return analysis
            
        except Exception as e:
            return self._create_error_analysis(filepath, "Python", str(e))
    
    def _analyze_ast(self, tree: ast.AST, analysis: FileAnalysis, content: str):
        lines = content.split('\n')
        
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    analysis.imports.append(alias.name)
                    
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    for alias in node.names:
                        analysis.imports.append(f"{node.module}.{alias.name}")
                        
            elif isinstance(node, ast.FunctionDef):
                if not self._is_method(node, tree):
                    func_info = self._extract_function_info(node, lines)
                    analysis.functions.append(func_info)
                    
            elif isinstance(node, ast.ClassDef):
                class_info = self._extract_class_info(node, lines)
                analysis.classes.append(class_info)
        
        # Busca por main
        if 'if __name__ == "__main__"' in content:
            analysis.entry_point = "__main__"
        
        analysis.dependencies = self._extract_dependencies(analysis.imports)
        analysis.complexity_score = self._calculate_complexity(analysis)
        analysis.main_purpose = self._determine_main_purpose(analysis, content)
    
    def _extract_function_info(self, node, lines):
        docstring = ast.get_docstring(node) if hasattr(ast, 'get_docstring') else None
        params = [arg.arg for arg in node.args.args]
        return_type = ast.unparse(node.returns) if node.returns else None
        visibility = "private" if node.name.startswith('_') else "public"
        
        return FunctionInfo(
            name=node.name,
            docstring=docstring,
            parameters=params,
            return_type=return_type,
            visibility=visibility,
            complexity="Média",
            line_number=node.lineno,
            annotations=[]
        )
    
    def _extract_class_info(self, node, lines):
        docstring = ast.get_docstring(node) if hasattr(ast, 'get_docstring') else None
        methods = [self._extract_function_info(item, lines) for item in node.body if isinstance(item, ast.FunctionDef)]
        inheritance = [base.id for base in node.bases if isinstance(base, ast.Name)]
        
        return ClassInfo(
            name=node.name,
            docstring=docstring,
            methods=methods,
            attributes=[],
            inheritance=inheritance,
            interfaces=[],
            visibility="public",
            is_abstract=False,
            line_number=node.lineno
        )
    
    def _is_method(self, node, tree):
        import ast
        for parent in ast.walk(tree):
            if isinstance(parent, ast.ClassDef) and node in parent.body:
                return True
        return False
    
    def _extract_dependencies(self, imports):
        external_deps = []
        standard_libs = {'os', 'sys', 'json', 'datetime', 'collections', 're', 'math', 'random'}
        
        for imp in imports:
            base_module = imp.split('.')[0]
            if base_module not in standard_libs and not base_module.startswith('_'):
                external_deps.append(base_module)
        
        return list(set(external_deps))
    
    def _calculate_complexity(self, analysis):
        return len(analysis.functions) * 1.5 + len(analysis.classes) * 2.0 + len(analysis.dependencies) * 0.5
    
    def _determine_main_purpose(self, analysis, content):
        lines = content.split('\n')
        for line in lines[:10]:
            if line.strip().startswith('#') and len(line.strip()) > 5:
                return line.strip()[1:].strip()
        
        if len(analysis.classes) > len(analysis.functions):
            return "Definição de classes e estruturas de dados"
        elif len(analysis.functions) > 0:
            return "Implementação de funções utilitárias"
        else:
            return "Configuração ou script auxiliar"
    
    def _create_error_analysis(self, filepath, language, error):
        return FileAnalysis(
            filepath=filepath,
            language=language,
            imports=[],
            functions=[],
            classes=[],
            dependencies=[],
            main_purpose=f"Erro na análise: {error}",
            complexity_score=0.0,
            package_namespace=None,
            entry_point=None
        )

# Analisador JavaScript/TypeScript
class JavaScriptAnalyzer(LanguageAnalyzer):
    def get_file_extensions(self) -> List[str]:
        return ['.js', '.ts', '.jsx', '.tsx']
    
    def analyze(self, content: str, filepath: str) -> FileAnalysis:
        lang = "TypeScript" if filepath.endswith(('.ts', '.tsx')) else "JavaScript"
        
        analysis = FileAnalysis(
            filepath=filepath,
            language=lang,
            imports=[],
            functions=[],
            classes=[],
            dependencies=[],
            main_purpose="",
            complexity_score=0.0,
            package_namespace=None,
            entry_point=None
        )
        
        self._analyze_js_content(content, analysis)
        return analysis
    
    def _analyze_js_content(self, content: str, analysis: FileAnalysis):
        lines = content.split('\n')
        
        # Imports/Requires
        import_patterns = [
            r'import\s+.*?\s+from\s+["\']([^"\']+)["\']',
            r'require\(["\']([^"\']+)["\']\)',
            r'import\s+["\']([^"\']+)["\']'
        ]
        
        for pattern in import_patterns:
            matches = re.findall(pattern, content)
            analysis.imports.extend(matches)
        
        # Functions
        func_patterns = [
            r'function\s+(\w+)\s*\([^)]*\)',
            r'const\s+(\w+)\s*=\s*\([^)]*\)\s*=>\s*\{',
            r'(\w+)\s*:\s*function\s*\([^)]*\)',
            r'(\w+)\s*:\s*\([^)]*\)\s*=>\s*\{'
        ]
        
        for pattern in func_patterns:
            matches = re.findall(pattern, content)
            for match in matches:
                if isinstance(match, tuple):
                    func_name = match[0]
                else:
                    func_name = match
                
                line_num = self._find_line_number(content, func_name)
                analysis.functions.append(FunctionInfo(
                    name=func_name,
                    docstring=None,
                    parameters=[],
                    return_type=None,
                    visibility="public",
                    complexity="Média",
                    line_number=line_num,
                    annotations=[]
                ))
        
        # Classes
        class_pattern = r'class\s+(\w+)(?:\s+extends\s+(\w+))?'
        class_matches = re.findall(class_pattern, content)
        
        for match in class_matches:
            class_name = match[0]
            inheritance = [match[1]] if match[1] else []
            line_num = self._find_line_number(content, class_name)
            
            analysis.classes.append(ClassInfo(
                name=class_name,
                docstring=None,
                methods=[],
                attributes=[],
                inheritance=inheritance,
                interfaces=[],
                visibility="public",
                is_abstract=False,
                line_number=line_num
            ))
        
        analysis.dependencies = self._extract_js_dependencies(analysis.imports)
        analysis.complexity_score = len(analysis.functions) * 1.5 + len(analysis.classes) * 2.0
        analysis.main_purpose = self._determine_js_purpose(content)
    
    def _find_line_number(self, content: str, identifier: str) -> int:
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if identifier in line:
                return i + 1
        return 1
    
    def _extract_js_dependencies(self, imports: List[str]) -> List[str]:
        external_deps = []
        for imp in imports:
            if not imp.startswith('.') and not imp.startswith('/'):
                external_deps.append(imp.split('/')[0])
        return list(set(external_deps))
    
    def _determine_js_purpose(self, content: str) -> str:
        if 'export default' in content or 'module.exports' in content:
            return "Módulo para exportação"
        elif 'React' in content or 'Component' in content:
            return "Componente React"
        elif 'express' in content or 'app.listen' in content:
            return "Servidor/API"
        else:
            return "Script JavaScript"

# Analisador Java
class JavaAnalyzer(LanguageAnalyzer):
    def get_file_extensions(self) -> List[str]:
        return ['.java']
    
    def analyze(self, content: str, filepath: str) -> FileAnalysis:
        analysis = FileAnalysis(
            filepath=filepath,
            language="Java",
            imports=[],
            functions=[],
            classes=[],
            dependencies=[],
            main_purpose="",
            complexity_score=0.0,
            package_namespace=None,
            entry_point=None
        )
        
        self._analyze_java_content(content, analysis)
        return analysis
    
    def _analyze_java_content(self, content: str, analysis: FileAnalysis):
        # Package
        package_match = re.search(r'package\s+([^;]+);', content)
        if package_match:
            analysis.package_namespace = package_match.group(1)
        
        # Imports
        import_matches = re.findall(r'import\s+([^;]+);', content)
        analysis.imports = import_matches
        
        # Classes
        class_pattern = r'(?:public\s+)?(?:abstract\s+)?class\s+(\w+)(?:\s+extends\s+(\w+))?(?:\s+implements\s+([^{]+))?'
        class_matches = re.findall(class_pattern, content)
        
        for match in class_matches:
            class_name = match[0]
            inheritance = [match[1]] if match[1] else []
            interfaces = [i.strip() for i in match[2].split(',')] if match[2] else []
            
            analysis.classes.append(ClassInfo(
                name=class_name,
                docstring=None,
                methods=[],
                attributes=[],
                inheritance=inheritance,
                interfaces=interfaces,
                visibility="public",
                is_abstract="abstract" in content,
                line_number=self._find_line_number(content, class_name)
            ))
        
        # Methods
        method_pattern = r'(?:public|private|protected)?\s*(?:static\s+)?(?:final\s+)?(\w+)\s+(\w+)\s*\([^)]*\)'
        method_matches = re.findall(method_pattern, content)
        
        for match in method_matches:
            return_type = match[0]
            method_name = match[1]
            
            if method_name not in ['class', 'if', 'for', 'while']:  # Filtrar palavras-chave
                analysis.functions.append(FunctionInfo(
                    name=method_name,
                    docstring=None,
                    parameters=[],
                    return_type=return_type,
                    visibility="public",
                    complexity="Média",
                    line_number=self._find_line_number(content, method_name),
                    annotations=[]
                ))
        
        # Main method
        if 'public static void main' in content:
            analysis.entry_point = "main"
        
        analysis.dependencies = self._extract_java_dependencies(analysis.imports)
        analysis.complexity_score = len(analysis.functions) * 1.5 + len(analysis.classes) * 2.0
        analysis.main_purpose = self._determine_java_purpose(content, analysis)
    
    def _find_line_number(self, content: str, identifier: str) -> int:
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if identifier in line:
                return i + 1
        return 1
    
    def _extract_java_dependencies(self, imports: List[str]) -> List[str]:
        external_deps = []
        for imp in imports:
            if not imp.startswith('java.') and not imp.startswith('javax.'):
                package = imp.split('.')[0]
                external_deps.append(package)
        return list(set(external_deps))
    
    def _determine_java_purpose(self, content: str, analysis: FileAnalysis) -> str:
        if analysis.entry_point == "main":
            return "Aplicação principal"
        elif any('Test' in cls.name for cls in analysis.classes):
            return "Testes unitários"
        elif any('Controller' in cls.name for cls in analysis.classes):
            return "Controlador web"
        elif any('Service' in cls.name for cls in analysis.classes):
            return "Serviço de negócio"
        else:
            return "Classe de domínio"

# Ferramenta principal
class MultiLanguageCodeAnalyzer(BaseTool):
    name: str = "multi_language_code_analyzer"
    description: str = "Analisa código em múltiplas linguagens (Python, JavaScript, Java, etc.)"
    
    def _run(self, file_path: str) -> Dict[str, Any]:
        """Analisa um arquivo de código em qualquer linguagem suportada"""
        try:
            # Inicializar analisadores aqui dentro do método
            analyzers = [
                PythonAnalyzer(),
                JavaScriptAnalyzer(),
                JavaAnalyzer()
            ]
            
            # Detectar linguagem por extensão
            file_ext = Path(file_path).suffix.lower()
            analyzer = self._get_analyzer_for_extension(file_ext, analyzers)
            
            if not analyzer:
                return {"error": f"Linguagem não suportada para extensão {file_ext}"}
            
            # Ler arquivo
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            
            # Analisar
            analysis = analyzer.analyze(content, file_path)
            
            # Converter para dict
            return {
                "filepath": analysis.filepath,
                "language": analysis.language,
                "package_namespace": analysis.package_namespace,
                "entry_point": analysis.entry_point,
                "imports": analysis.imports,
                "functions": [self._function_to_dict(f) for f in analysis.functions],
                "classes": [self._class_to_dict(c) for c in analysis.classes],
                "dependencies": analysis.dependencies,
                "main_purpose": analysis.main_purpose,
                "complexity_score": analysis.complexity_score,
                "total_lines": len(content.split('\n')),
                "summary": self._generate_summary(analysis),
                "supported_languages": [ext for analyzer in analyzers for ext in analyzer.get_file_extensions()]
            }
            
        except Exception as e:
            return {"error": f"Erro ao analisar {file_path}: {str(e)}"}
    
    def _get_analyzer_for_extension(self, extension: str, analyzers: List[LanguageAnalyzer]) -> Optional[LanguageAnalyzer]:
        """Encontra o analisador apropriado para a extensão"""
        for analyzer in analyzers:
            if extension in analyzer.get_file_extensions():
                return analyzer
        return None
    
    def _function_to_dict(self, func: FunctionInfo) -> Dict[str, Any]:
        return {
            "name": func.name,
            "docstring": func.docstring,
            "parameters": func.parameters,
            "return_type": func.return_type,
            "visibility": func.visibility,
            "complexity": func.complexity,
            "line_number": func.line_number,
            "annotations": func.annotations
        }
    
    def _class_to_dict(self, cls: ClassInfo) -> Dict[str, Any]:
        return {
            "name": cls.name,
            "docstring": cls.docstring,
            "methods": [self._function_to_dict(m) for m in cls.methods],
            "attributes": cls.attributes,
            "inheritance": cls.inheritance,
            "interfaces": cls.interfaces,
            "visibility": cls.visibility,
            "is_abstract": cls.is_abstract,
            "line_number": cls.line_number
        }
    
    def _generate_summary(self, analysis: FileAnalysis) -> str:
        """Gera resumo da análise"""
        parts = []
        
        if analysis.language:
            parts.append(f"Arquivo {analysis.language}")
        
        if analysis.classes:
            parts.append(f"{len(analysis.classes)} classe(s)")
        
        if analysis.functions:
            parts.append(f"{len(analysis.functions)} função(ões)")
        
        if analysis.dependencies:
            deps_str = ", ".join(analysis.dependencies[:3])
            if len(analysis.dependencies) > 3:
                deps_str += f" e mais {len(analysis.dependencies) - 3}"
            parts.append(f"Dependências: {deps_str}")
        
        return ". ".join(parts) if parts else "Análise básica concluída"



class ReadmeGeneratorTool(BaseTool):
    name: str = "readme_generator"
    description: str = "Gera documentação README.md baseada na análise de código"
    
    def _run(self, analysis_data: str) -> Dict[str, Any]:
        """Gera README baseado na análise do código"""
        try:
            if isinstance(analysis_data, str):
                analysis = json.loads(analysis_data)
            else:
                analysis = analysis_data
            
            # Detectar tipo de projeto baseado na análise
            project_type = self._detect_project_type(analysis)
            
            # Gerar seções do README
            sections = self._generate_readme_sections(analysis, project_type)
            
            # Compilar README final
            readme_content = self._compile_readme(sections, analysis)
            
            return {
                "readme_content": readme_content,
                "project_type": project_type,
                "sections_generated": len(sections),
                "language": analysis.get("language", "Unknown")
                # "estimated_completeness": self._calculate_completeness(analysis)
            }
            
        except Exception as e:
            return {"error": f"Erro ao gerar README: {str(e)}"}
    
    def _detect_project_type(self, analysis: Dict[str, Any]) -> str:
        """Detecta o tipo de projeto baseado na análise"""
        language = analysis.get("language", "").lower()
        dependencies = analysis.get("dependencies", [])
        classes = analysis.get("classes", [])
        functions = analysis.get("functions", [])
        main_purpose = analysis.get("main_purpose", "").lower()
        
        # Detectar frameworks e tipos específicos
        if language == "python":
            if any("flask" in dep.lower() for dep in dependencies):
                return "flask_api"
            elif any("django" in dep.lower() for dep in dependencies):
                return "django_app"
            elif any("fastapi" in dep.lower() for dep in dependencies):
                return "fastapi_api"
            elif any("streamlit" in dep.lower() for dep in dependencies):
                return "streamlit_app"
            elif "test" in main_purpose or any("test" in cls["name"].lower() for cls in classes):
                return "python_testing"
            elif len(classes) > len(functions):
                return "python_library"
            else:
                return "python_script"
        
        elif language in ["javascript", "typescript"]:
            if any("react" in dep.lower() for dep in dependencies):
                return "react_app"
            elif any("express" in dep.lower() for dep in dependencies):
                return "node_api"
            elif any("vue" in dep.lower() for dep in dependencies):
                return "vue_app"
            elif any("angular" in dep.lower() for dep in dependencies):
                return "angular_app"
            elif "component" in main_purpose:
                return "js_component"
            else:
                return "js_utility"
        
        elif language == "java":
            if any("spring" in dep.lower() for dep in dependencies):
                return "spring_app"
            elif analysis.get("entry_point") == "main":
                return "java_application"
            elif "test" in main_purpose:
                return "java_testing"
            else:
                return "java_library"
        
        return "generic_project"
    
    def _generate_readme_sections(self, analysis: Dict[str, Any], project_type: str) -> List[ReadmeSection]:
        """Gera seções do README baseado no tipo de projeto"""
        sections = []
        
        # Título e Descrição
        sections.append(self._create_title_section(analysis))
        sections.append(self._create_description_section(analysis, project_type))
        
        badges_section = self._create_badges_section(analysis, project_type)
        if badges_section:
            sections.append(badges_section)
        
        # Índice
        sections.append(self._create_table_of_contents())
        
        # Instalação
        sections.append(self._create_installation_section(analysis, project_type))
        
        # Uso
        sections.append(self._create_usage_section(analysis, project_type))
        
        if analysis.get("classes") or analysis.get("functions"):
            sections.append(self._create_api_section(analysis))
        
        # Estrutura do projeto
        sections.append(self._create_structure_section(analysis))
        
        # Dependências
        if analysis.get("dependencies"):
            sections.append(self._create_dependencies_section(analysis))
        
        # Contribuição
        # sections.append(self._create_contributing_section())
        
        # Licença
        # sections.append(self._create_license_section())
        
        return sections
    
    def _create_title_section(self, analysis: Dict[str, Any]) -> ReadmeSection:
        """Cria seção de título"""
        filepath = analysis.get("filepath", "")
        project_name = Path(filepath).stem if filepath else "Projeto"
        
        return ReadmeSection(
            title="# " + project_name.replace("_", " ").title(),
            content="",
            order=1
        )
    
    def _create_description_section(self, analysis: Dict[str, Any], project_type: str) -> ReadmeSection:
        """Cria seção de descrição"""
        main_purpose = analysis.get("main_purpose", "")
        language = analysis.get("language", "")
        
        # Descrições específicas por tipo de projeto
        type_descriptions = {
            "flask_api": "API REST desenvolvida com Flask",
            "django_app": "Aplicação web desenvolvida com Django",
            "fastapi_api": "API moderna e rápida desenvolvida com FastAPI",
            "streamlit_app": "Aplicação web interativa desenvolvida com Streamlit",
            "react_app": "Aplicação web desenvolvida com React",
            "node_api": "API Node.js desenvolvida com Express",
            "spring_app": "Aplicação Java desenvolvida com Spring Framework",
            "python_library": "Biblioteca Python para reutilização",
            "js_utility": "Utilitário JavaScript",
            "java_application": "Aplicação Java standalone"
        }
        
        base_description = type_descriptions.get(project_type, f"Projeto desenvolvido em {language}")
        
        content = f"{base_description}.\n\n"
        if main_purpose and main_purpose != base_description:
            content += f"**Propósito:** {main_purpose}\n\n"
        
        # Adicionar métricas do projeto
        total_classes = len(analysis.get("classes", []))
        total_functions = len(analysis.get("functions", []))
        # complexity = analysis.get("complexity_score", 0)
        
        # content += f"**Características:**\n"
        # if total_classes > 0:
        #     content += f"- {total_classes} classe(s) implementada(s)\n"
        # if total_functions > 0:
        #     content += f"- {total_functions} função(ões) disponível(eis)\n"
        # content += f"- Complexidade estimada: {self._format_complexity(complexity)}\n"
        
        return ReadmeSection(
            title="## Descrição",
            content=content,
            order=2
        )
    
    def _create_badges_section(self, analysis: Dict[str, Any], project_type: str) -> Optional[ReadmeSection]:
        """Cria seção de badges"""
        language = analysis.get("language", "").lower()
        
        badges = []
        
        # Badges de linguagem
        if language == "python":
            badges.append("![Python](https://img.shields.io/badge/python-v3.7+-blue.svg)")
        elif language in ["javascript", "typescript"]:
            badges.append("![Node.js](https://img.shields.io/badge/node.js-v14+-green.svg)")
        elif language == "java":
            badges.append("![Java](https://img.shields.io/badge/java-v11+-orange.svg)")
        
        # Badges de framework
        dependencies = analysis.get("dependencies", [])
        for dep in dependencies:
            dep_lower = dep.lower()
            if dep_lower == "flask":
                badges.append("![Flask](https://img.shields.io/badge/flask-2.0+-red.svg)")
            elif dep_lower == "django":
                badges.append("![Django](https://img.shields.io/badge/django-4.0+-green.svg)")
            elif dep_lower == "react":
                badges.append("![React](https://img.shields.io/badge/react-18+-blue.svg)")
            elif dep_lower == "express":
                badges.append("![Express](https://img.shields.io/badge/express-4.0+-lightgrey.svg)")
        
        if badges:
            return ReadmeSection(
                title="",
                content="\n".join(badges) + "\n",
                order=1.5
            )
        
        return None
    
    def _create_table_of_contents(self) -> ReadmeSection:
        """Cria índice"""
        content = """
- [Instalação](#instalação)
- [Uso](#uso)
- [API/Funcionalidades](#apifuncionalidades)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Dependências](#dependências)
- [Contribuição](#contribuição)
- [Licença](#licença)
"""
        return ReadmeSection(
            title="## Índice",
            content=content,
            order=3
        )
    
    def _create_installation_section(self, analysis: Dict[str, Any], project_type: str) -> ReadmeSection:
        """Cria seção de instalação"""
        language = analysis.get("language", "").lower()
        dependencies = analysis.get("dependencies", [])
        
        content = "### Pré-requisitos\n\n"
        
        # Pré-requisitos por linguagem
        if language == "python":
            content += "- Python 3.7 ou superior\n"
            if dependencies:
                content += "- pip (gerenciador de pacotes Python)\n"
        elif language in ["javascript", "typescript"]:
            content += "- Node.js 14 ou superior\n"
            content += "- npm ou yarn\n"
        elif language == "java":
            content += "- Java 11 ou superior\n"
            content += "- Maven ou Gradle (se aplicável)\n"
        
        content += "\n### Instalação\n\n"
        
        # Comandos de instalação
        if language == "python":
            content += "1. Clone o repositório:\n"
            content += "```bash\n"
            content += "git clone <url-do-repositorio>\n"
            content += "cd <nome-do-projeto>\n"
            content += "```\n\n"
            
            if dependencies:
                content += "2. Instale as dependências:\n"
                content += "```bash\n"
                content += "pip install -r requirements.txt\n"
                content += "```\n\n"
                
                content += "Ou instale as dependências individuais:\n"
                content += "```bash\n"
                for dep in dependencies[:10]:  
                    content += f"pip install {dep}\n"
                content += "```\n\n"
        
        elif language in ["javascript", "typescript"]:
            content += "1. Clone o repositório:\n"
            content += "```bash\n"
            content += "git clone <url-do-repositorio>\n"
            content += "cd <nome-do-projeto>\n"
            content += "```\n\n"
            
            content += "2. Instale as dependências:\n"
            content += "```bash\n"
            content += "npm install\n"
            content += "# ou\n"
            content += "yarn install\n"
            content += "```\n\n"
        
        elif language == "java":
            content += "1. Clone o repositório:\n"
            content += "```bash\n"
            content += "git clone <url-do-repositorio>\n"
            content += "cd <nome-do-projeto>\n"
            content += "```\n\n"
            
            content += "2. Compile o projeto:\n"
            content += "```bash\n"
            content += "javac *.java\n"
            content += "# ou se usar Maven:\n"
            content += "mvn compile\n"
            content += "```\n\n"
        
        return ReadmeSection(
            title="## Instalação",
            content=content,
            order=4
        )
    
    def _create_usage_section(self, analysis: Dict[str, Any], project_type: str) -> ReadmeSection:
        """Cria seção de uso"""
        language = analysis.get("language", "").lower()
        entry_point = analysis.get("entry_point")
        filepath = analysis.get("filepath", "")
        filename = Path(filepath).name if filepath else "main"
        
        content = "### Uso Básico\n\n"
        
        # Exemplos específicos por tipo de projeto
        if project_type == "flask_api":
            content += "Execute a aplicação Flask:\n\n"
            content += "```bash\n"
            content += f"python {filename}\n"
            content += "```\n\n"
            content += "A API estará disponível em `http://localhost:5000`\n\n"
            
        elif project_type == "fastapi_api":
            content += "Execute a aplicação FastAPI:\n\n"
            content += "```bash\n"
            content += f"uvicorn {filename.replace('.py', '')}:app --reload\n"
            content += "```\n\n"
            content += "A API estará disponível em `http://localhost:8000`\n"
            content += "Documentação automática em `http://localhost:8000/docs`\n\n"
            
        elif project_type == "streamlit_app":
            content += "Execute a aplicação Streamlit:\n\n"
            content += "```bash\n"
            content += f"streamlit run {filename}\n"
            content += "```\n\n"
            
        elif project_type == "react_app":
            content += "Execute a aplicação em modo de desenvolvimento:\n\n"
            content += "```bash\n"
            content += "npm start\n"
            content += "# ou\n"
            content += "yarn start\n"
            content += "```\n\n"
            content += "A aplicação estará disponível em `http://localhost:3000`\n\n"
            
        elif project_type == "node_api":
            content += "Execute o servidor:\n\n"
            content += "```bash\n"
            content += f"node {filename}\n"
            content += "# ou\n"
            content += "npm start\n"
            content += "```\n\n"
            
        elif language == "python" and entry_point == "__main__":
            content += f"Execute o script Python:\n\n"
            content += "```bash\n"
            content += f"python {filename}\n"
            content += "```\n\n"
            
        elif language == "java" and entry_point == "main":
            content += "Execute a aplicação Java:\n\n"
            content += "```bash\n"
            content += f"java {filename.replace('.java', '')}\n"
            content += "```\n\n"
        
        else:
            content += f"Importe e use o módulo em seu código:\n\n"
            if language == "python":
                module_name = filename.replace('.py', '')
                content += f"```python\n"
                content += f"import {module_name}\n\n"
                content += f"# Use as funções disponíveis\n"
                content += f"```\n\n"
            elif language in ["javascript", "typescript"]:
                content += f"```javascript\n"
                content += f"const module = require('./{filename}');\n\n"
                content += f"// Use as funções disponíveis\n"
                content += f"```\n\n"
        
        return ReadmeSection(
            title="## Uso",
            content=content,
            order=5
        )
    
    def _create_api_section(self, analysis: Dict[str, Any]) -> ReadmeSection:
        """Cria seção de API/Funcionalidades"""
        classes = analysis.get("classes", [])
        functions = analysis.get("functions", [])
        
        content = ""
        
        if classes:
            content += "### Classes\n\n"
            for cls in classes[:5]:  # Limitar a 5 classes
                content += f"#### `{cls['name']}`\n\n"
                if cls.get('docstring'):
                    content += f"{cls['docstring']}\n\n"
                
                if cls.get('methods'):
                    content += "**Métodos:**\n"
                    for method in cls['methods'][:3]:  # Limitar a 3 métodos por classe
                        params_str = ", ".join(method.get('parameters', []))
                        content += f"- `{method['name']}({params_str})`"
                        if method.get('docstring'):
                            content += f": {method['docstring'][:100]}..."
                        content += "\n"
                    content += "\n"
        
        if functions:
            content += "### Funções\n\n"
            for func in functions[:8]:  # Limitar a 8 funções
                params_str = ", ".join(func.get('parameters', []))
                content += f"#### `{func['name']}({params_str})`\n\n"
                
                if func.get('docstring'):
                    content += f"{func['docstring']}\n\n"
                
                if func.get('return_type'):
                    content += f"**Retorna:** `{func['return_type']}`\n\n"
        
        return ReadmeSection(
            title="## API/Funcionalidades",
            content=content,
            order=6
        )
    
    def _create_structure_section(self, analysis: Dict[str, Any]) -> ReadmeSection:
        """Cria seção de estrutura do projeto"""
        filepath = analysis.get("filepath", "")
        language = analysis.get("language", "")
        
        content = "```\n"
        content += "projeto/\n"
        content += "├── " + (Path(filepath).name if filepath else "main.py") + "\n"
        
        # Adicionar arquivos comuns baseado na linguagem
        if language.lower() == "python":
            content += "├── requirements.txt\n"
            content += "├── README.md\n"
            content += "└── tests/\n"
            content += "    └── test_main.py\n"
        elif language.lower() in ["javascript", "typescript"]:
            content += "├── package.json\n"
            content += "├── README.md\n"
            content += "└── tests/\n"
            content += "    └── main.test.js\n"
        elif language.lower() == "java":
            content += "├── pom.xml (ou build.gradle)\n"
            content += "├── README.md\n"
            content += "└── src/\n"
            content += "    ├── main/java/\n"
            content += "    └── test/java/\n"
        
        content += "```\n"
        
        return ReadmeSection(
            title="## Estrutura do Projeto",
            content=content,
            order=7
        )
    
    def _create_dependencies_section(self, analysis: Dict[str, Any]) -> ReadmeSection:
        """Cria seção de dependências"""
        dependencies = analysis.get("dependencies", [])
        language = analysis.get("language", "")
        
        content = f"Este projeto utiliza as seguintes dependências principais:\n\n"
        
        for dep in dependencies:
            content += f"- **{dep}**: [Descrição da dependência]\n"
        
        content += f"\n### Instalação das Dependências\n\n"
        
        if language.lower() == "python":
            content += "```bash\n"
            content += "pip install " + " ".join(dependencies) + "\n"
            content += "```\n"
        elif language.lower() in ["javascript", "typescript"]:
            content += "```bash\n"
            content += "npm install " + " ".join(dependencies) + "\n"
            content += "```\n"
        elif language.lower() == "java":
            content += "Adicione as dependências ao seu `pom.xml` ou `build.gradle`\n"
        
        return ReadmeSection(
            title="## Dependências",
            content=content,
            order=8
        )
    
#     def _create_contributing_section(self) -> ReadmeSection:
#         """Cria seção de contribuição"""
#         content = """
# 1. Faça um fork do projeto
# 2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
# 3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
# 4. Push para a branch (`git push origin feature/AmazingFeature`)
# 5. Abra um Pull Request

# ### Diretrizes de Contribuição

# - Siga os padrões de código existentes
# - Adicione testes para novas funcionalidades
# - Atualize a documentação quando necessário
# - Mantenha o código limpo e bem comentado
# """
        
#         return ReadmeSection(
#             title="## Contribuição",
#             content=content,
#             order=9
#         )
    
#     def _create_license_section(self) -> ReadmeSection:
#         """Cria seção de licença"""
#         content = """
# Este projeto está licenciado sob a [MIT License](LICENSE) - veja o arquivo LICENSE para detalhes.
# """
        
#         return ReadmeSection(
#             title="## Licença",
#             content=content,
#             order=10
#         )
    
#     def _format_complexity(self, complexity: float) -> str:
#         """Formata a complexidade para legibilidade"""
#         if complexity < 5:
#             return "Baixa"
#         elif complexity < 15:
#             return "Média"
#         else:
#             return "Alta"
    
#     def _calculate_completeness(self, analysis: Dict[str, Any]) -> float:
#         """Calcula percentual de completude da análise"""
#         score = 0
#         max_score = 100
        
#         if analysis.get("language"):
#             score += 15
#         if analysis.get("main_purpose"):
#             score += 15
#         if analysis.get("functions"):
#             score += 20
#         if analysis.get("classes"):
#             score += 20
#         if analysis.get("dependencies"):
#             score += 15
#         if analysis.get("imports"):
#             score += 10
#         if analysis.get("entry_point"):
#             score += 5
        
#         return round(score, 1)
    
    def _compile_readme(self, sections: List[ReadmeSection], analysis: Dict[str, Any]) -> str:
        """Compila as seções em um README final"""
        # Ordenar seções
        sections.sort(key=lambda x: x.order)
        
        readme_content = ""
        
        for section in sections:
            if section.title:
                readme_content += section.title + "\n\n"
            if section.content:
                readme_content += section.content + "\n\n"
        
        readme_content += "---\n\n"
        readme_content += f"*Documentação gerada automaticamente baseada na análise do código.*\n"
        
        return readme_content