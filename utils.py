from keyboard import KeyboardEvent
import os
from typing import List


def to_utf(event: KeyboardEvent):
    if len(event.name) == 1:
        return event.name
    elif event.name == "tab":
        return "\t"
    elif event.name == "return":
        return "\n"
    elif event.name == "space":
        return " "
    return None


def list_top_level_files(directory: str) -> List[str]:
    try:
        # Check if path exists, is a directory, and is readable
        if not os.path.isdir(directory) or not os.access(directory, os.R_OK):
            return []

        files = []
        with os.scandir(directory) as entries:
            for entry in entries:
                if entry.is_file(follow_symlinks=False):
                    files.append(entry.path)

        return files

    except (PermissionError, FileNotFoundError, OSError):
        # Covers unreadable dirs, race conditions, etc.
        return []
