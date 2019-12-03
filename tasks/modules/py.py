from invoke import task

from ..config import *

@task
def sdist(cx):

    cx.cd("src")
    cx.run("python setup.py sdist")

@task
def clean(cx):
    cx.cd("src")
    cx.run("python setup.py clean")
