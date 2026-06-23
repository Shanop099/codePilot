from pathlib import Path


class FileScanner:

    ALLOWED_EXTENSIONS = {
        ".py",
        ".js",
        ".ts",
        ".tsx",
        ".jsx"
    }

    IGNORED_DIRECTORIES = {
            "tests",
            "test",
            "__pycache__",
            ".git",
            "node_modules",
            "venv",
            "dist",
            "build"
        }

    def scan_repository(self, repository_path: str):

        repository = Path(repository_path)

        code_files = []

        for file_path in repository.rglob("*"):

            if not file_path.is_file():
                continue

            if any(
                ignored in file_path.parts
                for ignored in self.IGNORED_DIRECTORIES
            ):
                continue

            if file_path.suffix in self.ALLOWED_EXTENSIONS:

                code_files.append(
                    str(file_path)
                )

        return code_files