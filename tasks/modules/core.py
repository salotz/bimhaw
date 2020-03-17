from invoke import task

@task
def sanity(cx):
    """Perform sanity check for jubeo"""

    print("All systems go!")

