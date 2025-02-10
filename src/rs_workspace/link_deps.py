from pathlib import Path

from rs_workspace.paths import GAME_DIR, R4EXT, R4EXT_PLUGINS, R6, R6_SCRIPTS


def make_links(source: Path, tgt: Path, exclude: set = None):
    exclude = exclude or set()
    if not tgt.exists():
        tgt.mkdir(parents=True)
    for plugin_dir in source.iterdir():
        if (
            plugin_dir.is_dir() or plugin_dir.is_file()
        ) and plugin_dir.name not in exclude:
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


def install_deps_symlinks(deps_dir: Path, game_dir: Path = None, exclude: set = None):
    """Install symlinks to the game directory for r6 and r4ext"""
    game_dir = game_dir or GAME_DIR
    exclude = exclude or set()

    make_links(game_dir / R6_SCRIPTS, deps_dir / R6, exclude=exclude)
    make_links(game_dir / R4EXT_PLUGINS, deps_dir / R4EXT, exclude=exclude)


#####


# def install_deps_symlinks1(deps_dir: Path, game_dir: Path = None, exclude: set = None):
#     """Install symlinks to the game directory for r6 and r4ext"""
#     game_dir = game_dir or game_dir_from_env()
#     game_dir = Path(game_dir)
#     exclude = exclude or set()
#
#     r6_dir = game_dir / 'r6' / 'scripts'
#     r4ext_dir = game_dir / 'red4ext' / 'plugins'
#     r6_out = deps_dir / 'r6'
#     r4ext_out = deps_dir / 'r4ext'
#
#     make_links(r6_dir, r6_out, exclude=exclude)
#     make_links(r4ext_dir, r4ext_out, exclude=exclude)
