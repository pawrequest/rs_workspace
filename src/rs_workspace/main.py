from pathlib import Path

from rs_workspace import workspace
from rs_workspace.project import install_mod, install_mod_from_config_json, make_config

if __name__ == '__main__':
    setup_workspace.rs_init()
    # install_mod(name="toronto", src=Path(r'D:\prdev\repos\redscript_workspace\mods\toronto\src'), version="0.0.1")

    # toronto_config = r'D:\prdev\repos\redscript_workspace\mods\toronto\red_config.json'
    # install_mod_from_config_json(Path(toronto_config))

    # gen_config = r'D:\prdev\repos\redscript_workspace\mods\generative-texting\red.config.json'
    # install_mod_from_config_json(Path(gen_config))

    config = make_config(name="GenerativeTexting", src=Path(r'D:\prdev\repos\redscript_workspace\mods\generative-texting\src'), version="0.0.1")
    install_mod(config)


