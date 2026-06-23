class ExecutionAgent:

    def __init__(
        self,
        call_graph
    ):

        self.call_graph = call_graph

    def analyze(
        self,
        function_name
    ):

        calls = (
            self.call_graph
            .get_called_functions(
                function_name
            )
        )

        return {
            "target": function_name,
            "direct_calls": calls
        }