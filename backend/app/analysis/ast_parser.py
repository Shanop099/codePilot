from tree_sitter import Language, Parser
import tree_sitter_python


class ASTParser:

    def __init__(self):

        PY_LANGUAGE = Language(
            tree_sitter_python.language()
        )

        self.parser = Parser(PY_LANGUAGE)

    def parse_file(self, content):

        return self.parser.parse(
            bytes(content, "utf-8")
        )

    def extract_functions(
        self,
        tree,
        source_code
    ):

        functions = []

        def traverse(node):

            if node.type == "function_definition":

                name_node = node.child_by_field_name(
                    "name"
                )

                if name_node:

                    function_name = source_code[
                        name_node.start_byte:
                        name_node.end_byte
                    ]

                    functions.append(
                        function_name
                    )

            for child in node.children:
                traverse(child)

        traverse(tree.root_node)

        return functions

    def extract_classes(
        self,
        tree,
        source_code
    ):

        classes = []

        def traverse(node):

            if node.type == "class_definition":

                name_node = node.child_by_field_name(
                    "name"
                )

                if name_node:

                    class_name = source_code[
                        name_node.start_byte:
                        name_node.end_byte
                    ]

                    classes.append(
                        class_name
                    )

            for child in node.children:
                traverse(child)

        traverse(tree.root_node)

        return classes

    def extract_imports(
        self,
        tree,
        source_code
    ):

        imports = []

        def traverse(node):

            if node.type in [
                "import_statement",
                "import_from_statement"
            ]:

                import_text = source_code[
                    node.start_byte:
                    node.end_byte
                ]

                imports.append(
                    import_text
                )

            for child in node.children:
                traverse(child)

        traverse(tree.root_node)

        return imports
    
    def extract_function_calls(
        self,
        tree,
        source_code
    ):

        calls = []

        def traverse(node):

            if node.type == "call":

                function_node = node.child_by_field_name(
                    "function"
                )

                if function_node:

                    function_name = source_code[
                        function_node.start_byte:
                        function_node.end_byte
                    ]
                    if "." in function_name:
                        function_name = (
                            function_name.split(".")[-1]
                        )

                    calls.append(
                        function_name
                    )

            for child in node.children:
                traverse(child)

        traverse(tree.root_node)

        return calls
    
    def extract_call_graph(
        self,
        tree,
        source_code
    ):

        call_graph = {}

        def get_function_name(node):

            name_node = node.child_by_field_name(
                "name"
            )

            if name_node:

                return source_code[
                    name_node.start_byte:
                    name_node.end_byte
                ]

            return None

        def collect_calls(node):

            calls = []

            def traverse(current):

                if current.type == "call":

                    function_node = (
                        current.child_by_field_name(
                            "function"
                        )
                    )

                    if function_node:

                        function_name = source_code[
                            function_node.start_byte:
                            function_node.end_byte
                        ]
                        if "." in function_name:
                            function_name = (
                                function_name.split(".")[-1]
                            )
                        calls.append(
                            function_name
                        )

                for child in current.children:
                    traverse(child)

            traverse(node)

            return calls

        def traverse(node):

            if node.type == "function_definition":

                function_name = get_function_name(
                    node
                )

                if function_name:

                    call_graph[
                        function_name
                    ] = collect_calls(
                        node
                    )

            for child in node.children:
                traverse(child)

        traverse(tree.root_node)

        return call_graph