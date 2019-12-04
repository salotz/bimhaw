import click

import pkgutil
import os
import os.path as osp

from bimhaw import CONFIG_DIR

SHELL_DOTFILES_DIRNAME = 'shell_dotfiles'
LIB_DIRNAME = 'lib'
PROFILES_DIRNAME = 'profiles'

SHELL_DOTFILE_NAMES = (
    'profile',
    'bash_profile',
    'bashrc',
    'bash_logout',
)

LIB_DIRS = (
    'setups',
    'configs',
    'inits',
    'checkins',
    'checkouts',
    'shell/sh/aliases',
    'shell/sh/envs',
    'shell/sh/funcs',
    'shell/sh/logouts',
    'shell/sh/prompts',
    'shell/bash/envs',
    'shell/bash/funcs',
    'shell/bash/prompts',
    'shell/bash/autocomplete',
)

@click.command()
def cli():

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

    # then make the lib dirs
    lib_dir = osp.join(CONFIG_DIR, LIB_DIRNAME)

    os.makedirs(lib_dir)

    for sub_lib_dir in LIB_DIRS:
        sub_dir = osp.join(lib_dir, sub_lib_dir)
        os.makedirs(sub_dir)

    # then generate the default config.py file
    config_str = pkgutil.get_data(__name__,
                                  'profile_config/config.py')

    config_path = osp.join(CONFIG_DIR, 'config.py')
    with open(config_path, 'wb') as wf:
        wf.write(config_str)


    # the profiles dir
    profiles_dir = osp.join(CONFIG_DIR, PROFILES_DIRNAME)
    os.makedirs(profiles_dir)


if __name__ == "__main__":

    cli()
