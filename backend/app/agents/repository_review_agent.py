from groq import Groq

from app.config import GROQ_API_KEY
from app.analysis.call_graph import CallGraph


class RepositoryReviewAgent:

    def __init__(
        self,
        call_graph: CallGraph
    ):

        self.call_graph = call_graph

        self.client = Groq(
            api_key=GROQ_API_KEY
        )

    def review(
        self,
        symbol_name: str,
        file_content: str
    ) -> str:

        callers = (
            self.call_graph.get_callers(
                symbol_name
            )
        )

        callees = (
            self.call_graph.get_called_functions(
                symbol_name
            )
        )

        callers_text = (
            "\n".join(
                f"- {caller}"
                for caller in callers
            )
            if callers
            else "None"
        )

        callees_text = (
            "\n".join(
                f"- {callee}"
                for callee in callees
            )
            if callees
            else "None"
        )

        prompt = f"""
You are a senior software architect and code reviewer.

Review the repository component below.

Rules:
- Use ONLY the provided code and dependency graph.
- Never hallucinate.
- Never assume missing functionality.
- If information is missing, explicitly say:
  "Not evident from the provided information."

Component:
{symbol_name}

Called By:
{callers_text}

Calls:
{callees_text}

Code:
{file_content}

Provide a detailed review using the format below.

Summary:
<what this component does>

Responsibilities:
- item
- item

Architectural Role:
<how it fits into the repository>

Incoming Dependencies:
<what depends on this component>

Outgoing Dependencies:
<what this component depends on>

Risks Of Modification:
- risk
- risk

Maintainability Issues:
- issue
- issue

Suggested Improvements:
- improvement
- improvement

Overall Assessment:
<final evaluation>
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
                f"Repository review error: {e}"
            )

            return (
                "Failed to generate repository review."
            )