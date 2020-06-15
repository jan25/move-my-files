import shutil
import os
import re
import click

def match(pat, filename):
    return re.search(pat, filename) is not None

def move_files(srcdir, pat, destdir):
    assert os.path.isdir(srcdir)
    assert os.path.isdir(destdir)

    entries = os.scandir(srcdir)
    for entry in entries:
        if entry.is_file() and match(pat, entry.name):
            final_dest = shutil.move(entry.path, destdir)
            print(f'{entry.name} moved to {final_dest}')

@click.command()
@click.option('-s', '--source', 'source', default='.', type=click.STRING, help='Source directory path')
@click.option('-d', '--dest-dir', required=True, type=click.STRING, help='Destination directory path')
@click.option('-p', '--pattern', default='.*', type=click.STRING, help='Regex to match file names in source directory')
def mmf(source, dest_dir, pattern):
    click.echo(f'{source} {dest_dir} {pattern}')
    move_files(source, pattern, dest_dir)

if __name__ == '__main__':
    mmf()