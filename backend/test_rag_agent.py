# test_rag.py

from app.services.chat_service import ChatService

chat = ChatService()

response = chat.ask(
    "How does Flask routing work?"
)

print(response["retrieval_type"])
print(response["sources"])