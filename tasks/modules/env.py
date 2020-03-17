from invoke import task

import sys
import os
import os.path as osp
from pathlib import Path

from ..config import (
    ENV_METHOD,
    DEFAULT_ENV,
    ENVS_DIR,
)

## user config examples

# SNIPPET:

# # which virtual environment tool to use: venv or conda
# ENV_METHOD = 'venv'

# # which env spec to use by default
# DEFAULT_ENV = 'dev'

# # directory where env specs are read from
# ENVS_DIR = 'envs'

## Constants

# directories the actual environments are stored
VENV_DIR = "_venv"
CONDA_ENVS_DIR = "_conda_envs"

# specified names of env specs files
SELF_REQUIREMENTS = 'self.requirements.txt'
"""How to install the work piece"""

PYTHON_VERSION_FILE = 'pyversion.txt'
"""Specify which version of python to use for the env"""

DEV_REQUIREMENTS_LIST = 'dev.requirements.list'
"""Multi-development mode repos to read dependencies from."""

### Util

def parse_list_format(list_str):

    return [line for line in list_str.split('\n')
            if not line.startswith("#") and line.strip()]


### Dependencies
# managing dependencies for the project at runtime

## pip: things that can be controlled by pip

def deps_pip_pin(cx,
                 name=DEFAULT_ENV,
                 upgrade=False):

    path = Path(ENVS_DIR) / name

    # gather any development repos that are colocated on this machine
    # and solve the dependencies together

    specs = [f"{path}/requirements.in"]

    # to get the development repos read the DEV list
    if osp.exists(path / DEV_REQUIREMENTS_LIST):
        with open(path / DEV_REQUIREMENTS_LIST) as rf:
            dev_repo_specs = parse_list_format(rf.read())

        # for each repo spec add this to the list of specs to evaluate for
        for dev_repo_spec in dev_repo_specs:
            assert osp.exists(dev_repo_spec), f"Repo spec {dev_repo_spec} doesn't exist"

            specs.append(dev_repo_spec)


    spec_str =  " ".join(specs)

    print(spec_str)

    upgrade_str = ''
    if upgrade:
        upgrade_str = "--upgrade"


    cx.run("pip-compile "
           f"{upgrade_str} "
           f"--output-file={path}/requirements.txt "
           f"{spec_str}")

    # SNIPPET: generate hashes is not working right, or just confusing me
    # cx.run("python -m piptools compile "
    #        "--generate-hashes "
    #        "--output-file=requirements.txt "
    #        f"requirements.in")


## conda: managing conda dependencies

def deps_conda_pin(cx,
                   name=DEFAULT_ENV,
                   upgrade=False,
                   optional=False,
):

    # STUB: currently upgrade does nothing

    env_spec_path = Path(ENVS_DIR) / name

    if not optional:
        assert osp.exists(env_spec_path / 'env.yaml'), \
            "There must be an 'env.yaml' file to compile from"

    else:
        if not osp.exists(env_spec_path / 'env.yaml'):
            return None

    # delete the pinned file
    if osp.exists(env_spec_path / 'env.pinned.yaml'):
        os.remove(env_spec_path / 'env.pinned.yaml')

    # make the environment under a mangled name so we don't screw with
    # the other one
    mangled_name = f"__mangled_{name}"
    env_dir = conda_env(cx, name=mangled_name)

    # REFACT: This is copied from the conda_env function and should be
    # factored into it's own thing

    # then install the packages so we can export them
    with cx.prefix(f'eval "$(conda shell.bash hook)" && conda activate {env_dir}'):

        # only install the declared dependencies
        cx.run(f"conda env update "
               f"--prefix {env_dir} "
               f"--file {env_spec_path}/env.yaml")

    # pin to a 'env.pinned.yaml' file
    cx.run(f"conda env export "
           f"-p {env_dir} "
           f"-f {env_spec_path}/env.pinned.yaml")


    # then destroy the temporary mangled env
    cx.run(f"rm -rf {env_dir}")

# altogether
@task
def deps_pin(cx, name=DEFAULT_ENV):

    deps_pip_pin(cx,
                 name=name,
                 upgrade=False)

    deps_conda_pin(cx,
                   name=name,
                   upgrade=False,
                   optional=True,)

