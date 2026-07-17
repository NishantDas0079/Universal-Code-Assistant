# Universal AI Code Review Assistant

[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-brightgreen?style=for-the-badge&logo=fastapi)](https://github.com/fastapi/fastapi)
[![Python](https://img.shields.io/badge/Python-3.14-blue?style=for-the-badge&logo=python)](https://www.python.org/)
[![Status](https://img.shields.io/badge/Status-Active-success?style=for-the-badge)]()

AI‑powered, multi‑language code review assistant built with FastAPI.  
Paste or upload code in different languages, get instant static analysis, see detected bugs and security issues, and view suggested safe fixes in a modern interactive web UI.

---

## ✨ Features

- **FastAPI backend** with JSON API and HTML frontend.
- **Multi‑language analysis** (Python, JavaScript, TypeScript, C/C++, Java, and more via heuristics).
- **Static analysis for Python** using:
  - custom AST rules (bare `except`, `eval`, etc.),
  - `pylint` for style and errors,
  - `bandit` for security checks.
- **Language detection** by file extension and content heuristics.
- **Smart issue aggregation** with severity, category, line number, and suggestions.
- **Fixed code preview** using conservative auto‑fixers (AST round‑trip for Python, simple JS normalization).
- **Interactive UI**:
  - code textarea and drag‑and‑drop file upload,
  - language selector and analyze buttons,
  - tabs for Issues, Fixed Code, and Summary,
  - live stats for issues, language, and status,
  - dark/light theme toggle and copy‑to‑clipboard for fixed code.

---

## 🛠️ Tech Stack

- **Backend:** FastAPI, Uvicorn
- **Templates:** Jinja2 (HTML) served by FastAPI [web:116][web:263]
- **Static analysis:** Python `ast`, `pylint`, `bandit`, custom rules
- **Frontend:** Vanilla HTML/CSS/JS dashboard UI
- **Environment:** Python 3.14 (tested), Git, optional virtualenv

---

## 📂 Project Structure

```text
universal_code_review_assistant/
├── main.py                 # FastAPI app entrypoint
├── app/
│   ├── analyzer.py         # Core analysis pipeline
│   ├── fixer.py            # Auto-fix helpers
│   ├── language_detector.py# Lightweight language detector
│   ├── schemas.py          # Pydantic models
│   ├── rules/
│   │   ├── common_rules.py
│   │   ├── python_rules.py
│   │   └── javascript_rules.py
│   └── utils.py            # Utility helpers
├── templates/
│   └── index.html          # Interactive web UI
└── static/
    └── style.css           # Optional extra styling
```

*(Your actual layout may differ slightly; update this tree accordingly.)*

---

## 🚀 Getting Started (Local)

### 1. Clone the repository

```bash
git clone https://github.com/<your-username>/<your-repo-name>.git
cd <your-repo-name>
```

### 2. (Recommended) Create and activate a virtual environment

```bash
python -m venv .venv
.venv\Scripts\activate    # Windows
# or
source .venv/bin/activate # macOS/Linux
```

### 3. Install dependencies

```bash
python -m pip install fastapi uvicorn python-multipart jinja2 pydantic-settings \
    tree-sitter tree-sitter-languages pylint bandit black isort
```

You can later move these into `requirements.txt` or `pyproject.toml` if you prefer. [web:98][web:102]

### 4. Run the development server

From the project root:

```bash
python -m uvicorn main:app --reload --log-level debug
```

- Server will start at `http://127.0.0.1:8000`.
- Interactive API docs at `http://127.0.0.1:8000/docs`. [web:263][web:268]

---

## 🌐 Using the Web UI

1. Open `http://127.0.0.1:8000/` in your browser.
2. Paste code into the **Code Input** textarea, or drag‑and‑drop a file.
3. Choose a language (or leave **Auto Detect**).
4. Click **Analyze Code** or **Analyze File**.
5. Explore the results:
   - **Issues tab**: list of findings (severity, category, line, message, suggestion).
   - **Fixed Code tab**: conservative auto‑fixed version of the code.
   - **Summary tab**: textual summary of the analysis.
6. Use **Copy Fixed Code** to copy the suggested fixed version to your clipboard.
7. Toggle theme for dark/light mode as you like.

---

## 🧠 How Analysis Works

### Language Detection

`app.language_detector.detect_language(code, filename)`:

- First checks file extension against a mapping (e.g., `.py` → Python, `.js` → JavaScript). [web:203][web:201]
- If no filename or unknown extension, uses simple content heuristics (keywords like `def`, `console.log`, `#include`, etc.)
- Falls back to `"generic"` for unknown cases.

### Python Path

- `analyze_python(code)` walks the AST to detect:
  - bare `except` handlers,
  - direct `eval()` calls,
  - and basic syntax errors. [web:193][web:196]
- `run_linters(code)` writes the code to a temporary file and runs:
  - `pylint` for style and error checks,
  - `bandit` for security checks,
  then converts interesting lines into `Issue` objects. [web:231][web:234]
- `run_common_rules` and `run_python_rules` add generic and Python-specific checks.
- All issues are deduplicated and sorted by severity and line before being returned.

### JavaScript / TypeScript Path

- `run_javascript_rules(code)` applies simple pattern-based checks (e.g., `eval`, `console.log`, `var`, loose `==`).
- For TypeScript, the same rules are applied as a starting point.
- (You can extend this later with ESLint/TypeScript integration via Node for real type-aware analysis.) [web:234][web:235][web:237]

### Fixing Code

- `generate_fixed_code(code, language, issues)` dispatches to:
  - `fix_python_code`: AST round-trip using `ast.unparse` for normalization; falls back to original code if errors arise. [web:191][web:195]
  - `fix_javascript_code`: simple `var` → `let` normalization.
- For other languages, returns the original code unchanged (conservative behavior).

---

## 📡 API Endpoints

### `GET /`

- Returns the main HTML page (`index.html`) rendered via Jinja2. [web:116][web:41]

### `POST /analyze`

- **Body (JSON):**  
  ```json
  {
    "code": "<source code>",
    "language": "auto" | "python" | "javascript" | "typescript" | "java" | "cpp" | "c" | "go" | "generic"
  }
  ```
- **Response:**
  ```json
  {
    "summary": "Detected N issue(s) in python code.",
    "language": "python",
    "issues": [
      {
        "line": 10,
        "severity": "medium",
        "category": "bad_practice",
        "message": "Bare except detected.",
        "suggestion": "Catch specific exceptions."
      }
    ],
    "fixed_code": "<fixed code here>"
  }
  ```

### `POST /analyze-file`

- **Body (multipart/form-data):**
  - `file`: uploaded source file
  - `language`: optional language hint (default `"auto"`) [web:175][web:179]
- Returns the same `CodeResponse` structure as `/analyze`.

---

## 🧩 Pydantic Models

Defined in `app/schemas.py`:

```py
class CodeRequest(BaseModel):
    code: str
    language: str = "auto"

class Issue(BaseModel):
    line: Optional[int] = None
    severity: str
    category: str
    message: str
    suggestion: str

class CodeResponse(BaseModel):
    summary: str
    language: str
    issues: List[Issue]
    fixed_code: Optional[str] = None
```

(You may already have an upgraded version with `Field(...)` descriptions.) [web:187][web:188]

---

## 🧪 Testing the Assistant

Try feeding the app some intentionally buggy code (for example):

- Python: bare `except`, `eval`, division by zero, infinite loops.
- JavaScript: `eval`, `var`, `==` instead of `===`, wrong property names, bad loops.
- TypeScript: unsafe casts, non-null assertions, property mismatches, union misuse.

Synthetic buggy programs are a common way to stress-test code analysis tools. [web:216][web:217][web:133]

---

## 📌 Roadmap / Ideas

- Integrate ESLint + `@typescript-eslint` for richer JS/TS analysis.
- Add more language-specific rule sets (Java, C++, Rust).
- Support project-wide analysis (multiple files).
- Add configuration for rule severity and categories.
- Dockerfile for easy deployment.

---

## 🤝 Contributing

Pull requests, issues, and suggestions are welcome!

- Fork the repo.
- Create a feature branch:
  ```bash
  git checkout -b feature/my-improvement
  ```
- Commit changes and push:
  ```bash
  git commit -m "Improve analyzer for JavaScript"
  git push origin feature/my-improvement
  ```
- Open a Pull Request on GitHub.

---

---

## 🙌 Credits

Built with:

- [FastAPI](https://github.com/fastapi/fastapi) – high-performance Python web framework. [web:268]
- `pylint`, `bandit`, and custom rules for static analysis.
- Synthetic buggy code examples inspired by research and tooling around automated bug generation and code review. [web:216][web:217][web:133]
