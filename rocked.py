#!/usr/bin/env python

import json
import os
import subprocess
import docopt
import yaml


cli = '''Rocked, a thin wrapper to manage Docker containers.

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
'''

args = docopt.docopt(cli)

if os.path.exists(args['<file.yml>']):
    yml_file = args['<file.yml>']
else:
    yml_file = os.path.join(os.getcwd(), args['<file.yml>'])

manifest = yaml.load(os.path.expandvars(open(yml_file).read()))

if args['build']:
    subprocess.call(['docker', 'build', '-t', manifest['image'], manifest['build']])
    exit(0)

ps_command = ['docker', 'ps']
show_status = False
if args['status'] or not any([args['build'], args['kill'], args['logs'], args['run'], args['start'], args['stop']]):
    show_status = True
else:
    ps_command.extend(['-a'])

container = None
container_list = subprocess.check_output(ps_command).strip().split('\n')
if len(container_list) > 1:
    for line in [c.split() for c in container_list[1:]]:
        container_id = line[0]
        inspect = json.loads(subprocess.check_output(['docker', 'inspect', container_id])[1:-1])
        if inspect['Name'] == u'/{name}'.format(name=manifest['name']):
            container = container_id
            break

if show_status:
    if container:
        print manifest['name'] + ': running'
    else:
        print manifest['name'] + ': not running'

if container:
    if args['kill']:
        subprocess.call(['docker', 'kill', container])
    if args['logs']:
        subprocess.call(['docker', 'logs', container])
    if args['stop']:
        subprocess.call(['docker', 'stop', container])

if args['start'] or args['run']:
    run_command = ['docker', 'run']
    if not args['run']:
        if container:
            subprocess.call(['docker', 'rm', container])
        run_command.extend(['-d'])
        run_command.extend(['--name', manifest['name']])
    else:
        run_command.extend(['--rm', '-t', '-i'])
    if 'environment' in manifest:
        for e in manifest['environment']:
            run_command.extend(['-e', e])
    if 'links' in manifest:
        for l in manifest['links']:
            run_command.extend(['--link', l])
    if 'ports' in manifest and not args['run']:
        for p in manifest['ports']:
            run_command.extend(['-p', p])
    if 'volumes' in manifest:
        for v in manifest['volumes']:
            run_command.extend(['-v', v])
    run_command.extend([manifest['image']])
    if args['<command>']:
        run_command.extend(args['<command>'])
    elif 'command' in manifest:
        run_command.extend(manifest['command'].split())
    subprocess.call(run_command)
