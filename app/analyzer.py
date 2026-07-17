import ast
import tempfile
import subprocess
import os

from app.schemas import Issue
from app.rules.common_rules import run_common_rules
from app.rules.python_rules import run_python_rules
from app.rules.javascript_rules import run_javascript_rules
from app.utils import safe_line_extract


def run_command(cmd, file_path):
    try:
        result = subprocess.run(
            cmd + [file_path],
            capture_output=True,
            text=True,
            timeout=20
        )
        return (result.stdout or "") + (result.stderr or "")
    except Exception as e:
        return str(e)


def analyze_python(code: str):
    issues = []
    try:
        tree = ast.parse(code)
        for node in ast.walk(tree):
            if isinstance(node, ast.ExceptHandler) and node.type is None:
                issues.append(Issue(
                    line=getattr(node, "lineno", None),
                    severity="medium",
                    category="bad_practice",
                    message="Bare except detected.",
                    suggestion="Catch specific exceptions."
                ))
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "eval":
                issues.append(Issue(
                    line=getattr(node, "lineno", None),
                    severity="high",
                    category="security",
                    message="eval() detected.",
                    suggestion="Use safer alternatives."
                ))
    except SyntaxError as e:
        issues.append(Issue(
            line=e.lineno,
            severity="high",
            category="syntax",
            message=e.msg,
            suggestion="Fix the syntax error at the highlighted line."
        ))
    return issues


def run_linters(code: str):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".py", mode="w", encoding="utf-8") as tmp:
        tmp.write(code)
        path = tmp.name

    pylint_out = run_command(["pylint", "--disable=all", "--enable=E,F,W"], path)
    bandit_out = run_command(["bandit", "-q", "-r"], path)

    try:
        os.remove(path)
    except:
        pass

    return pylint_out + "\n" + bandit_out


def _deduplicate_issues(issues):
    unique = []
    seen = set()

    for issue in issues:
        line = issue.line if issue.line is not None else "N/A"
        key = (
            line,
            issue.severity.strip().lower(),
            issue.category.strip().lower(),
            issue.message.strip().lower(),
            issue.suggestion.strip().lower()
        )
        if key not in seen:
            seen.add(key)
            unique.append(issue)

    return unique


def _sort_issues(issues):
    severity_rank = {
        "high": 0,
        "medium": 1,
        "low": 2
    }

    return sorted(
        issues,
        key=lambda x: (
            severity_rank.get(x.severity.strip().lower(), 3),
            x.line is None,
            x.line if x.line is not None else 10**9,
            x.category.strip().lower(),
            x.message.strip().lower()
        )
    )


def analyze_code(code: str, language: str):
    issues = []
    code = code.replace("\r\n", "\n")

    issues.extend(run_common_rules(code))

    if language == "python":
        issues.extend(analyze_python(code))
        issues.extend(run_python_rules(code))

        lint_out = run_linters(code)
        for line in lint_out.splitlines():
            lower = line.lower()

            if "unused variable" in lower:
                issues.append(Issue(
                    line=safe_line_extract(line),
                    severity="low",
                    category="style",
                    message=line.strip(),
                    suggestion="Remove or use the variable."
                ))

            elif "syntax-error" in lower:
                issues.append(Issue(
                    line=safe_line_extract(line),
                    severity="high",
                    category="syntax",
                    message=line.strip(),
                    suggestion="Correct the syntax."
                ))

            elif "bandit" in lower or "security" in lower:
                issues.append(Issue(
                    line=safe_line_extract(line),
                    severity="high",
                    category="security",
                    message=line.strip(),
                    suggestion="Review this security-sensitive part carefully."
                ))

    elif language in ["javascript", "typescript"]:
        issues.extend(run_javascript_rules(code))

    else:
        if len(code.strip()) < 5:
            issues.append(Issue(
                line=None,
                severity="low",
                category="quality",
                message="Very small or empty input.",
                suggestion="Submit a full source file for better analysis."
            ))

    issues = _deduplicate_issues(issues)
    issues = _sort_issues(issues)

    summary = f"Detected {len(issues)} issue(s) in {language} code."
    return {"summary": summary, "issues": issues}