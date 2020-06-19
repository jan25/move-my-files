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


def validate_srcdir(srcdir):
    if not os.path.exists(srcdir):
        raise Error('source directory does not exist')
    if not os.path.isdir(srcdir):
        raise Error('source is not a valid directory')


def validate_destdir(destdir):
    if not os.path.exists(destdir):
        raise Error('destination directory does not exist')
    if not os.path.isdir(destdir):
        raise Error('destination is not a valid directory')


def move_files(srcdir, pat, destdir):
    validate_srcdir(srcdir)
    validate_destdir(destdir)

    with os.scandir(srcdir) as it:
        for entry in it:
            if entry.is_file() and match(pat, entry.name):
                final_dest = shutil.move(entry.path, destdir)
                print(f'{entry.path} moved to {final_dest}')


def handle_one_off_move(srcdir, pat=None, destdir=None, name=None):
    validate_srcdir(srcdir)

    if not destdir:
        configs = configfile.load_configs()
        for config in configs:
            if name:
                if name == config.name:
                    move_files(srcdir, config.pattern, config.dest_dir)
            else:
                move_files(srcdir, config.pattern, config.dest_dir)
    else:
        move_files(srcdir, pat, destdir)


def handle_watch(srcdir, pat=None, destdir=None, name=None):
    validate_srcdir(srcdir)

    event_handler = LoggingEventHandler()
    observer = Observer()
    observer.schedule(event_handler, srcdir, recursive=False)
    observer.start()

    try:
        while True:
            handle_one_off_move(srcdir, pat, destdir, name)
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
    type=click.STRING,
    help='Name of configuration to use')
@click.option(
    '-w',
    '--watch',
    is_flag=True,
    help='Watch a source directory for files to move')
def move(source, dest_dir, pattern, name, watch):
    try:
        if watch:
            handle_watch(source, pattern, dest_dir, name)
        else:
            handle_one_off_move(source, pattern, dest_dir, name)
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
        config = configfile.add_new_config(name, dest_dir, pattern, patterns)
        click.echo(f'Added: {config}')
    except configfile.Error as err:
        click.echo(err)
    except:
        click.echo(Error("Unexpected error"))
        traceback.print_exc()


@click.command(help='List configurations')
def ls():
    try:
        configs = configfile.load_configs()
        for config in configs:
            click.echo(config)
    except configfile.Error as err:
        click.echo(err)
    except:
        click.echo(Error("Unexpected error"))
        traceback.print_exc()
