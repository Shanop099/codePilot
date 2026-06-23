from app.agents.code_review_agent import (
    CodeReviewAgent
)

agent = CodeReviewAgent()

print(
    agent.review(
        """
def divide(a,b):
    return a/b
"""
    )
)