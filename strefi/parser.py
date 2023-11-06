"""Provide methods to dynamically read line of a file.

The module contains the following functions:

- `yield_last_lines(file, running_path)` - Yield lines of a file from current position.
- `stream_file(file_path, running_path, from_beginning)` - Wait creation and open file before calling yield_last_lines.
- `file_rows_to_topic(file_path, topic, producer, defaults, headers, running_path)` -
Stream file and write last row in a kafka topic.
"""

import logging
import os
import time
from typing import Iterator, TextIO

from kafka import KafkaProducer

from strefi import kafka_utils

logger = logging.getLogger(__name__)


def yield_last_lines(file: TextIO, running_path: str) -> Iterator[str]:
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
    logger.info(f"Starting stream {file.name}.")
    file_size = 0
    while os.path.exists(running_path):
        try:
            new_file_size = os.path.getsize(file.name)
            if new_file_size < file_size:
                logger.info(f"Some bytes were removed from {file.name}. Streaming finished.")
                break
            else:
                file_size = new_file_size
            lines = file.readlines()
            for line in lines:
                if line and line not in ["\n", ""]:
                    yield line
            time.sleep(0.5)
        except FileNotFoundError:
            logger.info(f"{file.name} was removed. Streaming finished.")
            break


def stream_file(file_path: str, running_path: str, from_beginning: bool = True) -> Iterator[str]:
    """Wait file creation before calling yield_last_lines.
        Choose this method if you want stream log file which doesn't exist yet.

    Args:
        file_path: File path to stream.
        running_path: Path of running file. The function terminate when it's removed.
        from_beginning: If true, whole file will be streamed, if false, just new rows will be streamed.

    Returns:
        Yield the last line. Ignore empty line.
    """
    while os.path.exists(running_path):
        if os.path.exists(file_path):
            with open(file_path, "r") as file:
                if not from_beginning:
                    file.seek(0, os.SEEK_END)
                yield from yield_last_lines(file, running_path)
        from_beginning = True


def file_rows_to_topic(
    file_path: str,
    topic: str,
    producer: KafkaProducer,
    defaults: dict[str, object],
    headers: dict[str, object],
    running_path: str,
):
    """Stream file and write last row in a kafka topic.
    This function is the streamed file thread entrypoint.

    Args:
        file_path: File path to stream.
        topic: Name of the target topic.
        producer: Instance of KafkaProducer.
        defaults: Configured dictionary to add in the record value.
        headers: Configured headers dictionary.
        running_path: Running file path
    """
    try:
        for line in stream_file(file_path, running_path, from_beginning=False):
            producer.send(topic, kafka_utils.format_record_value(file_path, line, defaults).encode(), headers=headers)
    except Exception as e:  # pragma: no cover
        logger.error(e)
        raise e
