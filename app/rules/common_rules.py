from app.schemas import Issue


def run_common_rules(code: str):
    issues = []

    if "eval(" in code:
        issues.append(Issue(
            line=None,
            severity="high",
            category="security",
            message="Use of eval() detected.",
            suggestion="Replace eval() with a safe parser or strict validation."
        ))

    if "TODO" in code or "FIXME" in code:
        issues.append(Issue(
            line=None,
            severity="low",
            category="maintenance",
            message="TODO/FIXME comment found.",
            suggestion="Either complete the work or move it into an issue tracker."
        ))

    return issues