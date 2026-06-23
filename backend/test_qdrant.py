from app.retrieval.vector_store import VectorStore

store = VectorStore()

store.create_collection()

print(
    "Collection created successfully."
)