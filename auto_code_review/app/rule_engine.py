import ast
import re
from typing import List


def get_function_length(node: ast.FunctionDef) -> int:
    if not node.body:
        return 0
    start = node.lineno
    end = max(getattr(child, "lineno", start) for child in ast.walk(node))
    return end - start + 1


def find_unused_variables(tree: ast.AST) -> List[str]:
    assigned = set()
    used = set()

    class VariableVisitor(ast.NodeVisitor):
        def visit_Name(self, node):
            if isinstance(node.ctx, ast.Store):
                assigned.add(node.id)
            elif isinstance(node.ctx, ast.Load):
                used.add(node.id)
            self.generic_visit(node)

    VariableVisitor().visit(tree)
    unused = assigned - used

    ignore = {"self"}
    return [var for var in unused if var not in ignore and not var.startswith("_")]


def run_python_rules(code: str) -> List[str]:
    issues = []

    lines = code.splitlines()

    try:
        tree = ast.parse(code)
    except SyntaxError:
        issues.append("Code has syntax errors, so advanced rule checks were skipped.")
        return issues

    # Rule 1: file too long
    if len(lines) > 300:
        issues.append("File is too long. Consider splitting into smaller modules.")

    # Rule 2: long functions
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            func_length = get_function_length(node)
            if func_length > 40:
                issues.append(
                    f"Function '{node.name}' is too long ({func_length} lines). Consider breaking it into smaller functions."
                )

            if len(node.args.args) > 5:
                issues.append(
                    f"Function '{node.name}' has too many parameters ({len(node.args.args)})."
                )

            # Rule 3: no docstring
            if ast.get_docstring(node) is None:
                issues.append(f"Function '{node.name}' has no docstring.")

    # Rule 4: too many loops
    loop_count = sum(isinstance(node, (ast.For, ast.While)) for node in ast.walk(tree))
    if loop_count > 10:
        issues.append("Code contains too many loops. Review complexity and optimize if possible.")

    # Rule 5: classes without docstring
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            if ast.get_docstring(node) is None:
                issues.append(f"Class '{node.name}' has no docstring.")

    # Rule 6: unused variables
    unused_vars = find_unused_variables(tree)
    for var in unused_vars:
        issues.append(f"Variable '{var}' may be unused.")

    # Rule 7: print overuse
    print_count = code.count("print(")
    if print_count > 5:
        issues.append("Too many print statements found. Consider using logging.")

    # Rule 8: very long lines
    for idx, line in enumerate(lines, start=1):
        if len(line) > 100:
            issues.append(f"Line {idx} is too long ({len(line)} chars).")

    if not issues:
        issues.append("No major rule-based issues detected.")

    return issues


GENERIC_DEBUG_PATTERNS = {
    "javascript": "console.log(",
    "typescript": "console.log(",
    "java": "System.out.println(",
    "go": "fmt.Println(",
    "cpp": "std::cout",
    "c": "printf(",
}


def run_generic_rules(code: str, language: str) -> List[str]:
    issues = []
    lines = code.splitlines()
    debug_pattern = GENERIC_DEBUG_PATTERNS.get(language)

    if len(lines) > 400:
        issues.append("File is too long. Consider splitting the logic into smaller modules.")

    long_lines = [idx for idx, line in enumerate(lines, start=1) if len(line) > 120]
    for idx in long_lines[:10]:
        issues.append(f"Line {idx} is too long ({len(lines[idx - 1])} chars).")

    todo_count = len(re.findall(r"\b(TODO|FIXME|HACK)\b", code))
    if todo_count:
        issues.append(f"Found {todo_count} unfinished TODO/FIXME markers.")

    if "\t" in code:
        issues.append("Tab indentation detected. Prefer consistent spaces for readability.")

    if debug_pattern and code.count(debug_pattern) > 3:
        issues.append("Too many debug output statements found. Consider structured logging.")

    if re.search(r"\beval\s*\(", code):
        issues.append("Potentially unsafe dynamic evaluation detected.")

    if re.search(r"(password|secret|token)\s*=", code, flags=re.IGNORECASE):
        issues.append("Possible hardcoded secret detected. Move secrets to environment variables.")

    if not issues:
        issues.append("No major rule-based issues detected.")

    return issues
