import os

import requests
from dotenv import load_dotenv

load_dotenv()


def build_prompt(language: str, code: str, ast_summary: dict, rule_issues: list[str]) -> str:
    return f"""
You are a senior software engineer and code reviewer.

Review the following {language} code.

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


def mock_llm_review(language: str, code: str, ast_summary: dict, rule_issues: list[str]) -> str:
    feedback = []
    feedback.append(f"Code quality: The {language} code is readable but can be improved for maintainability.")
    feedback.append("Possible bugs: Review edge cases, null handling, and error paths carefully.")
    feedback.append("Performance improvements: Reduce repeated work and keep expensive operations isolated.")
    feedback.append("Readability improvements: Improve naming, documentation, and separation of concerns.")
    feedback.append("Best practices: Prefer structured logging, validation, and smaller reusable functions.")

    if rule_issues:
        feedback.append("Detected issues:")
        for issue in rule_issues[:5]:
            feedback.append(f"- {issue}")

    feedback.append("Final summary: This code is a good start, but it can be cleaner, more modular, and easier to maintain.")

    return "\n".join(feedback)


def request_openai_review(language: str, code: str, ast_summary: dict, rule_issues: list[str]) -> str:
    api_key = os.getenv("OPENAI_API_KEY")
    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    base_url = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")

    if not api_key:
        raise ValueError("OPENAI_API_KEY is not set.")

    response = requests.post(
        f"{base_url.rstrip('/')}/chat/completions",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={
            "model": model,
            "messages": [
                {
                    "role": "system",
                    "content": "You are a senior code reviewer focused on quality, bugs, performance, and maintainability.",
                },
                {
                    "role": "user",
                    "content": build_prompt(language, code, ast_summary, rule_issues),
                },
            ],
            "temperature": 0.2,
        },
        timeout=20,
    )
    response.raise_for_status()
    payload = response.json()
    return payload["choices"][0]["message"]["content"].strip()


def review_with_llm(language: str, code: str, ast_summary: dict, rule_issues: list[str]) -> str:
    provider = os.getenv("LLM_PROVIDER", "mock").lower()

    if provider in {"openai", "api"}:
        try:
            return request_openai_review(language, code, ast_summary, rule_issues)
        except (requests.RequestException, KeyError, IndexError, ValueError):
            return mock_llm_review(language, code, ast_summary, rule_issues)

    return mock_llm_review(language, code, ast_summary, rule_issues)
