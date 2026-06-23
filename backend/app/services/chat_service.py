import re
from pathlib import Path
from typing import Dict, Any, Optional

from groq import Groq

from app.config import GROQ_API_KEY
from app.retrieval.embeddings import EmbeddingGenerator
from app.retrieval.vector_store import VectorStore
from app.analysis.symbol_index import SymbolIndex
from app.analysis.call_graph import CallGraph
from app.analysis.ast_parser import ASTParser
from app.ingestion.file_scanner import FileScanner
from app.agents.architecture_agent import ArchitectureAgent
from app.agents.impact_agent import (
    ImpactAgent
)
from app.agents.execution_agent import (
    ExecutionAgent
)
from app.agents.rag_agent import (
    RAGAgent
)
from app.agents.repository_review_agent import (
    RepositoryReviewAgent
)
from app.agents.dependency_agent import (
    DependencyAgent
)
from app.agents.bug_localization_agent import (
    BugLocalizationAgent
)
from app.agents.multi_review_agent import (
    MultiReviewAgent
)
from app.utils.code_extractor import (
    CodeExtractor
)
from app.core.repository_manager import (
    RepositoryManager
)
from app.ingestion.github_cloner import (
    GitHubCloner
)
from app.agents.refactor_agent import (
    RefactorAgent
)
from app.agents.repository_health_agent import (
    RepositoryHealthAgent
)

