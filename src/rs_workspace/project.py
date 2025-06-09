import json
import subprocess
from os import mkdir
from pathlib import Path

from rs_workspace.paths import (
    BUILD_DIR,
    COMPILER,
    GAME_DIR,
    R4EXT_PLUGINS,
    R4EXT_PLUGINS_REDSCRIPT_PATHS,
    R6_SCRIPTS,
)
import shutil

def red_install(cwd: Path):
    """Run red install in the cwd"""
    subprocess.run('red install', cwd=str(cwd))


def install_mod_from_config_json(json_config = None):
    json_config = json_config or 'red.config.json'
    print(f'Installing mod from {json_config}')
    json_path = Path(json_config).resolve()
    config = load_json(json_path)
    src=json_path.parent / config['scripts']['redscript']['src']
    storages = src.parent / 'storages'
    copy_storages(storages=storages, name=config['name'], game_dir=Path(config['game']))
    red_install(json_path.parent)
    compile_to_game_dir()


def compile_to_game_dir(game_dir: Path = GAME_DIR):
    """Compile redscript files in the game_dir"""
    # cwd = cwd or get_pyproject_root()
    scc = game_dir / COMPILER
    rs_scripts_dir = game_dir / R6_SCRIPTS
    r4ext_paths_file = game_dir / R4EXT_PLUGINS_REDSCRIPT_PATHS
    args = [
        str(scc),
        '-compile',
        str(rs_scripts_dir),
        '-compilePathsFile',
        str(r4ext_paths_file),
    ]
    subprocess.run(args)
    # subprocess.run(args, cwd=cwd)


def make_redscript_path_txt(game_dir: Path = GAME_DIR, overwrite=False):
    """Make a redscript_paths.txt file in the red4ext/plugins directory - pass game_dir, or use CYBERPUNK_GAME_DIR env var"""
    r4ext_plugins_dir = game_dir / R4EXT_PLUGINS
    pathfile = game_dir / R4EXT_PLUGINS_REDSCRIPT_PATHS

    if pathfile.exists() and not overwrite:
        print(
            f'File {pathfile} already exists. If you want to overwrite it, call the function with overwrite=True'
        )
        return
    plugins = [_ for _ in r4ext_plugins_dir.iterdir() if _.is_dir()]

    with open(pathfile, 'w') as f:
        for plugin in plugins:
            f.write(f'{plugin.resolve()}\n')


def load_json(config_json: Path) -> dict:
    with open(str(config_json), 'r') as f:
        config = json.load(f)
    return config


def make_config(
    name: str,
    src: Path,
    version: str,
    game_dir: Path = GAME_DIR,
    build_dir: Path = BUILD_DIR,
) -> dict:
    return {
        'name': name,
        'version': version,
        'game': str(game_dir),
        'license': True,
        'stage': str(build_dir / name),
        'scripts': {
            'redscript': {
                'debounceTime': 3000,
                'src': str(src),
                'output': 'r6\\scripts\\',
            }
        },
    }


def make_config_json(config) -> Path:
    mod_build_dir = Path(config['stage'])
    mod_build_dir.mkdir(parents=True, exist_ok=True)

    config_json = mod_build_dir / 'red.config.json'
    with open(str(config_json), 'w') as f:
        json.dump(config, f, indent=4)
    print(f'Created {config=} at {config_json}')
    return config_json

def copy_storages(storages: Path, name: str, game_dir: Path = GAME_DIR):
    strg = game_dir / 'r6' / 'storages' / name
    strg.mkdir(parents=True, exist_ok=True)
    shutil.copytree(storages, strg, dirs_exist_ok=True)


if __name__ == '__main__':
    install_mod_from_config_json(json_config=r'C:\prdev\mod\alberta\red.config.json')