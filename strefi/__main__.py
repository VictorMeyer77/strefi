"""Entrypoint of the program.
    Provides functions to read arguments then call command.

The module contains the following functions:

- `parse_args(args)` - Read and verify program arguments.
- `configure_logger(logger_conf_path: str)` - Configure strefi logger.
- `main()` - Entrypoint function. Launch the right method.
"""

import argparse
import logging
import sys
from logging import config
from logging.handlers import RotatingFileHandler

from strefi import command

logger = logging.getLogger(__name__)


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
        description="Stream each new rows of a file and write in kafka",
        epilog="More information on GitHub",
    )
    parser.add_argument("command", help='"start" to launch stream or "stop" to kill stream')
    parser.add_argument("-c", "--config", help="configuration file path")
    parser.add_argument("-i", "--jobid", help="stream id")
    parser.add_argument("-l", "--log", help="log configuration file path (configparser file format)")

    namespace = parser.parse_args(args)

    if namespace.command.lower() not in ["start", "stop", "ls"]:
        parser.error(f"unknown command {namespace.command}")

    if namespace.command.lower() == "start":
        if namespace.config is None:
            parser.error("missing configuration file path")
    elif namespace.command.lower() == "stop":
        if namespace.jobid is None:
            parser.error("missing configuration job id")

    return namespace


def configure_logger(logger_conf_path: str):
    """Configure strefi logger.
    By default, the logger writes in .strefi.log and rotates 5 times each 10 MB.
    You can specify your own log configuration file in configparser file format.
    See also <https://docs.python.org/3/library/logging.config.html#logging-config-fileformat>

    Args:
        logger_conf_path: path of the configuration file (configparser file format).

    """
    if logger_conf_path is None:
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(name)s - %(threadName)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%dT%H:%M:%SZ",
            handlers=[RotatingFileHandler(filename=".strefi.log", maxBytes=10 * 1024 * 1024, backupCount=5)],
        )
    else:
        config.fileConfig(logger_conf_path, disable_existing_loggers=False)


def main():
    """Entrypoint function. Launch the right method."""
    args = sys.argv[1:]
    namespace = parse_args(args)
    configure_logger(namespace.log)
    logger.debug(f"Strefi called with args {args}.")
    if namespace.command.lower() == "start":
        command.start(namespace.config)
    elif namespace.command.lower() == "stop":
        command.stop(namespace.jobid)
    elif namespace.command.lower() == "ls":
        command.ls()


if __name__ == "__main__":
    main()  # pragma: no cover
