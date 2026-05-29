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
    # TODO: DOC
    try:
        parsed_date = datetime.strptime(date_arg, DATE_STRING_FMT)
    except ValueError:
        parsed_date = None
    return parsed_date


def get_target_dir_path(parsed_date):
    # TODO: DOC. emphasize that this does not include the filename, just dirs
    date_dir_path = parsed_date.strftime(DATE_PATH_STRING_FMT)
    target_dir_path = os.path.join(IMAGES_DIR, date_dir_path)
    return target_dir_path


def create_dirs(target_dir_path):
    # TODO: DOC
    # TODO: make sure relative paths are handled ok
    os.makedirs(target_dir_path, exist_ok=True)


def get_target_image_path(target_dir_path, image_to_copy_path):
    # TODO: DOC
    filename = os.path.basename(image_to_copy_path)
    return os.path.join(target_dir_path, filename)


def copy_image_to_target_path(image_to_copy_path, target_image_path):
    # TODO: DOC
    shutil.copy(image_to_copy_path, target_image_path)


# ================================================================================
# Script Command Class
# ================================================================================

# TODO: This script should take a path to an image (and optionally a date, default to today) (with validation and all that)
# TODO: Create dirs based on date (if necessary) i.e. ./assets/images/<year>/<month>/<day>/
# TODO: Copy the target images to the new dir
# TODO: Print new image path as it would be linked in a post md file (i.e. include baseurl prefix)

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
            '-d', '--date',
            metavar='<YYYY-MM-DD>',
            help='Use a custom date for path. Defaults to current date',
            default=datetime.now().strftime(DATE_STRING_FMT)
        )

        return parser

    def run(self):
        # TODO: DOC
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
        target_image_path = get_target_image_path(target_dir_path, self.parsed_args.image_to_copy_path)
        # Copy the file
        copy_image_to_target_path(self.parsed_args.image_to_copy_path, target_image_path)

        print('Image copied to:')
        print(f'"{target_image_path}"')

