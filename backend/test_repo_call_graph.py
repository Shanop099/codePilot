from pathlib import Path

from app.analysis.ast_parser import ASTParser
from app.analysis.call_graph import CallGraph
from app.ingestion.file_scanner import FileScanner


scanner = FileScanner()

files = scanner.scan_repository(
    "repositories/flask"
)

parser = ASTParser()

graph = CallGraph()

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

        call_graph = parser.extract_call_graph(
            tree,
            content
        )

        graph.add_call_graph(
            call_graph
        )

    except Exception:
        pass


print(
    graph.get_called_functions(
        "__init__"
    )
)