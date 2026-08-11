from backend.loader import load_repository_files
from backend.chunker import chunk_documents


# Step 1: Load repository files
documents = load_repository_files("cloned_repo")

print(f"\nDocuments loaded: {len(documents)}")


# Step 2: Break documents into smaller chunks
chunks = chunk_documents(documents)

print(f"Chunks created: {len(chunks)}")
print("=" * 60)


# Step 3: Display first 5 chunks
for chunk in chunks[:5]:

    print(f"\nFILE: {chunk['path']}")
    print(f"CHUNK ID: {chunk['chunk_id']}")
    print(f"SIZE: {len(chunk['content'])}")

    print("\nCONTENT:")
    print(chunk["content"][:400])

    print("\n" + "=" * 60)