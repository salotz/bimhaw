from invoke import task

from ..config import *

from . import org as org_tasks

@task(default=True)
def build(cx, name='dev'):
    """Recreate from scratch the wepy development environment."""

    env_name=f"bimhaw.{name}"

    cx.run(f"conda create -y -n {env_name} python={PY_VERSION}",
        pty=True)

    # install the pip dev dependencies
    cx.run(f"$ANACONDA_DIR/envs/{env_name}/bin/pip install -r configs/{name}.requirements.txt")

    # install the conda dev dependencies
    cx.run(f"conda env update -n {env_name} --file configs/{name}.env.yaml")

    print("--------------------------------------------------------------------------------")
    print(f"run: conda activate {env_name}")

