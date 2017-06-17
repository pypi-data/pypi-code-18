import os
import shutil
import sys
import subprocess
import time
import json


class Experiment:

    def __init__(self, expman_args, exp_args):
        self.expman_args = expman_args
        self.exp_args = exp_args
        self.log = None

    def announce(self, s):
        a = '>>> {} '.format(s)
        print(a)
        self.log.write(a + '\n')
        self.log.flush()

    @property
    def name(self):
        return self.expman_args['name']

    @property
    def path(self):
        return os.path.join(self.expman_args['dir'], self.name)

    @property
    def envs(self):
        gpu = self.expman_args['gpu']
        return {
            'CUDA_VISIBLE_DEVICES': ','.join([str(g) for g in gpu]) if gpu is not None else '',
            'OUT_DIR': self.path,
        }

    @property
    def config(self):
        return {
            'expman_args': self.expman_args,
            'exp_args': self.exp_args,
        }

    @classmethod
    def load(cls, path):
        with open(os.path.join(path, 'config.json')) as f:
            config = json.load(f)
        return cls(**config)

    def exp_dict(self):
        key_cache = None
        val_cache = []
        d = {'name': self.name, 'path': self.path}
        for k in self.exp_args:
            if '--' in k:
                if key_cache:
                    if len(val_cache) == 0:
                        d[key_cache] = True
                    elif len(val_cache) == 1:
                        d[key_cache] = val_cache[0]
                    else:
                        d[key_cache] = val_cache
                    val_cache.clear()
                key_cache = k
            else:
                val_cache.append(k)
        return d

    def set_env(self):
        for k, v in self.envs.items():
            os.environ[k] = v

    def setup(self):
        self.set_env()
        if os.path.isdir(self.path) and self.expman_args['force']:
            print('Removing (--force is True) old directory at: {}'.format(self.path))
            shutil.rmtree(self.path)
        if not os.path.isdir(self.path):
            print('Making directory: {}'.format(self.path))
            os.makedirs(self.path)

        with open(os.path.join(self.path, 'config.json'), 'wt') as f:
            json.dump(self.config, f, indent=4)

    def tear_down(self):
        fresult = os.path.join(self.path, 'results.json')
        if os.path.isfile(fresult):
            with open(fresult) as f:
                result = json.load(f)
                self.announce('Experiment created: {}\n{}'.format(fresult, result))
        else:
            self.announce('Experiment did not create: {}'.format(fresult))

    def execute(self):
        self.log = open(os.path.join(self.path, 'log.txt'), 'a')
        cmd = self.exp_args
        self.announce('Executing command:\n{}'.format(' '.join(cmd)))
        start = time.time()
        self.announce('starting experiment on {}'.format(time.ctime(int(start))))
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        while p.poll() is None:
            l = p.stdout.readline().decode()
            print(l.rstrip())
            self.log.write(l)
            self.log.flush()
        l = p.stdout.read().decode()
        print(l.rstrip())
        self.log.write(l)
        l = p.stdout.read()
        end = time.time()
        self.announce('ending experiment on {}'.format(time.ctime(int(end))))
        self.announce('elpased time: {} seconds'.format(end - start))
        sys.stderr.write(p.stderr.read().decode())
        if p.returncode:
            raise Exception('Command failed:\n{}'.format(' '.join(cmd)))

    def run(self):
        self.setup()
        self.execute()
        self.tear_down()
