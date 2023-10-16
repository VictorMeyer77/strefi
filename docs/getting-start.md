# Getting Start

## Prerequisites

## Installation

## Usage

```txt
usage: strefi [-h] [-c CONFIG] [-i JOBID] command

Stream each new rows of a file and write in kafka

positional arguments:
  command               "start" to launch stream or "stop" to kill stream

options:
  -h, --help            show this help message and exit
  -c CONFIG, --config CONFIG
                        configuration file path
  -i JOBID, --jobid JOBID
                        stream id
```

Launch job

    strefi start -c config.json

Stop a job

    strefi stop -i {job_id}

Stop all jobs

    strefi stop -i all
