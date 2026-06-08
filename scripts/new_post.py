import argparse
from datetime import datetime
import os
import re
# Abstract script class
from .base import ScriptBase

# ================================================================================
# Constants
# ================================================================================

# Format string for dates used in filenames
DATE_STRING_FMT = '%Y-%m-%d'

# ================================================================================
# Static Helpers
# ================================================================================

def post_title_args_to_string(post_title_args):
    '''Join positional arguments into a space-separated string.

    :param post_title_args: Parsed post title args list.

    :return: Space-separated string title.
    '''
    return ' '.join(post_title_args)


def format_post_title(title_arg_string):
    '''Remove invalid characters and convert title args to hyphen-separated lowercase string.

    :param title_arg_string: Title args converted to string via post_title_args_to_string().

    :return: (formatted_title, uses_special_chars), where:
        - formatted_title: Hyphen-separated lowercase string representation of title
        - uses_special_chars: True if non-alphanumeric characters in title were detected
    '''
    # Strip any characters that aren't alphanumeric, spaces, or hyphens
    sanitized_title = re.sub(r'[^\w\s-]', '', title_arg_string)
    # If the name is different after sanitizing, then there's special characters,
    # which means we'll want to use the title variable in front matter for the
    # custom title
    uses_special_chars = title_arg_string != sanitized_title
    # Replace spaces with hyphens
    hyphenated_title = re.sub(r'\s+', '-', sanitized_title)
    # Convert to lowercase
    post_title = hyphenated_title.lower()

    return post_title, uses_special_chars


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


def generate_front_matter_string(title=None):
    '''Generate Front Matter to include at top of new file.

    :param title: (Optional) If specified, will add 'title: "{title}"' variable.

    :return: String of Front Matter with trailing blank line.
    '''
    lines = [
        '---'
    ]
    # Optionally insert custom formatted title
    if title is not None:
        lines.append(f'title: "{title}"')
    lines.append('---')
    lines_string = '\n'.join(lines)
    # Append a couple blank lines
    lines_string += '\n\n'
    return lines_string


def create_post_file(filename, title=None):
    '''Create the new post file with Front Matter followed by a newline.

    Will create this file in the _posts/ directory.

    :param filename: Formatted filename for post markdown file.
    :param title: (Optional) If specified, will add 'title: "{title}"' variable
        to front matter.

    :return: The relative path of the file that was created.
    '''
    # TODO: we should probably make sure this is running from the root dir
    filepath = os.path.join('_posts', filename)
    front_matter = generate_front_matter_string(title)
    with open(filepath, 'w') as f:
        f.write(front_matter)
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
            help='Title to use when generating the filename. Can be multiple space-separated words. If this contains special characters, generated file with use the exact title in the title front matter variable.',
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
        # Convert post args list to string
        post_title_string = post_title_args_to_string(self.parsed_args.post_title)
        # Format post title text
        formatted_post_title, uses_special_chars = format_post_title(post_title_string)
        # Determine whether we should use the front matter title variable
        front_matter_title = None if not uses_special_chars else post_title_string

        # Validate date
        formatted_date_string = validate_and_format_date_arg(self.parsed_args.date)
        if formatted_date_string is None:
            print(f'Error: Unable to parse provided date "{self.parsed_args.date}", please use YYYY-MM-DD format.')
            return

        # Format filename
        filename = format_filename(formatted_post_title, formatted_date_string)
        # Create the file
        filepath = create_post_file(filename, title=front_matter_title)

        print(f'File created at "{filepath}"')
        print('Opening file in editor...')
        open_file_in_editor(filepath)

