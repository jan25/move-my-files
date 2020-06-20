# move-my-files

`mmf` is a cli tool for organising files on your computer. Tell it the file name patterns, where to move and matching files from a source directory are moved to target directory. Run it as one-off command or in watch mode to continously observe a source directory.

## Installation

Prerequisites:

- Python >=3.5
- `pip` package manager

Install `mmf` using:

```sh
# Install or upgrade mmf
pip install move-my-files -U
```

## Usage

Move files using either one time command or watch mode:

```sh
# Supply source and destination directory explicitly
mmf move --source ~/Documents --dest-dir ~/Documents/images --pattern .png

# Uses predefined configuration(provided in using add command)
mmf move --source ~/Documents

# Watch ~/Documents directory for moving files
mmf move --source ~/Documents --dest-dir ~/Documents/images --pattern .png --watch
mmf move --source ~/Documents --watch
```

Define your favorite configurations using `add` command. This command keeps track of your configurations so they are not required to be typed in future. Use `list` command to list configurations you've previosly added.

```sh
# Add configuration
mmf add --dest-dir ~/Documents/images --pattern .png --name imagefiles
mmf add --dest-dir ~/Documents/pyfiles --pattern .py --name pyfiles

# List configurations (previously added)
mmf list

# move without --dest-dir will use configurations
mmf move --source ~/Documents --watch
```

Available shortcuts for options:

- `--source`: `-s`
- `--dest-dir`: `-d`
- `--pattern`: `-p`
- `--watch`: `-w`
- `--name`: `-n`

## Development

Fork and clone this repository to develop on latest master branch. General steps to execute python code from this repo:

```sh
# Create development environment
cd /move-my-files
python3 -m venv .env && source .env/bin/activate
pip install -e '.[dev]'

# Execute CLI (from code)
cd ./app
python3 .
python3 . list
# Or directly
mmf --help
```

Local testing with unit tests and CLI:

```sh
# Run available unit tests
python3 -m pytest tests -v

# Install CLI locally to test (basically testing setup.py)
pip install -e .
mmf --help
```

You can also use `tox` to test on different environments.

For Packaging and publishing see here:

- https://packaging.python.org/guides/distributing-packages-using-setuptools

## Contribute

If you have ideas to improve this tool, feel free to raise a new issue in the Issues section or open a PR :)
