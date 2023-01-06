import os
import re
from argparse import ArgumentParser, Namespace
from pathlib import Path

ROMAN_NUMERALS = {'II': 2, 'III': 3, 'IV': 4, 'V': 5, 'VI': 6, 'VII': 7, 'VIII': 8, 'IX': 9}
RULESET = Namespace(NORMALIZE='normalize')
TARGET_PATH = '.'
VERSION = '1.0'


def configure_parser():
    parser = ArgumentParser(prog='rom-rename',
                            description='Rename local ROM files according to preset rules')
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument('-d', '--directory', help='Source directory path')
    source.add_argument('-f', '--file', help='Source file path')
    parser.add_argument('-r', '--ruleset', choices=[RULESET.NORMALIZE], default=RULESET.NORMALIZE,
                        help='Naming ruleset to use')
    parser.add_argument('-t', '--target', default=TARGET_PATH, help='Target path')
    parser.add_argument('-v', '--version', action='version', help='Print program version',
                        version='%(prog)s ' + VERSION)
    return parser


def rename_all(arguments):
    for rom_path in get_rom_paths(arguments):
        rename(rom_path, arguments.target)


def rename(source_path, target_dir):
    normalized_name = normalize(source_path)
    target_path = Path(target_dir).joinpath(normalized_name)
    target_path.parent.mkdir(parents=True, exist_ok=True)
    os.rename(source_path, target_path)


def get_rom_paths(arguments):
    source_file = arguments.file
    if source_file:
        return Path(source_file)
    else:
        source_dir = Path(arguments.directory).iterdir()
        return [path for path in source_dir if path.is_file()]


def normalize(path):
    without_parentheses = normalize_parentheses(path.stem)
    converted_numerals = normalize_numerals(without_parentheses)
    snake_cased = '_'.join(converted_numerals.split())
    without_special = re.sub(r'\W+', '', snake_cased)
    return (without_special + path.suffix).lower()


def normalize_parentheses(name_stem):
    flattened_track = normalize_track(name_stem)
    without_region = re.sub(r'[(\[].*?[)\]]', '', flattened_track)
    return without_region.strip()


def normalize_track(name_stem):
    return re.sub(r'\(Track (\d+)\)', r'track\1', name_stem, flags=re.I)


def normalize_numerals(name_stem):
    result = name_stem
    for roman, arabic in ROMAN_NUMERALS.items():
        pattern = r'(\s)({})([\s:]|\Z)'.format(roman)
        replacement = r'\g<1>{}\3'.format(arabic)
        result = re.sub(pattern, replacement, result, flags=re.I)
    return result


if __name__ == '__main__':
    args = configure_parser().parse_args()
    rename_all(args)