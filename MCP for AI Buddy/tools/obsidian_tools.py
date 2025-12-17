from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()

VAULT_PATH = Path(os.getenv("FOLDER_PATH"))

def read_note(path: str) -> str:
    file = VAULT_PATH / path
    return file.read_text() if file.exists() else "Note not found."

def search_notes(query: str) -> str:
    matches = []
    for md in VAULT_PATH.rglob("*.md"):
        if query.lower() in md.read_text().lower():
            matches.append(md.relative_to(VAULT_PATH).as_posix())
    return "\n".join(matches) or "No matches found."

def append_to_note(path: str, text: str) -> str:
    file = VAULT_PATH / path
    with open(file, "a") as f:
        f.write("\n" + text)
    return "Appended successfully."

def create_note(path: str, text: str) -> str:
    file = VAULT_PATH / path
    file.parent.mkdir(parents=True, exist_ok=True)
    file.write_text(text)
    return "Note created."
