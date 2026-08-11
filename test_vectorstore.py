from backend.loader import load_repository_files
from backend.chunker import chunk_documents
from backend.vectorstore import create_vector_store


# Step 1 - Load repository
print("\nLoading repository...")

documents = load_repository_files("cloned_repo")

print(f"Documents loaded: {len(documents)}")


# Step 2 - Chunk repository
print("\nCreating chunks...")

chunks = chunk_documents(documents)

print(f"Chunks created: {len(chunks)}")


# Step 3 - Create embeddings + Chroma database
print("\nCreating embeddings and vector database...")

vector_store = create_vector_store(chunks)

print("Vector database created successfully!")


# Step 4 - Test semantic search
query = "How are tasks searched?"

print(f"\nQuestion: {query}")

results = vector_store.similarity_search(
    query,
    k=3
)


# Step 5 - Display results
print("\nTop matching code chunks:")
print("=" * 70)

for index, result in enumerate(results, start=1):

    print(f"\nRESULT {index}")

    print(f"FILE: {result.metadata.get('path')}")
    print(f"CHUNK: {result.metadata.get('chunk_id')}")

    print("\nCONTENT:")
    print(result.page_content[:700])

    print("\n" + "=" * 70)