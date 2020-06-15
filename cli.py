import shutil
import os
import re
import time
import click
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler

def match(pat, filename):
    return re.search(pat, filename) is not None

def move_files(srcdir, pat, destdir):
    assert os.path.isdir(srcdir)
    assert os.path.isdir(destdir)

    with os.scandir(srcdir) as it:
        for entry in it:
            if entry.is_file() and match(pat, entry.name):
                final_dest = shutil.move(entry.path, destdir)
                print(f'{entry.path} moved to {final_dest}')

def watch_srcdir(srcdir, pat, destdir):
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
    finally:
        observer.join()

@click.command()
@click.option('-s', '--source', 'source', default='.', type=click.STRING, help='Source directory path')
@click.option('-d', '--dest-dir', required=True, type=click.STRING, help='Destination directory path')
@click.option('-p', '--pattern', default='.*', type=click.STRING, help='Regex to match file names in source directory')
@click.option('-w', '--watch', is_flag=True)
def mmf(source, dest_dir, pattern, watch):
    if watch:
        watch_srcdir(source, pattern, dest_dir)
    else:
        move_files(source, pattern, dest_dir)

if __name__ == '__main__':
    mmf()
    