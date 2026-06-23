import networkx as nx


class CallGraph:

    def __init__(self):

        self.graph = nx.DiGraph()

    def add_call_graph(
        self,
        call_graph
    ):

        for source_function, called_functions in call_graph.items():

            self.graph.add_node(
                source_function
            )

            for called_function in called_functions:
                

                self.graph.add_edge(
                    source_function,
                    called_function
                )

    def get_called_functions(
        self,
        function_name
    ):

        if function_name not in self.graph:
            return []

        return list(
            self.graph.successors(
                function_name
            )
        )

    def get_callers(
        self,
        function_name
    ):

        if function_name not in self.graph:
            return []

        return list(
            self.graph.predecessors(
                function_name
            )
        )

    def trace_execution(
        self,
        start_function,
        max_depth=3
    ):

        visited = set()

        path = []

        def dfs(
            function_name,
            depth
        ):

            if depth > max_depth:
                return

            if function_name in visited:
                return

            visited.add(
                function_name
            )

            path.append(
                function_name
            )

            for called_function in self.graph.successors(
                function_name
            ):

                dfs(
                    called_function,
                    depth + 1
                )

        dfs(
            start_function,
            0
        )

        return path
    def set_valid_symbols(
            self,
            valid_symbols
        ):
            self.valid_symbols = valid_symbols
        
    def impact_analysis(
        self,
        target_function,
        max_depth=5
    ):  
        impacted = set()
             
        def dfs(
            function_name,
            depth
        ):

            if depth > max_depth:
                return

            callers = self.get_callers(
                function_name
            )

            for caller in callers:
                if caller == target_function:
                    continue
                if caller not in impacted:

                    impacted.add(
                        caller
                    )

                    dfs(
                        caller,
                        depth + 1
                    )

        dfs(
            target_function,
            0
        )

        return list(
            impacted
        )