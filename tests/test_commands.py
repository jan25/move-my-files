import os
from click.testing import CliRunner
import pytest
import signal
import configfile
from commands import ls, add, move


def test_add(tmp_path):
    runner = CliRunner()
    configfile.CONFIG_FILE_PATH = './conf.yml'

    with runner.isolated_filesystem():
        result = runner.invoke(
            add, ['-d', './test/to', '-p', '.py', '-n', 'pyfiles'])
        assert result.exit_code == 0
        assert 'Error: Destination is not a valid directory\n' == result.output

        result = runner.invoke(
            add, ['-d', './test/to', '-p', '.py', '-n'])
        assert result.exit_code != 0  # Click error: missing arg
        result = runner.invoke(
            add, ['-d', './test/to', '-p', '.py'])
        assert result.exit_code != 0  # Click error: missing option

    with runner.isolated_filesystem():
        os.makedirs('./test/to')
        result = runner.invoke(
            add, ['-d', './test/to', '-p', '.py', '-n', 'pyfiles'])
        assert result.exit_code == 0
        config = configfile.Config({
            'name': 'pyfiles',
            'dest_dir': os.path.abspath('./test/from'),
            'pattern': '.py',
            'patterns': None
        })
        assert 'Added: Name=pyfiles' in result.stdout

        result = runner.invoke(
            add, ['-d', './test/to', '-p', '.py', '-n', 'pyfiles'])
        assert result.exit_code == 0
        assert result.stdout == 'Error: Configuration pyfiles already exists\n'


def test_ls():
    runner = CliRunner()
    configfile.CONFIG_FILE_PATH = './conf.yml'

    with runner.isolated_filesystem():
        os.makedirs('./test/to')
        result = runner.invoke(ls)
        assert result.exit_code == 0
        assert result.stdout == 'No configurations available\n'
        result = runner.invoke(
            add, ['-d', './test/to', '-p', '.py', '-n', 'pyfiles'])
        assert result.exit_code == 0
        result = runner.invoke(
            add, ['-d', './test/to', '-p', '.png', '-n', 'images'])
        assert result.exit_code == 0
        result = runner.invoke(ls)
        assert result.exit_code == 0
        assert 'Name=pyfiles' in result.stdout
        assert 'Name=images' in result.stdout


def test_move():
    runner = CliRunner()
    configfile.CONFIG_FILE_PATH = './conf.yml'

    with runner.isolated_filesystem():
        os.makedirs('./test/from')
        os.makedirs('./test/to')
        with open('./test/from/hello.py', 'w') as f:
            f.write("print('hello!'")
        result = runner.invoke(
            add, ['-d', './test/to', '-p', '.py', '-n', 'pyfiles'])
        assert result.exit_code == 0

        result = runner.invoke(
            move, ['-s', './test/from'])
        assert result.exit_code == 0
        assert 'hello.py' in result.stdout
        assert 'moved to' in result.stdout
        assert 'hello.py' in os.listdir('./test/to')
        assert 'hello.py' not in os.listdir('./test/from')

        # TODO add test for move and watch (-w option)
