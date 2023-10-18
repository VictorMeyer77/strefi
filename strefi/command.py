"""Provides strefi main functions.

The module contains the following functions:

- `stream_file_to_topic(file_path, producer, topic, defaults, headers, running_path)` -
Stream file and write last row to a kafka topic.
- `create_threads(config)` - Create one thread by table from all the configuration.
- `start(config_path)` - Read configuration file and launch all streams.
- `stop(jobid)` - Stop strefi threads.
"""
import json
import threading
from typing import Any

from kafka import KafkaProducer

from strefi import kafka_utils, parser, stopper


def stream_file_to_topic(
    file_path: str,
    producer: KafkaProducer,
    topic: str,
    defaults: dict[str, object],
    headers: dict[str, object],
    running_path: str,
):
    """Stream file and write last row to a kafka topic.

    Args:
        file_path: File path to stream.
        producer: Instance of KafkaProducer.
        topic: Name of the target topic.
        defaults: Configured dictionary to add in the record value.
        headers: Configured headers dictionary.
        running_path: Running file path
    """
    for line in parser.stream_file(file_path, running_path):
        producer.send(topic, kafka_utils.format_record_value(file_path, line, defaults).encode(), headers=headers)


def create_threads(config: dict[str, Any]) -> list[threading.Thread]:
    """Create one thread by table from all the configuration.

    Args:
        config: dictionary loads from configuration file.

    Returns:
        List composed by one thread per file to stream.
    """
    threads = []
    headers = kafka_utils.format_record_headers(config["headers"])
    running_path = stopper.write_running_file()

    for file in config["files"].keys():
        producer = kafka_utils.create_producer(config["producer"])
        topic = config["files"][file]
        thread = threading.Thread(
            target=stream_file_to_topic,
            args=(file, producer, topic, config["defaults"], headers, running_path),
        )
        threads.append(thread)

    return threads


def start(config_path: str):
    """Read configuration file and launch all streams.
    This function is the entrypoint of stefi start command.

    Args:
        config_path: Configuration file path.
    """
    with open(config_path, "r") as f:
        config = json.loads(f.read())
    threads = create_threads(config)
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()


def stop(jobid: str):
    """Stop strefi threads.
    This function is the entrypoint of strefi stop command.

    Args:
        jobid: ID of the stream to kill, 'all' to kill all streams.
    """
    stopper.remove_running_file(jobid)
