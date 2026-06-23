from app.services.chat_service import ChatService

chat = ChatService()

result = chat.load_repository(
    "repositories/flask"
)

print(result)

response = chat.ask(
    "What is Flask"
)

print(response["retrieval_type"])

chat.close()