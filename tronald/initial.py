import os
import shelve
import inquirer
import configparser
from .config import DOTFILE_NAME, TronaldConfig

import pdb

pdb.set_trace()


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
    try:
        file = open(DOTFILE_NAME, "r", encoding="ISO-8859-1")
    except FileNotFoundError:
        return

    config = configparser.ConfigParser()
    config.read(file)

    if not "tronald:general" in config.sections():
        questions = [
            KEY_PATH_SETUP,
            DEFAULT_DATABASE_SETUP,
            CONTAINER_PREFIX,
            CONTAINER_SUFFIX,
        ]
        answers = inquirer.prompt(questions)

        config["tronald:general"]["KeyPath"] = answers["key_path"]
        config["tronald:general"]["DefaultDatabase"] = answers["db_name"]
        config["tronald:general"]["Prefix"] = answers["prefix"]
        config["tronald:general"]["Suffix"] = answers["suffix"]
        config.write(file)
        return

    if not "key_path" in config["tronald:general"]:
        answer = inquirer.prompt(KEY_PATH_SETUP)
        key_path = answer["key_path"]

        if key_path.startswith("~"):
            key_location = os.path.expanduser(key_path)
        else:
            key_location = key_path

        config["tronald:general"]["KeyPath"] = key_location

    if not "DefaultDatabase" in config["tronald:general"]:
        answer = inquirer.prompt(DEFAULT_DATABASE_SETUP)
        config["tronald:general"]["DefaultDatabase"] = answer["db_name"]

    if not "Prefix" in config["tronald:general"]:
        answer = inquirer.prompt(CONTAINER_PREFIX)
        config["tronald:general"]["Prefix"] = answer["prefix"]

    if not "suffix" in config["tronald:general"]:
        answer = inquirer.prompt(CONTAINER_SUFFIX)
        config["tronald:general"]["Suffix"] = answer["suffix"]
