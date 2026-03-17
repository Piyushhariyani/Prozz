import sys
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
AUTO_CODE_REVIEW_ROOT = PROJECT_ROOT / "auto_code_review"

if str(PROJECT_ROOT) in sys.path:
    sys.path.remove(str(PROJECT_ROOT))

if str(AUTO_CODE_REVIEW_ROOT) not in sys.path:
    sys.path.insert(0, str(AUTO_CODE_REVIEW_ROOT))

from app.reviewer import review_code
from app.utils import MAX_UPLOAD_BYTES, detect_language, safe_read_file, validate_upload


class ReviewSystemTests(unittest.TestCase):
    def test_detect_language_supports_multiple_extensions(self):
        self.assertEqual(detect_language("service.py"), "python")
        self.assertEqual(detect_language("handler.js"), "javascript")
        self.assertEqual(detect_language("worker.ts"), "typescript")
        self.assertEqual(detect_language("Main.java"), "java")
        self.assertEqual(detect_language("algo.cpp"), "cpp")
        self.assertEqual(detect_language("main.go"), "go")

    def test_validate_upload_rejects_unknown_and_large_files(self):
        issues = validate_upload("archive.zip", b"x" * (MAX_UPLOAD_BYTES + 1))
        self.assertTrue(any("Unsupported file type" in issue for issue in issues))
        self.assertTrue(any("too large" in issue for issue in issues))

    def test_safe_read_file_handles_utf16(self):
        content = "print('hello')".encode("utf-16")
        self.assertIn("print", safe_read_file(content))

    def test_python_review_returns_ast_and_rule_feedback(self):
        code = """
def sample(a, b, c, d, e, f):
    print("debug")
    return a + b
"""
        result = review_code("sample.py", code, "python")
        self.assertEqual(result["language"], "python")
        self.assertTrue(result["syntax_valid"])
        self.assertIn("functions", result["ast_summary"])
        self.assertGreaterEqual(len(result["rule_issues"]), 1)

    def test_javascript_review_uses_generic_pipeline(self):
        code = """
import lib from "lib";
function greet(name) {
    console.log(name);
    console.log(name);
    console.log(name);
    console.log(name);
    return name;
}
"""
        result = review_code("greet.js", code, "javascript")
        self.assertEqual(result["language"], "javascript")
        self.assertTrue(result["syntax_valid"])
        self.assertEqual(result["ast_summary"]["analysis_type"], "heuristic")
        self.assertTrue(
            any("debug output" in issue.lower() for issue in result["rule_issues"])
        )


if __name__ == "__main__":
    unittest.main()
