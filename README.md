Rocked
======

A thin wrapper to manage [Docker][docker] containers. It just generates command line arguments to be passed to the `docker` client, based on the chosen command and loading the container configuration data from a manifest file, written in [YAML][yaml] format. So, instead of typing `docker run --rm -t -i -e DATABASE_NAME=django_app -e DJANGO_SECRET_KEY --link db_postgres:db -v /home/myhro/projects/django-example:/app python-baseimage python manage.py shell` every time you want to access the [Django Shell][django-shell], you would just type `rocked run web.yml python manage.py shell`, which produces the same result.

## Dependencies

Its only dependencies are [docopt][docopt] and [PyYAML][pyyaml], which can be installed either in a virtualenv or in a system-wide installation using [pip][pip]:

`pip install -r requirements.txt`

## Installation

As Rocked is not available on [PyPI][pypi] yet, you have to clone this repository and add its executable to anywhere on your `$PATH`, e.g.:

    sudo git clone https://github.com/myhro/rocked.git /usr/local/lib/rocked
    sudo ln -s /usr/local/lib/rocked/rocked.py /usr/local/bin/rocked

Then you can just use the `rocked` command:

    [myhro@wheezy:~]$ rocked -h
    Rocked, a thin wrapper to manage Docker containers.

    Usage:
        rocked build [--no-cache] <file.yml>
        rocked kill <file.yml>
        rocked logs [-f] <file.yml>
        rocked run <file.yml> [--] [<command>...]
        rocked restart <file.yml>
        rocked start <file.yml>
        rocked status <file.yml>
        rocked stop <file.yml>
        rocked -h | --help

    Options:
        -h --help   Show this screen.

## Manifest

The manifest file is written in YAML format. This is the list of supported and required keys:

| Key         | Type   | Description                                           | Required |
| ----------- | ------ | ----------------------------------------------------- | -------- |
| build       | string | Directory where a `Dockerfile` to be built is located | no       |
| command     | string | Command to be executed on the container               | no       |
| environment | list   | List of environment variables to be set               | no       |
| image       | string | Name of the image                                     | yes      |
| links       | list   | List of other containers to be linked                 | no       |
| name        | string | Name of the container                                 | yes      |
| ports       | list   | List of ports to be published                         | no       |
| volumes     | list   | List of volumes to be mounted                         | no       |

## Examples

### Database container

Create a container based on the `postgres` image (tag `9.3`), named `db_postgres` and mount a persistent volume to store [PostgresSQL][postgresql]'s data:

```yaml
image: "postgres:9.3"
name: "db_postgres"
volumes:
    - "/var/lib/postgresql/docker:/var/lib/postgresql/data"
```

Start the container daemon:

`[myhro@wheezy:~]$ rocked start db.yml`

### Web application container

Based on this Dockerfile...

```
RUN apt-get update
RUN apt-get install -y build-essential libpq-dev python-dev python-pip
ADD . /app
WORKDIR /app
RUN pip install -r requirements.txt
```

... and this manifest ...

```yaml
image: "python-baseimage"
build: "."
command: "gunicorn -b 0.0.0.0:8000 django_app.wsgi"
environment:
    - "DATABASE_NAME=django_app"
    - "DJANGO_SECRET_KEY"
name: "web_djangoapp"
links:
    - "db_postgres:db"
ports:
    - "${GUNICORN_PORT}:8000"
volumes:
    - "${PROJECT_ROOT}:/app"
```

... build an image prepared to run a [Django][django] web application, then serve it using [Gunicorn][gunicorn]:

    [myhro@wheezy:~]$ rocked build web.yml
    Step 0 : FROM ubuntu:trusty
     ---> e54ca5efa2e9
    (...)
    Step 5 : RUN pip install -r requirements.txt
     ---> 6c13fc4515aa
    Successfully built 8d2d8f4be123
    [myhro@wheezy:~]$ rocked start web.yml

**Note**: environment variables, like `${GUNICORN_PORT}` and `${PROJECT_ROOT}` will be parsed when reading the manifest.

### A note about the rocked run command

With the `rocked run` command, it's possible to run arbitrary commands in a temporary container, using the image specified on the manifest, like:

`[myhro@wheezy:~]$ rocked run web.yml python manage.py migrate`

But if the command contains dashes, it needs to be escaped with `--`, e.g.:

`[myhro@wheezy:~]$ rocked run web.yml -- wc -l /etc/passwd`

Otherwise it would be interpreted as an argument of Rocked itself.

## License

[MIT License][license]


[django-shell]: https://docs.djangoproject.com/en/dev/ref/django-admin/#shell
[django]: https://www.djangoproject.com/
[docker]: http://www.docker.com/
[docopt]: https://pypi.python.org/pypi/docopt
[gunicorn]: http://gunicorn.org/
[license]: https://github.com/myhro/rocked/blob/master/LICENSE
[pip]: http://pip.readthedocs.org/en/latest/
[postgresql]: http://www.postgresql.org/
[pypi]: https://pypi.python.org/
[pyyaml]: https://pypi.python.org/pypi/PyYAML
[yaml]: https://en.wikipedia.org/wiki/YAML
