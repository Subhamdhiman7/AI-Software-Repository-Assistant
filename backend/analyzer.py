import os

from backend.llm import get_llm


# ============================================================
# ANALYZER LIMITS
# ============================================================

MAX_ANALYZER_FILES = 40

MAX_TOTAL_CHARACTERS = 80000

DEFAULT_PREVIEW_SIZE = 4000

IMPORTANT_PREVIEW_SIZE = 8000


# ============================================================
# IMPORTANT ARCHITECTURE FILES
# ============================================================

IMPORTANT_FILES = {
    "readme.md",

    # JavaScript
    "package.json",

    # Python
    "requirements.txt",
    "pyproject.toml",
    "setup.py",

    # Java
    "pom.xml",
    "build.gradle",

    # Containers
    "dockerfile",
    "docker-compose.yml",
    "docker-compose.yaml",

    # Other
    "makefile",
    "cargo.toml",
    "go.mod"
}


# ============================================================
# IMPORTANT FILE NAMES / PATTERNS
# ============================================================

ENTRY_POINT_NAMES = {
    "main.py",
    "app.py",
    "server.py",
    "manage.py",

    "main.js",
    "main.jsx",
    "main.ts",
    "main.tsx",

    "index.js",
    "index.jsx",
    "index.ts",
    "index.tsx",

    "app.js",
    "app.jsx",
    "app.ts",
    "app.tsx",

    "index.html"
}


# ============================================================
# RESPONSE TEXT
# ============================================================

def extract_text(response):

    content = response.content

    if isinstance(content, str):
        return content.strip()

    if isinstance(content, list):

        parts = []

        for item in content:

            if isinstance(item, dict):

                text = item.get(
                    "text"
                )

                if text:
                    parts.append(
                        text
                    )

            elif isinstance(item, str):

                parts.append(
                    item
                )

        return "\n".join(
            parts
        ).strip()

    return str(
        content
    ).strip()


# ============================================================
# DOCUMENT DATA
# ============================================================

def get_document_data(document):
    """
    Support both RepoMind dictionaries and LangChain
    Document objects.
    """

    if isinstance(
        document,
        dict
    ):

        return (
            document.get(
                "path",
                "Unknown file"
            ),
            document.get(
                "content",
                ""
            )
        )


    metadata = getattr(
        document,
        "metadata",
        {}
    )

    return (
        metadata.get(
            "path",
            "Unknown file"
        ),
        getattr(
            document,
            "page_content",
            ""
        )
    )


# ============================================================
# NORMALIZE PATH
# ============================================================

def normalize_path(path):

    return path.replace(
        "\\",
        "/"
    )


# ============================================================
# FILE IMPORTANCE SCORE
# ============================================================

def get_file_importance(path):
    """
    Assign an architecture relevance score.

    Higher score = more likely to be useful for generating
    the repository overview.
    """

    normalized = normalize_path(
        path
    )

    lower_path = normalized.lower()

    filename = os.path.basename(
        lower_path
    )

    score = 0


    # ========================================================
    # PROJECT MANIFEST / DOCUMENTATION
    # ========================================================

    if filename in IMPORTANT_FILES:
        score += 100


    # ========================================================
    # ENTRY POINT
    # ========================================================

    if filename in ENTRY_POINT_NAMES:
        score += 90


    # ========================================================
    # SOURCE DIRECTORY
    # ========================================================

    if lower_path.startswith(
        "src/"
    ):
        score += 30


    if "/src/" in lower_path:
        score += 30


    # ========================================================
    # BACKEND
    # ========================================================

    if lower_path.startswith(
        "backend/"
    ):
        score += 35


    if "/backend/" in lower_path:
        score += 35


    # ========================================================
    # FRONTEND
    # ========================================================

    if lower_path.startswith(
        "frontend/"
    ):
        score += 35


    if "/frontend/" in lower_path:
        score += 35


    # ========================================================
    # API / ROUTES / SERVICES
    # ========================================================

    architecture_terms = [
        "api",
        "route",
        "router",
        "service",
        "controller",
        "model",
        "schema",
        "database",
        "db",
        "auth",
        "config",
        "middleware",
        "store"
    ]

    for term in architecture_terms:

        if term in lower_path:
            score += 12


    # ========================================================
    # TESTS ARE USEFUL, BUT LESS IMPORTANT
    # ========================================================

    if (
        "/test/" in lower_path
        or "/tests/" in lower_path
        or filename.startswith("test_")
        or filename.endswith(".test.js")
        or filename.endswith(".test.jsx")
        or filename.endswith(".test.ts")
        or filename.endswith(".test.tsx")
    ):
        score -= 30


    return score


# ============================================================
# SELECT IMPORTANT FILES
# ============================================================

