from groq import Groq

from app.config import GROQ_API_KEY


class RefactorAgent:

    def __init__(self):

        self.client = Groq(
            api_key=GROQ_API_KEY
        )

    def analyze(
        self,
        symbol_name,
        code
    ):

        prompt = f"""
You are a senior software architect.

Analyze the code below.

Symbol:
{symbol_name}

Code:
{code}
Rules:
- Use ONLY the provided code.
- Never invent helper methods.
- Never invent new APIs.
- If the code is abstract or intentionally unimplemented,
  explicitly state that.
- Refactor only visible code.
Tasks:

1. Identify code smells
2. Identify maintainability issues
3. Suggest refactorings
4. Assess risk
5. Estimate complexity

Output:

Refactoring Report

Code Smells:
- item

Maintainability Issues:
- item

Suggested Refactoring:
- item
Improved Version:
Only provide code if a safe refactor is possible.
Otherwise write:
"No safe refactor evident from provided code."
Complexity:
<Low/Medium/High>

Risk:
<Low/Medium/High>
"""

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