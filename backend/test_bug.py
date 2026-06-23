from app.services.chat_service import ChatService

chat = ChatService()

response = chat.ask(
    "Route decorator not registering endpoint"
)

print(
    response["retrieval_type"]
)

print(
    response["answer"]
)

chat.close()