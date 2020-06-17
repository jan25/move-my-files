import yaml
import os

CONFIG_FILE_PATH = './test/conf.yml'


class Error(Exception):
    def __init__(self, message):
        self.message = message or 'default error message'

    def __str__(self):
        return f'Error: {self.message}'


class Config(yaml.YAMLObject):
    def __init__(self):
        self.name = 'Unnamed config'
        self.dest_dir = None
        self.pattern = None
        self.patterns = None

    def serialize(self, obj):
        try:
            self.name = obj['name']
            self.dest_dir = obj['dest_dir']
            self.pattern = obj['pattern']
            self.patterns = obj['patterns']
        except:
            raise Error('Invalid configuration')
        return self

    def __str__(self):
        patterns_str = ','.join(list(set(self.patterns + [self.pattern])))
        return f'Name={self.name}, ' + \
            f'Destination={self.dest_dir}, ' + \
            f'Patterns={patterns_str}'


def load_configs():
    with open(CONFIG_FILE_PATH, 'r') as f:
        conf = f.read()
        yml = yaml.safe_load(conf)
        print(Config().serialize(yml['config'][0]))
        print('-%s-' % yaml.dump(yml))


load_configs()


def dump_configs(configs):
    # TODO make yaml string
    yml = ''
    yaml.dump(yml, os.file(CONFIG_FILE_PATH, 'w'))
