"""For updating the tasks modules."""

from invoke import task

from git import Repo
import os.path as osp

from ..config import *

@task
def init(cx):
    """Initialize the store for the repos to be downloaded to."""

    cx.run(f"mkdir -p {COOKIEJAR_DIR}")

@task(pre=[init])
def clean(cx):
    """Remove all downloaded repos for updating."""

    cx.run(f"rm -rf {COOKIEJAR_DIR}/*")

@task(pre=[init, clean], post=[clean], default=True)
def update(cx):
    """Update the shared modules for this project."""

    repo_path = osp.expanduser(osp.expandvars(f"{COOKIEJAR_DIR}/{COOKIECUTTER_NAME}"))
    # download the repo
    repo = Repo.clone_from(UPDATE_URL,
                           repo_path)


    # then get modules we need and replace the ones in this project
    # with them
    print("Updating tasks/sysconfig.py")
    cx.run(f"cp -f {repo_path}/" +
           "*cookiecutter.project_name*/tasks/sysconfig.py ./tasks/sysconfig.py",
           pty=True)

    print("Updating tasks/__init__.py")
    cx.run(f"cp -f {repo_path}/" +
           "*cookiecutter.project_name*/tasks/__init__.py ./tasks/__init__.py",
           pty=True)

    print("Updating tasks/modules")
    cx.run(f"cp -rf {repo_path}/" +
           "*cookiecutter.project_name*/tasks/modules/ ./tasks/")
