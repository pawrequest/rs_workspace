import os

from rs_workspace.paths import GAME_EXE
from rs_workspace.workspace import rs_init
from rs_workspace.project import (
    install_mod_from_config_json,
    make_config,
)


def rs_install():
    install_mod_from_config_json()


def rs_init_install():
    rs_init()
    install_mod_from_config_json()


def launch():
    os.startfile(str(GAME_EXE))

def rs_install_launch():
    install_mod_from_config_json()
    launch()


def rs_init_install_launch():
    rs_init_install()
    launch()


all = [
    make_config,
    launch,
    rs_init,
    rs_install,
    rs_init_install,
    rs_install_launch,
    rs_init_install_launch,
]
