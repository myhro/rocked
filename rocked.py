#!/usr/bin/env python

import json
import os
import subprocess
import docopt
import yaml


class Rocked:
    def __init__(self, cli):
        self.args = docopt.docopt(cli.strip())
        self.container = None
        self.show_status = False

        if os.path.exists(self.args['<file.yml>']):
            yml_file = self.args['<file.yml>']
        else:
            yml_file = os.path.join(os.getcwd(), self.args['<file.yml>'])
        self.manifest = yaml.safe_load(os.path.expandvars(open(yml_file).read()))

        if self.args['status']:
            self.show_status = True

        self.get_container()

        if self.args['build']:
            self.build()
        elif self.args['kill']:
            self.kill()
        elif self.args['logs']:
            self.logs()
        elif self.args['run'] or self.args['start']:
            self.run()
        elif self.args['restart']:
            self.restart()
        elif self.args['status']:
            self.status()
        elif self.args['stop']:
            self.stop()

    def build(self):
        build_command = ['docker', 'build', '-t', self.manifest['image']]
        if self.args['--no-cache']:
            build_command.extend(['--no-cache'])
        build_command.extend([self.manifest['build']])
        subprocess.call(build_command)

    def get_container(self):
        ps_command = ['docker', 'ps']
        if not self.show_status:
            ps_command.extend(['-a'])
        container_list = subprocess.check_output(ps_command).strip().split('\n')
        if len(container_list) > 1:
            for line in [c.split() for c in container_list[1:]]:
                container_id = line[0]
                inspect = json.loads(subprocess.check_output(['docker', 'inspect', container_id])[1:-1])
                if inspect['Name'] == u'/{name}'.format(name=self.manifest['name']):
                    self.container = container_id
                    break

    def kill(self):
        if self.container:
            subprocess.call(['docker', 'kill', self.container])

    def logs(self):
        if self.container:
            subprocess.call(['docker', 'logs', self.container])

    def restart(self):
        self.stop()
        self.run()

    def stop(self):
        if self.container:
            subprocess.call(['docker', 'stop', self.container])

    def status(self):
        if self.container:
            print self.manifest['name'] + ': running'
        else:
            print self.manifest['name'] + ': not running'

    def run(self):
        run_command = ['docker', 'run']
        if self.args['run']:
            run_command.extend(['--rm', '-t', '-i'])
        else:
            if self.container:
                subprocess.call(['docker', 'rm', self.container])
            run_command.extend(['-d'])
            run_command.extend(['--name', self.manifest['name']])
        if 'environment' in self.manifest:
            for e in self.manifest['environment']:
                run_command.extend(['-e', e])
        if 'links' in self.manifest:
            for l in self.manifest['links']:
                run_command.extend(['--link', l])
        if 'ports' in self.manifest and not self.args['run']:
            for p in self.manifest['ports']:
                run_command.extend(['-p', p])
        if 'volumes' in self.manifest:
            for v in self.manifest['volumes']:
                run_command.extend(['-v', v])
        run_command.extend([self.manifest['image']])
        if self.args['<command>']:
            run_command.extend(self.args['<command>'])
        elif 'command' in self.manifest:
            run_command.extend(self.manifest['command'].split())
        subprocess.call(run_command)


def main():
    cli = '''
    Rocked, a thin wrapper to manage Docker containers.

    Usage:
        rocked build [--no-cache] <file.yml>
        rocked kill <file.yml>
        rocked logs <file.yml>
        rocked run <file.yml> [--] [<command>...]
        rocked restart <file.yml>
        rocked start <file.yml>
        rocked status <file.yml>
        rocked stop <file.yml>
        rocked -h | --help

    Options:
        -h --help   Show this screen.
    '''
    rocked = Rocked(cli)

if __name__ == '__main__':
    main()
