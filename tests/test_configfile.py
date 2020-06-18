import os
import pytest
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


def _create_tmp_configfile(tmp_path, content=None):
    d = tmp_path / 'mmf-data-test'
    d.mkdir()
    f = d / 'conf.yml'
    content = content or SAMPLE_CONFIG
    f.write_text(content)
    assert f.read_text() == content
    configfile.CONFIG_FILE_PATH = f.as_posix()


def test_initialize_datadir(tmp_path):
    conf_file_path = tmp_path / 'mmf-data-test/conf.yml'
    configfile.CONFIG_FILE_PATH = conf_file_path.as_posix()
    configfile._initialize_datadir()
    assert os.path.exists(conf_file_path)


def test_load_configs_invalid(tmp_path):
    _create_tmp_configfile(tmp_path, 'invalid')
    with pytest.raises(configfile.Error):
        configs = configfile.load_configs()
        assert len(configs) == 0


def test_load_configs(tmp_path):
    # empty config file
    conf_file_path = tmp_path / 'mmf-data-test/conf.yml'
    configfile.CONFIG_FILE_PATH = conf_file_path.as_posix()
    configs = configfile.load_configs()
    assert len(configs) == 0

    # add new and test
    tmp_dir = tmp_path / 'target-dir'
    tmp_dir.mkdir()
    configfile.add_new_config(
        'new-config', tmp_dir.as_posix(), None, ['.png', '.jpg'])
    configs = configfile.load_configs()
    assert len(configs) == 1
    new_config = configs[0]
    assert new_config.name == 'new-config' and new_config.dest_dir == tmp_dir.as_posix()
    assert new_config.pattern == None and new_config.patterns == [
        '.png', '.jpg']


def test_add_new_config(tmp_path):
    conf_file_path = tmp_path / 'mmf-data-test/conf.yml'
    configfile.CONFIG_FILE_PATH = conf_file_path.as_posix()
    tmp_dir = tmp_path / 'target-dir'
    tmp_dir.mkdir()

    # error cases
    with pytest.raises(configfile.Error):
        configfile.add_new_config(
            'new-config', tmp_dir.as_posix(), None, None)
    with pytest.raises(configfile.Error):
        configfile.add_new_config(
            'new-config', '/invalid/dest/dir', '.py', None)
    with pytest.raises(configfile.Error):
        configfile.add_new_config(
            'new-config', tmp_dir.as_posix(), None, [])

    # non-error case
    configfile.add_new_config(
        'new-config', tmp_dir.as_posix(), None, ['.png', '.jpg'])
    configs = configfile.load_configs()
    assert len(configs) == 1
    new_config = configs[-1]
    assert new_config.name == 'new-config' and new_config.dest_dir == tmp_dir.as_posix()
    assert new_config.pattern == None and new_config.patterns == [
        '.png', '.jpg']
