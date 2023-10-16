"""Provides methods to manage streams life cycle.

When a strefi start command is launched, a file is created in /tmp directory.
The stream is running while this file exists.

The module contains the following functions:

- `write_running_file()` - Create a running file in /tmp directory.
- `remove_running_file(job_id)` - Remove a running file from a job id.
"""

import os
import tempfile
import time


def write_running_file() -> str:
    """Create a running file in /tmp directory.
    The file name is composed with an ID generated and print in the stdout.
    This id identify the stream and is used to delete running file.

    Returns:
        Absolute path of the running file.
    """
    job_id = abs(hash(time.time()))
    running_file = tempfile.NamedTemporaryFile(prefix=f"strefi_{job_id}_", delete=False)
    print(job_id)
    return running_file.name


def remove_running_file(job_id: str):
    """Remove a running file from a job id.

    Args:
        job_id: job id of the running file to delete. 'all' to delete all strefi running file.
    """
    job_id = "" if job_id == "all" else job_id
    running_files = list(filter(lambda x: f"strefi_{str(job_id)}" in x, os.listdir(tempfile.gettempdir())))
    for running_file in running_files:
        os.remove(os.path.join(tempfile.gettempdir(), running_file))
