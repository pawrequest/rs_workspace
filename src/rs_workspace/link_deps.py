"""Copy SymLinks for dependencies into the local directory... like a rustic VsCode Workspace or IntelliJ Project"""
from pathlib import Path

from rs_workspace.paths import GAME_DIR, R4EXT, R4EXT_PLUGINS, R6, R6_SCRIPTS, DEPS_DIR


def make_links(source: Path, tgt: Path, exclude: set = None):
    exclude = exclude or set()
    if not tgt.exists():
        tgt.mkdir(parents=True)
    for plugin_dir in source.iterdir():
        if plugin_dir in exclude:
            continue
        try:
            plugin_dir = plugin_dir.resolve()
            plugin_name = plugin_dir.name
            output_path = tgt / plugin_name
            output_path.symlink_to(
                plugin_dir, target_is_directory=plugin_dir.is_dir()
            )
            print(f'Linked {plugin_name} to {plugin_dir}')
        except FileExistsError:
            print(f'Link {plugin_dir} already exists')


def install_deps_symlinks(deps_dir: Path = DEPS_DIR, game_dir: Path = GAME_DIR, exclude: set = None):
    """Install symlinks to the game directory for r6 and r4ext"""
    exclude = exclude or set()

    make_links(game_dir / R6_SCRIPTS, deps_dir / R6, exclude=exclude)
    make_links(game_dir / R4EXT_PLUGINS, deps_dir / R4EXT, exclude=exclude)

