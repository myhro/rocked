Rocked
======

A thin wrapper to manage [Docker][docker] containers. It just generates command line arguments to be passed to the `docker` client, based on the chosen command and loading the container configuration data from a manifest file, written in [YAML][yaml] format.

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
        rocked build <file.yml>
        rocked kill <file.yml>
        rocked logs <file.yml>
        rocked run <file.yml> [--] [<command>...]
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


[docker]: http://www.docker.com/
[docopt]: https://pypi.python.org/pypi/docopt
[pip]: http://pip.readthedocs.org/en/latest/
[pypi]: https://pypi.python.org/
[pyyaml]: https://pypi.python.org/pypi/PyYAML
[yaml]: https://en.wikipedia.org/wiki/YAML
