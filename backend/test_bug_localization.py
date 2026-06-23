from app.services.chat_service import ChatService
from app.agents.bug_localization_agent import (
    BugLocalizationAgent
)

chat = ChatService()

agent = BugLocalizationAgent(
    chat.vector_store,
    chat.embedder
)

result = agent.analyze(
    "Routing is not registering endpoints"
)

print(result[:5])