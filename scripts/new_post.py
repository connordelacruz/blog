#!/usr/bin/env python3
import argparse
from datetime import datetime
import os
# Abstract script class
# TODO: this import syntax fails if we run this script directly, so I guess just delete main and always use exec_script.py
from .base import ScriptBase

# ================================================================================
# Constants
# ================================================================================

# Format string for dates used in filenames
DATE_STRING_FMT = '%Y-%m-%d'

# ================================================================================
# Static Helpers
# ================================================================================

def format_post_title(post_title_args):
    '''Convert title args to hyphen-separated lowercase string.

    :param post_title_args: Array of words used in post title.

    :return: Hyphen-separated lowercase string.
    '''
    # TODO: support formatted title arg to insert via frontmatter?
    # TODO: sanitize?
    post_title = '-'.join(post_title_args)
    post_title = post_title.lower()
    return post_title


def validate_and_format_date_arg(date_arg):
    '''Sanitize and format date arg into string formatted 'YYYY-MM-DD'.

    :param date_arg: Value passed to --date argument.

    :return: Formatted date string or None if a ValueError occurred.
    '''
    try:
        parsed_date = datetime.strptime(date_arg, DATE_STRING_FMT)
        # Format back into string, this fixes any missing leading 0's
        parsed_date_string = parsed_date.strftime(DATE_STRING_FMT)
    except ValueError as e:
        parsed_date_string = None
    return parsed_date_string


def format_filename(formatted_post_title, formatted_date_string):
    '''Format filename of post .md file.

    Format: '<post-title-text>-<YYYY-MM-DD>.md'

    :param formatted_post_title: Post title formatted via format_post_title()
    :param formatted_date_string: Date string formatted via validate_and_format_date_arg()

    :return: Formatted filename for markdown file.
    '''
    return f'{formatted_date_string}-{formatted_post_title}.md'


def create_post_file(filename):
    '''Create the new post file with empty frontmatter followed by a newline.

    Will create this file in the _posts/ directory.

    :param filename: Formatted filename for post markdown file.

    :return: The relative path of the file that was created.
    '''
    # TODO: we should probably make sure this is running from the root dir
    filepath = os.path.join('_posts', filename)
    with open(filepath, 'w') as f:
        f.write('---\n---\n\n')
    return filepath


def open_file_in_editor(filepath):
    '''Open the created file in an editor.

    Pulls editor command from EDITOR env var, defaults to vim if unset.

    Will jump to the bottom of the file and enter insert mode on open.

    :param filepath: Relative path to the post file to open.
    '''
    # Get the configured $EDITOR, default to vim if not set
    editor_command = os.environ.get('EDITOR', 'vim')
    # Args: jump to bottom of file and enter insert mode
    vim_args = '+"exec \'norm G\' | startinsert!"'
    command = f'{editor_command} "{filepath}" {vim_args}'
    os.system(command)


# ================================================================================
# Script Command Class
# ================================================================================

class NewPostScript(ScriptBase):
    '''Create a new post and open it in editor.'''

    command = 'new-post'
    description = 'Create a new post and open it in editor'

    @classmethod
    def get_parser(cls):
        # TODO: usage description and all that
        parser = argparse.ArgumentParser(
            description=cls.description,
        )

        # Positional
        parser.add_argument(
            'post_title',
            # TODO: usage text is funky with this:
            metavar='<post title>',
            help='Title to use when generating the filename. Can be multiple space-separated words',
            nargs='+'
        )

        # Optional
        parser.add_argument(
            '-d', '--date',
            metavar='<YYYY-MM-DD>',
            help='Use a custom date for post. Defaults to current date',
            default=datetime.now().strftime(DATE_STRING_FMT)
        )

        return parser

    def run(self):
        '''Parse and validate args, then create a new markdown file for a post and open it in editor.'''
        # Format post title text
        formatted_post_title = format_post_title(self.parsed_args.post_title)
        # Validate date
        formatted_date_string = validate_and_format_date_arg(self.parsed_args.date)
        if formatted_date_string is None:
            print(f'Error: Unable to parse provided date "{self.parsed_args.date}", please use YYYY-MM-DD format.')
            return
        # Format filename
        filename = format_filename(formatted_post_title, formatted_date_string)
        # Create the file
        filepath = create_post_file(filename)
        print(f'File created at "{filepath}"')
        print('Opening file in editor...')
        open_file_in_editor(filepath)

# ================================================================================
# Main
# ================================================================================

def main():
    '''Parse args and run script.'''
    parser = NewPostScript.get_parser()
    parsed_args = parser.parse_args()
    script = NewPostScript(parsed_args)
    script.run()


if __name__ == '__main__':
    main()
