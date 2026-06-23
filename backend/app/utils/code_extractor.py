import ast


class CodeExtractor:

    @staticmethod
    def get_function_code(
        file_content,
        function_name
    ):

        try:

            tree = ast.parse(
                file_content
            )

            for node in ast.walk(tree):

                if (
                    isinstance(
                        node,
                        ast.FunctionDef
                    )
                    and node.name
                    == function_name
                ):

                    start = node.lineno - 1

                    end = (
                        node.end_lineno
                    )

                    lines = (
                        file_content.splitlines()
                    )

                    return "\n".join(
                        lines[start:end]
                    )

        except Exception:

            pass

        return None