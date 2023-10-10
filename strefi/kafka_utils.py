from kafka import KafkaProducer
import json


def format_record_headers(headers_config):
    return [(k, headers_config[k].encode("UTF8")) for k in headers_config.keys()]


def create_producer(producer_config):
    return KafkaProducer(**producer_config)


def create_record(file_path, row, defaults_config):
    record = {"file": file_path, "row": row}
    record.update(dict(defaults_config))
    return json.dumps(record)
