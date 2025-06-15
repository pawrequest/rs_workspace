import subprocess
from pathlib import Path
from pprint import pprint
import argparse

from rs_workspace.paths import GAME_EXE
from rs_workspace.project import (
    install_mod_from_config_path,
    make_config,
    rs_add_utils,
    remove_utils,
)


def parseargs():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--src',
        nargs='?',
        default=Path.cwd(),
        help="red.config.json or it's parent directory",
        type=Path,
    )
    return parser.parse_args()


def rs_install(src_dir: Path = Path.cwd()):
    args = parseargs()
    print(f'RedScriptWorkspace Installing from: {src_dir}')
    pprint(args)
    install_mod_from_config_path(args.src)


def rs_launch():
    subprocess.Popen([GAME_EXE])


def rs_install_launch(config_path: Path = Path.cwd()):
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
