from __future__ import absolute_import, print_function, unicode_literals

import os
import argparse
import logging
import yaml
import json
import importlib
import fnmatch
import subprocess

from datetime import datetime

from .util import deep_merge


class Entrypoint(object):

    def run(self):
        logging.getLogger().setLevel(logging.INFO)

        parser = argparse.ArgumentParser()
        parser.add_argument('name', help='reference to the job that should be run from the config')
        parser.add_argument('--runner', dest='runner', default=None, help='Specify a runner for the job.')
        parser.add_argument('--config', dest='config', default='config', help='Path to directory containing configuration files to be merged.')
        parser.add_argument('--env', dest='env', default='development', help='Environment used to select configuration and secrets')
        args = parser.parse_args()

        # Build base config from core yml and jobs files.
        base_config_path = os.path.join(args.config, 'config.yml')
        base_config = self._read_yaml(base_config_path) or {}
        if 'jobs' not in base_config:
            base_config['jobs'] = {}
        jobs_config_dir = os.path.join(args.config, 'jobs')
        for config_file in self._list_files_r(jobs_config_dir, 'yml'):
            jobs_config = self._read_yaml(config_file)
            base_config['jobs'].update(jobs_config['jobs'])

        # Build the envionment-specific config, and merged to rendered config.json.
        env_config_path = os.path.join(args.config, 'config.%s.yml' % (args.env, ))
        env_config = self._read_yaml(env_config_path) or {}
        config = deep_merge(base_config, env_config)

        # Build secrets by decrypting available EJSONs.
        env_ejson_secrets_path = os.path.join(args.config, 'secrets.%s.ejson' % (args.env, ))
        env_ejson_secrets = self._read_json(env_ejson_secrets_path)
        ejson_public_key = env_ejson_secrets['_public_key']
        ejson_private_key_path = os.path.join('/opt/ejson/keys/%s' % (ejson_public_key, ))
        if not os.path.isfile(ejson_private_key_path):
            if not os.environ.get('EJSON_PRIVATE_KEY'):
                raise ValueError('ENV[EJSON_PRIVATE_KEY] must be set or %s must exist containing it.' % (ejson_private_key_path, ))
            else:
                raise ValueError('going to create it')
        try:
            out = subprocess.check_output(['ejson', 'decrypt', env_ejson_secrets_path], stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError as e:
            raise ValueError(e.output)
        secrets = json.loads(out)

        # Build the job.
        job = self._build_job(args.name, config, secrets)

        # Derive and initialize the runner class.
        runner_name = 'direct' if args.runner is None else args.runner
        if '.' in runner_name:
            runner_class = self._get_module_class(runner_name)
        else:
            if runner_name not in job.RUNNERS:
                raise ValueError('specified runner "%s" is not supported by job type %s, only %s' % (runner_name, job.__class__.__name__, job.RUNNERS.keys()))
            runner_class = job.RUNNERS[runner_name]

        runner_class().run(job, config)

    def _build_job(self, job_name, config, secrets):
        job_config = config.get('jobs', {}).get(job_name, {})
        job_config.update({
            'name': job_name,
            'timestamp': datetime.utcnow().strftime('%Y%m%d%H%M%S%f')
        })
        job_class = self._get_module_class(config['jobs'][job_name]['adapter'])
        job_secrets = secrets.get(job_name, {})

        job_config['store'] = config['store']
        if 'store' not in job_secrets:
            job_secrets['store'] = {}
        if 'store' in job_config and 'connection' in job_config['store']:
            job_secrets['store']['connection'] = secrets.get('connections', {}).get(job_config['store']['connection'],)

        job_connection = job_config.get('connection')
        if isinstance(job_connection, str):
            job_config['connection'] = config['connections'].get(job_connection, {})
            job_secrets['connection'] = secrets['connections'].get(job_connection, {})

        # Merge job cloud config into global cloud config defaults
        cloud_config = config.get('cloud', {})
        job_cloud_config = job_config.get('cloud', {})
        job_cloud_config.update()
        job_cloud_config = deep_merge(cloud_config, job_cloud_config)
        if len(job_cloud_config) > 0:
            job_config['cloud'] = job_cloud_config

        return job_class(job_config, job_secrets)

    def _read_json(self, path):
        if os.path.isfile(path):
            with open(path, 'r') as f:
                return json.loads(f.read())
        else:
            return {}

    def _read_yaml(self, path):
        with open(path, 'r') as f:
            return yaml.load(f)

    def _get_module_class(self, module_class_path):
        module_and_class_parts = module_class_path.split('.')
        module = importlib.import_module('.'.join(module_and_class_parts[:-1]))
        return getattr(module, module_and_class_parts[-1])

    def _list_files_r(self, path, extension):
        matches = []
        for root, dirnames, filenames in os.walk(path):
            for filename in fnmatch.filter(filenames, '*.%s' % (extension, )):
                matches.append(os.path.join(root, filename))
        return matches


if __name__ == '__main__':
    Entrypoint().run()