class ChatService:
    def __init__(self) -> None:
        self.embedder = EmbeddingGenerator()
        self.vector_store = VectorStore()
        
        self.client = Groq(api_key=GROQ_API_KEY)

        
        self.repository_manager = (
    RepositoryManager()
)

        (
            files,
            self.symbol_index,
            self.call_graph
        ) = (
            self.repository_manager
            .load_repository(
                "repositories/flask"
            )
        )
        self.current_repository = (
    "repositories/flask"
)
        self.architecture_agent = ArchitectureAgent(self.call_graph)
        self.impact_agent = ImpactAgent(self.call_graph)
        self.execution_agent = (
    ExecutionAgent(
        self.call_graph
    ))
        self.rag_agent = (
    RAGAgent(
        self.embedder,
        self.vector_store
    )
)
        self.repository_health_agent = (
    RepositoryHealthAgent(
        self.symbol_index,
        self.call_graph,
        self.current_repository
    )
)
        self.github_cloner = (
    GitHubCloner()
)
        self.repository_review_agent = (
    RepositoryReviewAgent(
        self.call_graph
    )
)
        self.dependency_agent = (
        DependencyAgent(
            self.call_graph
        )
    )
        self.bug_localization_agent = (
        BugLocalizationAgent(   
        self.vector_store,
         self.embedder,
           self.call_graph
        )
    )
        self.multi_review_agent = (
    MultiReviewAgent(
        self.architecture_agent,
        self.dependency_agent,
        self.impact_agent,
        self.repository_review_agent
    )
)
        self.refactor_agent = RefactorAgent()
        
    def load_github_repository(
        self,
        repo_url
    ):

        repo_path = (
            self.github_cloner
            .clone_repository(
                repo_url
            )
        )

        return self.load_repository(
            repo_path
        )
    def load_repository(
    self,
    repo_path
):

        (
            files,
            self.symbol_index,
            self.call_graph
        ) = (
            self.repository_manager
            .load_repository(
                repo_path
            )
        )
        self.current_repository = (
    repo_path
)
        self.architecture_agent = (
            ArchitectureAgent(
                self.call_graph
            )
        )

        self.impact_agent = (
            ImpactAgent(
                self.call_graph
            )
        )

        self.execution_agent = (
            ExecutionAgent(
                self.call_graph
            )
        )

        self.dependency_agent = (
            DependencyAgent(
                self.call_graph
            )
        )
        self.repository_review_agent = (
    RepositoryReviewAgent(
        self.call_graph
    )
    )   
        self.multi_review_agent = (
        MultiReviewAgent(
            self.architecture_agent,
            self.dependency_agent,
            self.impact_agent,
            self.repository_review_agent
        )
    )
        self.repository_health_agent = (
    RepositoryHealthAgent(
        self.symbol_index,
        self.call_graph,
        self.current_repository
    )
)
        self.bug_localization_agent.call_graph = (
            self.call_graph
        )

        return {
            "status": "success",
            "repository": repo_path,
            "files_indexed": len(files)
        }
    def generate_response(self, prompt: str) -> str:
        try:
            response = self.client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}]
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error generating response: {e}")
            return "An error occurred while generating the response."

    def detect_intent(self, query: str) -> str:
        query = query.lower()

        if any(keyword in query for keyword in [
            "break", "impact", "affected", "affect"
        ]):
            return "impact"
            
        if any(word in query for word in [
            "architecture", "design", "workflow", "structure"
        ]):
            return "architecture"
            
        if any(keyword in query for keyword in [
            "trace", "execution", "flow"
        ]):
            return "trace"
        if any(
            keyword in query
            for keyword in [
                "review",
                "audit",
                "analyze code"
            ]
        ):
            return "review"
        if any(
            keyword in query
            for keyword in [
                "dependency",
                "dependencies",
                "depends on",
                "dependencies of",
                "dependency of"
            ]
        ):
            return "dependency"
        if any(
            keyword in query
            for keyword in [
                "refactor",
                "improve code",
                "clean up"
            ]
        ):
            return "refactor"
        if any(keyword in query for keyword in [
              "bug",
        "issue",
        "error",
        "fix",
        "failure",
        "fails",
        "failing",
        "not working",
        "not registering",
        "crash",
        "broken"
        ]):
            return "bug"
        if any(
            keyword in query
            for keyword in [
                "repository health",
                "health report",
                "analyze repository",
                "repository statistics"
            ]
        ):
            return "health"
        return "default"

    def lookup_symbol(self, query: str) -> Optional[Dict[str, str]]:
        symbols = re.findall(r"[A-Za-z_][A-Za-z0-9_]*", query)

        for symbol in symbols:
            function_file = self.symbol_index.find_function(symbol)
            if function_file:
                return {
                    "type": "function",
                    "symbol": symbol,
                    "file": function_file
                }

            class_file = self.symbol_index.find_class(symbol)
            if class_file:
                return {
                    "type": "class",
                    "symbol": symbol,
                    "file": class_file
                }

        return None

    def ask(self, query: str) -> Dict[str, Any]:
        intent = self.detect_intent(query)
        symbol_result = self.lookup_symbol(query)

        if intent == "architecture":
            if symbol_result:
                try:
                    file_content = Path(symbol_result["file"]).read_text(encoding="utf-8")[:4000]
                except Exception as e:
                    print(f"Error reading file for architecture: {e}")
                    file_content = ""

                return {
                    "answer": self.architecture_agent.explain(
                        symbol_result["symbol"],
                        file_content
                    ),
                    "sources": [symbol_result["file"]],
                    "retrieval_type": "architecture"
                }
            return {
                "answer": "No matching repository symbol was found for architecture analysis.",
                "sources": [],
                "retrieval_type": "architecture"
            }

        


        if intent == "impact":

            if symbol_result:

                result = (
                    self.impact_agent.analyze(
                        symbol_result["symbol"]
                    )
                )

                return {
                    "answer": result,
                    "sources": [
                        symbol_result["file"]
                    ],
                    "retrieval_type":
                    "impact_analysis"
                }
            
        if intent == "trace":

            if symbol_result:

                result = (
                    self.execution_agent.analyze(
                        symbol_result["symbol"]
                    )
                )

                return {
                    "answer": result,
                    "sources": [
                        symbol_result["file"]
                    ],
                    "retrieval_type":
                    "execution_trace"
                }
        if intent == "health":

            result = (
                self.repository_health_agent
                .analyze()
            )

            return {
                "answer": result,
                "sources": [],
                "retrieval_type":
                "repository_health"
            }    
        if intent == "dependency":

            if symbol_result:

                result = (
                    self.dependency_agent.analyze(
                        symbol_result["symbol"]
                    )
                )

                return {
                    "answer": result,
                    "sources": [
                        symbol_result["file"]
                    ],
                    "retrieval_type":
                    "dependency_analysis"
                }    
        if intent == "bug":

            result = (
                self.bug_localization_agent.analyze(
                    query
                )
            )

            return {
                "answer": result,
                "sources": [],
                "retrieval_type":
                "bug_localization"
            }    
       
        if intent == "refactor":

         if symbol_result:

            file_content = Path(
                symbol_result["file"]
            ).read_text(
                encoding="utf-8"
            )

            function_code = (
                CodeExtractor.get_function_code(
                    file_content,
                    symbol_result["symbol"]
                )
            )

            result = (
                self.refactor_agent.analyze(
                    symbol_result["symbol"],
                    function_code or file_content
                )
            )

            return {
                "answer": result,
                "sources": [
                    symbol_result["file"]
                ],
                "retrieval_type":
                "refactor_review"
            }
        if intent == "review":

            if symbol_result:

                try:

                    file_content = Path(
    symbol_result["file"]
).read_text(
    encoding="utf-8"
)

                    function_code = (
                                    CodeExtractor.get_function_code(
                                        file_content,
                                        symbol_result["symbol"]
                                    )
                                )

                    if function_code:

                                    file_content = function_code

                except Exception:

                    file_content = ""

                review = (
                    self.multi_review_agent.review(
                        symbol_result["symbol"],
                        file_content
                    )
                )

                return {
                    "answer": review,
                    "sources": [
                        symbol_result["file"]
                    ],
                    "retrieval_type":
                    "multi_agent_review"
                }
            
        if (
    symbol_result
    and intent == "default"
    and len(query.split()) <= 4
):
            try:
                file_content = Path(symbol_result["file"]).read_text(encoding="utf-8")[:4000]
            except Exception as e:
                print(f"Error reading file for symbol retrieval: {e}")
                file_content = ""

            prompt = f"""
You are CodePilot AI.

Use ONLY the code provided below. Do not invent functionality. Explain only visible behavior.

Symbol Type: {symbol_result['type']}
Symbol Name: {symbol_result['symbol']}
File: {symbol_result['file']}

Code:
{file_content}

Rules:
- Do not invent information.
- Only explain what is visible in the code.
- If something is unclear, say so.

Response Format:

Summary:
<what this symbol is>

Responsibilities:
- item
- item

Answer:
<detailed explanation>
"""

            answer = self.generate_response(prompt)

            return {
                "answer": answer,
                "sources": [symbol_result["file"]],
                "retrieval_type": "symbol"
            }

      

        result = self.rag_agent.answer(
        query
    )

        return {
            "answer": result["answer"],
            "sources": result["sources"],
            "retrieval_type": "rag"
        }
    
    def close(self) -> None:
        try:
            self.vector_store.client.close()
        except Exception as e:
            print(f"Error closing vector store client: {e}")