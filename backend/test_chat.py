from app.services.chat_service import ChatService

chat = ChatService()

query = "Explain architecture of route"

response = chat.ask(
    query
)

print("\nTYPE:")
print(response["retrieval_type"])

print("\nANSWER:")
print(response["answer"])

print("\nSOURCES:")
print(response["sources"])