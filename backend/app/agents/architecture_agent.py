
from groq import Groq

from app.config import GROQ_API_KEY
from app.analysis.call_graph import CallGraph


class ArchitectureAgent:
    def __init__(self, call_graph: CallGraph) -> None:
        self.call_graph = call_graph
        self.client = Groq(api_key=GROQ_API_KEY)

    def _get_incoming_dependencies(self, symbol_name: str) -> list[str]:
        return self.call_graph.get_callers(symbol_name)

    def _get_outgoing_dependencies(self, symbol_name: str) -> list[str]:
        return self.call_graph.get_called_functions(symbol_name)

    def explain(self, symbol_name: str, file_content: str) -> str:
        incoming = self._get_incoming_dependencies(symbol_name)
        outgoing = self._get_outgoing_dependencies(symbol_name)

        called_by_str = ", ".join(incoming) if incoming else "None"
        calls_str = ", ".join(outgoing) if outgoing else "None"

        prompt = f"""
You are an expert software architect AI.

Rules:
- Never hallucinate.
- Never assume functionality.
- Never infer business logic.
- Never speculate.
- Only use supplied code and dependency information.
- Do not make assumptions about runtime behavior, external systems, business logic, user flows, or hidden implementation details.

Allowed Evidence Sources:
- Source code
- Incoming dependencies
- Outgoing dependencies

If a claim cannot be directly supported by the evidence, you must explicitly write:
"Not evident from the provided information."

Component:
{symbol_name}

Called By:
{called_by_str}

Calls:
{calls_str}

Code:
{file_content}

Based strictly on the provided code and dependency lists above, analyze the architecture.

Ensure your output strictly follows this format:

Architecture Summary:
<explain the primary purpose and structural role of this component>

Incoming Dependencies:
<explain what calls this component and why>

Outgoing Dependencies:
<explain what this component calls and what it delegates>

Execution Flow:
<step-by-step trace of how data or execution moves through this component>

Impact:
<what happens to the overall system if this component is modified or breaks>
"""

        try:
            response = self.client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}]
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error generating architecture explanation: {e}")
            return "An error occurred while generating the architecture explanation."

