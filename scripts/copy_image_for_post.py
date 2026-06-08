import argparse
from datetime import datetime
import os
import shutil
# Abstract script class
from .base import ScriptBase

# ================================================================================
# Constants
# ================================================================================

# TODO: shared constant? Date arg utilities for common code?
# Format string for dates used in filenames
DATE_STRING_FMT = '%Y-%m-%d'
# Format string for date directories (relative to IMAGES_DIR)
DATE_PATH_STRING_FMT = os.path.join('%Y', '%m', '%d')

# Image assets dir, relative to blog root
IMAGES_DIR = 'assets/images'

# ================================================================================
# Static Helpers
# ================================================================================

def convert_date_arg_to_datetime(date_arg):
    '''Convert date arg string to a datetime object.

    :param date_arg: String matching DATE_STRING_FMT format.

    :return: datetime object or None if an error occurred while parsing.
    '''
    try:
        parsed_date = datetime.strptime(date_arg, DATE_STRING_FMT)
    except ValueError:
        parsed_date = None
    return parsed_date


def get_target_dir_path(parsed_date):
    '''Returns a string for the target path to copy the image to.

    Format is 'assets/images/<year>/<month>/<day>/'

    :param parsed_date: datetime object for post date.

    :return: Path to target directory.
    '''
    date_dir_path = parsed_date.strftime(DATE_PATH_STRING_FMT)
    target_dir_path = os.path.join(IMAGES_DIR, date_dir_path)
    return target_dir_path


def create_dirs(target_dir_path):
    '''Creates all dirs in the provided path if they do not exist.

    :param target_dir_path: Path to target directory.
    '''
    os.makedirs(target_dir_path, exist_ok=True)


def validate_target_filename_extension(source_filename, target_filename):
    '''Ensures that target filename extension matches source.

    If there's a mismatch or no extension, will remove target filename's bad
    extension and append source filename's extension.

    :param source_filename: Source image filename.
    :param target_filename: Target image filename.

    :return: Target image filename with correct extension.
    '''
    source_tup = os.path.splitext(source_filename)
    target_tup = os.path.splitext(target_filename)
    if source_tup[1] != target_tup[1]:
        # Append source's file ext
        target_filename = target_tup[0] + source_tup[1]
    return target_filename


def get_target_image_path(target_dir_path, image_to_copy_path, target_filename=None):
    '''Returns a string for the target path with filename.

    If target_filename is None, uses original image's filename for the target
    file, e.g.:

        'assets/images/<year>/<month>/<day>/<original-image-filename.ext>'

    If target_filename is not None, will ensure that the original filename's
    extension is appended to target filename.

    :param target_dir_path: Path to target directory.
    :param image_to_copy_path: Path to source image file.
    :param target_filename: (Optional) Name for the copied image file, with or
        without extension.

    :return: Target filepath.
    '''
    source_filename = os.path.basename(image_to_copy_path)
    if target_filename is not None:
        target_filename = validate_target_filename_extension(source_filename, target_filename)
    else:
        target_filename = source_filename
    return os.path.join(target_dir_path, target_filename)


def copy_image_to_target_path(image_to_copy_path, target_image_path):
    '''Copy file to the target path.

    :param image_to_copy_path: Path to source image.
    :param target_image_path: Path to target (with filename).
    '''
    shutil.copy(image_to_copy_path, target_image_path)


# ================================================================================
# Script Command Class
# ================================================================================

class CopyImageForPostScript(ScriptBase):
    command = 'copy-image'
    description = 'Copy image into assets/images/<year>/<month>/<day>/'

    @classmethod
    def get_parser(cls):
        # TODO: usage description and all that
        parser = argparse.ArgumentParser(
            description=cls.description,
        )

        # Positional
        parser.add_argument(
            'image_to_copy_path',
            metavar='<src/image/path.ext>',
            help='Path to the image to copy'
        )

        # Optional
        parser.add_argument(
            '-f', '--filename',
            metavar='<copied image filename>',
            help='If specified, the new image file will use this as its filename. Default behavior is to keep the filename of the original'
        )
        parser.add_argument(
            '-d', '--date',
            metavar='<YYYY-MM-DD>',
            help='Use a custom date for path. Defaults to current date',
            default=datetime.now().strftime(DATE_STRING_FMT)
        )

        return parser

    def run(self):
        '''Execute the script.

        - Validates optional date arg
        - Formats target dir path
        - Creates directories as necessary
        - Copies the image to the target path
        - Prints the path to the copied image to sdout
        '''
        # TODO: validate image to copy path
        # Validate and parse date arg
        parsed_date = convert_date_arg_to_datetime(self.parsed_args.date)
        if parsed_date is None:
            print(f'Error: Unable to parse provided date "{self.parsed_args.date}", please use YYYY-MM-DD format.')
            return
        # Directory path where file will be copied to
        target_dir_path = get_target_dir_path(parsed_date)
        # Create any non-existant dirs in the target path
        create_dirs(target_dir_path)
        # Full path to image destination w/ filename
        target_image_path = get_target_image_path(target_dir_path, self.parsed_args.image_to_copy_path, self.parsed_args.filename)
        # Copy the file
        copy_image_to_target_path(self.parsed_args.image_to_copy_path, target_image_path)

        print('Image copied to:')
        print(f'"{target_image_path}"')

