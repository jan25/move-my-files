import configfile

SAMPLE_CONFIG = '''config:
- dest_dir: /Users/user/home/test/dest
  name: images
  pattern: .*
  patterns: []
- dest_dir: /Users/user/home/test/dest
  name: pyfiles
  pattern: .py$
  patterns: []'''


def _create_tmp_configfile(tmp_path):
    d = tmp_path / 'mmf-data'
    d.mkdir()
    f = d / 'conf.yml'
    f.write_text(SAMPLE_CONFIG)
    assert f.read_text() == SAMPLE_CONFIG
    configfile.CONFIG_FILE_PATH = f.as_posix()


def test_load_configs(tmp_path):
    _create_tmp_configfile(tmp_path)
    assert configfile.CONFIG_FILE_PATH == (
        tmp_path / 'mmf-data/conf.yml').as_posix()

    configs = configfile.load_configs()
    assert len(configs) == 2
    config = configs[0]
    assert config.name == 'images' and config.dest_dir == '/Users/user/home/test/dest'
    assert config.pattern == '.*' and config.patterns == []


def test_add_new_config(tmp_path):
    _create_tmp_configfile(tmp_path)
    assert configfile.CONFIG_FILE_PATH == (
        tmp_path / 'mmf-data/conf.yml').as_posix()

    configfile.add_new_config(
        'new-config', '/Users/user/some/path', '.png', [])
    configs = configfile.load_configs()
    new_config = configs[-1]
    assert new_config.name == 'new-config' and new_config.dest_dir == '/Users/user/some/path'
    assert new_config.pattern == '.png' and new_config.patterns == []
