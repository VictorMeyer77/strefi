from strefi import kafka_utils


def test_format_record_headers_transform_dict_to_config():
    headers_config = {"version": "0.1", "type": "json"}
    headers_tuple = kafka_utils.format_record_headers(headers_config)
    assert headers_tuple == [("version", b"0.1"), ("type", b"json")]


def test_create_record_should_create_dict_with_defaults():
    defaults = {"hostname": "lpt01", "system": "Linux"}
    record = kafka_utils.create_record("/path/to/file", "foo", defaults)
    assert record == """{"file": "/path/to/file", "row": "foo", "hostname": "lpt01", "system": "Linux"}"""
