from pathlib import Path

from app.analysis.code_indexer import CodeIndexer


class SymbolIndex:

    def __init__(self):

        self.indexer = CodeIndexer()

        self.function_index = {}
        self.class_index = {}

    def build(
        self,
        file_paths
    ):

        for file_path in file_paths:

            result = self.indexer.index_file(
                file_path
            )

            if not result:
                continue

            for function in result["functions"]:

                self.function_index[
                    function
                ] = file_path

            for cls in result["classes"]:

                self.class_index[
                    cls
                ] = file_path

    def find_function(
        self,
        function_name
    ):

        return self.function_index.get(
            function_name
        )

    def find_class(
        self,
        class_name
    ):

        return self.class_index.get(
            class_name
        )