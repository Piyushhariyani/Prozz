import ast
import re
from typing import Dict, Any


def analyze_python_ast(code: str) -> Dict[str, Any]:
    result = {
        "syntax_valid": True,
        "syntax_error": None,
        "functions": [],
        "classes": [],
        "imports": [],
        "loops_count": 0,
        "if_count": 0,
        "total_lines": len(code.splitlines()),
    }

    try:
        tree = ast.parse(code)
    except SyntaxError as e:
        result["syntax_valid"] = False
        result["syntax_error"] = f"SyntaxError: {e}"
        return result

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            result["functions"].append({
                "name": node.name,
                "args_count": len(node.args.args),
                "line": node.lineno
            })

        elif isinstance(node, ast.ClassDef):
            result["classes"].append({
                "name": node.name,
                "line": node.lineno
            })

        elif isinstance(node, ast.Import):
            for alias in node.names:
                result["imports"].append(alias.name)

        elif isinstance(node, ast.ImportFrom):
            module_name = node.module if node.module else ""
            result["imports"].append(module_name)

        elif isinstance(node, (ast.For, ast.While)):
            result["loops_count"] += 1

        elif isinstance(node, ast.If):
            result["if_count"] += 1

    return result


GENERIC_IMPORT_PATTERNS = {
    "javascript": r"^\s*(import\s.+from\s.+|const\s+\w+\s*=\s*require\()",
    "typescript": r"^\s*(import\s.+from\s.+|const\s+\w+\s*=\s*require\()",
    "java": r"^\s*import\s+[\w.]+;",
    "go": r"^\s*(import\s+\(|import\s+\".+\")",
    "cpp": r"^\s*#include\s+[<\"].+[>\"]",
    "c": r"^\s*#include\s+[<\"].+[>\"]",
}

GENERIC_FUNCTION_PATTERNS = {
    "javascript": r"\bfunction\s+\w+\s*\(|\b\w+\s*=\s*\(?.*\)?\s*=>",
    "typescript": r"\bfunction\s+\w+\s*\(|\b\w+\s*=\s*\(?.*\)?\s*=>",
    "java": r"\b(?:public|private|protected)?\s*(?:static\s+)?[\w<>\[\]]+\s+\w+\s*\(",
    "go": r"\bfunc\s+\w+\s*\(",
    "cpp": r"\b[\w:<>]+\s+\w+\s*\([^;]*\)\s*\{",
    "c": r"\b[\w\*]+\s+\w+\s*\([^;]*\)\s*\{",
}

GENERIC_CLASS_PATTERNS = {
    "javascript": r"\bclass\s+\w+",
    "typescript": r"\bclass\s+\w+",
    "java": r"\bclass\s+\w+",
    "cpp": r"\bclass\s+\w+|\bstruct\s+\w+",
}


def analyze_generic_code(code: str, language: str) -> Dict[str, Any]:
    lines = code.splitlines()
    functions_pattern = GENERIC_FUNCTION_PATTERNS.get(language, r"$^")
    imports_pattern = GENERIC_IMPORT_PATTERNS.get(language, r"$^")
    classes_pattern = GENERIC_CLASS_PATTERNS.get(language, r"$^")

    return {
        "syntax_valid": True,
        "syntax_error": None,
        "functions": re.findall(functions_pattern, code, flags=re.MULTILINE),
        "classes": re.findall(classes_pattern, code, flags=re.MULTILINE),
        "imports": re.findall(imports_pattern, code, flags=re.MULTILINE),
        "loops_count": len(re.findall(r"\b(for|while)\b", code)),
        "if_count": len(re.findall(r"\bif\b", code)),
        "total_lines": len(lines),
        "analysis_type": "heuristic",
    }
