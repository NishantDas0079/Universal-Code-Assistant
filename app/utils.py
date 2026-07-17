import re


def normalize_code(code: str) -> str:
    return code.replace("\r\n", "\n").strip()


def get_extension(filename: str | None) -> str | None:
    if not filename or "." not in filename:
        return None
    return filename.rsplit(".", 1)[-1].lower()


def safe_line_extract(text: str):
    m = re.search(r"line\s+(\d+)", text, re.IGNORECASE)
    return int(m.group(1)) if m else None