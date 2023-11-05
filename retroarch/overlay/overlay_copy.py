"""RetroArch overlay image copy tool

This script copies RetroArch overlay images from a public library to a local collection.
"""

import logging
import sys
from argparse import ArgumentParser
from pathlib import Path
from shutil import copy

SCRIPT_NAME = 'overlay-copy'
TARGET_PATH = '.'
VERSION = '1.0'


def main(args):
    """Main entry point."""
    configure_logger()
    arguments = configure_parser().parse_args(args[1:])
    logging.info('%s %s - Process started', SCRIPT_NAME, VERSION)
    log_arguments(arguments)
    copy_images(arguments)
    logging.info('%s %s - Process finished', SCRIPT_NAME, VERSION)


def configure_logger():
    """Configure logging."""
    pattern = '%(asctime)s %(levelname)s - %(message)s'
    logging.basicConfig(format=pattern, level=logging.DEBUG, stream=sys.stdout)


def configure_parser():
    """Configure CLI argument parser."""
    parser = ArgumentParser(
        prog=SCRIPT_NAME,
        description='Copy RetroArch overlay images from library to local collection')
    reference = parser.add_mutually_exclusive_group(required=True)
    reference.add_argument('-d', '--directory', help='ROM directory path')
    parser.add_argument('-e', '--extension', default='png', help='File format of overlay image(s)')
    reference.add_argument('-f', '--file', help='ROM file path')
    parser.add_argument('-l', '--library', help='Library directory path', required=True)
    parser.add_argument('-n', '--dry-run', action='store_true', help='Perform a trial run')
    parser.add_argument('-t', '--target', default=TARGET_PATH, help='Target path')
    parser.add_argument('-v', '--version', action='version', help='Print program version',
                        version='%(prog)s ' + VERSION)
    return parser


def log_arguments(arguments):
    """Log key CLI arguments."""
    logging.debug('Library path is \'%s\'', arguments.library)
    if arguments.dry_run:
        logging.info('Dry run enabled, no changes will be made')


def copy_images(arguments):
    """Copy overlay images to local collection."""
    rom_names = get_rom_names(arguments)
    if not rom_names:
        logging.info('No ROM files found, nothing to do')

    for rom_name in rom_names:
        logging.debug('Seeking overlay image for ROM file \'%s\'', rom_name)
        filename = f'{rom_name}.{arguments.extension}'
        copy_image(filename, arguments)


def get_rom_names(arguments):
    """Extract ROM names."""
    source_file = arguments.file
    if source_file:
        return [Path(source_file).stem]
    source_dir = Path(arguments.directory).iterdir()
    return [path.stem for path in source_dir if path.is_file()]


def copy_image(filename, arguments):
    """Copy overlay image to target path."""
    source_path = Path(arguments.library).joinpath(filename)
    if source_path.exists():
        target_path = Path(arguments.target).joinpath(filename)
        copy_from_to(source_path, target_path, arguments.dry_run)
    else:
        logging.warning('Overlay image \'%s\' not found', filename)


def copy_from_to(source_path, target_path, dry_run):
    """Copy file from source to target path."""
    logging.info('Copying overlay image to \'%s\'', target_path)
    if dry_run:
        return
    target_path.parent.mkdir(parents=True, exist_ok=True)
    copy(source_path, target_path)


if __name__ == '__main__':
    main(sys.argv)
