from pathlib import Path

ALLOWED_PATH = Path("payload.txt").resolve()


def file_retriever(path: str) -> str:
    """Read payload.txt and return its text content."""
    if Path(path).resolve() != ALLOWED_PATH:
        return "Access denied."
    return ALLOWED_PATH.read_text()
