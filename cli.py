import shutil
import os
import sys
import re
import time
import click
import traceback
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler
import configfile


class Error(Exception):
    def __init__(self, message):
        self.message = message or 'default error message'

    def __str__(self):
        return f'Error: {self.message}'


def match(pat, filename):
    return re.search(pat, filename) is not None


def validate_dirs(srcdir, destdir):
    if not os.path.exists(srcdir):
        raise Error('source directory does not exist')
    if not os.path.exists(destdir):
        raise Error('destination directory does not exist')
    if not os.path.isdir(srcdir):
        raise Error('source is not a valid directory')
    if not os.path.isdir(destdir):
        raise Error('destination is not a valid directory')


def move_files(srcdir, pat, destdir):
    validate_dirs(srcdir, destdir)

    with os.scandir(srcdir) as it:
        for entry in it:
            if entry.is_file() and match(pat, entry.name):
                final_dest = shutil.move(entry.path, destdir)
                print(f'{entry.path} moved to {final_dest}')


def watch_srcdir(srcdir, pat, destdir):
    validate_dirs(srcdir, destdir)

    event_handler = LoggingEventHandler()
    observer = Observer()
    observer.schedule(event_handler, srcdir, recursive=False)
    observer.start()

    try:
        while True:
            move_files(srcdir, pat, destdir)
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    except Error as err:
        raise err
    finally:
        observer.join()


@click.command(help='Move files')
@click.option(
    '-s',
    '--source',
    'source',
    default='.',
    type=click.STRING,
    help='Source directory path. Defaults to current directory')
@click.option(
    '-d',
    '--dest-dir',
    required=True,
    type=click.STRING,
    help='Destination directory path')
@click.option(
    '-p',
    '--pattern',
    default='.*',
    type=click.STRING,
    help='Regex to match file names in source directory. Defaults to .* (all files)')
@click.option(
    '-w',
    '--watch',
    is_flag=True,
    help='Watch a source directory for files to move')
def move(source, dest_dir, pattern, watch):
    try:
        if watch:
            watch_srcdir(source, pattern, dest_dir)
        else:
            move_files(source, pattern, dest_dir)
    except Error as err:
        print(err)
    except:
        print(Error("Unexpected error"))
        traceback.print_exc()


@click.command(help='Add new configuration')
@click.option(
    '-d',
    '--dest-dir',
    required=True,
    type=click.STRING,
    help='Destination directory path')
@click.option(
    '-p',
    '--pattern',
    default='.*',
    type=click.STRING,
    help='Regex to match file names in source directory. Defaults to .* (all files)')
@click.option(
    '-n',
    '--name',
    required=True,
    type=click.STRING,
    help='Unique name for configuration')
def add(dest_dir, pattern, name):
    patterns = None  # TODO add support for multiple patterns
    try:
        configfile.add_new_config(name, dest_dir, pattern, patterns)
    except configfile.Error as err:
        click.echo(err)
    except:
        click.echo(Error("Unexpected error"))
        traceback.print_exc()


@click.command(help='List configurations')
def ls():
    try:
        configs = configfile.load_configs()
        for c in configs:
            click.echo(c)
    except configfile.Error as err:
        click.echo(err)
    except:
        click.echo(Error("Unexpected error"))
        traceback.print_exc()


@click.group(help='Move My Files CLI tool')
def mmf():
    pass


mmf.add_command(move, 'move')
mmf.add_command(add, 'add')
mmf.add_command(ls, 'list')

if __name__ == '__main__':
    mmf()
