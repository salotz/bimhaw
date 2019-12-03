from invoke import task

from ..config import *

@task
def lfs_track(cx):
    """Update all the files that need tracking via git-lfs."""

    for lfs_target in GIT_LFS_TARGETS:
        cx.run("git lfs track {}".format(lfs_target))
