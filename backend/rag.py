from langchain_google_genai import ChatGoogleGenerativeAI

from backend.config import GOOGLE_API_KEY


# ============================================================
# GEMINI MODEL
# ============================================================

def get_llm():
    """
    Gemini model used by RepoMind.
    """

    return ChatGoogleGenerativeAI(
        model="gemini-3.6-flash",
        google_api_key=GOOGLE_API_KEY,
        temperature=0.1
    )


# ============================================================
# RESPONSE TEXT EXTRACTION
# ============================================================

def extract_text(response):
    """
    Safely extract text from Gemini responses.
    """

    content = response.content

    if isinstance(content, str):
        return content.strip()

    if isinstance(content, list):

        parts = []

        for item in content:

            if isinstance(item, dict):

                text = item.get("text")

                if text:
                    parts.append(text)

            elif isinstance(item, str):

                parts.append(item)

        return "\n".join(parts).strip()

    return str(content).strip()


# ============================================================
# FORMAT CONVERSATION
# ============================================================

def format_messages(messages, limit=8):
    """
    Convert recent conversation messages into text
    for Gemini.
    """

    if not messages:
        return "No previous conversation."

    recent_messages = messages[-limit:]

    formatted = []

    for message in recent_messages:

        role = message.get(
            "role",
            "user"
        )

        content = message.get(
            "content",
            ""
        )

        if role == "user":
            speaker = "USER"
        else:
            speaker = "REPOMIND"

        formatted.append(
            f"{speaker}:\n{content}"
        )

    return "\n\n".join(formatted)


# ============================================================
# CREATE CONTEXTUAL RETRIEVAL QUERY
# ============================================================

def create_contextual_query(
    question,
    messages
):
    """
    Convert conversational questions into standalone
    semantic-search queries.

    Example:

    Previous:
        How are tasks searched?

    RepoMind:
        Tasks use linearSearch().

    Current:
        What is its complexity?

    Retrieval query:
        linearSearch task searching time complexity
    """

    if not messages:
        return question

    conversation = format_messages(
        messages,
        limit=6
    )

    prompt = f"""
You are the retrieval-query generator for RepoMind,
an AI source-code repository assistant.

The user is having a continuous conversation about
a software repository.

Create ONE concise semantic-search query for finding
source code relevant to the CURRENT QUESTION.

Use previous conversation to resolve references.


EXAMPLE:

PREVIOUS CONVERSATION:

USER:
How are tasks searched?

REPOMIND:
Tasks are searched using the linearSearch method.

CURRENT QUESTION:

What is its time complexity?

CORRECT SEARCH QUERY:

linearSearch task search implementation time complexity


RULES:

1. Resolve references such as:

   it
   its
   this
   that
   they
   them
   that function
   that method
   this class
   that algorithm
   previous function

2. Prefer exact technical names mentioned in the
   previous conversation.

3. Do NOT answer the question.

4. Do NOT explain your reasoning.

5. Do NOT invent repository details.

6. Return ONLY the search query.

7. Keep the query concise and useful for semantic
   source-code retrieval.


PREVIOUS CONVERSATION:

{conversation}


CURRENT QUESTION:

{question}


SEARCH QUERY:
"""

    try:

        llm = get_llm()

        response = llm.invoke(
            prompt
        )

        query = extract_text(
            response
        )

        if query:
            return query

    except Exception:
        pass

    # Safe fallback
    return question


# ============================================================
# BUILD RETRIEVED CODE CONTEXT
# ============================================================

def build_context(documents):
    """
    Convert retrieved Chroma documents into structured
    repository evidence.
    """

    context_parts = []

    sources = []

    for doc in documents:

        path = doc.metadata.get(
            "path",
            "Unknown file"
        )

        chunk_id = doc.metadata.get(
            "chunk_id",
            "?"
        )

        context_parts.append(
            f"""
============================================================
FILE: {path}
CHUNK: {chunk_id}
============================================================

{doc.page_content}
"""
        )

        if path not in sources:
            sources.append(path)

    return (
        "\n\n".join(context_parts),
        sources
    )


# ============================================================
# ASK REPOSITORY
# ============================================================

