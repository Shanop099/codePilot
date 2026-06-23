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

classes = parser.extract_classes(
    tree,
    content
)

imports = parser.extract_imports(
    tree,
    content
)

print("\nCLASSES")
print("-" * 50)

for cls in classes[:20]:
    print(cls)

print("\nFUNCTIONS")
print("-" * 50)

for func in functions[:20]:
    print(func)

print("\nIMPORTS")
print("-" * 50)

for imp in imports[:20]:
    print(imp)