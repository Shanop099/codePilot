from app.services.chat_service import ChatService

from app.agents.dependency_agent import (
    DependencyAgent
)

chat = ChatService()

try:

    agent = DependencyAgent(
        chat.call_graph
    )

    result = agent.analyze(
        "add_url_rule"
    )

    print(result)

finally:

    chat.close()