def select_important_documents(
    documents,
    max_files=MAX_ANALYZER_FILES
):
    """
    Rank files by architectural importance and keep the
    most useful subset.
    """

    ranked = []

    for document in documents:

        path, content = get_document_data(
            document
        )

        if not content:
            continue

        score = get_file_importance(
            path
        )

        ranked.append(
            (
                score,
                path,
                content
            )
        )


    # Highest score first.
    #
    # For equal scores, smaller files come first because
    # they're often easier architectural signals.
    ranked.sort(
        key=lambda item: (
            -item[0],
            len(item[2])
        )
    )


    return ranked[
        :max_files
    ]


# ============================================================
# PREVIEW SIZE
# ============================================================

def get_preview_size(
    path,
    score
):

    filename = os.path.basename(
        path.lower()
    )

    if (
        filename in IMPORTANT_FILES
        or filename in ENTRY_POINT_NAMES
        or score >= 80
    ):
        return IMPORTANT_PREVIEW_SIZE

    return DEFAULT_PREVIEW_SIZE


# ============================================================
# BUILD REPOSITORY OVERVIEW
# ============================================================

def build_repository_overview(
    documents
):

    selected_documents = (
        select_important_documents(
            documents
        )
    )


    overview_parts = []

    total_characters = 0


    for (
        score,
        path,
        content
    ) in selected_documents:

        path = normalize_path(
            path
        )

        if not isinstance(
            content,
            str
        ):
            content = str(
                content
            )


        preview_size = get_preview_size(
            path,
            score
        )


        preview = content[
            :preview_size
        ]


        block = f"""
============================================================
FILE: {path}
FILE SIZE: {len(content)} characters
ARCHITECTURE SCORE: {score}
============================================================

{preview}
"""


        # ====================================================
        # GLOBAL TOKEN/COST SAFETY LIMIT
        # ====================================================

        if (
            total_characters
            + len(block)
            > MAX_TOTAL_CHARACTERS
        ):

            remaining = (
                MAX_TOTAL_CHARACTERS
                - total_characters
            )

            if remaining > 1000:

                overview_parts.append(
                    block[:remaining]
                )

            break


        overview_parts.append(
            block
        )

        total_characters += len(
            block
        )


    return "\n\n".join(
        overview_parts
    )


# ============================================================
# ANALYZE REPOSITORY
# ============================================================

def analyze_repository(
    documents
):

    if not documents:

        return (
            "Repository analysis could not be generated "
            "because no supported files were loaded."
        )


    repository_overview = (
        build_repository_overview(
            documents
        )
    )


    if not repository_overview:

        return (
            "Repository analysis could not be generated "
            "because no suitable source files were found."
        )


    prompt = f"""
You are RepoMind AI, a senior software engineer analyzing
a software repository.

Create a concise but useful architectural understanding
of the repository.

This summary will later be used by RepoMind's RAG system
to answer high-level repository questions.

Use ONLY the repository evidence provided below.


============================================================
ANALYZE
============================================================

Identify:

1. PROJECT PURPOSE

What does this project appear to do?


2. PROJECT TYPE

Examples:

- frontend application
- backend API
- full-stack application
- Python application
- machine-learning project
- CLI
- library


3. TECHNOLOGY STACK

Identify supported evidence for:

- programming languages
- frameworks
- libraries
- build tools
- databases
- AI/ML technologies
- styling systems
- infrastructure


4. ENTRY POINTS

Identify where execution begins and explain the startup
flow when possible.


5. IMPORTANT FILES

Identify the most architecturally important files and
their responsibilities.


6. IMPORTANT COMPONENTS

Identify major:

- classes
- functions
- components
- services
- modules
- models
- controllers
- utilities


7. ARCHITECTURE

Explain how the major pieces connect.


8. DATA FLOW

Explain how information moves through the application.


9. DATA STORAGE

Identify evidence for:

- databases
- localStorage
- sessionStorage
- files
- caches
- state management


10. APIs / EXTERNAL SERVICES

Identify external APIs and services only when supported
by evidence.


11. ALGORITHMS / DATA STRUCTURES

Identify important algorithms and data structures.


12. DEPENDENCIES

Identify major project dependencies and their likely
roles when clear from repository evidence.


13. LIMITATIONS

State what cannot be confidently determined from the
provided evidence.


============================================================
CRITICAL RULES
============================================================

1. Never invent files.

2. Never invent functions.

3. Never invent classes.

4. Never invent databases.

5. Never invent authentication.

6. Never invent APIs.

7. Never invent external services.

8. Never assume a backend exists.

9. Never assume a frontend exists.

10. Use exact filenames when possible.

11. Use exact technical names when possible.

12. If evidence is insufficient, explicitly say so.

13. Focus on architecture rather than minor styling.

14. Repository evidence is the source of truth.

15. Some large source files may only be partially shown.
    Do not describe those files as actually truncated in
    the repository. Say only that the supplied evidence
    contains a partial preview if that limitation matters.


============================================================
REPOSITORY EVIDENCE
============================================================

{repository_overview}


============================================================
REPOSITORY ARCHITECTURE SUMMARY
============================================================
"""


    llm = get_llm()

    response = llm.invoke(
        prompt
    )

    return extract_text(
        response
    )