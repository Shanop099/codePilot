from pathlib import Path

from app.analysis.ast_parser import ASTParser


class CodeIndexer:

    def __init__(self):

        self.parser = ASTParser()

    def index_file(
        self,
        file_path: str
    ):

        try:

            content = Path(
                file_path
            ).read_text(
                encoding="utf-8"
            )

            tree = self.parser.parse_file(
                content
            )

            functions = self.parser.extract_functions(
                tree,
                content
            )

            classes = self.parser.extract_classes(
                tree,
                content
            )

            imports = self.parser.extract_imports(
                tree,
                content
            )

            return {
                "file_path": file_path,
                "functions": functions,
                "classes": classes,
                "imports": imports
            }

        except Exception as e:

            print(
                f"Failed indexing {file_path}: {e}"
            )

            return None