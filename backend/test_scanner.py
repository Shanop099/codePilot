from app.ingestion.file_scanner import FileScanner

scanner = FileScanner()

files = scanner.scan_repository(
    "repositories/flask"
)

print(f"Found {len(files)} files\n")

for file in files[:20]:
    print(file)