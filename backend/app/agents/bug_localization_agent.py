from pathlib import Path

from groq import Groq

from app.config import GROQ_API_KEY


class BugLocalizationAgent:

    def __init__(
        self,
        vector_store,
        embedder,
        call_graph=None
    ):

        self.vector_store = vector_store
        self.embedder = embedder
        self.call_graph = call_graph

        self.client = Groq(
            api_key=GROQ_API_KEY
        )

    def analyze(
        self,
        bug_description
    ):

        embedding = (
            self.embedder.generate_embedding(
                bug_description
            )
        )

        results = (
            self.vector_store.search(
                query_embedding=embedding,
                limit=5
            )
        )

        context = ""

        related_functions = []
        dependency_info = []

        if self.call_graph:

            try:

                words = set(
                    bug_description.lower().split()
                )

                for node in list(
                    self.call_graph.graph.nodes()
                ):

                    node_lower = node.lower()

                    if any(
                        word in node_lower
                        for word in words
                        if len(word) > 3
                    ):

                        if node not in related_functions:

                            related_functions.append(
                                node
                            )

                        callers = (
                            self.call_graph.get_callers(
                                node
                            )
                        )

                        callees = (
                            self.call_graph.get_called_functions(
                                node
                            )
                        )

                        for caller in callers[:5]:

                            relation = (
                                f"{caller} -> {node}"
                            )

                            if relation not in dependency_info:

                                dependency_info.append(
                                    relation
                                )

                        for callee in callees[:5]:

                            relation = (
                                f"{node} -> {callee}"
                            )

                            if relation not in dependency_info:

                                dependency_info.append(
                                    relation
                                )

            except Exception:

                pass

        relevant_files = []

        for result in results:

            file_path = (
                result.payload[
                    "file_path"
                ]
            )

            relevant_files.append(
                file_path
            )

            try:

                content = Path(
                    file_path
                ).read_text(
                    encoding="utf-8"
                )

                context += (
                    f"\nFILE: {file_path}\n\n"
                    f"{content[:2000]}\n\n"
                )

            except Exception:

                continue

        prompt = f"""
You are a senior software debugging engineer.

Use ONLY the repository context below.

Rules:
- Do not hallucinate.
- Do not invent files.
- Do not invent functions.
- Do not invent dependencies.
- Use only the provided repository information.
- If something is unclear, explicitly say so.

Bug Description:
{bug_description}

Relevant Functions:
{related_functions}

Dependencies:
{dependency_info}

Repository Context:
{context}

Tasks:

1. Identify files most likely related to the bug.
2. Identify relevant functions.
3. Explain dependency relationships.
4. Suggest possible root causes.
5. Mention confidence level.
6. Recommend investigation steps.

Output Format:

Bug Localization Report

Likely Files:
- file

Relevant Functions:
- function

Dependencies:
- function_a -> function_b

Possible Causes:
- item

Confidence:
High / Medium / Low

Recommended Investigation:
- item

Explanation:
<detailed reasoning>
"""

        try:

            response = (
                self.client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ]
                )
            )

            return (
                response
                .choices[0]
                .message.content
            )

        except Exception as e:

            return (
                f"Bug localization failed: "
                f"{str(e)}"
            )