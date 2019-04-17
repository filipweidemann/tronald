import time
import paramiko
from .commands import (
    build_postgres_dump,
    remove_remote_dump,
    import_dump_to_local_container,
)


def get_channel(client):
    return client.get_transport().open_session()


class RemoteController:
    def __init__(self, config):
        self.client = paramiko.SSHClient()
        self.config = config
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    def dump_and_transfer(self):
        self.client.connect(
            self.config.host,
            username=self.config.ssh_user,
            key_filename=self.config.key_path,
        )
        channel = get_channel(self.client)
        channel.exec_command(build_postgres_dump(self.config))

        while not channel.exit_status_ready():
            time.sleep(0.5)

        sftp = self.client.open_sftp()
        sftp.get(self.config.dump_name, self.config.target)

        channel = get_channel(self.client)
        channel.exec_command(remove_remote_dump(self.config))

        sftp.close()
        self.client.close()


class LocalController:
    def __init__(self, dump_path, container_identifier, postgres_user):
        self.postgres_user = postgres_user
        self.dump_path = dump_path
        self.container = container_identifier

    def import_dump(self):
        configuration_parameters = {
            "dump_path": self.dump_path,
            "container_identifier": self.container,
            "postgres_user": self.postgres_user,
        }
        import_dump_to_local_container(**configuration_parameters)
