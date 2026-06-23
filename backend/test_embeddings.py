from app.ingestion.file_scanner import FileScanner
from app.ingestion.chunker import Chunker
from app.retrieval.embeddings import EmbeddingGenerator


scanner = FileScanner()
chunker = Chunker()
embedder = EmbeddingGenerator()

files = scanner.scan_repository(
    "repositories/flask"
)

chunks = chunker.chunk_files(files)

sample_chunk = chunks[0]["content"]

embedding = embedder.generate_embedding(
    sample_chunk
)

print(
    f"Embedding Dimension: {len(embedding)}"
)

print(
    embedding[:10]
)