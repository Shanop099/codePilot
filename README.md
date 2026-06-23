# 🤖 CodePilot AI

AI-powered Repository Intelligence Platform that helps developers understand, review, analyze, and navigate large codebases using LLMs, AST parsing, dependency analysis, and Retrieval-Augmented Generation (RAG).

---

## 🚀 Features

### Architecture Analysis

Understand how a component fits into the overall repository architecture.

Example:

```text
Explain architecture of add_url_rule
```

---

### Dependency Analysis

Analyze incoming and outgoing dependencies.

Example:

```text
Show dependencies of add_url_rule
```

---

### Impact Analysis

Identify what may break if a function or class is modified.

Example:

```text
What breaks if I modify add_url_rule?
```

---

### Execution Tracing

Trace function execution flow across the repository.

Example:

```text
Trace execution from route
```

---

### Multi-Agent Code Review

Combines multiple specialized agents to generate repository-aware code reviews.

Includes:

* Architecture Review
* Dependency Review
* Impact Analysis
* Repository Review

Example:

```text
Review add_url_rule
```

---

### Bug Localization

Locate likely root causes for repository issues using semantic search and dependency analysis.

Example:

```text
add_url_rule not registering routes
```

---

### Refactoring Suggestions

Detect maintainability issues and generate refactoring recommendations.

Example:

```text
Refactor add_url_rule
```

---

### Repository Health Report

Generate repository-wide insights including:

* Repository statistics
* Architectural hotspots
* Technical debt candidates
* High-coupling components
* Largest files
* Overall health assessment

Example:

```text
Repository health report
```

---

### RAG-Based Repository Q&A

Ask natural language questions about the repository.

Examples:

```text
Summarize repository
How does Flask routing work?
What is Blueprint?
```

---

### Interactive Dependency Graphs

Visualize function relationships and call graphs.

Example:

```text
Generate graph for add_url_rule
```

---

### Export Reports

Export generated analyses and reviews as downloadable reports.

---

## 🏗️ Architecture

```text
User
 │
 ▼
Streamlit UI
 │
 ▼
FastAPI Backend
 │
 ├── Architecture Agent
 ├── Dependency Agent
 ├── Impact Agent
 ├── Execution Agent
 ├── Repository Review Agent
 ├── Bug Localization Agent
 ├── Refactor Agent
 ├── Repository Health Agent
 │
 ▼
Repository Manager
 │
 ├── AST Parser
 ├── Symbol Index
 ├── Call Graph Builder
 ├── Vector Store (Qdrant)
 └── Embedding Generator
```

---

## 🛠️ Tech Stack

### Backend

* FastAPI
* Python

### AI & Retrieval

* Groq API
* Llama 3.3 70B
* Sentence Transformers
* Qdrant Vector Database

### Static Analysis

* AST Parsing
* Symbol Indexing
* Call Graph Analysis

### Frontend

* Streamlit

### Visualization

* PyVis
* NetworkX

---

## 📂 Project Structure

```text
CodePilotAI/
│
├── app/
│   ├── agents/
│   ├── analysis/
│   ├── ingestion/
│   ├── retrieval/
│   ├── services/
│   └── visualization/
│
├── main.py
├── streamlit.py
├── requirements.txt
└── README.md
```

---

## ⚙️ Installation

Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/CodePilotAI.git
cd CodePilotAI
```

Create virtual environment:

```bash
python -m venv venv
```

Activate:

### Windows

```bash
venv\Scripts\activate
```

### Linux / Mac

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## 🔑 Environment Variables

Create a `.env` file:

```env
GROQ_API_KEY=your_groq_api_key
```

---

## ▶️ Run Backend

```bash
uvicorn main:app --reload
```

Backend API:

```text
http://127.0.0.1:8000
```

Swagger Docs:

```text
http://127.0.0.1:8000/docs
```

---

## ▶️ Run Frontend

```bash
streamlit run streamlit.py
```

---

## 🎯 Future Improvements

* Multi-repository analysis
* Pull request review automation
* CI/CD integration
* GitHub App integration
* Security vulnerability analysis
* Code quality scoring
* Repository comparison engine

---

## 👨‍💻 Author

**Ishan Gupta**

B.Tech CSE, IIIT Nagpur

GitHub:
https://github.com/Shanop099
