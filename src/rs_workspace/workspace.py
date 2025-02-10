import os
from pathlib import Path

from rs_workspace.project import load_json, make_redscript_path_txt
from rs_workspace.paths import DEPS_DIR
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
        default=DEPS_DIR,
    )
    return parser.parse_args()


def rs_init(config_json='red.config.json', dependencies_links=r'deps/'):
    json_path = Path(config_json)
    config = load_json(json_path)
    name = config['name']
    deps_dir = Path(dependencies_links).resolve()

    install_deps_symlinks(deps_dir, exclude={name})
    make_redscript_path_txt(overwrite=True)


def main():
    # args = parseargs()
    rs_init(
        # game_dir=Path(args.game_dir),
        # deps_dir=Path(args.deps_dir),
        # overwrite=args.overwrite,
    )


if __name__ == '__main__':
    main()


def get_pyproject_root():
    project_root = Path.cwd().resolve().parent
    while (
        not (project_root / 'pyproject.toml').exists()
        and project_root.parent != project_root
    ):
        project_root = project_root.parent
    return project_root
