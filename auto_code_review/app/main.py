from fastapi import FastAPI, Request, UploadFile, File
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.reviewer import review_code
from app.utils import detect_language, safe_read_file, validate_upload

app = FastAPI(title="Auto Code Review System")

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "result": None})


@app.post("/review", response_class=HTMLResponse)
async def review_file(request: Request, file: UploadFile = File(...)):
    content = await file.read()
    validation_issues = validate_upload(file.filename or "", content)

    if validation_issues:
        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "result": {
                    "filename": file.filename or "unknown",
                    "language": detect_language(file.filename or ""),
                    "syntax_valid": False,
                    "syntax_error": validation_issues[0],
                    "ast_summary": {},
                    "rule_issues": validation_issues,
                    "llm_feedback": "LLM review skipped because file validation failed.",
                    "overall_score": 0,
                },
                "code": "",
            },
            status_code=400,
        )

    code = safe_read_file(content)
    language = detect_language(file.filename)

    result = review_code(file.filename, code, language)

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "result": result,
            "code": code
        }
    )
