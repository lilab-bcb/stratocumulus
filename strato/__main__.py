import sys
import argparse

from strato.commands import cp, exists, rm, sync


try:
    from importlib.metadata import version
except ImportError:  # < Python 3.8: Use backport module
    from importlib_metadata import version


def main():
    command_list = [cp, sync, rm, exists]
    parser = argparse.ArgumentParser(description="Run a strato command")
    command_list_strings = list(map(lambda c: c.__name__[len("strato.commands.") :], command_list))
    parser.add_argument("command", help="The command", choices=command_list_strings)
    parser.add_argument("command_args", help="The command arguments", nargs=argparse.REMAINDER)
    parser.add_argument("-v", "--version", action="version", version=version("stratocumulus"))

    my_args = parser.parse_args()
    command_name = my_args.command
    command_args = my_args.command_args
    cmd = command_list[command_list_strings.index(command_name)]
    sys.argv[0] = f"strato {my_args.command}"
    cmd.main(command_args)


if __name__ == "__main__":
    main()
