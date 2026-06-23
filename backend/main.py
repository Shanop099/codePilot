from fastapi import FastAPI
from pydantic import BaseModel

from app.api.ingest import (
    router as ingest_router
)

from app.services.chat_service import (
    ChatService
)

from app.visualization.graph_visualizer import (
    GraphVisualizer
)

from app.agents.report_generator import (
    ReportGenerator
)


app = FastAPI(
    title="CodePilot AI"
)

app.include_router(
    ingest_router
)

chat = ChatService()


class ChatRequest(
    BaseModel
):
    query: str


class GitHubRepositoryRequest(
    BaseModel
):
    repo_url: str


class GraphRequest(
    BaseModel
):
    function_name: str


class ReportRequest(
    BaseModel
):
    title: str
    content: str


@app.get("/")
def home():

    return {
        "message":
        "CodePilot AI Backend Running"
    }


@app.post("/chat")
def chat_endpoint(
    request: ChatRequest
):

    return chat.ask(
        request.query
    )


@app.post(
    "/load-github-repository"
)
def load_github_repository(
    request: GitHubRepositoryRequest
):

    return (
        chat
        .load_github_repository(
            request.repo_url
        )
    )


@app.post(
    "/export-report"
)
def export_report(
    request: ReportRequest
):

    file_path = (
        ReportGenerator
        .export_report(
            request.title,
            request.content
        )
    )

    return {
        "success": True,
        "file": file_path
    }


@app.post("/graph")
def graph_endpoint(
    request: GraphRequest
):

    try:

        visualizer = (
            GraphVisualizer(
                chat.call_graph
            )
        )

        graph_file = (
            visualizer.build_graph(
                request.function_name
            )
        )

        return {
            "success": True,
            "graph_file": graph_file
        }

    except Exception as e:

        return {
            "success": False,
            "error": str(e)
        }