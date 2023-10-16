import os
import tempfile

from strefi import stopper


def test_write_running_file_should_create_temp_file():
    running_path = stopper.write_running_file()
    assert os.path.exists(running_path)


def test_remove_running_file_should_remove_one_temp_file():
    running_path = stopper.write_running_file()
    stopper.remove_running_file(running_path.split("_")[1])
    assert not all(["strefi" in file for file in os.listdir(tempfile.gettempdir())])


def test_remove_running_file_should_remove_all_temp_file():
    stopper.write_running_file()
    stopper.write_running_file()
    stopper.write_running_file()
    stopper.remove_running_file("all")
    assert not all(["strefi" in file for file in os.listdir(tempfile.gettempdir())])
