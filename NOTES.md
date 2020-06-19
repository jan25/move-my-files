# Features

- Add configuration to patten match file names and destination directory
- One-off command to move files with a source directory option
- Watch a source directory and move files

# Design

- Store configuration in `HOME/mmf-data` directory
- Configuration as yaml file. First use of cli created the configuration directory and default config file

```
config:
  - name: MY_PATTERN
    dest: DEST_DIR
    patterns: [ PATTERN1, PATTERN2 ]
    pattern: PATTERN3
```

- DEST_DIR field in config file must be absolute path to a directory on disk

- Usage

```
# Define configuration

mmf add --pattern ".jpg$" --dest-dir dest/dir/path --name jpg_files
mmf add --patterns ".jpg$,.png$" --dest-dir dest/dir/path --name image_files
mmf list

# Uses predefined configuration to move files

mmf --source source/dir/path

# Watch source dir and use predifined config to move files

mmf --watch --source source/dir/path

# Use one-off configuration

mmf --source soure/dir --dest-dir dest/dir --pattern ".jpg$"
```

- Some limitations:

  - Files are matched at top level only. No recursive comparisions done.
  - Sub directories are not moved from source dir
  - Source and Target paths must be existing valid directories
  - Configuration don't include explicit source directory

- Source is the source directory to move files from
- Pattern is a regex to used to match and move files
- Destination and target directory mean the same thing

- Emojis in output
