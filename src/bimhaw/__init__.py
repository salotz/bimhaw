# -*- coding: utf-8 -*-

"""Top-level package."""

from ._version import __version__

__author__ = "Samuel D. Lotz"
__email__ = 'samuel.lotz@salotz.info'


# module stuff
import os.path as osp


CONFIG_DIR = osp.expanduser(osp.expandvars("$HOME/.bimhaw"))

SHELL_DOTFILES_DIRNAME = 'shell_dotfiles'

PROFILES_DIRNAME = 'profiles'

SHELL_DOTFILE_NAMES = (
    'profile',
    'bash_profile',
    'bashrc',
    'bash_logout',
)

LIB_DIRNAME = 'lib'
LIB_DIRS = (
    'sh/aliases',
    'sh/envs',
    'sh/funcs',
    'sh/logouts',
    'sh/prompts',
    'bash/envs',
    'bash/funcs',
    'bash/prompts',
    'bash/autocomplete',
)
