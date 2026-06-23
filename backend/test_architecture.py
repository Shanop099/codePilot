from app.services.chat_service import ChatService

from app.agents.architecture_agent import (
    ArchitectureAgent
)

chat = ChatService()

agent = ArchitectureAgent(
    chat.symbol_index,
    chat.call_graph
)

print(
    agent.explain(
        "route"
    )
)