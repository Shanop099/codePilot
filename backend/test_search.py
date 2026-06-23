from app.retrieval.embeddings import EmbeddingGenerator
from app.retrieval.vector_store import VectorStore


embedder = EmbeddingGenerator()
store = VectorStore()

query = "routing and urls"

query_embedding = embedder.generate_embedding(
    query
)

results = store.search(
    query_embedding=query_embedding,
    limit=3
)

print("\nTop Results:\n")

for result in results:

    print("=" * 50)

    print(
        result.payload["file_path"]
    )

    print("\n")

    print(
        result.payload["content"][:300]
    )