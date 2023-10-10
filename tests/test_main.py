import unittest
from argparse import Namespace
from strefi import __main__


class TestMain(unittest.TestCase):

    def test_parse_args_should_return_namespace(self):
        args_start = ["start", "-c", "test.json"]
        args_stop = ["stop", "-i", "91262"]

        namespace_start = __main__.parse_args(args_start)
        namespace_stop = __main__.parse_args(args_stop)

        self.assertEqual(namespace_start, Namespace(command="start", config="test.json", jobid=None))
        self.assertEqual(namespace_stop, Namespace(command="stop", config=None, jobid="91262"))

    def test_parse_args_should_raises_error_when_args_are_invalids(self):
        # unknown command
        with self.assertRaises(SystemExit):
            __main__.parse_args(["unknown"])

        # missing config file path with start command
        with self.assertRaises(SystemExit):
            __main__.parse_args(["start"])

        # missing job id with stop command
        with self.assertRaises(SystemExit):
            __main__.parse_args(["stop"])
