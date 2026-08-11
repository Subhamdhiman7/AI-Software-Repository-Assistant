import os
import shutil
import stat
import time

from git import Repo


REPO_PATH = "cloned_repo"


def remove_readonly(func, path, exc_info):
    """
    Handles read-only/locked Git files on Windows.
    """
    try:
        os.chmod(path, stat.S_IWRITE)
        func(path)
    except Exception:
        pass


def delete_existing_repository():
    """
    Safely removes the previously cloned repository.
    """

    if not os.path.exists(REPO_PATH):
        return

    # Retry a few times because Windows can temporarily
    # keep Git pack files locked.
    for attempt in range(3):

        try:
            shutil.rmtree(
                REPO_PATH,
                onerror=remove_readonly
            )

            return

        except PermissionError:

            if attempt < 2:
                time.sleep(1)
            else:
                raise


def clone_repository(repo_url):
    """
    Clone a GitHub repository locally and return its path.
    """

    repo_url = repo_url.strip()

    if not repo_url:
        raise ValueError(
            "Repository URL cannot be empty."
        )

    # Remove previously cloned repository
    delete_existing_repository()

    # Clone new repository
    Repo.clone_from(
        repo_url,
        REPO_PATH
    )

    return REPO_PATH