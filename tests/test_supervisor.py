import os
import tempfile
import json
import time
from strefi import supervisor


def test_write_running_file_should_create_temp_file():
    running_path = supervisor.write_running_file("test_file", "test_topic")
    with open(running_path, "r") as f:
        running_file_content = json.loads(f.read())
        assert running_file_content["file"] == "test_file"
        assert running_file_content["topic"] == "test_topic"
        assert time.time() - running_file_content["last_update"] < 2.0


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
