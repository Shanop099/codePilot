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

for idx, chunk in enumerate(chunks):

    embedding = embedder.generate_embedding(
        chunk["content"]
    )

    store.insert_chunk(
        chunk_id=idx + 1,
        embedding=embedding,
        payload={
            "file_path": chunk["file_path"],
            "content": chunk["content"][:1000]
        }
    )

    print(
        f"Indexed {idx + 1}/{len(chunks)}"
    )

print("\nRepository indexed successfully.")