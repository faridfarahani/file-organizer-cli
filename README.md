# File Organizer CLI

A small Python command-line project that organizes files in a folder by file type.

It supports dry-run mode, collision-safe renaming, and an undo log so changes can be reviewed and reversed.

## Features

- Organize files into category folders
- Dry-run mode before moving anything
- Collision-safe destination names
- JSON operation log
- Undo the most recent organization run
- Uses only the Python standard library
- Includes unit tests

## Categories

- Images
- Documents
- Spreadsheets
- Archives
- Audio
- Video
- Code
- Other

## Installation

Requires Python 3.11 or newer. Install from the project root:

    python -m pip install .

## Run

Preview changes first:

```bash
python -m file_organizer.cli organize "C:\Users\YourName\Downloads" --dry-run
```

Apply changes:

```bash
python -m file_organizer.cli organize "C:\Users\YourName\Downloads"
```

Undo the last run:

```bash
python -m file_organizer.cli undo "C:\Users\YourName\Downloads"
```

## Tests

```bash
python -m unittest discover -s tests
```

## Author

Farid Farahani

Python Developer | Web Developer

Website: https://faridfarahani.ir


## Example

Before: mixed files are stored together in one folder.

After: files are automatically organized into category folders such as Images, Documents, Spreadsheets, and Code.
