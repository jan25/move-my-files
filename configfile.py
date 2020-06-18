import yaml
import os

CONFIG_FILE_PATH = './test/conf.yml'


class Error(Exception):
    def __init__(self, message):
        self.message = message or 'default error message'

    def __str__(self):
        return f'Error: {self.message}'


class Config(yaml.YAMLObject):
    def __init__(self, obj):
        try:
            self.name = obj['name']
            self.dest_dir = obj['dest_dir']
            self.pattern = obj['pattern']
            self.patterns = obj['patterns']
        except:
            raise Error('Invalid configuration')

    def to_dict(self):
        return self.__dict__

    def __str__(self):
        patterns_str = ','.join(list(set(self.patterns + [self.pattern])))
        return f'Name={self.name}, ' + \
            f'Destination={self.dest_dir}, ' + \
            f'Patterns={patterns_str}'


def load_configs():
    with open(CONFIG_FILE_PATH, 'r') as f:
        conf = f.read()
        yml = yaml.safe_load(conf)
        entries = yml['config']
        return [Config(e) for e in entries]


def add_new_config(name, dest_dir, pattern, patterns):
    # TODO validate dest_dir, pattern(s) args, check duplicate config names
    configs = load_configs()
    configs.append(Config({
        'name': name,
        'dest_dir': dest_dir,
        'pattern': pattern,
        'patterns': patterns,
    }))
    _dump_configs(configs)


def _dump_configs(configs):
    yml = {'config': []}
    for c in configs:
        yml['config'].append(c.to_dict())
    with open(CONFIG_FILE_PATH, 'w') as f:
        yaml.dump(yml, f)


add_new_config('custom', 'new/dest/dir', '.', ['.'])
configs = load_configs()
for c in configs:
    print(c)
