from typing import Optional

from app.utils import get_extension


EXTENSION_MAP = {
    "py": "python",
    "js": "javascript",
    "mjs": "javascript",
    "cjs": "javascript",
    "ts": "typescript",
    "tsx": "typescript",
    "jsx": "javascript",
    "java": "java",
    "cpp": "cpp",
    "cc": "cpp",
    "cxx": "cpp",
    "hpp": "cpp",
    "hh": "cpp",
    "hxx": "cpp",
    "h": "c",          # ambiguous, but common
    "c": "c",
    "go": "go",
    "rb": "ruby",
    "php": "php",
    "rs": "rust",
    "cs": "csharp",
    "kt": "kotlin",
    "swift": "swift",
    "sh": "bash",
    "ps1": "powershell",
    "html": "html",
    "css": "css",
}


def _detect_from_extension(filename: Optional[str]) -> Optional[str]:
    if not filename:
        return None
    ext = get_extension(filename)
    if not ext:
        return None
    ext = ext.lower()
    return EXTENSION_MAP.get(ext)


def _detect_from_content(snippet: str) -> str:
    s = snippet.lower()

    # Python
    if any(tok in s for tok in ("def ", "import ", "self", "async def", "from ")):
        return "python"

    # JavaScript / TypeScript (JS-ish)
    if any(tok in s for tok in ("console.log", "function ", "=>", "document.getelementbyid")):
        return "javascript"

    # Java
    if any(tok in s for tok in ("public class ", "system.out", "implements ", "extends ")):
        return "java"

    # C++
    if "#include" in s or "std::" in s:
        return "cpp"

    # C (very rough, only if not already matched as C++)
    if "#include" in s and "std::" not in s:
        return "c"

    # Go
    if "package main" in s or "func main(" in s:
        return "go"

    # PHP
    if "<?php" in s:
        return "php"

    # HTML
    if "<html" in s or "<!doctype html" in s:
        return "html"

    return "generic"


def detect_language(code: str, filename: Optional[str] = None) -> str:
    """
    Very lightweight language detector.
    1) Try by extension if filename is provided.
    2) Fall back to simple content heuristics.
    3) Default to 'generic'.
    """
    by_ext = _detect_from_extension(filename)
    if by_ext:
        return by_ext

    snippet = code[:4000] if code else ""
    if not snippet.strip():
        return "generic"

    return _detect_from_content(snippet)