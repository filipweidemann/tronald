import os


def build_postgres_dump(config):
    return "docker exec -t {} pg_dump {} -c -U {} > {}".format(
        config.container, config.db_name, config.postgres_user, config.dump_name
    )


def remove_remote_dump(config):
    return "rm {}".format(config.dump_name)


def import_dump_to_local_container(dump_path, container_identifier, postgres_user):
    return os.system(
        "cat {} | docker exec -i {} psql -U {}".format(
            dump_path, container_identifier, postgres_user
        )
    )

