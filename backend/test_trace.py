from app.services.chat_service import ChatService

chat = ChatService()

response = chat.ask(
    "Trace execution from route"
)

print(response)