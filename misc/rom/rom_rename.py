"""ROM file rename utility

This script renames local ROM files according to one of the predefined rulesets.
"""

import logging
import re
import sys
from argparse import ArgumentParser, Namespace
from pathlib import Path

ROMAN_NUMERALS = {'II': 2, 'III': 3, 'IV': 4, 'V': 5, 'VI': 6, 'VII': 7, 'VIII': 8, 'IX': 9}
RULESET = Namespace(NORMALIZE='normalize')
SCRIPT_NAME = 'rom-rename'
TARGET_PATH = '.'
VERSION = '1.0'


def main(args):
    """Main entry point."""
    configure_logger()
    arguments = configure_parser().parse_args(args[1:])
    logging.info('%s %s - Process started', SCRIPT_NAME, VERSION)
    log_arguments(arguments)
    rename_all(arguments)
    logging.info('%s %s - Process finished', SCRIPT_NAME, VERSION)


def configure_logger():
    """Configure logging."""
    pattern = '%(asctime)s %(levelname)s - %(message)s'
    logging.basicConfig(format=pattern, level=logging.DEBUG, stream=sys.stdout)


def configure_parser():
    """Configure CLI argument parser."""
    parser = ArgumentParser(prog=SCRIPT_NAME,
                            description='Rename local ROM files according to preset rules')
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument('-d', '--directory', help='Source directory path')
    source.add_argument('-f', '--file', help='Source file path')
    parser.add_argument('-n', '--dry-run', action='store_true', help='Perform a trial run')
    parser.add_argument('-r', '--ruleset', choices=[RULESET.NORMALIZE], default=RULESET.NORMALIZE,
                        help='Naming ruleset to use')
    parser.add_argument('-t', '--target', default=TARGET_PATH, help='Target path')
    parser.add_argument('-v', '--version', action='version', help='Print program version',
                        version='%(prog)s ' + VERSION)
    return parser


def log_arguments(arguments):
    """Log key CLI arguments."""
    logging.debug('Active ruleset is \'%s\'', arguments.ruleset)
    if arguments.dry_run:
        logging.info('Dry run enabled, no changes will be made')


def rename_all(arguments):
    """Rename all ROM files."""
    rom_paths = get_rom_paths(arguments)
    if not rom_paths:
        logging.info('No ROM files found, nothing to do')

    for rom_path in rom_paths:
        rename(rom_path, arguments)


def get_rom_paths(arguments):
    """Extract ROM paths."""
    source_file = arguments.file
    if source_file:
        return Path(source_file)
    source_dir = Path(arguments.directory).iterdir()
    return [path for path in source_dir if path.is_file()]


def rename(source_path, arguments):
    """Rename ROM file according to ruleset."""
    normalized_name = normalize(source_path)
    target_path = Path(arguments.target).joinpath(normalized_name)
    logging.info('Renaming ROM file \'%s\' to \'%s\'', source_path, target_path)
    if arguments.dry_run:
        return
    target_path.parent.mkdir(parents=True, exist_ok=True)
    source_path.rename(target_path)


def normalize(path):
    """Normalize ROM filename."""
    without_parentheses = normalize_parentheses(path.stem)
    converted_numerals = normalize_numerals(without_parentheses)
    without_special = re.sub(r'([^\w ]|_)+', '', converted_numerals)
    snake_cased = '_'.join(without_special.split())
    return (snake_cased + path.suffix).lower()


def normalize_parentheses(name):
    """Normalize filename parentheses."""
    flattened_track = normalize_track(name)
    without_region = re.sub(r'[(\[].*?[)\]]', '', flattened_track)
    return without_region.strip()


def normalize_track(name):
    """Normalize filename track number."""
    return re.sub(r'\(Track 0*(\d+)\)', r'track\1', name, flags=re.I)


def normalize_numerals(name):
    """Normalize filename numerals."""
    result = name
    for roman, arabic in ROMAN_NUMERALS.items():
        pattern = fr'(\s)({roman})([\s:]|\Z)'
        replacement = fr'\g<1>{arabic}\3'
        result = re.sub(pattern, replacement, result, flags=re.I)
    return result


if __name__ == '__main__':
    main(sys.argv)
