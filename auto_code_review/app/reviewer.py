from app.ast_analyzer import analyze_generic_code, analyze_python_ast
from app.rule_engine import run_generic_rules, run_python_rules
from app.llm_engine import review_with_llm
from app.utils import calculate_score


def review_code(filename: str, code: str, language: str) -> dict:
    if language == "unknown":
        return {
            "filename": filename,
            "language": language,
            "syntax_valid": False,
            "syntax_error": "Unsupported file type.",
            "ast_summary": {},
            "rule_issues": ["Upload a supported source file to run review analysis."],
            "llm_feedback": "LLM review skipped because file type is unsupported.",
            "overall_score": 0,
        }

    if language == "python":
        ast_result = analyze_python_ast(code)
        syntax_valid = ast_result["syntax_valid"]
        syntax_error = ast_result["syntax_error"]

        if syntax_valid:
            rule_issues = run_python_rules(code)
        else:
            rule_issues = ["Syntax error detected. Fix syntax before deeper review."]
    else:
        ast_result = analyze_generic_code(code, language)
        syntax_valid = ast_result["syntax_valid"]
        syntax_error = ast_result["syntax_error"]
        rule_issues = run_generic_rules(code, language)

    llm_feedback = review_with_llm(language, code, ast_result, rule_issues)
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
