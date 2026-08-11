from backend.loader import load_repository_files
from backend.chunker import chunk_documents
from backend.vectorstore import create_vector_store
from backend.rag import ask_repository


print("\nLoading repository...")

documents = load_repository_files(
    "cloned_repo"
)

chunks = chunk_documents(documents)

print(f"Documents: {len(documents)}")
print(f"Chunks: {len(chunks)}")


print("\nCreating vector store...")

vector_store = create_vector_store(chunks)


question = "How are tasks searched?"

print(f"\nQuestion: {question}")
print("\nAsking RepoMind...\n")


answer, sources = ask_repository(
    question,
    vector_store
)


print("=" * 70)

print("\nANSWER:\n")

print(answer)


print("\nSOURCES:")

for source in sources:
    print(f"- {source}")

print("\n" + "=" * 70)