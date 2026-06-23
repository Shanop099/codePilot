import networkx as nx


class DependencyGraph:

    def __init__(self):

        self.graph = nx.DiGraph()

    def add_file(
        self,
        file_path,
        imports
    ):

        self.graph.add_node(file_path)

        for imp in imports:

            self.graph.add_edge(
                file_path,
                imp
            )

    def get_dependencies(
        self,
        file_path
    ):

        return list(
            self.graph.successors(
                file_path
            )
        )