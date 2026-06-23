# test_repository_review_chat.py

from app.services.chat_service import ChatService

chat = ChatService()

queries = [
    "What is Flask",
    "What breaks if I modify add_url_rule",
    "Trace execution from route",
    "Review add_url_rule",
    "How does Flask routing work?"
]

for query in queries:

    print("\n" + "=" * 80)
    print("QUERY:")
    print(query)

    response = chat.ask(query)

    print("\nRETRIEVAL TYPE:")
    print(response["retrieval_type"])

    print("\nSOURCES:")
    print(response["sources"])

    print("\nANSWER:")
    print(str(response["answer"])[:1500])

print("\n" + "=" * 80)
print("ALL TESTS COMPLETED")