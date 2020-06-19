# move-my-files

mmf is a cli tool for organising files on your computer. Tell it the file name patterns, where to move and matching files from a source directory are moved to target directory. Run it as one-off command or in watch mode to continously observe a source directory.

## Install

## Usage

## Develop

Fork and clone this repository to develop on latest master branch. General steps to execute python code form this repo:

```
cd /move-my-files
virtualenv .env && source .env/bin/activate
pip install -r requirements.txt

python3 .
python3 . list
```

Test any changes against available unit tests:

```
python3 -m pytest tests -v
```

If you have ideas to improve this tool, feel free to raise a new issue in the Issues section or open a PR :)
