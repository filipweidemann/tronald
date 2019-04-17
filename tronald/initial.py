import os
import shelve
import inquirer
from .config import SHELVE_NAME


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
    with shelve.open(SHELVE_NAME) as settings:
        if not "key_path" in settings:
            answer = inquirer.prompt(KEY_PATH_SETUP)
            key_path = answer["key_path"]

            if key_path.startswith("~"):
                key_location = os.path.expanduser(key_path)
            else:
                key_location = key_path

            settings["key_path"] = key_location

        if not "db_name" in settings:
            answer = inquirer.prompt(DEFAULT_DATABASE_SETUP)
            settings["db_name"] = answer["db_name"]

        if not "prefix" in settings:
            answer = inquirer.prompt(CONTAINER_PREFIX)
            settings["prefix"] = answer["prefix"]

        if not "suffix" in settings:
            answer = inquirer.prompt(CONTAINER_SUFFIX)
            settings["suffix"] = answer["suffix"]
