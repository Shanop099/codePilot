from groq import Groq
from app.config import GROQ_API_KEY


class CodeReviewAgent:

    def __init__(self):

        self.client = Groq(
            api_key=GROQ_API_KEY
        )

    def review(
        self,
        code: str
    ):

        prompt = f"""
You are a senior software engineer.

Review this code.

Identify:

1. Bugs
2. Code smells
3. Maintainability issues
4. Security concerns
5. Improvements

Code:

{code}
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