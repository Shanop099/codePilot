from pathlib import Path

from groq import Groq

from app.config import GROQ_API_KEY


class RepositoryHealthAgent:

    def __init__(
        self,
        symbol_index,
        call_graph,
        repository_path
    ):

        self.symbol_index = symbol_index
        self.call_graph = call_graph
        self.repository_path = repository_path

        self.client = Groq(
            api_key=GROQ_API_KEY
        )

    def analyze(
        self
    ):

        total_nodes = len(
            self.call_graph.graph.nodes()
        )

        total_edges = len(
            self.call_graph.graph.edges()
        )

        hotspots = []

        for node in self.call_graph.graph.nodes():

            degree = (
                self.call_graph.graph.degree(
                    node
                )
            )

            hotspots.append(
                (
                    node,
                    degree
                )
            )

        hotspots.sort(
            key=lambda x: x[1],
            reverse=True
        )

        hotspots = hotspots[:10]

        hotspot_text = "\n".join(
            f"- {name}: {degree} connections"
            for name, degree in hotspots
        )

        files = list(
            Path(
                self.repository_path
            ).rglob(
                "*.py"
            )
        )

        largest_files = []

        for file in files:

            try:

                largest_files.append(
                    (
                        str(file),
                        file.stat().st_size
                    )
                )

            except Exception:

                continue

        largest_files.sort(
            key=lambda x: x[1],
            reverse=True
        )

        largest_files = largest_files[:10]

        file_text = "\n".join(
            f"- {file} ({size} bytes)"
            for file, size in largest_files
        )

        prompt = f"""
You are a senior software architect.

Analyze the repository health using ONLY the metrics below.

Repository Path:
{self.repository_path}

Call Graph Nodes:
{total_nodes}

Call Graph Edges:
{total_edges}

Architectural Hotspots:
{hotspot_text}

Largest Files:
{file_text}

Generate a repository health report.

Format:

Repository Overview:
<summary>

Architecture Assessment:
<assessment>

Hotspots:
- item

Risk Areas:
- item

Technical Debt Candidates:
- item

Refactoring Opportunities:
- item

Overall Health Score:
<score out of 10>

Final Recommendation:
<summary>
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

            print(
                f"Repository health error: {e}"
            )

            return (
                "Failed to generate repository health report."
            )