import sys
import os.path
import yaml
from collections import defaultdict

class PathConfig:
    def __init__(self):
        self.paths = defaultdict(list)
        self.paths[None].append('.')
        self.configs = []
    def load_config(self, fname, optional=False):
        try:
            conf = yaml.load(file(fname))
            self.configs.append(conf)
        except IOError:
            if not optional:
                raise
    def get_key(self, key, fillers=None):
        if fillers is None:
            fillers = {}
        actual_key = (key%fillers).split('.')
        for conf in self.configs[::-1]:
            conf0 = conf
            try:
                for part in actual_key:
                    conf0 = conf0[part]
            except KeyError:
                continue
            return conf0
    def push_path(self, kind, path):
        self.paths[kind].append(path)
    def pop_path(self, kind):
        del self.paths[kind][-1]
    def find_file(self, path, kinds=None, fillers=None,
                  log_fn=None):
        if kinds is None:
            kinds = [None]
        all_paths = [self.paths[x] for x in kinds]
        if fillers is None:
            fillers = {}
        local_part = path%fillers
        for dir_part in all_paths:
            fname = os.path.join(dir_part, local_part)
            if os.path.exists(fname):
                if log_fn is not None:
                    log_fn('paths', 'found', path=path,
                           fname=fname)
                return fname
        if log_fn is not None:
            log_fn('paths', 'not_found', path=path,
                   kinds=kinds, local_part=local_part,
                   all_paths=all_paths)
        return None
