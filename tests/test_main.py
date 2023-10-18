import os
import threading
import time
from argparse import Namespace
from unittest.mock import patch

import pytest
from kafka import KafkaConsumer

from strefi import __main__, stopper


def test_parse_args_should_return_namespace():
    args_start = ["start", "-c", "test.json"]
    args_stop = ["stop", "-i", "91262"]

    namespace_start = __main__.parse_args(args_start)
    namespace_stop = __main__.parse_args(args_stop)

    assert namespace_start == Namespace(command="start", config="test.json", jobid=None)
    assert namespace_stop == Namespace(command="stop", config=None, jobid="91262")


def test_parse_args_should_raises_error_when_args_are_invalids():
    # unknown command
    with pytest.raises(SystemExit):
        __main__.parse_args(["unknown"])

    # missing config file path with start command
    with pytest.raises(SystemExit):
        __main__.parse_args(["start"])

    # missing job id with stop command
    with pytest.raises(SystemExit):
        __main__.parse_args(["stop"])


def test_start_should_run_strefi():
    consumed_record_values = []
    consumed_record_headers = []

    def write_file_thread_function(file_path, prefix):
        with open(file_path, "w") as f:
            for i in range(100):
                f.write(f"{prefix}_{i}\n")
                time.sleep(0.01)

    def consumer_thread_function():
        consumer = KafkaConsumer("strefi-tests", bootstrap_servers="localhost:9092", consumer_timeout_ms=5000)
        for record in consumer:
            consumed_record_values.append(record.value)
            consumed_record_headers.append(record.headers)

    def start_thread_function():
        with patch("sys.argv", ["__main__.py", "start", "-c", "tests/resources/conf/tests.json"]):
            __main__.main()

    def get_target_records():
        record_base = (
            """{{"file": "{0}", "row": "{1}", "hostname": "lpt01", "system": "Linux", "version": "22.04.1-Ubuntu"}}"""
        )
        return [record_base.format("test_file_0.log", f"file_a_{i}\\n").encode() for i in range(100)] + [
            record_base.format("test_file_1.log", f"file_b_{i}\\n").encode() for i in range(100)
        ]

    write_file_thread_a = threading.Thread(target=write_file_thread_function, args=("test_file_0.log", "file_a"))
    write_file_thread_b = threading.Thread(target=write_file_thread_function, args=("test_file_1.log", "file_b"))
    consumer_thread = threading.Thread(target=consumer_thread_function)
    start_thread = threading.Thread(target=start_thread_function)

    start_thread.start()
    consumer_thread.start()
    write_file_thread_a.start()
    write_file_thread_b.start()

    time.sleep(5)
    with patch("sys.argv", ["__main__.py", "stop", "-i", "all"]):
        __main__.main()

    consumer_thread.join()
    start_thread.join()
    write_file_thread_a.join()
    write_file_thread_b.join()

    assert sorted(get_target_records()) == sorted(consumed_record_values)
    assert consumed_record_headers == [[("version", b"0.1"), ("type", b"json")] for _ in range(200)]


def test_stop_should_kill_strefi():
    running_path_a = stopper.write_running_file()
    with patch("sys.argv", ["__main__.py", "stop", "-i", f"{running_path_a.split('_')[1]}"]):
        __main__.main()
    assert not os.path.exists(running_path_a)

    running_path_b = stopper.write_running_file()
    running_path_c = stopper.write_running_file()
    with patch("sys.argv", ["__main__.py", "stop", "-i", "all"]):
        __main__.main()
    assert not os.path.exists(running_path_b)
    assert not os.path.exists(running_path_c)
