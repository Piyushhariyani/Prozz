from pathlib import Path

MAX_UPLOAD_BYTES = 200_000

SUPPORTED_EXTENSIONS = {
    ".py": "python",
    ".js": "javascript",
    ".ts": "typescript",
    ".java": "java",
    ".cpp": "cpp",
    ".cc": "cpp",
    ".cxx": "cpp",
    ".c": "c",
    ".go": "go",
}


def detect_language(filename: str) -> str:
    extension = Path(filename).suffix.lower()
    return SUPPORTED_EXTENSIONS.get(extension, "unknown")


def validate_upload(filename: str, file_bytes: bytes) -> list[str]:
    issues = []

    if not filename:
        issues.append("Uploaded file must have a filename.")

    if len(file_bytes) == 0:
        issues.append("Uploaded file is empty.")

    if len(file_bytes) > MAX_UPLOAD_BYTES:
        issues.append(
            f"Uploaded file is too large ({len(file_bytes)} bytes). Maximum allowed size is {MAX_UPLOAD_BYTES} bytes."
        )

    if detect_language(filename) == "unknown":
        issues.append(
            "Unsupported file type. Supported extensions are: .py, .js, .ts, .java, .cpp, .cc, .cxx, .c, .go."
        )

    return issues


def safe_read_file(file_bytes: bytes) -> str:
    for encoding in ("utf-8", "utf-16", "latin-1"):
        try:
            return file_bytes.decode(encoding)
        except UnicodeDecodeError:
            continue

    return file_bytes.decode("utf-8", errors="ignore")


def calculate_score(syntax_valid: bool, issues_count: int) -> int:
    score = 100
    if not syntax_valid:
        score -= 40

    score -= min(issues_count * 8, 40)

    if score < 0:
        score = 0

    return score
