import os


# ============================================================
# SUPPORTED SOURCE / CONFIG FILE EXTENSIONS
# ============================================================

SUPPORTED_EXTENSIONS = {
    # Python
    ".py",

    # JavaScript / TypeScript
    ".js",
    ".jsx",
    ".ts",
    ".tsx",

    # Web
    ".html",
    ".htm",
    ".css",
    ".scss",
    ".sass",
    ".less",

    # Java / JVM
    ".java",
    ".kt",
    ".kts",

    # C / C++
    ".c",
    ".h",
    ".cpp",
    ".cc",
    ".cxx",
    ".hpp",

    # C#
    ".cs",

    # Go
    ".go",

    # Rust
    ".rs",

    # PHP
    ".php",

    # Ruby
    ".rb",

    # Swift
    ".swift",

    # Shell
    ".sh",
    ".bash",
    ".zsh",

    # SQL
    ".sql",

    # Config / data
    ".json",
    ".yaml",
    ".yml",
    ".toml",
    ".xml",

    # Documentation
    ".md",
    ".txt"
}


# ============================================================
# IMPORTANT FILES WITHOUT NORMAL EXTENSIONS
# ============================================================

IMPORTANT_FILENAMES = {
    "dockerfile",
    "makefile",
    "procfile",
    "gemfile",
    "rakefile"
}


# ============================================================
# DIRECTORIES TO IGNORE
# ============================================================

IGNORED_DIRECTORIES = {
    ".git",
    ".github",

    # JavaScript
    "node_modules",
    ".next",
    ".nuxt",

    # Python
    "venv",
    ".venv",
    "env",
    ".env",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",

    # Build output
    "dist",
    "build",
    "out",
    "target",

    # IDE
    ".idea",
    ".vscode",

    # Testing / generated
    "coverage",
    ".coverage",
    "htmlcov",

    # Cache
    ".cache",
    ".parcel-cache",
    ".turbo"
}


# ============================================================
# FILES TO IGNORE
# ============================================================

IGNORED_FILENAMES = {
    # Lock files can be extremely large and usually provide
    # little value for repository understanding.
    "package-lock.json",
    "yarn.lock",
    "pnpm-lock.yaml",
    "poetry.lock",
    "composer.lock",
    "cargo.lock",

    # OS files
    ".ds_store",
    "thumbs.db",

    # Common generated metadata
    "npm-debug.log",
    "yarn-error.log"
}


# ============================================================
# FILE SIZE LIMIT
# ============================================================

# 500 KB per source file.
#
# This prevents generated/minified/huge files from creating
# thousands of chunks and slowing down RepoMind.
MAX_FILE_SIZE = 500 * 1024


# ============================================================
# REPOSITORY FILE LIMIT
# ============================================================

# Safety limit for public repositories.
#
# Later we can make this configurable.
MAX_FILES = 1500


# ============================================================
# CHECK DIRECTORY
# ============================================================

def should_ignore_directory(directory_name):
    """
    Return True if a directory should not be scanned.
    """

    return directory_name.lower() in {
        item.lower()
        for item in IGNORED_DIRECTORIES
    }


# ============================================================
# CHECK FILE
# ============================================================

def should_ignore_file(filename):
    """
    Return True if the file should be ignored.
    """

    lower_name = filename.lower()

    if lower_name in {
        item.lower()
        for item in IGNORED_FILENAMES
    }:
        return True

    # Ignore common minified/generated frontend files.
    if lower_name.endswith(".min.js"):
        return True

    if lower_name.endswith(".min.css"):
        return True

    if lower_name.endswith(".map"):
        return True

    return False


# ============================================================
# CHECK SUPPORTED FILE
# ============================================================

def is_supported_file(filename):
    """
    Determine whether RepoMind should read this file.
    """

    lower_name = filename.lower()

    # Special files such as Dockerfile
    if lower_name in IMPORTANT_FILENAMES:
        return True

    extension = os.path.splitext(
        lower_name
    )[1]

    return extension in SUPPORTED_EXTENSIONS


# ============================================================
# DETECT POSSIBLE BINARY FILE
# ============================================================

def is_binary_file(file_path):
    """
    Perform a lightweight binary-file check.

    Source files should contain normal text. If null bytes
    appear in the first few KB, the file is almost certainly
    binary.
    """

    try:

        with open(
            file_path,
            "rb"
        ) as file:

            sample = file.read(
                4096
            )

        return b"\x00" in sample

    except OSError:

        return True


# ============================================================
# READ TEXT FILE
# ============================================================

def read_text_file(file_path):
    """
    Read a repository file safely.

    UTF-8 is preferred. Invalid characters are replaced
    rather than crashing the repository loader.
    """

    try:

        with open(
            file_path,
            "r",
            encoding="utf-8",
            errors="replace"
        ) as file:

            return file.read()

    except (
        OSError,
        UnicodeError
    ):

        return None


# ============================================================
# LOAD REPOSITORY
# ============================================================

def load_repository_files(repo_path):
    """
    Scan a cloned repository and return useful text/source
    files.

    Output format:

    [
        {
            "path": "src/App.jsx",
            "content": "..."
        }
    ]
    """

    documents = []

    if not os.path.isdir(repo_path):
        return documents


    # ========================================================
    # WALK REPOSITORY
    # ========================================================

    for root, directories, files in os.walk(
        repo_path
    ):

        # ----------------------------------------------------
        # Remove ignored directories IN PLACE.
        #
        # This prevents os.walk from entering node_modules,
        # .git, venv, dist, etc.
        # ----------------------------------------------------

        directories[:] = [
            directory
            for directory in directories
            if not should_ignore_directory(
                directory
            )
        ]


        # ----------------------------------------------------
        # PROCESS FILES
        # ----------------------------------------------------

        for filename in files:

            if len(documents) >= MAX_FILES:
                return documents


            # Ignore lock/generated files
            if should_ignore_file(
                filename
            ):
                continue


            # Ignore unsupported extensions
            if not is_supported_file(
                filename
            ):
                continue


            file_path = os.path.join(
                root,
                filename
            )


            # ------------------------------------------------
            # FILE SIZE
            # ------------------------------------------------

            try:

                file_size = os.path.getsize(
                    file_path
                )

            except OSError:

                continue


            if file_size == 0:
                continue


            if file_size > MAX_FILE_SIZE:
                continue


            # ------------------------------------------------
            # BINARY CHECK
            # ------------------------------------------------

            if is_binary_file(
                file_path
            ):
                continue


            # ------------------------------------------------
            # READ FILE
            # ------------------------------------------------

            content = read_text_file(
                file_path
            )

            if content is None:
                continue


            # Ignore files containing only whitespace
            if not content.strip():
                continue


            # ------------------------------------------------
            # RELATIVE PATH
            # ------------------------------------------------

            relative_path = os.path.relpath(
                file_path,
                repo_path
            )


            # Normalize Windows paths:
            #
            # src\App.jsx
            #
            # becomes
            #
            # src/App.jsx
            # ------------------------------------------------

            relative_path = relative_path.replace(
                "\\",
                "/"
            )


            # ------------------------------------------------
            # STORE DOCUMENT
            # ------------------------------------------------

            documents.append(
                {
                    "path": relative_path,
                    "content": content
                }
            )


    return documents