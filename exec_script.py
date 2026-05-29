#!/usr/bin/env python3
import argparse
import sys
import traceback
# Script classes
from scripts.new_post import NewPostScript
from scripts.copy_image_for_post import CopyImageForPostScript

# Maps command names to script classes
commands = {
    NewPostScript.command: NewPostScript,
    CopyImageForPostScript.command: CopyImageForPostScript,
}

def get_parser():
    '''Returns argument parser with subparsers for scripts.'''
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(
        title='Scripts',
        description=f'Run "{parser.prog} <script> --help" for details',
        dest='script', metavar='<script>'
    )
    # Add command subparsers
    for command_class in commands.values():
        command_class.add_subparser(subparsers)

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
    try:
        command_object.run()
    except KeyboardInterrupt:
        print('')
        sys.exit(0)
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
