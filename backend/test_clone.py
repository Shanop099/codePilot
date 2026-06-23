from app.ingestion.github_loader import GitHubLoader

loader = GitHubLoader()

result = loader.clone_repository(
    "https://github.com/vercel/next.js"
)

print(result)