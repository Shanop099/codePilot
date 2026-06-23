from app.services.chat_service import ChatService

chat = ChatService()

symbol = "route"

result = (
    chat.call_graph.trace_execution(
        symbol
    )
)

print(result)