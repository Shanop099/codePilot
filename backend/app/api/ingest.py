from fastapi import APIRouter
from pydantic import BaseModel

from app.ingestion.github_loader import GitHubLoader

router = APIRouter()

loader = GitHubLoader()


class RepositoryRequest(BaseModel):
    repo_url: str


@router.post("/ingest")
def ingest_repository(request: RepositoryRequest):

    result = loader.clone_repository(
        request.repo_url
    )

    return result