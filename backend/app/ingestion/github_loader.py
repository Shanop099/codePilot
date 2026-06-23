from git import Repo
from pathlib import Path


class GitHubLoader:

    def __init__(self):
        self.repositories_dir = Path("repositories")
        self.repositories_dir.mkdir(exist_ok=True)

    def clone_repository(self, repo_url: str):

        print(f"Cloning repository: {repo_url}")

        repo_name = repo_url.split("/")[-1]

        if repo_name.endswith(".git"):
            repo_name = repo_name[:-4]

        destination = self.repositories_dir / repo_name

        if destination.exists():
            return {
                "status": "already_exists",
                "path": str(destination)
            }

        Repo.clone_from(repo_url, destination)

        print("Clone completed")

        return {
            "status": "success",
            "path": str(destination)
        }