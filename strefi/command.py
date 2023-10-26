"""Provides strefi main functions.

The module contains the following functions:

- `start(config_path)` - Read configuration file and launch all streams.
- `stop(jobid)` - Stop strefi threads.
- `ls()` - Display jobs with their status.
"""
import json
import re
import threading

from strefi import kafka_utils, parser, supervisor


def start(config_path: str):
    """Read configuration file and launch all streams.
    This function is the entrypoint of stefi start command.
    One thread with his own producer will be launched for each file.

    Args:
        config_path: Configuration file path.
    """
    with open(config_path, "r") as f:
        config = json.loads(f.read())

    headers = kafka_utils.format_record_headers(config["headers"])

    for file in config["files"].keys():
        producer = kafka_utils.create_producer(config["producer"])
        topic = config["files"][file]
        running_path = supervisor.write_running_file(file, config["files"][file])
        thread = threading.Thread(
            target=parser.file_rows_to_topic,
            args=(file, topic, producer, config["defaults"], headers, running_path),
            name=running_path,
        )
        print(f"{re.findall(r'strefi_([a-zA-Z0-9]*)_', running_path)[0]}: {file} --> {topic}")
        thread.start()

    supervisor.update_running_file()


def stop(jobid: str):
    """Stop strefi threads.
    This function is the entrypoint of strefi stop command.

    Args:
        jobid: ID of the stream to kill, 'all' to kill all streams.
    """
    supervisor.remove_running_file(jobid)


def ls():
    """Display jobs with their status."""
    jobs = supervisor.get_job_status()
    for job in jobs:
        status = "\033[92m RUNNING \033[00m" if job["status"] else "\033[91m FAILED \033[00m"
        print(f"{job['job_id']} \t {job['file']} \t {job['topic']} \t {status}")
