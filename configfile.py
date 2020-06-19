import yaml
import os

CONFIG_FILE_PATH = './conf-test/conf.yml'


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
        patterns_str = ','.join(list(set(self.patterns or [self.pattern])))
        return f'Name={self.name}, ' + \
            f'Destination={self.dest_dir}, ' + \
            f'Patterns={patterns_str}'  # TODO improve pattern printing


def _initialize_datadir():
    if not os.path.exists(os.path.dirname(CONFIG_FILE_PATH)):
        try:
            os.makedirs(os.path.dirname(CONFIG_FILE_PATH))
        except:
            raise Error('Failed to initialize configuration directory')
    with open(CONFIG_FILE_PATH, 'w') as f:
        f.write('config: []')  # empty config


def load_configs():
    if not os.path.exists(CONFIG_FILE_PATH):
        _initialize_datadir()

    try:
        with open(CONFIG_FILE_PATH, 'r') as f:
            conf = f.read()
            yml = yaml.safe_load(conf)
            entries = yml['config']
            return [Config(e) for e in entries]
    except:
        raise Error('Failed to load configuration from mmf-data/conf.yml')


def add_new_config(name, dest_dir, pattern=None, patterns=None):
    if not os.path.exists(CONFIG_FILE_PATH):
        _initialize_datadir()

    if pattern is None and (patterns is None or len(patterns) == 0):
        raise Error('No pattern supplied')
    if not os.path.isdir(dest_dir):
        raise Error('Destination is not a valid directory')

    dest_dir = os.path.abspath(dest_dir)
    configs = load_configs()
    for c in configs:
        if c.name == name:
            raise Error(f'Configuration {name} already exists')

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
