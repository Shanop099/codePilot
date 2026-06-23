from groq import Groq

from app.config import GROQ_API_KEY


class RAGAgent:

    def __init__(
        self,
        embedder,
        vector_store
    ):

        self.embedder = embedder

        self.vector_store = vector_store

        self.client = Groq(
            api_key=GROQ_API_KEY
        )

    def answer(
        self,
        query: str
    ):

        query_embedding = (
            self.embedder
            .generate_embedding(
                query
            )
        )

        results = (
            self.vector_store.search(
                query_embedding=query_embedding,
                limit=5
            )
        )

        context_parts = []

        sources = []

        for result in results:

            file_path = (
                result.payload["file_path"]
            )

            if file_path not in sources:

                sources.append(
                    file_path
                )

            context_parts.append(
                f"""
FILE:
{file_path}

CONTENT:
{result.payload["content"]}
"""
            )

        context = "\n\n".join(
            context_parts
        )

        prompt = f"""
You are CodePilot AI.

Use ONLY the repository context.

Repository Context:

{context}

Question:

{query}

Response Format:

Summary:
<summary>

Key Components:
- item

Relevant Files:
- file

Answer:
<detailed explanation>
"""

        response = (
            self.client.chat.completions.create(
                model=
                "llama-3.3-70b-versatile",

                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )
        )

        return {
            "answer":
            response.choices[0]
            .message.content,

            "sources":
            sources
        }