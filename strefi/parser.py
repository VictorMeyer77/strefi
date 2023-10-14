"""Provide methods to dynamically read line of a file.

The module contains the following functions:

- `yield_last_line(file, running_path)` - Yield last line of a file.
- `stream_file(file_path, running_path)` - Wait file creation before calling yield_last_line.

"""

import os
from typing import Iterator, TextIO


def yield_last_line(file: TextIO, running_path: str) -> Iterator[str]:
    """Yield last line of a file.

    Args:
        file: Read-open file to stream.
        running_path: Path of running file. The function terminate when it's removed.

    Returns:
        Yield the last line. Ignore empty line.
    """
    file.seek(0, os.SEEK_END)
    while os.path.exists(running_path):
        line = file.readline()
        if line and line not in ["\n", ""]:
            yield line


def stream_file(file_path: str, running_path: str) -> Iterator[str]:
    """Wait file creation before calling yield_last_line.
        Choose this method if you want stream log file which doesn't exist yet.

    Args:
        file_path: File path to stream.
        running_path: Path of running file. The function terminate when it's removed.

    Returns:
        Yield the last line. Ignore empty line.
    """
    while os.path.exists(running_path):
        if os.path.exists(file_path):
            with open(file_path, "r") as file:
                for line in yield_last_line(file, running_path):
                    yield line
