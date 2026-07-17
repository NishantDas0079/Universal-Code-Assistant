from app.schemas import Issue


def run_javascript_rules(code: str):
    issues = []

    if "var " in code:
        issues.append(Issue(
            line=None,
            severity="low",
            category="modernization",
            message="var keyword detected.",
            suggestion="Use let or const instead of var."
        ))

    if "eval(" in code:
        issues.append(Issue(
            line=None,
            severity="high",
            category="security",
            message="Use of eval() detected.",
            suggestion="Avoid eval() due to security risks."
        ))

    return issues