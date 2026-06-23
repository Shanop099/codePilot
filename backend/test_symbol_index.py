from app.ingestion.file_scanner import FileScanner
from app.analysis.symbol_index import SymbolIndex


scanner = FileScanner()

files = scanner.scan_repository(
    "repositories/flask"
)

index = SymbolIndex()

index.build(files)

print(
    index.find_function(
        "add_url_rule"
    )
)

print(
    index.find_class(
        "Flask"
    )
)