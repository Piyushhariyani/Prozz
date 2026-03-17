import os
from dotenv import load_dotenv

load_dotenv()


def build_prompt(code: str, ast_summary: dict, rule_issues: list[str]) -> str:
    return f"""
You are a senior software engineer and code reviewer.

Review the following Python code.

Give feedback in this format:
1. Code quality
2. Possible bugs
3. Performance improvements
4. Readability improvements
5. Best practices
6. Final summary

AST Summary:
{ast_summary}

Rule Issues:
{rule_issues}

Code:
{code}
""".strip()


def mock_llm_review(code: str, ast_summary: dict, rule_issues: list[str]) -> str:
    feedback = []
    feedback.append("Code quality: The code is readable but can be improved for maintainability.")
    feedback.append("Possible bugs: Check edge cases and input validation carefully.")
    feedback.append("Performance improvements: Reduce unnecessary loops and repeated computations.")
    feedback.append("Readability improvements: Add docstrings, better variable names, and modular functions.")
    feedback.append("Best practices: Use logging instead of many print statements and keep functions small.")

    if rule_issues:
        feedback.append("Detected issues:")
        for issue in rule_issues[:5]:
            feedback.append(f"- {issue}")

    feedback.append("Final summary: This code is a good start, but it can be cleaner, more modular, and easier to maintain.")

    return "\n".join(feedback)


def review_with_llm(code: str, ast_summary: dict, rule_issues: list[str]) -> str:
    provider = os.getenv("LLM_PROVIDER", "mock").lower()

    if provider == "mock":
        return mock_llm_review(code, ast_summary, rule_issues)

    return mock_llm_review(code, ast_summary, rule_issues)