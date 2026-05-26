#!/usr/bin/env python3
import argparse
# Script classes
from scripts.new_post import NewPostScript

# Maps command names to script classes
commands = {
    NewPostScript.command: NewPostScript,
}

def get_parser():
    '''Returns argument parser with subparsers for scripts.'''
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(
        title='Scripts',
        description=f'Run "{parser.prog} <script> --help" for details',
        dest='script', metavar='<script>'
    )

    for command_class in commands.values():
        command_class.add_subparser(subparsers)

    # TODO: use module parser as parent, don't double define add_help
    #       https://stackoverflow.com/a/18543732
    return parser

def main():
    '''Parse arguments, handle validation, and execute'''
    parser = get_parser()
    parsed_args = parser.parse_args()
    command = parsed_args.script
    command_class = commands.get(command, False)
    # Print help if command not found
    if not command_class:
        parser.print_help()
        return
    # Initialize command object and run it
    command_object = command_class(parsed_args)
    command_object.run()
    # TODO: handle any validation, try to run command, except KeyboardInterrupt, except Exception

if __name__ == '__main__':
    main()
