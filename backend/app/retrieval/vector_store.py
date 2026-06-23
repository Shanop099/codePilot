from qdrant_client import QdrantClient
from qdrant_client.models import (
    PointStruct,
    Distance,
    VectorParams
)


class VectorStore:

    def __init__(self):

        self.client = QdrantClient(
            path="./qdrant_data"
        )

        self.collection_name = "code_chunks"

    def create_collection(self):

        collections = [
            collection.name
            for collection
            in self.client.get_collections().collections
        ]

        if self.collection_name in collections:
            return

        self.client.create_collection(
            collection_name=self.collection_name,
            vectors_config=VectorParams(
                size=384,
                distance=Distance.COSINE
            )
        )

    def insert_chunk(
        self,
        chunk_id,
        embedding,
        payload
    ):

        self.client.upsert(
            collection_name=self.collection_name,
            points=[
                PointStruct(
                    id=chunk_id,
                    vector=embedding.tolist(),
                    payload=payload
                )
            ]
        )

    def search(
        self,
        query_embedding,
        limit=5
    ):

        results = self.client.query_points(
            collection_name=self.collection_name,
            query=query_embedding.tolist(),
            limit=limit
        )

        return results.points