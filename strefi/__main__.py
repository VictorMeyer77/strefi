import sys
import argparse
import strefi


def parse_args(args):
    parser = argparse.ArgumentParser(prog="strefi-client",
                                     description="Stream a file line per line and write in a kafka topic",
                                     epilog="More information on GitHub")
    parser.add_argument("command", help="\"start\" to launch stream or \"stop\" to kill stream")
    parser.add_argument("-c", "--config", help="configuration file path")
    parser.add_argument("-i", "--jobid", help="stream id")

    args = parser.parse_args(args)

    if args.command.lower() == "start":
        if args.config is None:
            parser.error("missing configuration file path")
    elif args.command.lower() == "stop":
        if args.jobid is None:
            parser.error("missing configuration job id")
    else:
        parser.error(f"unknown command {args.command}")

    return args


if __name__ == "__main__":
    args = parse_args(sys.argv[1:])
    if args.command.lower() == "start":
        strefi.start(args.config)
    elif args.command.lower() == "stop":
        strefi.stop(args.jobid)
