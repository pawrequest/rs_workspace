from pathlib import Path

from rs_workspace.project import load_json, make_redscript_path_txt
from rs_workspace.paths import DEPS_DIR, GAME_DIR
from rs_workspace.link_deps import (
    install_deps_symlinks,
)


def parseargs():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--overwrite',
        action='store_true',
        help='Overwrite redscript_paths.txt if it exists default=False',
    )
    parser.add_argument(
        '--game-dir',
        help='Game directory',
        nargs='?',
        default=GAME_DIR,
    )
    parser.add_argument(
        '--deps-dir',
        help='Dependencies directory',
        nargs='?',
        default=DEPS_DIR,
    )
    return parser.parse_args()


def rs_init(config_json='red.config.json', dependencies_links=r'deps/'):
    make_redscript_path_txt(overwrite=True)
    # red_config_json = Path(config_json)
    # config = load_json(red_config_json)
    # name = config['name']
    # deps_dir = Path(dependencies_links).resolve()
    #
    # install_deps_symlinks(deps_dir, exclude={name})

