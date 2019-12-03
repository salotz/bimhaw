from invoke import task

from ..config import *

@task(default=True)
def tangle(cx):
    """Tangle all the code blocks for dirs in TANGLE_DIRS."""

    # tangle them
    cx.run("emacs -Q --batch -l org project.org -f org-babel-tangle")

@task
def clean(cx):
    """Clean all the tangled documents in TANGLE_DIRS."""

    for tangle_dir in TANGLE_DIRS:
        cx.run(f"rm -f {tangle_dir}/*")
        cx.run(f"touch {tangle_dir}/.keep")
