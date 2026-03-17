from app.ast_analyzer import analyze_python_ast
from app.rule_engine import run_python_rules
from app.llm_engine import review_with_llm
from app.utils import calculate_score


def review_code(filename: str, code: str, language: str) -> dict:
    if language != "python":
        return {
            "filename": filename,
            "language": language,
            "syntax_valid": False,
            "syntax_error": "Currently only Python files are supported.",
            "ast_summary": {},
            "rule_issues": ["Only Python review is implemented in this version."],
            "llm_feedback": "LLM review skipped because file type is unsupported.",
            "overall_score": 0,
        }

    ast_result = analyze_python_ast(code)

    syntax_valid = ast_result["syntax_valid"]
    syntax_error = ast_result["syntax_error"]

    if syntax_valid:
        rule_issues = run_python_rules(code)
    else:
        rule_issues = ["Syntax error detected. Fix syntax before deeper review."]

    llm_feedback = review_with_llm(code, ast_result, rule_issues)
    overall_score = calculate_score(syntax_valid, len(rule_issues))

    return {
        "filename": filename,
        "language": language,
        "syntax_valid": syntax_valid,
        "syntax_error": syntax_error,
        "ast_summary": ast_result,
        "rule_issues": rule_issues,
        "llm_feedback": llm_feedback,
        "overall_score": overall_score,
    }