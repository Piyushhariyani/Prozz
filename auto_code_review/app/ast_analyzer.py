import ast
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