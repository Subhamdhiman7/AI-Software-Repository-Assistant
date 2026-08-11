# 🧠 RepoMind AI

> Understand any software repository with AI.

RepoMind AI is an AI-powered software repository assistant that lets
developers connect a public GitHub repository and ask questions about
its source code, architecture, algorithms, implementation, and data
flow.

It combines Gemini, LangChain, ChromaDB, semantic retrieval,
repository-level analysis, and conversational memory to produce answers
grounded in the loaded repository.

## 🚀 Live Demo

-   **RepoMind AI:** https://ai-repo.streamlit.app/
-   **GitHub:**
    https://github.com/Subhamdhiman7/AI-Software-Repository-Assistant

## ✨ Features

-   🔗 **GitHub Repository Loading** --- clone a repository, read
    supported source files, process them, create searchable chunks,
    build a ChromaDB vector store, and generate an architecture summary.
-   🔍 **Source-Based RAG** --- retrieve relevant source-code chunks and
    provide them to Gemini as technical evidence.
-   🏗️ **Architecture Analysis** --- generate high-level understanding
    of project architecture, important files, entry points, technology
    stack, and data flow.
-   💬 **Conversational Memory** --- resolve follow-up references such
    as "it", "this function", and "that algorithm" using previous
    conversation context.
-   📚 **Source References** --- preserve file paths and chunk metadata
    for retrieved evidence.
-   🎨 **Interactive UI** --- repository controls, statistics,
    architecture overview, source viewing, suggested questions, and AI
    chat.

## 🧠 How It Works

``` text
GitHub Repository URL
        │
        ▼
Clone Repository
        │
        ▼
Load Source Files
        │
        ▼
Chunk Source Code
        │
        ▼
Create ChromaDB Knowledge Base
        │
        ├───────────────┐
        ▼               ▼
Repository Analysis   User Question
                          │
                          ▼
                 Contextual Query
                     Generation
                          │
                          ▼
                 Semantic Retrieval
                     from ChromaDB
                          │
                          ▼
              Retrieved Code +
              Architecture Summary +
              Conversation History
                          │
                          ▼
                       Gemini
                          │
                          ▼
                  Grounded Answer
```

## 🏛️ Project Structure

``` text
AI-Software-Repository-Assistant/
│
├── app.py
│
├── backend/
│   ├── __init__.py
│   ├── analyzer.py
│   ├── chunker.py
│   ├── config.py
│   ├── llm.py
│   ├── loader.py
│   ├── rag.py
│   ├── repository.py
│   ├── utils.py
│   └── vectorstore.py
│
├── components/
│   ├── chat.py
│   ├── dashboard.py
│   ├── footer.py
│   ├── header.py
│   ├── repository_card.py
│   └── sidebar.py
│
├── styles/
│   └── theme.css
│
├── test_analyzer.py
├── test_loader.py
├── test_rag.py
├── test_vectorstore.py
│
├── requirements.txt
├── runtime.txt
└── .gitignore
```

## 🔧 Main Modules

  Module               Responsibility
  -------------------- -----------------------------------------------
  `repository.py`      Clone GitHub repositories
  `loader.py`          Load repository source files
  `chunker.py`         Split source documents into searchable chunks
  `vectorstore.py`     Create and use the ChromaDB vector store
  `analyzer.py`        Analyze the repository architecture
  `rag.py`             Conversational retrieval-augmented generation
  `llm.py`             LLM integration
  `config.py`          Environment/API configuration
  `utils.py`           Shared utilities
  `components/`        Streamlit UI components
  `styles/theme.css`   Global UI styling

## 🤖 RAG Pipeline

RepoMind uses **Gemini 3.6 Flash** through LangChain's Google GenAI
integration.

### 1. Contextual query generation

A follow-up question is converted into a concise semantic-search query
using recent conversation context.

### 2. Semantic retrieval

The query is searched against the ChromaDB vector store. The RAG
pipeline retrieves the most relevant source-code chunks.

### 3. Context construction

