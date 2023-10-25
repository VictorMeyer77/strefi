import os
import tempfile

from strefi import supervisor


def test_write_running_file_should_create_temp_file():
    running_path = supervisor.write_running_file("foo", "foo")
    assert os.path.exists(running_path)


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
