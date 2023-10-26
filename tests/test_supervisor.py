import json
import os
import re
import tempfile
import threading
import time

from strefi import supervisor


def test_write_running_file_should_create_temp_file():
    running_path = supervisor.write_running_file("test_file", "test_topic")
    with open(running_path, "r") as f:
        running_file_content = json.loads(f.read())
        assert running_file_content["file"] == "test_file"
        assert running_file_content["topic"] == "test_topic"
        assert time.time() - running_file_content["heartbeat"] < 1.0
    supervisor.remove_running_file("all")


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


def test_update_running_file_should_update_heartbeat_while_threads_run():
    running_file_path_a = supervisor.write_running_file("foo", "foo")
    running_file_path_b = supervisor.write_running_file("foo", "foo")

    thread_a = threading.Thread(target=time.sleep, args=(15.5,), name=running_file_path_a)
    thread_b = threading.Thread(target=time.sleep, args=(15.5,), name=running_file_path_b)

    thread_a.start()
    thread_b.start()

    supervisor.update_running_file()

    for running_file_path in [running_file_path_a, running_file_path_b]:
        with open(running_file_path, "r") as f:
            running_file_content = json.loads(f.read())
            assert time.time() - running_file_content["heartbeat"] - 15.0 < 0.5

    supervisor.remove_running_file("all")


def test_get_job_status_should_return_thread_summary():
    running_file_path_a = supervisor.write_running_file("file_a", "topic_a")
    time.sleep(16)
    running_file_path_b = supervisor.write_running_file("file_b", "topic_b")
    running_file_path_c = supervisor.write_running_file("file_c", "topic_c")

    assert sorted(supervisor.get_job_status(), key=lambda d: d["file"]) == [
        {
            "job_id": re.findall(r"strefi_([a-zA-Z0-9]*)_", running_file_path_a)[0],
            "file": "file_a",
            "topic": "topic_a",
            "status": False,
        },
        {
            "job_id": re.findall(r"strefi_([a-zA-Z0-9]*)_", running_file_path_b)[0],
            "file": "file_b",
            "topic": "topic_b",
            "status": True,
        },
        {
            "job_id": re.findall(r"strefi_([a-zA-Z0-9]*)_", running_file_path_c)[0],
            "file": "file_c",
            "topic": "topic_c",
            "status": True,
        },
    ]

    supervisor.remove_running_file("all")