@task
def deps_pin_update(cx, name=DEFAULT_ENV):

    deps_pip_update(cx,
                    name=name,
                    upgrade=True,
    )

    deps_conda_update(cx,
                      name=name,
                      optional=True,
                      upgrade=True)


### Environments

def conda_env(cx, name=DEFAULT_ENV):

    # locally scoped since the environment is global to the
    # anaconda installation
    env_name = name

    # where the specs of the environment are
    env_spec_path = Path(ENVS_DIR) / name

    # using the local envs dir
    env_dir = Path(CONDA_ENVS_DIR) / name

    # figure out which python version to use, if the 'py_version.txt'
    # file exists read it
    py_version_path = env_spec_path / PYTHON_VERSION_FILE
    if osp.exists(py_version_path):
        with open(py_version_path, 'r') as rf:
            py_version = rf.read().strip()

        # TODO: validate the string for python version

    # otherwise use the one you are currently using
    else:
        py_version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"

    # create the environment
    cx.run(f"conda create -y "
           f"--prefix {env_dir} "
           f"python={py_version}",
        pty=True)

    with cx.prefix(f'eval "$(conda shell.bash hook)" && conda activate {env_dir}'):

        # install the conda dependencies. choose a specification file
        # based on these priorities of most pinned to least frozen.
        if osp.exists(env_spec_path / "env.pinned.yaml"):

            cx.run(f"conda env update "
                   f"--prefix {env_dir} "
                   f"--file {env_spec_path}/env.pinned.yaml")


        elif osp.exists(env_spec_path / "env.yaml"):

            cx.run(f"conda env update "
                   f"--prefix {env_dir} "
                   f"--file {env_spec_path}/env.yaml")

        else:
            # don't do a conda env pin
            pass


        # install the extra pip dependencies
        if osp.exists(f"{env_spec_path}/requirements.txt"):
            cx.run(f"{env_dir}/bin/pip install "
                   f"-r {env_spec_path}/requirements.txt")

        # install the package itself
        if osp.exists(f"{env_spec_path}/self.requirements.txt"):
            cx.run(f"{env_dir}/bin/pip install -r {env_spec_path}/self.requirements.txt")

    print("--------------------------------------------------------------------------------")
    print(f"run: conda activate {env_dir}")


def venv_env(cx, name=DEFAULT_ENV):

    venv_dir_path = Path(VENV_DIR)
    venv_path = venv_dir_path / name

    env_spec_path = Path(ENVS_DIR) / name

    # ensure the directory
    cx.run(f"mkdir -p {venv_dir_path}")

    # create the env requested
    cx.run(f"python -m venv {venv_path}")

    # then install the things we need
    with cx.prefix(f"source {venv_path}/bin/activate"):

        # update pip
        cx.run("pip install --upgrade pip")

        if osp.exists(f"{env_spec_path}/{SELF_REQUIREMENTS}"):
            cx.run(f"pip install -r {env_spec_path}/requirements.txt")

        else:
            print("No requirements.txt found")

        # if there is a 'self.requirements.txt' file specifying how to
        # install the package that is being worked on install it
        if osp.exists(f"{env_spec_path}/{SELF_REQUIREMENTS}"):
            cx.run(f"pip install -r {env_spec_path}/{SELF_REQUIREMENTS}")

        else:
            print("No self.requirements.txt found")

    print("----------------------------------------")
    print("to activate run:")
    print(f"source {venv_path}/bin/activate")

@task
def make(cx, name=DEFAULT_ENV):

    # choose your method:
    if ENV_METHOD == 'conda':
        conda_env(cx, name=name)

    elif ENV_METHOD == 'venv':
        venv_env(cx, name=name)

@task
def conda_ls(cx):
    print('\n'.join(os.listdir(CONDA_ENVS_DIR)))

@task
def venv_ls(cx):

    print('\n'.join(os.listdir(VENV_DIR)))

@task
def specs(cx):

    print('\n'.join(os.listdir(ENV_SPEC_DIR)))

@task
def ls(cx):

    # choose your method:
    if ENV_METHOD == 'conda':
        conda_ls(cx)

    elif ENV_METHOD == 'venv':
        venv_ls(cx)

@task
def clean(cx):
    cx.run(f"rm -rf {VENV_DIR}")
