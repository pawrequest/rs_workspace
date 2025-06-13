import subprocess
from pathlib import Path
from pprint import pprint
import argparse

from rs_workspace.paths import  GAME_EXE
from rs_workspace.project import install_mod_from_config_path, make_config, rs_add_utils, remove_utils


def parseargs():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--src',
        nargs='?',
        default=Path.cwd(),
        help='directory containing red.config.json',
    )
    return parser.parse_args()


def rs_install(src_dir: Path = None):
    args = parseargs()
    pprint(args)
    src_dir = (
        Path(args.src) if hasattr(args, 'src') else src_dir if src_dir.is_dir() else Path.cwd()
    )
    print(f'RedScriptWorkspace Installing from src_dir: {src_dir}')

    install_mod_from_config_path(src_dir)


def rs_launch():
    subprocess.run([GAME_EXE])


def rs_install_launch(config_path: str = None):
    rs_install(config_path)
    rs_launch()


all = [
    make_config,
    rs_launch,
    rs_launch,
    rs_install_launch,
    rs_add_utils,
    remove_utils,
]
