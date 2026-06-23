from app.analysis.code_indexer import CodeIndexer


indexer = CodeIndexer()

result = indexer.index_file(
    "repositories/flask/src/flask/app.py"
)

print("\nFILE\n")
print(result["file_path"])

print("\nCLASSES\n")
print(result["classes"][:10])

print("\nFUNCTIONS\n")
print(result["functions"][:20])

print("\nIMPORTS\n")
print(result["imports"][:10])