"""
Sets up the environment variables from .env file in the project root
"""
import os
import click

env_file = "./.env"


def setup_env_variables():
    """
    This will setup the environment variables
    :return: 
    """
    if os.path.exists(env_file):
        click.echo(click.style(">>>> Importing environment variables", fg="cyan", bold=True))
        for line in open(env_file):
            var = line.strip().split("=")
            if len(var) == 2:
                os.environ[var[0]] = var[1]


if __name__ == "__main__":
    setup_env_variables()
