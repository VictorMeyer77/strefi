# Getting Started

## Installation

PyPi

```shell
pip install strefi
```

Git

```shell
git clone https://github.com/VictorMeyer77/strefi.git
cd strefi
make virtualenv # if you want create new environment
source .venv/bin/activate # if you want activate the new environment
make install
```

## Usage

```txt
usage: strefi [-h] [-c CONFIG] [-i JOBID] [-l LOG] command

Stream each new rows of a file and write in kafka

positional arguments:
  command               "start" to launch stream or "stop" to kill stream

options:
  -h, --help            show this help message and exit
  -c CONFIG, --config CONFIG
                        configuration file path
  -i JOBID, --jobid JOBID
                        stream id
  -l LOG, --log LOG     log configuration file path (configparser file format)
```

Launch job

```shell
strefi start -c config.json
```

Stop a job

```shell
strefi stop -i {job_id}
```

Stop all jobs

```shell
strefi stop -i all
```

List jobs status

```shell
strefi ls
```

Read the complete [example](example.md) for more details.