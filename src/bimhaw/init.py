import click

import pkgutil
import os
import os.path as osp

from . import (
    CONFIG_DIR,
    LIB_DIRNAME,
    LIB_DIRS,
    SHELL_DOTFILES_DIRNAME,
    SHELL_DOTFILE_NAMES,
    PROFILES_DIRNAME
)


def initialize(
        config=None,
        lib=None,
):

    dotfiles_dir = osp.join(CONFIG_DIR, SHELL_DOTFILES_DIRNAME)
    os.makedirs(dotfiles_dir)

    # load the shell files
    for dotfile_name in SHELL_DOTFILE_NAMES:
        dotfile = pkgutil.get_data(__name__,
                                   f'shell_dotfiles/{dotfile_name}')

        path = osp.join(dotfiles_dir, dotfile_name)
        # write them to the init dir
        with open(path, 'wb') as wf:
            wf.write(dotfile)


    # connect to or make a lib dir

    # the default, not loading an external one
    lib_dir = osp.join(CONFIG_DIR, LIB_DIRNAME)

    if lib is None:

        os.makedirs(lib_dir)

        for sub_lib_dir in LIB_DIRS:
            sub_dir = osp.join(lib_dir, sub_lib_dir)
            os.makedirs(sub_dir)

    else:
        # load the external one via a symlink
        os.symlink(lib, lib_dir)

    ## Generate or link to the config file

    config_path = osp.join(CONFIG_DIR, 'config.py')
    if config is None:
        # generate the default config.py file
        config_str = pkgutil.get_data(__name__,
                                      'profile_config/config.py')

        with open(config_path, 'wb') as wf:
            wf.write(config_str)

    else:
        os.symlink(config, config_path)

    # then generate the default env.sh file
    env_str = pkgutil.get_data(__name__,
                                  'env_script/env.sh')

    env_path = osp.join(CONFIG_DIR, 'env.sh')
    with open(env_path, 'wb') as wf:
        wf.write(env_str)


    # the profiles dir
    profiles_dir = osp.join(CONFIG_DIR, PROFILES_DIRNAME)
    os.makedirs(profiles_dir)


@click.command()
@click.option("--config", default=None, type=click.Path(exists=True))
@click.option("--lib", default=None, type=click.Path(exists=True))
def cli(config, lib):

    initialize(config, lib)


if __name__ == "__main__":

    cli()
