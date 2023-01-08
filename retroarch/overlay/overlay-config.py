import logging
import sys
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


def main(args):
    configure_logger()
    arguments = configure_parser().parse_args(args)
    logging.info('%s %s - Process started', get_script_name(), VERSION)
    logging.debug('Target platform is \'%s\'', arguments.platform)
    create_configs(arguments)
    logging.info('%s %s - Process finished', get_script_name(), VERSION)


def configure_logger():
    pattern = '%(asctime)s %(levelname)s - %(message)s'
    logging.basicConfig(format=pattern, level=logging.DEBUG, stream=sys.stdout)


def configure_parser():
    parser = ArgumentParser(prog=get_script_name(),
                            description='Configure RetroArch overlays for local ROM collection')
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument('-d', '--directory', help='Source directory path')
    parser.add_argument('-e', '--extension', default='png', help='File format of overlay image(s)')
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


def get_script_name():
    return Path(sys.argv[0]).stem


def create_configs(arguments):
    if not get_rom_filenames(arguments):
        logging.info('No ROM files found, nothing to do')
        return
    create_overlay_configs(arguments)
    create_rom_configs(arguments)


def create_overlay_configs(arguments):
    logging.debug('Creating overlay config(s) using template \'%s\'', arguments.overlay_tpl)
    template = get_config_template(arguments.overlay_tpl)
    for filename in get_rom_filenames(arguments):
        rom_name = Path(filename).stem
        create_overlay_config(rom_name, template, arguments)


def create_overlay_config(rom_name, template, arguments):
    output_path = Path(arguments.output).joinpath('overlay', rom_name + '.cfg')
    logging.info('Creating overlay config at \'%s\'', output_path)
    substitutions = dict(name=rom_name, extension=arguments.extension)
    config_text = template.safe_substitute(substitutions)
    write_file(output_path, config_text)


def create_rom_configs(arguments):
    logging.debug('Creating ROM config(s) using template \'%s\'', arguments.rom_tpl)
    template = get_config_template(arguments.rom_tpl)
    for filename in get_rom_filenames(arguments):
        create_rom_config(filename, template, arguments)


def create_rom_config(filename, template, arguments):
    output_path = Path(arguments.output).joinpath('rom', filename + '.cfg')
    logging.info('Creating ROM config at \'%s\'', output_path)
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
        source_dir = Path(arguments.directory).iterdir()
        return [path.name for path in source_dir if path.is_file()]


def write_file(pathname, content):
    path = Path(pathname)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)


if __name__ == '__main__':
    main(sys.argv)
