import ctypes
import os
import shutil
import subprocess
import sys
from pathlib import Path

from rs_workspace.paths import AUTOCONTINUE_REDS, GAME_DIR, GAME_EXE, R6_SCRIPTS, LOG_REDS
from rs_workspace.workspace import rs_init as rs1
from rs_workspace.project import (
    install_mod_from_config_json,
    make_config,
)

def rs_add_utils(autocontinue_reds: Path = AUTOCONTINUE_REDS, log_reds: Path = LOG_REDS):
    r6 = GAME_DIR / R6_SCRIPTS
    r6.mkdir(parents=True, exist_ok=True)
    auto_dest = r6 / autocontinue_reds.name
    log_dest = r6 / log_reds.name

    shutil.copy(log_reds, log_dest)
    shutil.copy(autocontinue_reds, auto_dest)


def rs_init():
    rs1()
    rs_add_utils()

def rs_install(config_path:str = None):
    config_path = config_path or 'red.config.json'
    install_mod_from_config_json(config_path)


def rs_init_install(config_path:str = None):
    rs_init()
    rs_install(config_path)


# def launch():
#     # subprocess.run([GAME_EXE, '-skipStartScreen', '--launcher-skip'])
#     subprocess.run(['runas', '/user:Administrator', GAME_EXE, '-skipStartScreen', '--launcher-skip'])


def rs_launch():
    # if not ctypes.windll.shell32.IsUserAnAdmin():
    #     # Run the game executable with admin rights
    #     args = ['-skipStartScreen', '--launcher-skip']
    #     ctypes.windll.shell32.ShellExecuteW(None, "runas", str(GAME_EXE), ' '.join(args), None, 1)
    # else:
        # Run the game directly
    subprocess.run([GAME_EXE])

# def launch():
#     if not ctypes.windll.shell32.IsUserAnAdmin():
#         # Re-run the program with admin rights
#         ctypes.windll.shell32.ShellExecuteW(None, "runas", GAME_EXE, None, 1)
#     else:
#         # Run the program directly
#         subprocess.run([GAME_EXE])
# def launch():
#     cms = [GAME_EXE]
#
#     if not ctypes.windll.shell32.IsUserAnAdmin():
#         prog = subprocess.run(['runas', '/noprofile', '/user:Administrator'] + cms, stdin=subprocess.PIPE)
#         # prog.communicate()
#         # ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, f'"{GAME_EXE}" -skipStartScreen --launcher-skip', None, 1)
#     else:
#         subprocess.run(cms)

def rs_install_launch(config_path:str = None):
    rs_install(config_path)
    rs_launch()


def rs_init_install_launch(config_path:str = None):
    rs_init_install(config_path)
    rs_launch()



def remove_utils(autocontinue_reds: Path = AUTOCONTINUE_REDS):
    os.remove(GAME_DIR / R6_SCRIPTS / autocontinue_reds.name)
    os.remove(GAME_DIR / R6_SCRIPTS / LOG_REDS.name)


all = [
    make_config,
    rs_launch,
    rs_init,
    rs_install,
    rs_init_install,
    rs_launch,
    rs_install_launch,
    rs_init_install_launch,
    rs_add_utils,
    remove_utils,
]
