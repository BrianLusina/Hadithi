"""
Sets up the environment variables from .env file in the project root
"""
import os

env_file = "./.env"


def setup_envvariables():
    """
    This will setup the environment variables
    :return: 
    """
    if os.path.exists(env_file):
        print("Importing environment variables")
        for line in open(env_file):
            var = line.strip().split("=")
            if len(var) == 2:
                os.environ[var[0]] = var[1]


if __name__ == "__main__":
    setup_envvariables()
