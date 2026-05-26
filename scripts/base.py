from abc import ABC, abstractmethod


class ScriptBase(ABC):
    '''Base object for script commands.'''

    def __init__(self, parsed_args=None):
        self.parsed_args = parsed_args

    @property
    @abstractmethod
    def command(self):
        '''Subcommand name'''
        pass

    @property
    @abstractmethod
    def description(self):
        '''Subcommand description'''
        pass

    @classmethod
    @abstractmethod
    def get_parser(cls):
        '''Return the ArgumentParser object for this command.'''
        pass

    @classmethod
    def add_subparser(cls, subparsers):
        '''Add this script's ArgumentParser object as a subparser.'''
        subparser = subparsers.add_parser(
            cls.command,
            description=cls.description,
            parents=[cls.get_parser()],
            add_help=False,
            help=cls.description,
        )
        return subparser

    @abstractmethod
    def run(self):
        '''Execute the script.'''
        pass
