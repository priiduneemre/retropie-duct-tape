import logging
import sys
from argparse import ArgumentParser
from pathlib import Path
from shutil import copy

SCRIPT_NAME = 'overlay-copy'
TARGET_PATH = '.'
VERSION = '1.0'


def main(args):
    configure_logger()
    arguments = parse_arguments(args)
    logging.info('%s %s - Process started', SCRIPT_NAME, VERSION)
    copy_images(arguments)
    logging.info('%s %s - Process finished', SCRIPT_NAME, VERSION)


def configure_logger():
    pattern = '%(asctime)s %(levelname)s - %(message)s'
    logging.basicConfig(format=pattern, level=logging.DEBUG, stream=sys.stdout)


def parse_arguments(args):
    arguments = configure_parser().parse_args(args[1:])
    logging.debug('Library path is \'%s\'', arguments.library)
    return arguments


def configure_parser():
    parser = ArgumentParser(
        prog=SCRIPT_NAME,
        description='Copy RetroArch overlay images from library to local collection')
    reference = parser.add_mutually_exclusive_group(required=True)
    reference.add_argument('-d', '--directory', help='ROM directory path')
    parser.add_argument('-e', '--extension', default='png', help='File format of overlay image(s)')
    reference.add_argument('-f', '--file', help='ROM file path')
    parser.add_argument('-l', '--library', help='Library directory path', required=True)
    parser.add_argument('-t', '--target', default=TARGET_PATH, help='Target path')
    parser.add_argument('-v', '--version', action='version', help='Print program version',
                        version='%(prog)s ' + VERSION)
    return parser


def copy_images(arguments):
    rom_names = get_rom_names(arguments)
    if not rom_names:
        logging.info('No ROM files found, nothing to do')

    for name in get_rom_names(arguments):
        logging.debug('Seeking overlay image for ROM file \'%s\'', name)
        filename = '{}.{}'.format(name, arguments.extension)
        copy_image(filename, arguments)


def get_rom_names(arguments):
    source_file = arguments.file
    if source_file:
        return [Path(source_file).stem]
    else:
        source_dir = Path(arguments.directory).iterdir()
        return [path.stem for path in source_dir if path.is_file()]


def copy_image(filename, arguments):
    source_path = Path(arguments.library).joinpath(filename)
    if source_path.exists():
        target_path = Path(arguments.target).joinpath(filename)
        copy_from_to(source_path, target_path)
    else:
        logging.warning('Overlay image \'%s\' not found', filename)


def copy_from_to(source_path, target_path):
    logging.info('Copying overlay image to \'%s\'', target_path)
    target_path.parent.mkdir(parents=True, exist_ok=True)
    copy(source_path, target_path)


if __name__ == '__main__':
    main(sys.argv)
