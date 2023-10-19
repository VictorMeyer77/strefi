# strefi

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
[![codecov](https://codecov.io/github/VictorMeyer77/strefi/graph/badge.svg?token=MCO1XZI4OO)](https://codecov.io/github/VictorMeyer77/strefi)
[![CI](https://github.com/VictorMeyer77/strefi/actions/workflows/ci.yml/badge.svg)](https://github.com/VictorMeyer77/strefi/actions/workflows/ci.yml)
[![docs](https://readthedocs.org/projects/strefi/badge/?version=latest&style=flat-default)](https://strefi.readthedocs.io)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
![style](https://img.shields.io/badge/code%20style-black-000000.svg)

Stream each new rows of a file and write in kafka. 

- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [License](#license)

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

## Configuration

Strefi configuration is stored in a simple json file.

```json
{
   "producer":{
      "bootstrap_servers":"localhost:9092",
      "acks":0,
      "retries":0
   },
   "headers":{
      "version":"0.1",
      "type":"json"
   },
   "defaults":{
      "key_one":"value_one",
      "key_two":"value_two"
   },
   "files":{
      "/path/to/file_1":"target_topic",
      "/path/to/file_2":"target_topic"
   }
}
```

#### files

Specify in the "files" objects the paths of all files you want stream. The field key is file path and
the field value is the topic.

```json
"files":{
  "/path/to/file_1":"target_topic",
  "/path/to/file_2":"target_topic"
}
```

#### producer

Producer configuration must have at least the field boostrap_servers.
All fields will be parameters of the [KafkaProducer](https://kafka-python.readthedocs.io/en/master/apidoc/KafkaProducer.html).
One producer is created foreach table to stream, but all producers have the same configuration.

```json
"producer":{
  "bootstrap_servers":"localhost:9092",
  "acks":0,
  "retries":0
}
```
#### defaults

This field can be empty. In this case, the record sent to kafka is just composed with streamed file
path and the file row.

```json
{"file": "/path/to/file_1", "row": "last file row"}
```

You can enhance records send to topic with th "defaults" object.

```json
"defaults":{
  "key_one":"value_one",
  "key_two":"value_two"
}
```
With this configuration, the record sent to kafka has also these values.

```json
{"file":"/path/to/file_1", "row":"last file row", "key_one":"value_one","key_two":"value_two"}
```

#### headers

You can join headers with the record with the "headers" field. It can be empty if you don't want
headers.

```json
"headers":{
  "version":"0.1",
  "type":"json"
}
```

These headers will be converted in this list of tuple. Headers key shall be a string and the value
will be encoded.

```txt
[("version", b"0.1"), ("type", b"json")]
```

## License

strefi is released under GPL-3.0 license. See [LICENSE](https://github.com/VictorMeyer77/strefi/blob/main/LICENSE).