import os
from argparse import ArgumentParser, Namespace
from pathlib import Path
from string import Template

PATH = Namespace(
    OUTPUT='output',
    TEMPLATE=Namespace(
        OVERLAY_CONFIG='template/overlay-config.tpl',
        ROM_CONFIG='template/rom-config.tpl'
    )
)
VERSION = '1.0'


def configure_parser():
    parser = ArgumentParser(prog='overlay-config',
                            description='Configure RetroArch overlays for local ROM collection')
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument('-d', '--directory', help='Source directory path')
    parser.add_argument('-e', '--extension', default='png', help='File type of overlay image(s)')
    source.add_argument('-f', '--file', help='Source file path')
    parser.add_argument('-o', '--output', default=PATH.OUTPUT, help='Output path')
    parser.add_argument('-ot', '--overlay-tpl', default=PATH.TEMPLATE.OVERLAY_CONFIG,
                        help='Overlay config template path')
    parser.add_argument('-p', '--platform', help='Name of target platform', required=True)
    parser.add_argument('-rt', '--rom-tpl', default=PATH.TEMPLATE.ROM_CONFIG,
                        help='ROM config template path')
    parser.add_argument('-v', '--version', action='version', help='Print program version',
                        version='%(prog)s ' + VERSION)
    return parser


def create_overlay_configs(arguments):
    template = get_config_template(arguments.overlay_tpl)
    for filename in get_rom_filenames(arguments):
        rom_name = Path(filename).stem
        create_overlay_config(rom_name, template, arguments)


def create_overlay_config(rom_name, template, arguments):
    output_path = Path(arguments.output).joinpath('overlay', rom_name + '.cfg')
    substitutions = dict(name=rom_name, extension=arguments.extension)
    config_text = template.safe_substitute(substitutions)
    write_file(output_path, config_text)


def create_rom_configs(arguments):
    template = get_config_template(arguments.rom_tpl)
    for filename in get_rom_filenames(arguments):
        create_rom_config(filename, template, arguments)


def create_rom_config(filename, template, arguments):
    output_path = Path(arguments.output).joinpath('rom', filename + '.cfg')
    substitutions = dict(name=Path(filename).stem, platform=arguments.platform)
    config_text = template.safe_substitute(substitutions)
    write_file(output_path, config_text)


def get_config_template(pathname):
    template = Path(pathname).read_text()
    return Template(template)


def get_rom_filenames(arguments):
    source_file = arguments.file
    if source_file:
        return [Path(source_file).name]
    else:
        return os.listdir(arguments.directory)


def write_file(pathname, content):
    path = Path(pathname)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)


if __name__ == '__main__':
    args = configure_parser().parse_args()
    create_overlay_configs(args)
    create_rom_configs(args)
