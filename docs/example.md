# Example

Here you can find a full simple use case of Strefi.

First, you must have an available kafka broker. For this use case, we are going to use the "tests" docker compose.

```shell
$ git clone https://github.com/VictorMeyer77/strefi.git
$ cd strefi/tests/resources/docker
$ docker compose up
```

This simple docker-compose.yml will create an instance of zookeeper and a kafka cluster with one single-partitioned
topic "strefi-tests" on port 9092.

Once we have our kafka cluster, we can install and configure strefi.

Run the installation command

```shell
pip install strefi
```

Then we create the configuration file "example.json"

```json
{
   "producer":{
      "bootstrap_servers":"localhost:9092"
   },
   "headers":{
      "source":"strefi"
   },
   "defaults":{
      "project":"example"
   },
   "files":{
      "log/example.log":"strefi-tests"
   }
}
```

This file will configure strefi to send each new rows of log/example.log in the topic "strefi-tests". 
Only the boostrap_servers are configured for the producer. One header "source": "strefi" will be joined to the record headers 
and a field "project": "example" will be added in the record payload.

Read the [configuration page](configuration.md) for more details.

Now we can launch our stream

```shell
$ strefi start -c example.json
1732987007481404186: log/example.log --> strefi-tests
```

We keep the default logging configuration. To personalize it, read the [associated page](logging.md).

We can list all strefi processes with the ls command

```shell
$ strefi ls
1732987007481404186      log/example.log         strefi-tests     RUNNING 
```

For the moment, the file log/example.log doesn't exist, strefi is waiting until his creation.
Then, if the file is removed, strefi will wait again for the file creation.
Strefi should also manage the situation when the file is partially or totally truncate, but it's not guarantee.
We strongly recommend to move your current file and create another, instead truncate it.

Before create and write in log/example.log, we will launch a Kafka Consumer in another shell to validate our test.

```shell
$ python
>>> from kafka import KafkaConsumer
>>> for record in KafkaConsumer("strefi-tests", bootstrap_servers="localhost:9092"):
...     print(record)
```

Now we will create log/example.log and add a line. When we save we can see that a record has been sent in our topic.

```shell
$ mkdir log
$ echo 'row_1' > log/example.log
```
```text
ConsumerRecord(topic='strefi-tests', partition=0, offset=952611, timestamp=1699471578864, timestamp_type=0, key=None, value=b'{"file": "log/example.log", "row": "row_1\\n", "project": "example"}', headers=[('source', b'strefi')], checksum=None, serialized_key_size=-1, serialized_value_size=67, serialized_header_size=12)
```

Now we add two more rows.

```shell
$ echo $'row_2\nrow_3' >> log/example.log
```
```text
ConsumerRecord(topic='strefi-tests', partition=0, offset=952612, timestamp=1699471746122, timestamp_type=0, key=None, value=b'{"file": "log/example.log", "row": "row_2\\n", "project": "example"}', headers=[('source', b'strefi')], checksum=None, serialized_key_size=-1, serialized_value_size=67, serialized_header_size=12)
ConsumerRecord(topic='strefi-tests', partition=0, offset=952613, timestamp=1699471746123, timestamp_type=0, key=None, value=b'{"file": "log/example.log", "row": "row_3\\n", "project": "example"}', headers=[('source', b'strefi')], checksum=None, serialized_key_size=-1, serialized_value_size=67, serialized_header_size=12)
```