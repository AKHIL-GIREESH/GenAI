from langchain.tools import tool
from tools.obsidian_tools import *

@tool
def obsidian_read(path: str) -> str:
    """Read an Obsidian note"""
    return read_note(path)

@tool
def obsidian_search(query: str) -> str:
    """Search Obsidian notes"""
    return search_notes(query)

@tool
def obsidian_create(path: str, text: str) -> str:
    """Create a new Obsidian note"""
    return create_note(path, text)

@tool
def obsidian_append(path: str, text: str) -> str:
    """Append to an Obsidian note"""
    return append_note(path, text)

TOOLS = [
    obsidian_read,
    obsidian_search,
    obsidian_create,
    obsidian_append,
]
