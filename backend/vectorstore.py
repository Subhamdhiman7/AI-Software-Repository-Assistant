import os
import uuid

from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma

from backend.config import GOOGLE_API_KEY


VECTOR_DB_ROOT = "chroma_db"


def get_embedding_model():

    return GoogleGenerativeAIEmbeddings(
        model="models/gemini-embedding-001",
        google_api_key=GOOGLE_API_KEY
    )


def create_vector_store(chunks):

    # Make sure main Chroma folder exists
    os.makedirs(
        VECTOR_DB_ROOT,
        exist_ok=True
    )

    # Every repository load gets its own database directory.
    # This avoids Windows file-lock problems.
    database_id = str(uuid.uuid4())

    database_path = os.path.join(
        VECTOR_DB_ROOT,
        database_id
    )

    embeddings = get_embedding_model()

    texts = []
    metadatas = []

    for chunk in chunks:

        texts.append(
            chunk["content"]
        )

        metadatas.append({
            "path": chunk["path"],
            "chunk_id": chunk["chunk_id"]
        })

    vector_store = Chroma.from_texts(
        texts=texts,
        embedding=embeddings,
        metadatas=metadatas,
        persist_directory=database_path
    )

    return vector_store