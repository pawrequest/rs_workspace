import json
import os
import subprocess
from pathlib import Path


def red_install(cwd: Path):
    """Run red install in the cwd"""
    subprocess.run('red install', shell=True, cwd=str(cwd))

def install_mod(config:dict):
    cwd_path = Path(config['stage'])
    cwd_path.mkdir(parents=True, exist_ok=True)
    red_install(cwd=cwd_path)
    # compile_to_game_dir()


def install_mod_from_config_json1(config_json:Path):

    # config = make_config(name=name, src=Path(src), version=version)
    config = load_json(config_json)
    # make_config_json(config)
    red_install(config_json.parent)
    compile_to_game_dir()


def install_mod_from_config_json():
    json_path = Path('red.config.json')
    # config = make_config(name=name, src=Path(src), version=version)
    config = load_json(json_path)
    # make_config_json(config)
    red_install(json_path.parent)
    compile_to_game_dir()



def compile_to_game_dir(game_dir: Path = None):
    """Compile redscript files in the game_dir"""
    # cwd = cwd or get_pyproject_root()
    game_dir = game_dir or Path(game_dir_from_env())
    scc = game_dir / 'engine/tools/scc.exe'
    rs_scripts_dir = game_dir / 'r6/scripts/'
    r4ext_paths_file = game_dir / 'red4ext/redscript_paths.txt'
    args = [
        str(scc),
        '-compile',
        str(rs_scripts_dir),
        '-compilePathsFile',
        str(r4ext_paths_file),
    ]
    subprocess.run(args)
    # subprocess.run(args, cwd=cwd)


def make_redscript_path_txt(game_dir: Path = None, overwrite=True):
    """Make a redscript_paths.txt file in the red4ext/plugins directory - pass game_dir, or use CYBERPUNK_GAME_DIR env var"""
    game_dir = game_dir or game_dir_from_env()
    game_dir = Path(game_dir)
    r4ext_plugins_dir = game_dir / 'red4ext/plugins/'
    pathfile = r4ext_plugins_dir / 'redscript_paths.txt'
    if pathfile.exists() and not overwrite:
        print(
            f'File {pathfile} already exists. If you want to overwrite it, call the function with overwrite=True'
        )
        return
    plugins = [_ for _ in r4ext_plugins_dir.iterdir() if _.is_dir()]

    with open(pathfile, 'w') as f:
        for plugin in plugins:
            f.write(f'{plugin.resolve()}\n')


def get_deps_dir():
    project_root = get_pyproject_root()
    rsrc = project_root / 'rsrc'
    print(f'Project Root: {project_root.name}, Dependencies Directory: {rsrc}')
    return rsrc


def get_pyproject_root():
    project_root = Path.cwd().resolve().parent
    while (
        not (project_root / 'pyproject.toml').exists()
        and project_root.parent != project_root
    ):
        project_root = project_root.parent
    return project_root


def get_build_dir() -> Path:
    project_root = get_pyproject_root()
    build_dir = project_root / 'build'
    print(f'Project Root: {project_root.name}, Build Directory: {build_dir}')
    return build_dir


def get_stage(name: str) -> Path:
    build_dir = get_build_dir() / name
    print(f'Build Directory: {build_dir}')
    return build_dir


def game_dir_from_env_path():
    game_dir = os.getenv('CYBERPUNK_GAME_DIR')
    if not game_dir:
        raise ValueError('game_dir not provided and CYBERPUNK_GAME_DIR not set')
    return Path(game_dir)


def game_dir_from_env():
    game_dir = os.getenv('CYBERPUNK_GAME_DIR')
    if not game_dir:
        raise ValueError('game_dir not provided and CYBERPUNK_GAME_DIR not set')
    return game_dir


def load_json(config_json:Path) -> dict:
    with open(str(config_json), 'r') as f:
        config = json.load(f)
    return config


def make_config(
    name: str,
    src: Path,
    version: str,
    game_dir: Path = None,
) -> dict:
    game_dir = game_dir or game_dir_from_env()
    return {
        'name': name,
        'version': version,
        'game': str(game_dir),
        'license': True,
        'stage': str(get_stage(name)),
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
    print(f'Created {mod_build_dir}')

    config_json = mod_build_dir / 'red_config.json'
    with open(str(config_json), 'w') as f:
        json.dump(config, f, indent=4)
    print(f'Created {config_json}')
    return config_json
