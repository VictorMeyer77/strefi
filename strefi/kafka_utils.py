"""Provides methods to create kafka objects from configuration.

The module contains the following functions:

- `format_record_headers(headers_config)` - Create record headers from dictionary.
- `create_producer(producer_config)` - Initialize a KafkaProducer instance from dictionary.
- `format_record_value(file_path, row, defaults_config)` - Serialize record value.
"""

import json

from kafka import KafkaProducer


def format_record_headers(headers_config: dict[str, str]) -> list[tuple[str, bytes]]:
    """Create record headers from dictionary.

    Examples:
        >>> format_record_headers({"version": "0.1", "type": "json"})
        [('version', b'0.1'), ('type', b'json')]

    Args:
        headers_config: Configuration dictionary.

    Returns:
        List of record headers. Values are encoded.
    """
    return [(k, headers_config[k].encode()) for k in headers_config.keys()]


def create_producer(producer_config: dict[str, object]) -> KafkaProducer:
    """Initialize a KafkaProducer instance from dictionary.

    Examples:
        >>> create_producer({"bootstrap_servers":"localhost:9092", "client_id":"strefi-client", "acks": 0})

    Args:
        producer_config: Configuration dictionary.

    Returns:
        KafkaProducer instance.
    """
    return KafkaProducer(**producer_config)


def format_record_value(file_path: str, row: str, defaults_config: dict[str, object]) -> str:
    """Serialize record value.

    Examples:
        >>> format_record_value("/path/to/file", "foo", {"hostname":"lpt01", "system":"Linux"})
        "{'file': '/path/to/file', 'row': 'foo', 'hostname': 'lpt01', 'system': 'Linux'}"

    Args:
        file_path: Path of the stream file.
        row: Last row writen in the streamed file.
        defaults_config: Configured dictionary to add in the record value.

    Returns:
        Formatted string record value.
    """
    record: dict[str, object] = {"file": file_path, "row": row}
    record.update(dict(defaults_config))
    return json.dumps(record)
