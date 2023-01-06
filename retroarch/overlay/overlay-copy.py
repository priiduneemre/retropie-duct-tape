from argparse import ArgumentParser

TARGET_PATH = '.'
VERSION = '1.0'


def configure_parser():
    parser = ArgumentParser(
        prog='overlay-copy',
        description='Copy RetroArch overlay images from library to local collection')
    reference = parser.add_mutually_exclusive_group(required=True)
    reference.add_argument('-d', '--directory', help='ROM directory path')
    reference.add_argument('-f', '--file', help='ROM file path')
    parser.add_argument('-l', '--library', help='Library directory path', required=True)
    parser.add_argument('-t', '--target', default=TARGET_PATH, help='Target path')
    parser.add_argument('-v', '--version', action='version', help='Print program version',
                        version='%(prog)s ' + VERSION)
    return parser


if __name__ == '__main__':
    args = configure_parser().parse_args()
    # TODO
