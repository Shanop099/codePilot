class RouterAgent:

    def route(
        self,
        query: str
    ) -> str:

        query = query.lower()

        if any(
            keyword in query
            for keyword in [
                "impact",
                "break",
                "affected",
                "affect",
                "dependency",
                "dependencies"
            ]
        ):
            return "impact"

        if any(
            keyword in query
            for keyword in [
                "trace",
                "execution",
                "flow"
            ]
        ):
            return "trace"

        if any(
            keyword in query
            for keyword in [
                "architecture",
                "design",
                "workflow",
                "structure"
            ]
        ):
            return "architecture"

        return "default"