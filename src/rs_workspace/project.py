import json
import os
import subprocess
from pathlib import Path
import shutil

from rs_workspace.paths import (
    AUTOCONTINUE_REDS,
    BUILD_DIR,
    COMPILER,
    GAME_DIR,
    LOG_REDS,
    R4EXT_PLUGINS,
    R4EXT_PLUGINS_REDSCRIPT_PATHS,
    R6_SCRIPTS,
)


def red_cli_install(cwd: Path):
    """Run red install in the cwd"""
    subprocess.run('red install', cwd=str(cwd))


def install_mod(red_config_json: Path):
    print(f'Installing mod from {red_config_json}')
    if not red_config_json.exists():
        raise FileNotFoundError(f'Config file {red_config_json} does not exist')
    if not red_config_json.is_file():
        raise NotADirectoryError(f'Config path {red_config_json} is not a file')
    config = load_json(red_config_json)
    src = red_config_json.parent / config['scripts']['redscript']['src']
    red_cli_install(red_config_json.parent)
    compile_to_game_dir()
    storages = src.parent / 'storages'
    copy_storages(storages=storages, name=config['name'], game_dir=Path(config['game']))


def install_mod_from_config_path(config_dir: Path = None):
    config_dir = config_dir or Path.cwd()
    print(f'Install mod from config path {config_dir}')
    red_config_json = config_dir / 'red.config.json'
    print(f'Installing mod from {red_config_json}')
    install_mod(red_config_json)


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
                'storages': str(src.parent / 'storages'),
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
    """Copy storages from the mod directory to the game directory"""
    if not storages.exists():
        print('Storages path does not exist, skipping copy')
        return
    if not storages.is_dir():
        raise NotADirectoryError(f'Storages path {storages} is not a directory')
    strg = game_dir / 'r6' / 'storages' / name
    print(f'Copying storages from {storages} to {strg}')
    strg.mkdir(parents=True, exist_ok=True)
    shutil.copytree(storages, strg, dirs_exist_ok=True)


def rs_add_utils(autocontinue_reds: Path = AUTOCONTINUE_REDS, log_reds: Path = LOG_REDS):
    r6 = GAME_DIR / R6_SCRIPTS
    r6.mkdir(parents=True, exist_ok=True)
    auto_dest = r6 / autocontinue_reds.name
    log_dest = r6 / log_reds.name

    shutil.copy(log_reds, log_dest)
    shutil.copy(autocontinue_reds, auto_dest)


def remove_utils(autocontinue_reds: Path = AUTOCONTINUE_REDS):
    os.remove(GAME_DIR / R6_SCRIPTS / autocontinue_reds.name)
    os.remove(GAME_DIR / R6_SCRIPTS / LOG_REDS.name)
