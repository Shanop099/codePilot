from app.ingestion.file_scanner import FileScanner
from app.ingestion.chunker import Chunker
from app.retrieval.embeddings import EmbeddingGenerator
from app.retrieval.vector_store import VectorStore


scanner = FileScanner()
chunker = Chunker()
embedder = EmbeddingGenerator()
store = VectorStore()

store.create_collection()

files = scanner.scan_repository(
    "repositories/flask"
)

chunks = chunker.chunk_files(files)

first_chunk = chunks[0]

embedding = embedder.generate_embedding(
    first_chunk["content"]
)

store.insert_chunk(
    chunk_id=1,
    embedding=embedding,
    payload={
        "file_path": first_chunk["file_path"],
        "content": first_chunk["content"][:1000]
    }
)

print("Chunk inserted successfully.")