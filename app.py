import streamlit as st

from backend.repository import clone_repository
from backend.loader import load_repository_files
from backend.chunker import chunk_documents
from backend.vectorstore import create_vector_store
from backend.rag import ask_repository
from backend.analyzer import analyze_repository


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="RepoMind AI",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# SESSION STATE
# ============================================================

if "vector_store" not in st.session_state:
    st.session_state.vector_store = None

if "repo_loaded" not in st.session_state:
    st.session_state.repo_loaded = False

if "repo_url" not in st.session_state:
    st.session_state.repo_url = ""

if "repo_stats" not in st.session_state:
    st.session_state.repo_stats = None

if "messages" not in st.session_state:
    st.session_state.messages = []

if "repository_summary" not in st.session_state:
    st.session_state.repository_summary = ""


# ============================================================
# PROFESSIONAL UI CSS
# ============================================================

st.markdown(
"""
<style>

/* ============================================================
   GLOBAL
   ============================================================ */

.stApp {
    background: #F7F8FC;
    color: #172033;
}

.block-container {
    max-width: 1250px;
    padding-top: 1.5rem;
    padding-bottom: 4rem;
}


/* ============================================================
   SIDEBAR
   ============================================================ */

[data-testid="stSidebar"] {
    background: #FFFFFF;
    border-right: 1px solid #E5E7EB;
}

[data-testid="stSidebar"] > div:first-child {
    padding-top: 1rem;
}

[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    color: #172033 !important;
}

[data-testid="stSidebar"] p,
[data-testid="stSidebar"] label {
    color: #4B5563;
}


/* ============================================================
   HEADER
   ============================================================ */

.repomind-header {
    text-align: center;
    padding: 5px 0 28px 0;
}

.repomind-logo {
    font-size: 48px;
    line-height: 1;
    margin-bottom: 8px;
}

.repomind-title {
    font-size: 42px;
    font-weight: 800;
    letter-spacing: -1px;
    color: #172033;
    margin: 0;
}

.repomind-subtitle {
    margin-top: 8px;
    font-size: 16px;
    color: #6B7280;
}

.repomind-badge {
    display: inline-block;
    margin-top: 14px;
    padding: 6px 13px;
    border-radius: 999px;
    background: #EEF4FF;
    color: #2563EB;
    font-size: 12px;
    font-weight: 700;
}


/* ============================================================
   HERO
   ============================================================ */

.hero-card {
    background: #FFFFFF;
    border: 1px solid #E5E7EB;
    border-radius: 20px;
    padding: 38px 30px;
    text-align: center;
    box-shadow: 0 8px 30px rgba(15, 23, 42, 0.06);
    margin-bottom: 22px;
}

.hero-icon {
    font-size: 48px;
    margin-bottom: 8px;
}

.hero-title {
    font-size: 30px;
    font-weight: 800;
    color: #172033;
    margin-bottom: 10px;
}

.hero-text {
    max-width: 700px;
    margin: auto;
    color: #6B7280;
    font-size: 16px;
    line-height: 1.7;
}


/* ============================================================
   FEATURE CARDS
   ============================================================ */

.feature-card {
    background: #FFFFFF;
    border: 1px solid #E5E7EB;
    border-radius: 17px;
    padding: 24px 18px;
    min-height: 175px;
    text-align: center;
    box-shadow: 0 5px 18px rgba(15, 23, 42, 0.04);
}

.feature-icon {
    font-size: 34px;
    margin-bottom: 9px;
}

.feature-title {
    font-size: 18px;
    font-weight: 700;
    color: #172033;
    margin-bottom: 7px;
}

.feature-text {
    color: #6B7280;
    font-size: 14px;
    line-height: 1.6;
}


/* ============================================================
   REPOSITORY CARD
   ============================================================ */

.repository-card {
    background: #FFFFFF;
    border: 1px solid #E5E7EB;
    border-radius: 18px;
    padding: 22px 24px;
    margin-bottom: 18px;
    box-shadow: 0 6px 22px rgba(15, 23, 42, 0.04);
}

.repository-name {
    font-size: 25px;
    font-weight: 800;
    color: #172033;
}

.repository-url {
    color: #6B7280;
    font-size: 13px;
    margin-top: 5px;
    word-break: break-all;
}

.connected-badge {
    display: inline-block;
    margin-top: 10px;
    padding: 5px 10px;
    border-radius: 999px;
    background: #ECFDF3;
    color: #15803D;
    font-size: 12px;
    font-weight: 700;
}


/* ============================================================
   DASHBOARD METRICS
   ============================================================ */

.dashboard-card {
    background: #FFFFFF;
    border: 1px solid #E5E7EB;
    border-radius: 16px;
    padding: 18px 20px;
    min-height: 100px;
    box-shadow: 0 5px 18px rgba(15, 23, 42, 0.035);
}

.dashboard-label {
    color: #6B7280;
    font-size: 13px;
    margin-bottom: 7px;
}

.dashboard-value {
    color: #172033;
    font-size: 26px;
    font-weight: 800;
}


/* ============================================================
   SECTION HEADINGS
   ============================================================ */

.section-title {
    color: #172033;
    font-size: 25px;
    font-weight: 800;
    margin-top: 25px;
    margin-bottom: 5px;
}

.section-description {
    color: #6B7280;
    font-size: 14px;
    margin-bottom: 18px;
}


/* ============================================================
   CHAT
   ============================================================ */

.chat-header {
    background: #FFFFFF;
    border: 1px solid #E5E7EB;
    border-radius: 17px;
    padding: 20px 22px;
    margin-top: 20px;
    margin-bottom: 14px;
}

.chat-title {
    color: #172033;
    font-size: 24px;
    font-weight: 800;
    margin: 0;
}

.chat-description {
    color: #6B7280;
    font-size: 13px;
    margin-top: 5px;
}

[data-testid="stChatMessage"] {
    border-radius: 14px;
    margin-bottom: 10px;
}


/* ============================================================
   BUTTONS
   ============================================================ */

.stButton > button {
    border-radius: 10px;
    font-weight: 600;
    min-height: 42px;
}


/* ============================================================
   INPUTS
   ============================================================ */

.stTextInput input {
    border-radius: 10px !important;
    border: 1px solid #D1D5DB !important;
    background: #FFFFFF !important;
    color: #172033 !important;
}


/* ============================================================
   EXPANDERS
   ============================================================ */

[data-testid="stExpander"] {
    border: 1px solid #E5E7EB;
    border-radius: 12px;
    background: #FFFFFF;
}


/* ============================================================
   FOOTER
   ============================================================ */

.repomind-footer {
    text-align: center;
    color: #9CA3AF;
    font-size: 12px;
    padding: 30px 0 10px;
}

</style>
""",
unsafe_allow_html=True
)


