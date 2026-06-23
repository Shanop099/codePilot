import streamlit as st
import streamlit.components.v1 as components
import requests

st.set_page_config(
    page_title="CodePilot AI",
    page_icon="🤖",
    layout="wide"
)

# ====================================
# SESSION STATE
# ====================================

if "last_answer" not in st.session_state:
    st.session_state["last_answer"] = ""

if "last_retrieval_type" not in st.session_state:
    st.session_state["last_retrieval_type"] = "report"

if "repo_name" not in st.session_state:
    st.session_state["repo_name"] = "No Repository"

if "files_indexed" not in st.session_state:
    st.session_state["files_indexed"] = 0

# ====================================
# HEADER
# ====================================

st.title("🤖 CodePilot AI")
st.caption(
    "AI-Powered Repository Intelligence Platform"
)

# ====================================
# METRICS
# ====================================

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Repository",
        st.session_state["repo_name"]
    )

with col2:
    st.metric(
        "Files Indexed",
        st.session_state["files_indexed"]
    )

with col3:
    st.metric(
        "Status",
        "Ready"
    )

st.divider()

# ====================================
# TABS
# ====================================

tab1, tab2, tab3 = st.tabs(
    [
        "📦 Repository",
        "🤖 Analysis",
        "📈 Graph"
    ]
)

# ====================================
# REPOSITORY TAB
# ====================================

with tab1:

    st.subheader(
        "Load GitHub Repository"
    )

    repo_url = st.text_input(
        "GitHub Repository URL",
        placeholder=
        "https://github.com/pallets/flask"
    )

    if st.button(
        "Load Repository"
    ):

        if not repo_url.strip():

            st.error(
                "Please enter a repository URL."
            )

        else:

            with st.spinner(
                "Cloning and indexing repository..."
            ):

                try:

                    response = requests.post(
                        "http://127.0.0.1:8000/load-github-repository",
                        json={
                            "repo_url":
                            repo_url
                        }
                    )

                    if response.status_code == 200:

                        result = (
                            response.json()
                        )

                        st.session_state[
                            "repo_name"
                        ] = result.get(
                            "repository",
                            "Unknown"
                        )

                        st.session_state[
                            "files_indexed"
                        ] = result.get(
                            "files_indexed",
                            0
                        )

                        st.success(
                            "Repository loaded successfully."
                        )

                        st.json(
                            result
                        )

                    else:

                        st.error(
                            response.text
                        )

                except Exception as e:

                    st.error(
                        str(e)
                    )

# ====================================
# ANALYSIS TAB
# ====================================

with tab2:

    st.subheader(
        "Ask About Repository"
    )

    query = st.text_area(
        "Ask a question",
        height=200,
        placeholder="""
Examples:

What is Flask?

Review add_url_rule

Repository health

Refactor add_url_rule

Show dependencies of add_url_rule

Trace execution from route

What breaks if I modify add_url_rule?

Bug: route decorator not registering endpoint
"""
    )

    if st.button(
        "Ask"
    ):

        if not query.strip():

            st.warning(
                "Enter a question."
            )

        else:

            with st.spinner(
                "Analyzing repository..."
            ):

                try:

                    response = requests.post(
                        "http://127.0.0.1:8000/chat",
                        json={
                            "query":
                            query
                        }
                    )

                    if response.status_code != 200:

                        st.error(
                            response.text
                        )

                    else:

                        result = (
                            response.json()
                        )

                        st.session_state[
                            "last_answer"
                        ] = result.get(
                            "answer",
                            ""
                        )

                        st.session_state[
                            "last_retrieval_type"
                        ] = result.get(
                            "retrieval_type",
                            "report"
                        )

                        st.subheader(
                            "Retrieval Type"
                        )

                        st.code(
                            result.get(
                                "retrieval_type",
                                "unknown"
                            )
                        )

                        st.subheader(
                            "Sources"
                        )

                        sources = result.get(
                            "sources",
                            []
                        )

                        if sources:

                            for source in sources:

                                st.write(
                                    f"📄 {source}"
                                )

                        else:

                            st.write(
                                "No sources found."
                            )

                        st.subheader(
                            "Answer"
                        )

                        st.markdown(
                            result.get(
                                "answer",
                                "No answer returned."
                            )
                        )

                except Exception as e:

                    st.error(
                        str(e)
                    )

    # ==============================
    # DOWNLOAD REPORT
    # ==============================

    if st.session_state[
        "last_answer"
    ]:

        st.divider()

        st.download_button(
            label=
            "⬇️ Download Report",
            data=
            st.session_state[
                "last_answer"
            ],
            file_name=
            f"{st.session_state['last_retrieval_type']}.md",
            mime=
            "text/markdown"
        )

# ====================================
# GRAPH TAB
# ====================================

with tab3:

    st.subheader(
        "Dependency Graph"
    )

    graph_function = st.text_input(
        "Function Name",
        placeholder="add_url_rule"
    )

    if st.button(
        "Generate Graph"
    ):

        if not graph_function.strip():

            st.warning(
                "Enter a function name."
            )

        else:

            with st.spinner(
                "Generating graph..."
            ):

                try:

                    response = requests.post(
                        "http://127.0.0.1:8000/graph",
                        json={
                            "function_name":
                            graph_function
                        }
                    )

                    if response.status_code == 200:

                        result = (
                            response.json()
                        )

                        if result.get(
                            "success",
                            False
                        ):

                            st.success(
                                "Graph Generated"
                            )

                            try:

                                with open(
                                    "graph.html",
                                    "r",
                                    encoding="utf-8"
                                ) as f:

                                    graph_html = (
                                        f.read()
                                    )

                                components.html(
                                    graph_html,
                                    height=800,
                                    scrolling=True
                                )

                            except Exception as e:

                                st.error(
                                    f"Could not display graph: {str(e)}"
                                )

                        else:

                            st.error(
                                result.get(
                                    "error",
                                    "Unknown error"
                                )
                            )

                    else:

                        st.error(
                            response.text
                        )

                except Exception as e:

                    st.error(
                        str(e)
                    )