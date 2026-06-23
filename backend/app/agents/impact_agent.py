class ImpactAgent:

    def __init__(
        self,
        call_graph
    ):

        self.call_graph = call_graph

    def analyze(
        self,
        function_name
    ):

        impacted = (
            self.call_graph.impact_analysis(
                function_name
            )
        )

        if not impacted:
            return f"No impacted functions found for '{function_name}'."

        impacted = impacted[:20]

        answer = (
            f"Impact Analysis for '{function_name}'\n\n"
        )

        answer += "Potentially Affected Functions:\n"

        for func in impacted:
            answer += f"- {func}\n"

        if len(impacted) >= 20:
            answer += "\n...additional dependencies omitted"

        return answer