# ============================================================
# HEADER
# ============================================================

st.markdown(
"""
<div class="repomind-header">

<div class="repomind-logo">🧠</div>

<div class="repomind-title">
RepoMind AI
</div>

<div class="repomind-subtitle">
Understand any software repository with AI
</div>

<div class="repomind-badge">
RAG · Gemini · ChromaDB
</div>

</div>
""",
unsafe_allow_html=True
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown("## ⚙️ Repository")

    repo_url_input = st.text_input(
        "GitHub Repository URL",
        value=st.session_state.repo_url,
        placeholder="https://github.com/user/project"
    )

    load_button = st.button(
        "🚀 Load Repository",
        type="primary",
        use_container_width=True
    )


    # ========================================================
    # LOAD REPOSITORY
    # ========================================================

    if load_button:

        clean_url = repo_url_input.strip()

        if not clean_url:

            st.warning(
                "Please enter a GitHub repository URL."
            )

        else:

            try:

                # ------------------------------------------------
                # CLONE
                # ------------------------------------------------

                with st.spinner(
                    "🔗 Cloning repository..."
                ):

                    repo_path = clone_repository(
                        clean_url
                    )


                # ------------------------------------------------
                # LOAD FILES
                # ------------------------------------------------

                with st.spinner(
                    "📂 Reading repository files..."
                ):

                    documents = load_repository_files(
                        repo_path
                    )


                # ------------------------------------------------
                # VALIDATE FILES
                # ------------------------------------------------

                if not documents:

                    st.session_state.repo_loaded = False
                    st.session_state.vector_store = None
                    st.session_state.repository_summary = ""
                    st.session_state.repo_stats = None

                    st.error(
                        "No supported source files found."
                    )

                    st.stop()


                # ------------------------------------------------
                # CHUNK DOCUMENTS
                # ------------------------------------------------

                with st.spinner(
                    "✂️ Processing source code..."
                ):

                    chunks = chunk_documents(
                        documents
                    )


                if not chunks:

                    st.session_state.repo_loaded = False
                    st.session_state.vector_store = None
                    st.session_state.repository_summary = ""
                    st.session_state.repo_stats = None

                    st.error(
                        "No searchable chunks were created."
                    )

                    st.stop()


                # ------------------------------------------------
                # CREATE VECTOR STORE
                # ------------------------------------------------

                with st.spinner(
                    "🧠 Creating repository knowledge base..."
                ):

                    vector_store = create_vector_store(
                        chunks
                    )


                # ------------------------------------------------
                # ARCHITECTURE ANALYSIS
                # ------------------------------------------------

                with st.spinner(
                    "🏗️ Analyzing project architecture..."
                ):

                    repository_summary = analyze_repository(
                        documents
                    )


                # ------------------------------------------------
                # SAVE STATE
                # ------------------------------------------------

                st.session_state.vector_store = (
                    vector_store
                )

                st.session_state.repository_summary = (
                    repository_summary
                )

                st.session_state.repo_loaded = True

                st.session_state.repo_url = (
                    clean_url
                )

                st.session_state.repo_stats = {
                    "files": len(documents),
                    "chunks": len(chunks)
                }

                # New repository = new conversation
                st.session_state.messages = []

                st.success(
                    "✅ Repository ready!"
                )


            except Exception as error:

                st.session_state.repo_loaded = False
                st.session_state.vector_store = None
                st.session_state.repository_summary = ""
                st.session_state.repo_stats = None

                st.error(
                    f"Failed to process repository: {error}"
                )


    # ========================================================
    # CONNECTED REPOSITORY
    # ========================================================

    if st.session_state.repo_loaded:

        st.divider()

        st.success(
            "🟢 Repository Connected"
        )

        st.caption(
            st.session_state.repo_url
        )


        # ----------------------------------------------------
        # REPOSITORY STATS
        # ----------------------------------------------------

        if st.session_state.repo_stats:

            stat_col1, stat_col2 = st.columns(2)

            with stat_col1:

                st.metric(
                    "Files",
                    st.session_state.repo_stats["files"]
                )

            with stat_col2:

                st.metric(
                    "Chunks",
                    st.session_state.repo_stats["chunks"]
                )


        # ----------------------------------------------------
        # REPOSITORY OVERVIEW
        # ----------------------------------------------------

        if st.session_state.repository_summary:

            with st.expander(
                "🧠 Repository Overview"
            ):

                st.markdown(
                    st.session_state.repository_summary
                )


        # ----------------------------------------------------
        # CLEAR CHAT
        # ----------------------------------------------------

        if st.button(
            "🗑️ Clear Conversation",
            use_container_width=True
        ):

            st.session_state.messages = []

            st.rerun()


    # ========================================================
    # EXAMPLE QUESTIONS
    # ========================================================

    st.divider()

    st.markdown("### 💡 Try asking")

    st.markdown(
"""
- Explain the project architecture
- What technologies are used?
- Where does execution start?
- How does data flow?
- What algorithms are implemented?
"""
    )


    st.divider()

    st.caption(
        "Powered by Gemini + LangChain + ChromaDB"
    )


# ============================================================
# LANDING PAGE
# ============================================================

if not st.session_state.repo_loaded:

    st.markdown(
"""
<div class="hero-card">

<div class="hero-icon">
🔍
</div>

<div class="hero-title">
Understand Any Repository
</div>

<div class="hero-text">
Connect a GitHub repository and ask RepoMind
about its architecture, source code,
algorithms, data flow and implementation.
</div>

</div>
""",
unsafe_allow_html=True
    )


    # --------------------------------------------------------
    # FEATURE CARDS
    # --------------------------------------------------------

    col1, col2, col3 = st.columns(3)


    with col1:

        st.markdown(
"""
<div class="feature-card">

<div class="feature-icon">
🔍
</div>

<div class="feature-title">
Explore Code
</div>

<div class="feature-text">
Search and understand source code
using semantic retrieval.
</div>

</div>
""",
unsafe_allow_html=True
        )


    with col2:

        st.markdown(
"""
<div class="feature-card">

<div class="feature-icon">
🏗️
</div>

<div class="feature-title">
Understand Architecture
</div>

<div class="feature-text">
Get an AI-generated overview of
your repository architecture.
</div>

</div>
""",
unsafe_allow_html=True
        )


    with col3:

        st.markdown(
"""
<div class="feature-card">

<div class="feature-icon">
🤖
</div>

<div class="feature-title">
Ask RepoMind
</div>

<div class="feature-text">
Have a conversation with your
repository using Gemini.
</div>

</div>
""",
unsafe_allow_html=True
        )


    st.markdown("")

    st.info(
        "👈 Enter a GitHub repository URL in the sidebar to get started."
    )


# ============================================================
# REPOSITORY DASHBOARD
# ============================================================

else:

    repo_name = "Repository"

    try:

        repo_name = (
            st.session_state.repo_url
            .rstrip("/")
            .split("/")
            [-1]
        )

        if repo_name.endswith(".git"):

            repo_name = repo_name[:-4]

    except Exception:

        repo_name = "Repository"


    # --------------------------------------------------------
    # REPOSITORY HEADER
    # --------------------------------------------------------

    st.markdown(
f"""
<div class="repository-card">

<div class="repository-name">
📦 {repo_name}
</div>

<div class="repository-url">
{st.session_state.repo_url}
</div>

<div class="connected-badge">
● Repository Connected
</div>

</div>
""",
unsafe_allow_html=True
    )


    # --------------------------------------------------------
    # DASHBOARD METRICS
    # --------------------------------------------------------

    stats = st.session_state.repo_stats or {
        "files": 0,
        "chunks": 0
    }


    metric1, metric2, metric3, metric4 = st.columns(4)


    with metric1:

        st.markdown(
f"""
<div class="dashboard-card">

<div class="dashboard-label">
📁 Files
</div>

<div class="dashboard-value">
{stats["files"]}
</div>

</div>
""",
unsafe_allow_html=True
        )


    with metric2:

        st.markdown(
f"""
<div class="dashboard-card">

<div class="dashboard-label">
🧩 Chunks
</div>

<div class="dashboard-value">
{stats["chunks"]}
</div>

</div>
""",
unsafe_allow_html=True
        )


    with metric3:

        st.markdown(
"""
<div class="dashboard-card">

<div class="dashboard-label">
🤖 AI Model
</div>

<div class="dashboard-value">
Gemini
</div>

</div>
""",
unsafe_allow_html=True
        )


    with metric4:

        st.markdown(
"""
<div class="dashboard-card">

<div class="dashboard-label">
📚 RAG
</div>

<div class="dashboard-value">
Active
</div>

</div>
""",
unsafe_allow_html=True
        )


    # --------------------------------------------------------
    # ARCHITECTURE
    # --------------------------------------------------------

    st.markdown(
"""
<div class="section-title">
🏗️ Repository Architecture
</div>

<div class="section-description">
AI-generated understanding of the repository structure and implementation.
</div>
""",
unsafe_allow_html=True
    )


    if st.session_state.repository_summary:

        with st.expander(
            "View AI-generated architecture analysis"
        ):

            st.markdown(
                st.session_state.repository_summary
            )


    # --------------------------------------------------------
    # CHAT HEADER
    # --------------------------------------------------------

    st.markdown(
"""
<div class="chat-header">

<div class="chat-title">
💬 Chat with your Repository
</div>

<div class="chat-description">
Ask questions about the codebase, architecture,
algorithms, implementation or data flow.
</div>

</div>
""",
unsafe_allow_html=True
    )


    # --------------------------------------------------------
    # CHAT HISTORY
    # --------------------------------------------------------

    for message in st.session_state.messages:

        role = message.get(
            "role",
            "user"
        )

        content = message.get(
            "content",
            ""
        )

        with st.chat_message(role):

            st.markdown(
                content
            )

            sources = message.get(
                "sources",
                []
            )

            if (
                role == "assistant"
                and sources
            ):

                with st.expander(
                    "📚 View Sources"
                ):

                    for source in sources:

                        st.code(
                            source,
                            language=None
                        )


    # --------------------------------------------------------
    # CHAT INPUT
    # --------------------------------------------------------

    question = st.chat_input(
        "Ask anything about this repository..."
    )


    # --------------------------------------------------------
    # PROCESS QUESTION
    # --------------------------------------------------------

    if question:

        clean_question = question.strip()

        if clean_question:

            # ------------------------------------------------
            # COPY PREVIOUS CONVERSATION
            # ------------------------------------------------

            previous_messages = list(
                st.session_state.messages
            )


            # ------------------------------------------------
            # SAVE USER MESSAGE
            # ------------------------------------------------

            st.session_state.messages.append(
                {
                    "role": "user",
                    "content": clean_question
                }
            )


            # ------------------------------------------------
            # DISPLAY USER MESSAGE
            # ------------------------------------------------

            with st.chat_message(
                "user"
            ):

                st.markdown(
                    clean_question
                )


            # ------------------------------------------------
            # GENERATE AI RESPONSE
            # ------------------------------------------------

            with st.chat_message(
                "assistant"
            ):

                try:

                    with st.spinner(
                        "🔎 Searching repository..."
                    ):

                        answer, sources = ask_repository(
                            question=clean_question,
                            vector_store=(
                                st.session_state.vector_store
                            ),
                            messages=previous_messages,
                            repository_summary=(
                                st.session_state.repository_summary
                            )
                        )


                    # ----------------------------------------
                    # DISPLAY ANSWER
                    # ----------------------------------------

                    st.markdown(
                        answer
                    )


                    # ----------------------------------------
                    # DISPLAY SOURCES
                    # ----------------------------------------

                    if sources:

                        with st.expander(
                            "📚 View Sources"
                        ):

                            for source in sources:

                                st.code(
                                    source,
                                    language=None
                                )


                    # ----------------------------------------
                    # SAVE ASSISTANT MESSAGE
                    # ----------------------------------------

                    st.session_state.messages.append(
                        {
                            "role": "assistant",
                            "content": answer,
                            "sources": sources
                        }
                    )


                except Exception as error:

                    st.error(
                        f"Something went wrong: {error}"
                    )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
"""
<div class="repomind-footer">
RepoMind AI · AI Software Repository Assistant
</div>
""",
unsafe_allow_html=True
)