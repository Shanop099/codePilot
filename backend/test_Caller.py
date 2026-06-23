# test_callers.py

from app.services.chat_service import ChatService

chat = ChatService()

print(
    chat.call_graph.impact_analysis(
        "add_url_rule"
    )
)