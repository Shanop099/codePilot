from sentence_transformers import SentenceTransformer


class EmbeddingGenerator:

    def __init__(self):

        self.model = SentenceTransformer(
            "BAAI/bge-small-en-v1.5" ###other models can also be used which are higher like Nomic embed-text-v1.5,Jina embeddings-v3,OpenAI text-3-small
        )

    def generate_embedding(
        self,
        text: str
    ):

        return self.model.encode(
            text,
            normalize_embeddings=True
        )