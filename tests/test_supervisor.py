import json
import os
import tempfile
import threading
import time
from unittest.mock import patch

import pytest

from strefi import __main__, supervisor


def test_write_running_file_should_create_temp_file():
    running_path = supervisor.write_running_file("test_file", "test_topic")
    with open(running_path, "r") as f:
        running_file_content = json.loads(f.read())
        assert running_file_content["file"] == "test_file"
        assert running_file_content["topic"] == "test_topic"
        assert time.time() - running_file_content["heartbeat"] < 1.0


def test_remove_running_file_should_remove_one_temp_file():
    running_path = supervisor.write_running_file("foo", "foo")
    supervisor.remove_running_file(running_path.split("_")[1])
    assert not all(["strefi" in file for file in os.listdir(tempfile.gettempdir())])


def test_remove_running_file_should_remove_all_temp_file():
    supervisor.write_running_file("foo", "foo")
    supervisor.write_running_file("foo", "foo")
    supervisor.write_running_file("foo", "foo")
    supervisor.remove_running_file("all")
    assert not all(["strefi" in file for file in os.listdir(tempfile.gettempdir())])


@pytest.mark.timeout(20)
def test_update_running_file_should_update_heartbeat_while_strefi_runs():
    def start_thread_function():
        with patch(
            "sys.argv",
            ["__main__.py", "start", "-c", "tests/resources/conf/tests.json"],
        ):
            __main__.main()

    start_thread = threading.Thread(target=start_thread_function)
    update_running_file_thread = threading.Thread(target=supervisor.write_running_file, args=("foo", "foo"))

    start_thread.start()
    time.sleep(0.1)
    update_running_file_thread.start()

    running_file_paths = [
        f"{tempfile.gettempdir()}/{file}" for file in os.listdir(tempfile.gettempdir()) if "strefi" in file
    ]

    for running_file_path in running_file_paths:
        with open(running_file_path, "r") as f:
            running_file_content = json.loads(f.read())
            assert time.time() - running_file_content["heartbeat"] < 1.0

    time.sleep(16)

    for running_file_path in running_file_paths:
        with open(running_file_path, "r") as f:
            running_file_content = json.loads(f.read())
            assert time.time() - running_file_content["heartbeat"] < 1.0

    supervisor.remove_running_file("all")
