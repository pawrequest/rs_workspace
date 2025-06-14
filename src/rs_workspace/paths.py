import os
from pathlib import Path

DIST = Path(__file__).parent.parent.parent / 'dist'

GAME_DIR = Path(os.getenv('CYBERPUNK_GAME_DIR'))
if not GAME_DIR:
    raise ValueError()

R4EXT = Path('red4ext')
R4EXT_PLUGINS = R4EXT / 'plugins'
R4EXT_PLUGINS_REDSCRIPT_PATHS = R4EXT_PLUGINS / 'redscript_paths.txt'
R6 = Path('r6')
R6_SCRIPTS = R6 / 'scripts'
COMPILER = Path('engine/tools/scc.exe')



def get_pyproject_root():
    project_root = Path.cwd().resolve()
    while (
        not (project_root / 'pyproject.toml').exists()
        and project_root.parent != project_root
    ):
        project_root = project_root.parent
    print('Project root = ', project_root.name)
    return project_root


PROJECT_ROOT = get_pyproject_root()
BUILD_DIR = PROJECT_ROOT / 'build'
DEPS_DIR = PROJECT_ROOT / 'deps'
GAME_EXE = GAME_DIR / 'bin' / 'x64' / 'Cyberpunk2077.exe'
AUTOCONTINUE_REDS = DIST / 'AutoContinue.reds'
LOG_REDS = DIST / 'Log.reds'