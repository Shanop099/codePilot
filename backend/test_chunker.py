from app.ingestion.file_scanner import FileScanner
from app.ingestion.chunker import Chunker


scanner = FileScanner()
chunker = Chunker()

files = scanner.scan_repository(
    "repositories/flask"
)

chunks = chunker.chunk_files(files)

print(f"Files Found: {len(files)}")
print(f"Chunks Created: {len(chunks)}")

print("\nFirst Chunk:\n")

print(chunks[0]["file_path"])

print("\n")

print(chunks[0]["content"][:500])