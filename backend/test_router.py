from app.agents.router_agent import RouterAgent

router = RouterAgent()

queries = [
    "What breaks if I modify add_url_rule",
    "Trace execution from route",
    "Explain architecture of route",
    "What is Flask"
]

for query in queries:

    print(
        query,
        "->",
        router.route(query)
    )