#!/usr/bin/env python

import json
import os
import subprocess
import argparse
import yaml


parser = argparse.ArgumentParser()
parser.add_argument('file', help='YAML manifest file to be loaded')
parser.add_argument('--build', help='build image', action='store_true')
parser.add_argument('--kill', help='kill container', action='store_true')
parser.add_argument('--logs', help='display container logs', action='store_true')
parser.add_argument('--run', help='run a one-off command', nargs='+')
parser.add_argument('--start', help='start container', action='store_true')
parser.add_argument('--stop', help='stop container', action='store_true')
args = parser.parse_args()

if os.path.exists(args.file):
    yml_file = args.file
else:
    yml_file = os.path.join(os.getcwd(), args.file)

manifest = yaml.load(os.path.expandvars(open(yml_file).read()))

if args.build:
    subprocess.call(['docker', 'build', '-t', manifest['image'], manifest['build']])
    exit(0)

container = None
container_list = subprocess.check_output(['docker', 'ps', '-a']).strip().split('\n')
if len(container_list) > 1:
    for line in [c.split() for c in container_list[1:]]:
        container_id = line[0]
        inspect = json.loads(subprocess.check_output(['docker', 'inspect', container_id])[1:-1])
        if inspect['Name'] == u'/{name}'.format(name=manifest['name']):
            container = container_id
            break

if container:
    if args.kill:
        subprocess.call(['docker', 'kill', container])
    if args.logs:
        subprocess.call(['docker', 'logs', container])
    if args.stop:
        subprocess.call(['docker', 'stop', container])

if args.start or args.run:
    run_command = ['docker', 'run']
    if not args.run:
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
    if 'ports' in manifest and not args.run:
        for p in manifest['ports']:
            run_command.extend(['-p', p])
    if 'volumes' in manifest:
        for v in manifest['volumes']:
            run_command.extend(['-v', v])
    run_command.extend([manifest['image']])
    if args.run:
        run_command.extend(args.run)
    elif 'command' in manifest:
        run_command.extend(manifest['command'].split())
    subprocess.call(run_command)
