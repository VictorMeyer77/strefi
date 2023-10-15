from strefi import kafka_utils


def test_format_record_headers_transform_dict_to_config():
    headers_config = {"version": "0.1", "type": "json"}
    headers_tuple = kafka_utils.format_record_headers(headers_config)
    assert headers_tuple == [("version", b"0.1"), ("type", b"json")]


def test_create_producer():
    producer_config = {"bootstrap_servers": "localhost:9092", "client_id": "test-id", "acks": 0, "retries": 0}
    producer = kafka_utils.create_producer(producer_config)
    for key, value in producer_config.items():
        assert value == producer.config[key]


def test_format_record_value_should_create_dict_with_defaults():
    defaults = {"hostname": "lpt01", "system": "Linux"}
    record = kafka_utils.format_record_value("/path/to/file", "foo", defaults)
    assert record == """{"file": "/path/to/file", "row": "foo", "hostname": "lpt01", "system": "Linux"}"""
