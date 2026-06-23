from app.ingestion.file_scanner import FileScanner
from app.analysis.symbol_index import SymbolIndex
from app.analysis.call_graph import CallGraph
from app.analysis.ast_parser import ASTParser
from pathlib import Path


class RepositoryManager:

    def load_repository(
        self,
        repo_path
    ):

        scanner = FileScanner()

        files = scanner.scan_repository(
            repo_path
        )

        symbol_index = SymbolIndex()
        symbol_index.build(files)

        call_graph = CallGraph()

        parser = ASTParser()

        for file_path in files:

            try:

                content = Path(
                    file_path
                ).read_text(
                    encoding="utf-8"
                )

                tree = parser.parse_file(
                    content
                )

                graph = (
                    parser.extract_call_graph(
                        tree,
                        content
                    )
                )

                call_graph.add_call_graph(
                    graph
                )

            except Exception:

                pass

        return (
            files,
            symbol_index,
            call_graph
        )