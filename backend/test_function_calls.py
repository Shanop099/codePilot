

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

calls = parser.extract_function_calls(
    tree,
    content
)

print(f"Calls Found: {len(calls)}")

for call in calls[:50]:
    print(call)