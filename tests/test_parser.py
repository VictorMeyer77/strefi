import os
import threading
import time

import pytest

from strefi import parser, supervisor

RESOURCES_PATH = "tests"


def test_yield_last_lines_should_yield_new_rows_from_current_position():
    function_outputs = []
    running_path = supervisor.write_running_file("foo", "foo")
    with open(f"{RESOURCES_PATH}/parser_0.txt", "w") as f:
        f.write("0\n1\n2\n")
    file_read = open(f"{RESOURCES_PATH}/parser_0.txt", "r")

    def thread_yield_last_lines():
        for line in parser.yield_last_lines(file_read, running_path):
            function_outputs.append(line.replace("\n", ""))

    test_thread = threading.Thread(target=thread_yield_last_lines)
    test_thread.start()
    time.sleep(1)

    with open(f"{RESOURCES_PATH}/parser_0.txt", "a") as file_write:
        for i in range(3, 100):
            file_write.write(f"{i}\n")
            file_write.flush()

    time.sleep(3)
    supervisor.remove_running_file("all")

    assert function_outputs == [str(i) for i in range(100)]

    file_read.close()
    os.remove(f"{RESOURCES_PATH}/parser_0.txt")


@pytest.mark.timeout(10)
def test_yield_last_lines_should_stop_gracefully_when_file_is_removed():
    running_path = supervisor.write_running_file("foo", "foo")
    with open(f"{RESOURCES_PATH}/parser_2.txt", "w") as f:
        f.write("")
    file_read = open(f"{RESOURCES_PATH}/parser_2.txt", "r")

    def thread_delete_file():
        time.sleep(3)
        os.remove(f"{RESOURCES_PATH}/parser_2.txt")

    test_thread = threading.Thread(target=thread_delete_file)
    test_thread.start()

    for _ in parser.yield_last_lines(file_read, running_path):
        continue

    assert True

    supervisor.remove_running_file("all")


@pytest.mark.timeout(10)
def test_yield_last_lines_should_stop_gracefully_when_byte_is_removed():
    running_path = supervisor.write_running_file("foo", "foo")
    with open(f"{RESOURCES_PATH}/parser_3.txt", "w") as f:
        f.write("")
    file_read = open(f"{RESOURCES_PATH}/parser_3.txt", "r")

    def thread_remove_bytes():
        time.sleep(2)
        with open(f"{RESOURCES_PATH}/parser_3.txt", "a") as file_write:
            file_write.write("0\n1\n2\n")
            file_write.flush()
            time.sleep(0.25)
            file_write.seek(0)
            file_write.truncate()

    test_thread = threading.Thread(target=thread_remove_bytes)
    test_thread.start()

    for _ in parser.yield_last_lines(file_read, running_path):
        continue

    assert True

    supervisor.remove_running_file("all")
    file_read.close()
    os.remove(f"{RESOURCES_PATH}/parser_3.txt")


def test_stream_file_should_wait_file_creation():
    function_outputs = []
    running_path = supervisor.write_running_file("foo", "foo")

    def thread_stream_file():
        for line in parser.stream_file(f"{RESOURCES_PATH}/parser_1.txt", running_path):
            function_outputs.append(line.replace("\n", ""))

    test_thread = threading.Thread(target=thread_stream_file)
    test_thread.start()
    time.sleep(2)

    with open(f"{RESOURCES_PATH}/parser_1.txt", "a") as file_write:
        for i in range(100):
            file_write.write(f"{i}\n")
            file_write.flush()

    time.sleep(3)
    supervisor.remove_running_file("all")

    assert function_outputs == [str(i) for i in range(100)]

    os.remove(f"{RESOURCES_PATH}/parser_1.txt")


def test_stream_file_should_stream_from_beginning_when_true():
    function_outputs = []
    running_path = supervisor.write_running_file("foo", "foo")
    with open(f"{RESOURCES_PATH}/parser_4.txt", "w") as f:
        f.write("0\n1\n2\n")

    def thread_stream_file():
        for line in parser.stream_file(f"{RESOURCES_PATH}/parser_4.txt", running_path, from_beginning=True):
            function_outputs.append(line.replace("\n", ""))

    test_thread = threading.Thread(target=thread_stream_file)
    test_thread.start()
    time.sleep(1)

    with open(f"{RESOURCES_PATH}/parser_4.txt", "a") as file_write:
        for i in range(3, 100):
            file_write.write(f"{i}\n")
            file_write.flush()

    time.sleep(3)
    supervisor.remove_running_file("all")

    assert function_outputs == [str(i) for i in range(100)]

    os.remove(f"{RESOURCES_PATH}/parser_4.txt")


def test_stream_file_should_stream_from_end_when_false():
    function_outputs = []
    running_path = supervisor.write_running_file("foo", "foo")
    with open(f"{RESOURCES_PATH}/parser_5.txt", "w") as f:
        f.write("0\n1\n2\n")

    def thread_stream_file():
        for line in parser.stream_file(f"{RESOURCES_PATH}/parser_5.txt", running_path, from_beginning=False):
            function_outputs.append(line.replace("\n", ""))

    test_thread = threading.Thread(target=thread_stream_file)
    test_thread.start()
    time.sleep(1)

    with open(f"{RESOURCES_PATH}/parser_5.txt", "a") as file_write:
        for i in range(3, 100):
            file_write.write(f"{i}\n")
            file_write.flush()

    time.sleep(3)
    supervisor.remove_running_file("all")

    assert function_outputs == [str(i) for i in range(3, 100)]

    os.remove(f"{RESOURCES_PATH}/parser_5.txt")


# The function file_rows_to_topic is too high-level to be tested here, its test is included in test_main.py
