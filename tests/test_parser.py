import os
import threading
import time

import pytest

from strefi import parser, stopper

RESOURCES_PATH = "tests"


def test_yield_last_line_should_yield_new_file_row_while_running_file_exists():
    function_outputs = []
    running_path = stopper.write_running_file()
    with open(f"{RESOURCES_PATH}/parser_0.txt", "w") as f:
        f.write("")
    file_read = open(f"{RESOURCES_PATH}/parser_0.txt", "r")

    def thread_yield_last_line():
        for line in parser.yield_last_line(file_read, running_path):
            function_outputs.append(line.replace("\n", ""))

    test_thread = threading.Thread(target=thread_yield_last_line)
    test_thread.start()

    with open(f"{RESOURCES_PATH}/parser_0.txt", "a") as file_write:
        for i in range(100):
            file_write.write(f"{i}\n")
            file_write.flush()

    time.sleep(3)
    stopper.remove_running_file(running_path.split("_")[1])
    test_thread.join()

    assert function_outputs == [str(i) for i in range(100)]

    file_read.close()
    os.remove(f"{RESOURCES_PATH}/parser_0.txt")


def test_yield_last_line_should_stop_gracefully_when_file_is_removed():
    running_path = stopper.write_running_file()
    with open(f"{RESOURCES_PATH}/parser_2.txt", "w") as f:
        f.write("")
    file_read = open(f"{RESOURCES_PATH}/parser_2.txt", "r")

    def thread_delete_file():
        time.sleep(3)
        os.remove(f"{RESOURCES_PATH}/parser_2.txt")

    test_thread = threading.Thread(target=thread_delete_file)
    test_thread.start()

    for _ in parser.yield_last_line(file_read, running_path):
        continue

    assert True


@pytest.mark.timeout(10)
def test_yield_last_line_should_stop_gracefully_when_byte_is_removed():
    function_outputs = []
    running_path = stopper.write_running_file()
    with open(f"{RESOURCES_PATH}/parser_3.txt", "w") as f:
        f.write("")
    file_read = open(f"{RESOURCES_PATH}/parser_3.txt", "r")

    def thread_yield_last_line():
        for line in parser.yield_last_line(file_read, running_path):
            function_outputs.append(line.replace("\n", ""))

    test_thread = threading.Thread(target=thread_yield_last_line)
    test_thread.start()

    with open(f"{RESOURCES_PATH}/parser_3.txt", "a") as file_write:
        for i in range(100):
            file_write.write(f"{i}\n")
            file_write.flush()
        file_write.seek(0)
        time.sleep(3)
        file_write.truncate()

    test_thread.join()

    assert function_outputs == [str(i) for i in range(100)]

    file_read.close()
    os.remove(f"{RESOURCES_PATH}/parser_3.txt")


def test_stream_file_should_wait_file_creation():
    function_outputs = []
    running_path = stopper.write_running_file()

    def thread_stream_file():
        for line in parser.stream_file(f"{RESOURCES_PATH}/parser_1.txt", running_path):
            function_outputs.append(line.replace("\n", ""))

    test_thread = threading.Thread(target=thread_stream_file)
    test_thread.start()
    time.sleep(2)

    with open(f"{RESOURCES_PATH}/parser_1.txt", "w") as f:
        f.write("")

    with open(f"{RESOURCES_PATH}/parser_1.txt", "a") as file_write:
        for i in range(100):
            file_write.write(f"{i}\n")
            file_write.flush()

    time.sleep(3)
    stopper.remove_running_file(running_path.split("_")[1])
    test_thread.join()

    assert function_outputs == [str(i) for i in range(100)]

    os.remove(f"{RESOURCES_PATH}/parser_1.txt")
