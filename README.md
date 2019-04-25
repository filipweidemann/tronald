# Tronald

> Transfer dumps from remote, dockerized PostgreSQL databases to your local machine without hassle.


- [Installation](#installation)
- [Usage](#usage)

## Installation

```bash
$ pip install tronald
```

---

## Usage

### Show your current settings:
> You will be prompted to enter them on first usage!

```bash
$ tronald settings
```

### Modify settings

```bash
$ tronald settings --key value [--key value ...]
```


| Available settings | Is required? | Description                                                                                                                                     | Example       |
|--------------------|--------------|-------------------------------------------------------------------------------------------------------------------------------------------------|---------------|
| key                | yes          | Path to your private RSA key                                                                                                                    | ~/.ssh/id_rsa |
| db                 | yes          | Default database name                                                                                                                           | app           |
| prefix             | no           | Prefix for container names (company.container_name),  will be used as final fallback for deriving container names from specified host.          | company.      |
| suffix             | no           | Suffix for container names (company.container_name.instance),  will be used as final fallback for deriving container names from specified host. | .instance     |

### Pulling a dump from a remote container

> This is a basic example of writing a PostgreSQL dump to a local file

```bash
$ tronald dump your.host.com dump-file.sql
```

> There's an option to specify the exact container name

```bash
$ tronald dump your.host.com --container your.container dump-file.sql
```

If you don't specify an explicit container name, `tronald` will try to
detect a container on the remote host that matches the host name.
In case of your-host.com, the detection would assume a container with
`your-host.com` in the name. If there is no match, `tronald` will fall
back to deriving a container name with prefix and suffix, if there are
none inside your settings, `tronald` will not continue.


### Importing a dump to your local containers

> It is possible to import the collected dump to your local containers too!

```bash
$ tronald import dump-file.sql container-identifier
```

This will import the dump to your local container.

> Be aware that there may be differences in database setups between remote
> and local environments, such as ownership and psql users.
> The best way would be to keep dockerized applications as close to each other as possible from development to production environment.
> `tronald` will not assume anything about your databases and is solely responsible for gettings dumps in an easy way for developers needing test data.

---

