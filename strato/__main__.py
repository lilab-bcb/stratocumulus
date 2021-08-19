import sys
from strato.commands import *


def main():
    command_list = [cp, sync, rm, exists]
    parser = argparse.ArgumentParser(description='Run a strato command')
    command_list_strings = list(map(lambda c: c.__name__[len('strato.commands.'):], command_list))
    parser.add_argument('command', help='The command', choices=command_list_strings)
    parser.add_argument('command_args', help='The command arguments', nargs=argparse.REMAINDER)

    my_args = parser.parse_args()
    command_name = my_args.command
    command_args = my_args.command_args
    cmd = command_list[command_list_strings.index(command_name)]
    sys.argv[0] = cmd.__file__
    cmd.main(command_args)

if __name__ == "__main__":
    main()
