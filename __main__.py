import click
from commands import move, add, ls


@click.group(help='Move My Files CLI tool')
def mmf():
    pass


mmf.add_command(move, 'move')
mmf.add_command(add, 'add')
mmf.add_command(ls, 'list')

if __name__ == '__main__':
    mmf()
