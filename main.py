from fastapi import FastAPI, Request, UploadFile, File, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from app.schemas import CodeRequest, CodeResponse
from app.analyzer import analyze_code
from app.fixer import generate_fixed_code
from app.language_detector import detect_language

app = FastAPI(title="Universal AI Code Review Assistant", version="2.0.0")
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(request, "index.html", {"request": request})


@app.post("/analyze", response_model=CodeResponse)
async def analyze(request: CodeRequest):
    language = request.language or detect_language(request.code, filename=None)
    result = analyze_code(request.code, language)
    fixed = generate_fixed_code(request.code, language, result["issues"])
    return CodeResponse(
        summary=result["summary"],
        language=language,
        issues=result["issues"],
        fixed_code=fixed
    )


@app.post("/analyze-file", response_model=CodeResponse)
async def analyze_file(file: UploadFile = File(...), language: str = Form("auto")):
    content = (await file.read()).decode("utf-8", errors="ignore")
    detected = detect_language(content, filename=file.filename) if language == "auto" else language
    result = analyze_code(content, detected)
    fixed = generate_fixed_code(content, detected, result["issues"])
    return CodeResponse(
        summary=result["summary"],
        language=detected,
        issues=result["issues"],
        fixed_code=fixed
    )