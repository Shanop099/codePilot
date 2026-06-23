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

graph = parser.extract_call_graph(
    tree,
    content
)

for function, calls in list(graph.items())[:10]:

    print("\n")
    print(function)

    for call in calls[:10]:
        print("  ->", call)