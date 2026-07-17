from app.schemas import Issue


def run_python_rules(code: str):
    issues = []

    if "except:" in code:
        issues.append(Issue(
            line=None,
            severity="medium",
            category="bad_practice",
            message="Bare except detected.",
            suggestion="Catch specific exceptions instead of using a bare except."
        ))

    if "global " in code:
        issues.append(Issue(
            line=None,
            severity="low",
            category="design",
            message="Global variable usage detected.",
            suggestion="Refactor to pass state through functions or classes."
        ))

    return issues