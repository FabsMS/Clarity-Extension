import ast
import os
import re
import json
from typing import Dict, List, Any, Optional, Union
from dataclasses import dataclass
from pathlib import Path
from abc import ABC, abstractmethod
from crewai import Agent, Task, Crew, Process
from crewai.tools import BaseTool
from pydantic import BaseModel, Field

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

