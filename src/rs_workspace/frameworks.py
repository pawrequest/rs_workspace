from pathlib import Path

from rs_workspace import GAME_DIR, paths, rs_install_launch
from long_temporary import re_combine_archives, redeploy_folder
# UNPACK_TGT = paths.BUILD_DIR / 'unpacked'
# UNPACK_TGT = GAME_DIR
TEST_DIR = paths.BUILD_DIR / 'test'
ARCHIVES = Path(r'C:\prdev\mod\frameworks\installers\do_all')

if __name__ == '__main__':
    # re_combine_archives(ARCHIVES, GAME_DIR)
    gtext = r"C:\prdev\mod\gtext\red.config.json"
    rs_install_launch(gtext)
    # redeploy_folder(UNPACK_TGT, TEST_DIR)
    ...

