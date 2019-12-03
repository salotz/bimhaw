"""Put user defined tasks in the plugins folder. You can start with
some customizations in this file which is included by default."""

from invoke import task

from ..config import *

@task
def hello(cx):
    """An example custom user task from the plugins."""
    print("Hello")
