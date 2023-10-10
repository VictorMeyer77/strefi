import kafka_utils
import threading
import parser
import json
import stopper


def stream_file_to_topic(file_path, producer, topic, defaults, headers, running_path):
    for line in parser.stream_file(file_path, running_path):
        producer.send(
            topic,
            kafka_utils.create_record(file_path, line, defaults).encode(),
            headers=headers,
        )
        producer.flush()


def create_threads(config):
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


def start(config_path):
    with open(config_path, "r") as f:
        config = json.loads(f.read())
    threads = create_threads(config)
    [thread.start() for thread in threads]
    [thread.join() for thread in threads]


def stop(jobid):
    stopper.remove_running_file(jobid)
