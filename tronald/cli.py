import click
import shelve
import inquirer
from time import sleep

from .config import Config, SHELVE_NAME
from .controllers import RemoteController, LocalController
from .initial import (
    KEY_PATH_SETUP,
    DEFAULT_DATABASE_SETUP,
    CONTAINER_PREFIX,
    CONTAINER_SUFFIX,
    perform_initial_setup,
)


@click.group()
def cli():
    pass


@cli.command(name="settings")
@click.option("--prefix", "prefix")
@click.option("--suffix", "suffix")
@click.option("--key", "key_path")
@click.option("--db", "db_name")
def set_prefix(prefix, suffix, key_path, db_name):
    with shelve.open(SHELVE_NAME) as settings:
        if not prefix and not suffix and not key_path and not db_name:
            click.echo("Current settings:\n")
            for key, value in settings.items():
                click.echo("{}: {}".format(key, value))

        if prefix:
            settings["prefix"] = prefix

        if suffix:
            settings["suffix"] = suffix

        if key_path:
            settings["key_path"] = key_path

        if db_name:
            settings["db_name"] = db_name


@cli.command()
@click.option("--container", "container")
@click.option("--ssh-user", "ssh_user")
@click.option("--postgres-user", "postgres_user")
@click.argument("host")
@click.argument("target")
def dump(host, container, ssh_user, postgres_user, target):
    configuration_parameters = {
        "host": host,
        "ssh_user": ssh_user,
        "postgres_user": postgres_user,
        "container": container,
        "target": target,
    }
    config = Config(**configuration_parameters)
    controller = RemoteController(config)
    controller.dump_and_transfer()


@cli.command(name="import")
@click.argument("dump_path")
@click.argument("container_identifier")
@click.option("--postgres-user", "postgres_user")
def import_dump(dump_path, container_identifier, postgres_user):
    configuration_parameters = {
        "dump_path": dump_path,
        "container_identifier": container_identifier,
        "postgres_user": postgres_user or "django",
    }
    controller = LocalController(**configuration_parameters)
    controller.import_dump()


def run_cli():
    perform_initial_setup()
    cli()


if __name__ == "__main__":
    perform_initial_setup()
    cli()
