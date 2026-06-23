from pathlib import Path
from langchain_text_splitters import RecursiveCharacterTextSplitter


class Chunker:

    def __init__(self):

        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=800,
            chunk_overlap=150
        )

    def chunk_files(self, file_paths):

        chunks = []

        for file_path in file_paths:

            try:

                content = Path(file_path).read_text(
                    encoding="utf-8"
                )

                split_chunks = self.splitter.split_text(
                    content
                )

                for idx, chunk in enumerate(split_chunks):

                    chunks.append(
                        {
                            "file_path": file_path,
                            "chunk_id": idx,
                            "content": chunk
                        }
                    )

            except Exception as e:

                print(
                    f"Failed reading {file_path}: {e}"
                )

        return chunks