import os
import shelve
import inquirer
import configparser
from .config import DOTFILE_NAME, TronaldConfig


KEY_PATH_SETUP = [
    inquirer.Text(
        "key_path",
        "Please enter the absolute path to your preferred RSA private key",
        default="~/.ssh/id_rsa",
    )
]

DEFAULT_DATABASE_SETUP = [
    inquirer.Text(
        "db_name",
        "Please enter the default database name to pull dumps from.",
        default="app",
    )
]

CONTAINER_PREFIX = [
    inquirer.Text(
        "prefix",
        "If there are common container prefixes, please provide them for container name derivation.",
    )
]

CONTAINER_SUFFIX = [
    inquirer.Text(
        "suffix",
        "If there are common container suffixes, please provide them for container name derivation.",
    )
]


def perform_initial_setup():
    config = TronaldConfig()

    if not config.get_value("keypath"):
        answer = inquirer.prompt(KEY_PATH_SETUP)
        key_path = answer["key_path"]

        if key_path.startswith("~"):
            key_location = os.path.expanduser(key_path)
        else:
            key_location = key_path

        config.set_value("keypath", key_location)

    if not config.get_value("defaultdatabase"):
        answer = inquirer.prompt(DEFAULT_DATABASE_SETUP)
        config.set_value("defaultdatabase", answer["db_name"])

    if not config.get_value("prefix"):
        answer = inquirer.prompt(CONTAINER_PREFIX)
        config.set_value("prefix", answer["prefix"])

    if not config.get_value("suffix"):
        answer = inquirer.prompt(CONTAINER_SUFFIX)
        config.set_value("suffix", answer["suffix"])
