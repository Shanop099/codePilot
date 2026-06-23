from pyvis.network import Network


class GraphVisualizer:

    def __init__(
        self,
        call_graph
    ):
        self.call_graph = call_graph

    def build_graph(
        self,
        function_name,
        output_file="graph.html"
    ):

        net = Network(
            height="700px",
            width="100%",
            directed=True
        )

        net.add_node(
            function_name,
            color="red"
        )

        callers = (
            self.call_graph.get_callers(
                function_name
            )
        )

        callees = (
            self.call_graph.get_called_functions(
                function_name
            )
        )

        for caller in callers:

            net.add_node(
                caller
            )

            net.add_edge(
                caller,
                function_name
            )

        for callee in callees:

            net.add_node(
                callee
            )

            net.add_edge(
                function_name,
                callee
            )

        net.save_graph(
            output_file
        )

        return output_file