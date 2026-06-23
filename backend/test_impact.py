from app.services.chat_service import ChatService

chat = ChatService()

response = chat.ask(
    "What breaks if I modify add_url_rule?"
)

print(response)