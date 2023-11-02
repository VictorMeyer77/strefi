"""Provides methods to manage streams life cycle.

When a strefi start command is launched, a file is created in /tmp directory.
The stream is running while this file exists.

The module contains the following functions:

- `write_running_file()` - Create a running file in /tmp directory.
- `remove_running_file(job_id)` - Remove a running file from a job id.
- `update_running_file()` - Update the heartbeat timestamp in whole running file of active threads.
- `get_job_status()` - Return a list of all strefi threads with current status.

Examples:
    >>> # Content of a running file
    >>> {"file": "streamed_file_path", "topic": "kafka_topic", "heartbeat": 1698262227.0394928}
"""

import json
import logging
import os
import re
import tempfile
import threading
import time

logger = logging.getLogger(__name__)

RUNNING_FILE_PATTERN = """{{

"file": "{0}",
"topic": "{1}",
"heartbeat": {2}

}}"""


def write_running_file(streamed_file_path: str, topic: str) -> str:
    """Create a running file in /tmp directory.
    The file name is composed with an ID generated.
    This id identify the stream and is used to delete running file.

    Returns:
        Absolute path of the running file.
    """
    job_id = abs(hash(time.time()))
    running_file = tempfile.NamedTemporaryFile(prefix=f"strefi_{job_id}_", delete=False)
    with open(running_file.name, "w") as f:
        f.write(RUNNING_FILE_PATTERN.format(streamed_file_path, topic, time.time()))
        logger.debug(f"Running file was created {running_file.name}.")
    return running_file.name


def update_running_file():
    """Update the heartbeat timestamp in whole running file of active threads.
    The heartbeat is updated every 15 seconds. If the heartbeat is older than 15 seconds, the strefi thread is dead.
    """
    active_thread_running_paths = [thread.name for thread in threading.enumerate() if "strefi_" in thread.name]
    if active_thread_running_paths:
        for running_path in active_thread_running_paths:
            with open(running_path, "r") as f:
                running_info = json.loads(f.read())
            with open(running_path, "w") as f:
                f.write(RUNNING_FILE_PATTERN.format(running_info["file"], running_info["topic"], time.time()))
            logger.debug(f"{running_path} heartbeat was updated.")
        time.sleep(15)
        update_running_file()


def remove_running_file(job_id: str):
    """Remove a running file from a job id.

    Args:
        job_id: job id of the running file to delete. 'all' to delete all strefi running file.
    """
    job_id = "" if job_id == "all" else job_id
    running_file_names = [file for file in os.listdir(tempfile.gettempdir()) if f"strefi_{str(job_id)}" in file]
    for running_file_name in running_file_names:
        os.remove(os.path.join(tempfile.gettempdir(), running_file_name))
        logger.debug(f"{os.path.join(tempfile.gettempdir(), running_file_name)} was removed.")


def get_job_status() -> list[dict[str, object]]:
    """Return a list of all strefi threads with current status.
    If status == True, the thread is active, if status == False the thread is dead.

    Examples:
        >>> get_job_status()
        [{'job_id': '163892105422928641', 'file': 'file_a', 'topic': 'topic_a', 'status': False}]

    Returns:
        list metadata dictionaries
    """
    job_status = []
    running_file_names = [file for file in os.listdir(tempfile.gettempdir()) if "strefi" in file]
    for running_file_name in running_file_names:
        with open(os.path.join(tempfile.gettempdir(), running_file_name), "r") as f:
            running_info = json.loads(f.read())
            job_status.append(
                {
                    "job_id": re.findall(r"strefi_([a-zA-Z0-9]*)_", running_file_name)[0],
                    "file": running_info["file"],
                    "topic": running_info["topic"],
                    "status": True if time.time() - running_info["heartbeat"] < 16 else False,
                }
            )
    return job_status
