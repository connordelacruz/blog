#!/usr/bin/env python3
import argparse
from datetime import datetime
import os


DATE_STRING_FMT = '%Y-%m-%d'


def get_parser():
    # TODO: usage description and all that
    parser = argparse.ArgumentParser()

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


def format_post_title(post_title_args):
    # TODO: DOC
    # TODO: support formatted title arg to insert via frontmatter?
    # TODO: sanitize?
    post_title = '-'.join(post_title_args)
    post_title = post_title.lower()
    return post_title


def validate_and_format_date_arg(date_arg):
    '''Sanitize and format date arg.

    Returns None if a ValueError occurred.
    '''
    try:
        parsed_date = datetime.strptime(date_arg, DATE_STRING_FMT)
    except ValueError as e:
        parsed_date = None
    # Format back into string, this fixes any missing leading 0's
    return parsed_date.strftime(DATE_STRING_FMT)


def format_filename(formatted_post_title, formatted_date_string):
    return f'{formatted_date_string}-{formatted_post_title}.md'


def create_post_file(filename):
    '''Create the new post file with empty frontmatter followed by a newline.

    Returns the path of the file that was written to.
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
    '''
    # Get the configured $EDITOR, default to vim if not set
    editor_command = os.environ.get('EDITOR', 'vim')
    # Args: jump to bottom of file and enter insert mode
    vim_args = '+"exec \'norm G\' | startinsert!"'
    command = f'{editor_command} "{filepath}" {vim_args}'
    os.system(command)



# Main =========================================================================

def main():
    parser = get_parser()
    parsed_args = parser.parse_args()
    # Format post title text
    formatted_post_title = format_post_title(parsed_args.post_title)
    # Validate date
    formatted_date_string = validate_and_format_date_arg(parsed_args.date)
    if formatted_date_string is None:
        print(f'Error: Unable to parse provided date "{parsed_args.date}", please use YYYY-MM-DD format.')
        return
    # Format filename
    filename = format_filename(formatted_post_title, formatted_date_string)
    # Create the file
    filepath = create_post_file(filename)
    print(f'File created at "{filepath}"')
    print('Opening file in editor...')
    open_file_in_editor(filepath)


if __name__ == '__main__':
    main()
