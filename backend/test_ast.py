from pathlib import Path

from app.analysis.ast_parser import ASTParser

parser = ASTParser()

content = Path(
    "repositories/flask/src/flask/app.py"
).read_text(
    encoding="utf-8"
)

root = parser.parse_file(
    content
)

print(root.root_node)