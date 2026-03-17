import os


def detect_language(filename: str) -> str:
    if filename.endswith(".py"):
        return "python"
    return "unknown"


def safe_read_file(file_bytes: bytes) -> str:
    try:
        return file_bytes.decode("utf-8")
    except UnicodeDecodeError:
        return file_bytes.decode("latin-1", errors="ignore")


def calculate_score(syntax_valid: bool, issues_count: int) -> int:
    score = 100
    if not syntax_valid:
        score -= 40

    score -= min(issues_count * 8, 40)

    if score < 0:
        score = 0

    return score