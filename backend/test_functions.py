from pathlib import Path

from app.analysis.ast_parser import ASTParser


parser = ASTParser()

content = Path(
    "repositories/flask/src/flask/app.py"
).read_text(
    encoding="utf-8"
)

tree = parser.parse_file(
    content
)

functions = parser.extract_functions(
    tree,
    content
)

print(
    f"Functions Found: {len(functions)}"
)

print()

for function in functions[:30]:
    print(function)