import os


def get_last_line(file, running_path):
    file.seek(0, os.SEEK_END)
    while os.path.exists(running_path):
        line = file.readline()
        if line and line not in ["\n", ""]:
            yield line


def stream_file(file_path, running_path):
    while os.path.exists(running_path):
        if os.path.exists(file_path):
            with open(file_path, "r") as file:
                for line in get_last_line(file, running_path):
                    yield line
