from pydantic import BaseModel
from typing import List, Dict, Any


class ReviewResult(BaseModel):
    filename: str
    language: str
    syntax_valid: bool
    syntax_error: str | None
    ast_summary: Dict[str, Any]
    rule_issues: List[str]
    llm_feedback: str
    overall_score: int