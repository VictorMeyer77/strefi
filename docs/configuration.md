# Configuration

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
