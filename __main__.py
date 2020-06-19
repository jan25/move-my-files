import click
import cmd


@click.group(help='Move My Files CLI tool')
def mmf():
    pass


mmf.add_command(cmd.move, 'move')
mmf.add_command(cmd.add, 'add')
mmf.add_command(cmd.ls, 'list')

if __name__ == '__main__':
    mmf()
