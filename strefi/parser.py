"""Provide methods to dynamically read line of a file.

The module contains the following functions:

- `yield_last_line(file, running_path)` - Yield last line of a file.
- `stream_file(file_path, running_path)` - Wait file creation before calling yield_last_line.
"""

import os
from typing import Iterator, TextIO


def yield_last_line(file: TextIO, running_path: str) -> Iterator[str]:
    """Yield last line of a file.
    This function terminates in 3 cases:
    The running file is removed, in this case all program stop.
    The streamed file is removed, in this case the program still running and waits for the file creation.
    One or more bytes were deleted from the streamed file,
    in this case the function is terminated, but it's called back just after.

    Args:
        file: Read-open file to stream.
        running_path: Path of running file. The function terminate when it's removed.

    Returns:
        Yield the last line. Ignore empty line.
    """
    file_size = 0
    file.seek(0, os.SEEK_END)
    while os.path.exists(running_path):
        try:
            new_file_size = os.path.getsize(file.name)
            if new_file_size < file_size:
                break
            else:
                file_size = new_file_size
            line = file.readline()
            if line and line not in ["\n", ""]:
                yield line
        except FileNotFoundError:
            break


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
