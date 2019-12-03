from invoke import task

from ..config import *

@task
def owner(cx):

    print(f"Owner: {OWNER_NAME}")
    print(f"Email: {OWNER_EMAIL}")
    print(f"Nickname: {OWNER_NICKNAME}")

@task
def env(cx):
    print(f"shell profile: {SHELL_PROFILE}")

@task
def license(cx):
    print(f"License: {PROJECT_COPYRIGHT}")

@task(post=[owner, license, env])
def info(cx):
    print(f"Project: {PROJECT_NAME}")
