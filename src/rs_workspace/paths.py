import os
from pathlib import Path

from rs_workspace.workspace import get_pyproject_root

GAME_DIR = Path(os.getenv('CYBERPUNK_GAME_DIR'))
R4EXT = Path('red4ext')
R4EXT_PLUGINS = R4EXT / 'plugins'
R4EXT_PLUGINS_REDSCRIPT_PATHS = R4EXT_PLUGINS / 'redscript_paths.txt'
R6 = Path('r6')
R6_SCRIPTS = R6 / 'scripts'
COMPILER = Path('engine/tools/scc.exe')
PROJECT_ROOT = get_pyproject_root()
BUILD_DIR = PROJECT_ROOT / 'build'
DEPS_DIR = PROJECT_ROOT / 'deps'
GAME_EXE = GAME_DIR / 'bin' / 'x64' / 'Cyberpunk2077.exe'
