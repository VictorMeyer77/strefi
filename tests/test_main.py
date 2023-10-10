import pytest
from argparse import Namespace
from strefi import __main__


def test_parse_args_should_return_namespace():
    args_start = ["start", "-c", "test.json"]
    args_stop = ["stop", "-i", "91262"]

    namespace_start = __main__.parse_args(args_start)
    namespace_stop = __main__.parse_args(args_stop)

    assert namespace_start == Namespace(command="start", config="test.json", jobid=None)
    assert namespace_stop == Namespace(command="stop", config=None, jobid="91262")


def test_parse_args_should_raises_error_when_args_are_invalids():
    # unknown command
    with pytest.raises(SystemExit):
        __main__.parse_args(["unknown"])

    # missing config file path with start command
    with pytest.raises(SystemExit):
        __main__.parse_args(["start"])

    # missing job id with stop command
    with pytest.raises(SystemExit):
        __main__.parse_args(["stop"])
