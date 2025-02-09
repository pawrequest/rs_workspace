import os
from pathlib import Path

from rs_workspace.project import get_deps_dir, make_redscript_path_txt, load_json
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
        default=Path(os.getenv('CYBERPUNK_GAME_DIR')),
    )
    parser.add_argument(
        '--deps-dir',
        help='Dependencies directory, defaults=pyproject as root / rsrc',
        nargs='?',
        default=get_deps_dir(),
    )
    return parser.parse_args()


# def rs_init1(deps_dir: Path, game_dir: Path=None, overwrite: bool = False):
#     install_deps_symlinks(deps_dir, game_dir=game_dir)
#     make_redscript_path_txt(game_dir=game_dir, overwrite=overwrite)


def rs_init():
    json_path = Path('red.config.json')
    config = load_json(json_path)
    name = config['name']
    deps_dir = Path(r'deps/').resolve()

    install_deps_symlinks(deps_dir, exclude={name})
    make_redscript_path_txt()


def main():
    # args = parseargs()
    rs_init(
        # game_dir=Path(args.game_dir),
        # deps_dir=Path(args.deps_dir),
        # overwrite=args.overwrite,
    )

if __name__ == '__main__':
    main()