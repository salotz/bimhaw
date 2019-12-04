import click

import pkgutil

@click.command()
def cli():

    env_script = pkgutil.get_data(__name__, 'env_script/env.sh')

    click.echo(env_script)

if __name__ == "__main__":

    cli()
