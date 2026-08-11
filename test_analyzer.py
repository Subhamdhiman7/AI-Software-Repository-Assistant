from backend.repository import clone_repository
from backend.loader import load_repository_files
from backend.analyzer import analyze_repository


REPOSITORY_URL = (
    "https://github.com/Subhamdhiman7/TaskFlow-List"
)


print("\nLoading repository...")

repo_path = clone_repository(
    REPOSITORY_URL
)


print("Reading repository files...")

documents = load_repository_files(
    repo_path
)


print(
    f"Files loaded: {len(documents)}"
)


print("\nAnalyzing repository architecture...")

summary = analyze_repository(
    documents
)


print("\n")
print("=" * 70)
print("REPOMIND REPOSITORY ANALYSIS")
print("=" * 70)

print(summary)

print("=" * 70)