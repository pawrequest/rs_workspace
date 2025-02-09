from rs_workspace.setup_workspace import rs_init
from rs_workspace.project_manager import (
    install_mod,
    install_mod_from_config_json,
    make_config,
)


def rs_init_install():
    rs_init()
    install_mod_from_config_json()


all = [
    rs_init,
    install_mod_from_config_json,
    install_mod,
    make_config,
    rs_init_install,
]
