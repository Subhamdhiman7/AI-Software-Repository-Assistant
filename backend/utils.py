import os


# ============================================================
# FILE HELPERS
# ============================================================

def get_filename(path):
    return os.path.basename(path)


def get_extension(path):
    return os.path.splitext(path)[1].lower()


# ============================================================
# PROJECT NAME
# ============================================================

def get_project_name(repo_path):
    return os.path.basename(repo_path)


# ============================================================
# LANGUAGE DETECTION
# ============================================================

LANGUAGE_MAP = {
    ".py": "Python",
    ".js": "JavaScript",
    ".jsx": "React JavaScript",
    ".ts": "TypeScript",
    ".tsx": "React TypeScript",
    ".java": "Java",
    ".cpp": "C++",
    ".c": "C",
    ".cs": "C#",
    ".go": "Go",
    ".php": "PHP",
    ".rb": "Ruby",
    ".swift": "Swift",
    ".html": "HTML",
    ".css": "CSS",
}


def detect_languages(documents):

    languages = set()

    for doc in documents:

        path = doc.get("path", "")

        ext = get_extension(path)

        if ext in LANGUAGE_MAP:
            languages.add(LANGUAGE_MAP[ext])

    return sorted(languages)


# ============================================================
# FRAMEWORK DETECTION
# ============================================================

FRAMEWORKS = {
    "react": "React",
    "next": "Next.js",
    "vite": "Vite",
    "fastapi": "FastAPI",
    "flask": "Flask",
    "django": "Django",
    "streamlit": "Streamlit",
    "express": "Express",
    "spring": "Spring Boot",
}


def detect_frameworks(documents):

    frameworks = set()

    for doc in documents:

        content = doc.get("content", "").lower()

        for key, value in FRAMEWORKS.items():

            if key in content:

                frameworks.add(value)

    return sorted(frameworks)


# ============================================================
# ENTRY FILES
# ============================================================

ENTRY_FILES = {
    "main.py",
    "app.py",
    "main.jsx",
    "main.tsx",
    "main.js",
    "index.js",
    "index.jsx",
    "index.html",
}


def find_entry_points(documents):

    files = []

    for doc in documents:

        name = get_filename(doc.get("path", ""))

        if name in ENTRY_FILES:
            files.append(doc.get("path"))

    return files


# ============================================================
# IMPORTANT FILES
# ============================================================

IMPORTANT = {
    "readme.md",
    "package.json",
    "requirements.txt",
    "pyproject.toml",
    "dockerfile",
    "pom.xml",
}


def important_files(documents):

    files = []

    for doc in documents:

        name = get_filename(doc.get("path", "")).lower()

        if name in IMPORTANT:
            files.append(doc.get("path"))

    return files