def ask_repository(
    question,
    vector_store,
    messages=None,
    repository_summary=""
):
    """
    Main RepoMind conversational RAG pipeline.

    Uses:

    1. Conversation memory
    2. Repository-level architecture summary
    3. Semantic retrieval from ChromaDB
    4. Gemini for grounded generation
    """

    if messages is None:
        messages = []


    # ========================================================
    # STEP 1 — CREATE CONTEXTUAL RETRIEVAL QUERY
    # ========================================================

    retrieval_query = create_contextual_query(
        question,
        messages
    )


    # ========================================================
    # STEP 2 — RETRIEVE RELEVANT CODE
    # ========================================================

    documents = vector_store.similarity_search(
        retrieval_query,
        k=6
    )


    # ========================================================
    # STEP 3 — BUILD RETRIEVED CONTEXT
    # ========================================================

    if documents:

        repository_context, sources = build_context(
            documents
        )

    else:

        repository_context = (
            "No directly relevant source-code chunks "
            "were retrieved."
        )

        sources = []


    # ========================================================
    # STEP 4 — FORMAT CONVERSATION
    # ========================================================

    conversation = format_messages(
        messages,
        limit=8
    )


    # ========================================================
    # STEP 5 — HANDLE SUMMARY
    # ========================================================

    if repository_summary:

        architecture_context = repository_summary

    else:

        architecture_context = (
            "No repository-level architecture summary "
            "is available."
        )


    # ========================================================
    # STEP 6 — FINAL RAG PROMPT
    # ========================================================

    prompt = f"""
You are RepoMind AI, an AI software repository assistant.

You help developers understand the currently loaded
software repository.

You have THREE types of context:

1. PREVIOUS CONVERSATION
   Used to understand conversational references.

2. REPOSITORY ARCHITECTURE SUMMARY
   Used for broad understanding of the project.

3. RETRIEVED SOURCE CODE
   Used as detailed technical evidence.


============================================================
EVIDENCE PRIORITY
============================================================

When answering:

RETRIEVED SOURCE CODE
        ↓
highest technical authority

REPOSITORY ARCHITECTURE SUMMARY
        ↓
high-level supporting context

PREVIOUS CONVERSATION
        ↓
used primarily to understand what the user refers to


If the architecture summary conflicts with retrieved
source code, trust the retrieved source code.


============================================================
PREVIOUS CONVERSATION
============================================================

{conversation}


============================================================
REPOSITORY ARCHITECTURE SUMMARY
============================================================

{architecture_context}


============================================================
RETRIEVED SOURCE CODE
============================================================

{repository_context}


============================================================
CURRENT QUESTION
============================================================

{question}


============================================================
RULES
============================================================

1. Answer the CURRENT QUESTION directly.

2. Use conversation history to understand references such as:

   it
   its
   this
   that
   they
   that function
   that method
   this class
   that algorithm

3. Do not say a reference is ambiguous when the previous
   conversation clearly identifies it.

4. Use retrieved source code as the strongest technical
   evidence.

5. Use the repository architecture summary for broad
   questions such as:

   - project architecture
   - project purpose
   - technology stack
   - important files
   - entry points
   - overall data flow

6. Never invent:

   - files
   - functions
   - classes
   - databases
   - APIs
   - frameworks
   - authentication
   - algorithms
   - external services

7. If evidence is insufficient, clearly state that.

8. Mention exact filenames, classes and function names
   whenever useful.

9. For algorithm complexity questions, briefly explain
   why the complexity has that value.

10. Do not include unrelated repository information merely
    because it appears in retrieved chunks.

11. Be clear and developer-friendly.

12. Do not claim the entire repository lacks a feature
    solely because retrieved chunks do not contain it.

13. Repository evidence is the source of truth.


============================================================
ANSWER
============================================================
"""

    # ========================================================
    # STEP 7 — GEMINI
    # ========================================================

    llm = get_llm()

    response = llm.invoke(
        prompt
    )

    answer = extract_text(
        response
    )


    # ========================================================
    # STEP 8 — RETURN
    # ========================================================

    return answer, sources