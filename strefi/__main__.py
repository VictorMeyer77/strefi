"""Entrypoint of the program.
    Provides functions to read arguments then call command.

The module contains the following functions:

- `parse_args(args)` - Read and verify program arguments.
- `main(args)` - Entrypoint function. Launch the right method.
"""

import sys
import argparse
import command


def parse_args(args: list[str]) -> argparse.Namespace:
    """Read and verify program arguments.
    Exit the program if arguments are invalid.

    Args:
        args: list of program arguments.

    Returns:
        Argparse namespace.
    """
    parser = argparse.ArgumentParser(
        prog="strefi",
        description="Stream a file line per line and write in a kafka topic",
        epilog="More information on GitHub",
    )
    parser.add_argument("command", help='"start" to launch stream or "stop" to kill stream')
    parser.add_argument("-c", "--config", help="configuration file path")
    parser.add_argument("-i", "--jobid", help="stream id")

    namespace = parser.parse_args(args)

    if namespace.command.lower() == "start":
        if namespace.config is None:
            parser.error("missing configuration file path")
    elif namespace.command.lower() == "stop":
        if namespace.jobid is None:
            parser.error("missing configuration job id")
    else:
        parser.error(f"unknown command {namespace.command}")

    return namespace


def main(args: list[str]):
    """Entrypoint function. Launch the right method.

    Args:
        args: list of program arguments.
    """
    namespace = parse_args(args)
    if namespace.command.lower() == "start":
        command.start(namespace.config)
    elif namespace.command.lower() == "stop":
        command.stop(namespace.jobid)


if __name__ == "__main__":
    main(sys.argv[1:])
