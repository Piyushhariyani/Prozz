import os
from fastapi import FastAPI, Request, UploadFile, File
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.reviewer import review_code
from app.utils import detect_language, safe_read_file

app = FastAPI(title="Auto Code Review System")

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "result": None})


@app.post("/review", response_class=HTMLResponse)
async def review_file(request: Request, file: UploadFile = File(...)):
    content = await file.read()
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