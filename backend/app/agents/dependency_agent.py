class DependencyAgent:

    def __init__(
        self,
        call_graph
    ):
        self.call_graph = call_graph

    def analyze(
        self,
        function_name
    ):

        callers = [
            caller
            for caller in self.call_graph.get_callers(
                function_name
            )
            if caller != function_name
        ]

        calls = [
            callee
            for callee in self.call_graph.get_called_functions(
                function_name
            )
            if callee != function_name
        ]

        answer = (
            f"Dependency Analysis\n\n"
        )

        answer += (
            f"Symbol:\n"
            f"{function_name}\n\n"
        )

        answer += "Called By:\n"

        if callers:

            for caller in callers:
                answer += f"- {caller}\n"

        else:

            answer += "None\n"

        answer += "\nCalls:\n"

        if calls:

            for call in calls:
                answer += f"- {call}\n"

        else:

            answer += "None\n"

        return answer