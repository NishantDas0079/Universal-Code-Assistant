import ast


def parse_python(code: str):
    return ast.parse(code)