Retrieved documents are organized with their file paths, chunk IDs, and
source-code content.

### 4. Grounded generation

Gemini receives:

1.  Previous conversation
2.  Repository architecture summary
3.  Retrieved source code
4.  Current question

Retrieved source code is treated as the strongest technical evidence.

### 5. Final answer

Gemini produces a developer-friendly answer grounded in the repository
evidence.

## 🛠️ Tech Stack

### UI

-   Streamlit
-   HTML
-   CSS

### AI

-   Google Gemini
-   LangChain
-   `langchain-google-genai`

### RAG

-   ChromaDB
-   LangChain vector-store integration
-   Semantic similarity search

### Repository Processing

-   GitPython
-   LangChain text splitters

### Configuration

-   Python Dotenv
-   Environment variables

### Testing

-   Python tests for analyzer, loader, RAG, and vector-store components

## ⚙️ Local Setup

### 1. Clone the repository

``` bash
git clone https://github.com/Subhamdhiman7/AI-Software-Repository-Assistant.git
cd AI-Software-Repository-Assistant
```

### 2. Create and activate a virtual environment

Windows:

``` powershell
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies

``` bash
pip install -r requirements.txt
```

### 4. Configure Gemini

Create `.env` in the project root:

``` env
GOOGLE_API_KEY=your_google_api_key
```

Never commit the `.env` file.

### 5. Run the application

``` bash
streamlit run app.py
```

## 🔐 Environment Variables

  Variable           Description
  ------------------ -----------------------
  `GOOGLE_API_KEY`   Google Gemini API key

For Streamlit Cloud, configure the key through **Secrets** instead of
committing `.env`.

## 💬 Example Questions

``` text
Explain the project architecture.
What technologies are used?
Where does execution start?
How does data flow through the application?
What algorithms are implemented?
Explain the main entry point.
Which files handle database operations?
What does this function do?
What is the time complexity of this algorithm?
```

## 🧪 Testing

The project contains focused tests:

``` text
test_analyzer.py
test_loader.py
test_rag.py
test_vectorstore.py
```

Run them with:

``` bash
python -m pytest
```

If needed:

``` bash
pip install pytest
```

## ☁️ Deployment

RepoMind AI is deployed on **Streamlit Community Cloud**.

-   Main file: `app.py`
-   Dependencies: `requirements.txt`
-   Runtime: `runtime.txt`
-   Secrets: Streamlit Cloud Secrets

**Live app:** https://ai-repo.streamlit.app/

## 🔒 Security Notes

-   Store API keys in environment variables or Streamlit Secrets.
-   Never commit `.env`.
-   Keep virtual environments and generated local data out of Git.
-   Treat repository contents as untrusted input.
-   Verify AI-generated explanations against source code for critical
    engineering decisions.

## ⚠️ Limitations

-   Processing time depends on repository size and source-code volume.
-   Very large repositories may require additional processing time and
    memory.
-   Retrieval quality depends on chunking and semantic similarity.
-   AI responses should be reviewed against the actual source code.
-   The current application is primarily designed for publicly
    accessible GitHub repositories.
-   Persistent vector storage across independent deployments/users is
    not the primary design goal.

## 📌 Project Status

-   [x] GitHub repository loading
-   [x] Source-code loading
-   [x] Source-code chunking
-   [x] ChromaDB knowledge base
-   [x] Semantic retrieval
-   [x] Gemini-powered answers
-   [x] Conversational memory
-   [x] Repository architecture analysis
-   [x] Source references
-   [x] UI polish
-   [x] Basic component tests
-   [x] Streamlit Cloud deployment

## 👨‍💻 Author

**Subham Dhiman**

GitHub: https://github.com/Subhamdhiman7

## ⭐ Why RepoMind AI?

Understanding an unfamiliar repository can require manually navigating
files, tracing imports, and searching for implementations.

RepoMind AI reduces that exploration overhead by combining
repository-level analysis with source-grounded retrieval, allowing
developers to interact with a codebase conversationally.
