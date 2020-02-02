import pkgutil
import os
import os.path as osp

from jinja2 import Template

from . import config

# import the templates from the package for the shell scripts we will
# generate

SH_TEMPLATES = (
    'aliases.sh.j2',
    'funcs.sh.j2',
    'interactive.sh.j2',
    'login_env.sh.j2',
    'login.sh.j2',
    'logout.sh.j2',
    'nonlogin_env.sh.j2',
    'prompt.sh.j2',
)

BASH_TEMPLATES = (
    'autocompletion.bash.j2',
    'funcs.bash.j2',
    'interactive.bash.j2',
    'login.bash.j2',
    'prompt.bash.j2',
)

SINGULARS = ('bash_prompt', 'sh_prompt',)

NONE_PROFILE = "BIMHAW_NONE_PROFILE_SPECIAL_STRING"

def load_profile_templates():

    sh_templates = {}
    for temp_name in SH_TEMPLATES:
        template = pkgutil.get_data(__name__,
                        f'profile_templates/shells/sh/{temp_name}')

        sh_templates[temp_name] = Template(template.decode())

    bash_templates = {}
    for temp_name in BASH_TEMPLATES:
        template = pkgutil.get_data(__name__,
                        f'profile_templates/shells/bash/{temp_name}')
        bash_templates[temp_name] = Template(template.decode())


    profile_d_templates = {
        'shells' : {
            'sh' : sh_templates,
            'bash' : bash_templates,
        }
    }

    return profile_d_templates

def gen_profile(profile_data):
    """Given parameters for the profile generate a dict struct that
    mirrors the directory structure of expanded template scripts.
    """

    profile_templates = load_profile_templates()

    # do the posix shell templates
    sh_scripts = {}
    for temp_name, temp in profile_templates['shells']['sh'].items():

        script_name = temp_name.replace('.j2', '')
        script = temp.render(**profile_data)
        sh_scripts[script_name] = script

    # and the bash scripts
    bash_scripts = {}
    for temp_name, temp in profile_templates['shells']['bash'].items():

        script_name = temp_name.replace('.j2', '')
        script = temp.render(**profile_data)
        bash_scripts[script_name] = script


    profile_d = {
        'shells' : {
            'sh' : sh_scripts,
            'bash' : bash_scripts,
        }
    }

    return profile_d


def make_dict_dir_struct(root_dir, d):
    """Recursively make directories and write files given a dictionary
mirroring that structure."""

    for key, sub in d.items():

        # if the sub is a dictionary descend in recursion
        if issubclass(type(sub), dict):

            dir_path = osp.join(root_dir, key)

            os.makedirs(osp.join(root_dir, key), exist_ok=True)

            make_dict_dir_struct(dir_path, sub)

        # otherwise it should be specifying a file
        else:
            path = osp.join(root_dir, key)
            script = sub

            with open(path, 'w') as wf:
                wf.write(script)


def get_profile_data(profile_name):

    profile_data = {

        # posix shell (sh)
        'sh_login_envs' : config.SH_LOGIN_ENVS[profile_name],
        'sh_nonlogin_envs' : config.SH_NONLOGIN_ENVS[profile_name],
        'sh_logouts' : config.SH_LOGOUTS[profile_name],
        'sh_aliases' : config.SH_ALIASES[profile_name],
        'sh_funcs' : config.SH_FUNCS[profile_name],
        'sh_prompt' : config.SH_PROMPT[profile_name],

        # bash
        'bash_login_sh_envs' : config.BASH_LOGIN_SH_ENVS[profile_name],
        'bash_login_bash_envs' : config.BASH_LOGIN_BASH_ENVS[profile_name],
        'bash_nonlogin_envs' : config.BASH_NONLOGIN_ENVS[profile_name],
        'bash_interactive_envs' : config.BASH_INTERACTIVE_ENVS[profile_name],
        'bash_aliases' : config.BASH_ALIASES[profile_name],
        'bash_funcs' : config.BASH_FUNCS[profile_name],
        'bash_prompt' : config.BASH_PROMPT[profile_name],
        'bash_autocompletions' : config.BASH_AUTOCOMPLETIONS[profile_name],

    }

    if profile_data['sh_prompt'] is None:
        profile_data['sh_prompt'] = NONE_PROFILE

    if profile_data['bash_prompt'] is None:
        profile_data['bash_prompt'] = NONE_PROFILE

    return profile_data


def format_profile_data(profile_data):


    new_d = {}
    for key, data in profile_data.items():

        if type(data) == str:
            fmt_value = "'{}'".format(data)

        else:
            # format for a space delimited list in the shell
            fmt_value = "'{}'".format(" ".join(data))

        new_d[key] = fmt_value

    return new_d


def write_profile(root_dir, profile_name):
    """Save the hierarchy of files and directories for a profile."""

    # get the profile data from the name
    profile_data = get_profile_data(profile_name)

    fmt_profile_data = format_profile_data(profile_data)

    # fill out the templates using the data
    profile_d = gen_profile(fmt_profile_data)

    os.makedirs(root_dir, exist_ok=True)

    profile_dir = osp.join(root_dir, profile_name)

    make_dict_dir_struct(profile_dir, profile_d)

