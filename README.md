Rocked
======

A thin wrapper to manage [Docker][docker] containers.

```
usage: rocked.py [-h] [--build] [--kill] [--logs] [--run RUN [RUN ...]]
                 [--start] [--stop]
                 file

positional arguments:
  file                 YAML manifest file to be loaded

optional arguments:
  -h, --help           show this help message and exit
  --build              build image
  --kill               kill container
  --logs               display container logs
  --run RUN [RUN ...]  run a one-off command
  --start              start container
  --stop               stop container
```

[docker]: http://www.docker.com/
