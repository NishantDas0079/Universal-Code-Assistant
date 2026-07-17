import ast
from typing import List

from app.schemas import Issue


def _safe_unparse(tree: ast.AST, original: str) -> str:
    """
    Try to unparse an AST back to source.
    If anything fails, fall back to the original code.
    """
    try:
        fixed = ast.unparse(tree)
    except (ValueError, TypeError, AttributeError, RecursionError):
        return original

    # Re-parse to ensure the result is syntactically valid
    try:
        ast.parse(fixed)
    except SyntaxError:
        return original

    return fixed


def fix_python_code(code: str, issues: List[Issue]) -> str:
    """
    Very conservative Python fixer:
    - Only normalizes code via AST round-trip.
    - Does NOT try aggressive refactors yet.
    """
    try:
        tree = ast.parse(code)
    except SyntaxError:
        # If the code is not even parsable, we cannot safely fix it
        return code

    return _safe_unparse(tree, code)


def fix_javascript_code(code: str, issues: List[Issue]) -> str:
    """
    Simple JavaScript fixer:
    - Replace 'var' with 'let' in a naive way.
    This is intentionally minimal and safe-ish.
    """
    # very naive example, but easy to expand later
    fixed = code.replace("var ", "let ")
    return fixed


def generate_fixed_code(code: str, language: str, issues: List[Issue]) -> str:
    """
    Dispatch fixer based on language.
    Currently very conservative: tries not to break code.
    """
    lang = (language or "").lower()

    if lang == "python":
        return fix_python_code(code, issues)

    if lang in ("javascript", "typescript"):
        return fix_javascript_code(code, issues)

    # For other languages, just echo the original code for now
    return code