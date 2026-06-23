from app.services.chat_service import ChatService

chat = ChatService()

response = chat.ask(
    "Review add_url_rule"
)

print(
    response["retrieval_type"]
)

print(
    response["answer"]
)

chat.close()