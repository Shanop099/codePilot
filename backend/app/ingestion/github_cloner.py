from pathlib import Path

from git import Repo


class GitHubCloner:

    def clone_repository(
        self,
        repo_url
    ):

        repo_name = (
            repo_url
            .rstrip("/")
            .split("/")[-1]
        )

        target_path = (
            Path("repositories")
            / repo_name
        )

        if target_path.exists():

            print(
                f"Repository already exists: {target_path}"
            )

            return str(
                target_path
            )

        Repo.clone_from(
            repo_url,
            str(target_path)
        )

        print(
            f"Repository cloned to: {target_path}"
        )

        return str(
            target_path
        )