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
    red_cli_install(red_config_json.parent)
    compile_to_game_dir()


def install_mod_from_config_path(config_path: Path = Path.cwd()):
    if config_path.is_dir():
        red_config_json = config_path / 'red.config.json'
    elif config_path.is_file():
        red_config_json = config_path
    else:
        raise ValueError(
            f'Config path {config_path} is neither a file nor a directory. Please provide a valid path.'
        )
    install_mod(red_config_json)


def compile_to_game_dir(game_dir: Path = GAME_DIR):
    """Compile redscript files in the game_dir"""
    # cwd = cwd or get_pyproject_root()
    if not game_dir.exists():
        raise FileNotFoundError(f'Game directory {game_dir} does not exist')
    if not game_dir.is_dir():
        raise NotADirectoryError(f'Game path {game_dir} is not a directory')
    if not (game_dir / 'bin' / 'x64' / 'Cyberpunk2077.exe').exists():
        raise FileNotFoundError(
            f'Game directory {game_dir} does not contain Cyberpunk2077.exe in bin/x64'
        )
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
