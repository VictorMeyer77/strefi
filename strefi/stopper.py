import tempfile
import time
import os


def write_running_file():
    job_id = abs(hash(time.time()))
    running_file = tempfile.NamedTemporaryFile(prefix=f"creno_{job_id}_", delete=False)
    print(job_id)
    return running_file.name


def remove_running_file(job_id):
    job_id = "" if job_id == "all" else job_id
    running_files = list(filter(lambda x: f"creno_{str(job_id)}" in x, os.listdir(tempfile.gettempdir())))
    [os.remove(os.path.join(tempfile.gettempdir(), running_file)) for running_file in running_files]
