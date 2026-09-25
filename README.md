# Document Parser - Knowledge Base

A Python command-line application for indexing documents in a folder and building
a small local knowledge base. For each document, the application stores its
content and metadata, making it possible to search the index by text.

## Features

- scans a folder and its subfolders;
- extracts content using specialized parsers;
- collects each document's title, path, size, modification date, and word count;
- searches document text and sorts results by relevance;
- stores the index in JSON files;
- updates, removes, and clears the index through an interactive menu;
- dynamically loads parsers from the `parser/` folder.

## Requirements

- Python 3.9 o superiore;
- The project primarily uses the Python standard library;
- The `chardet` library automatically detects file encodings.

## Getting Started

From the project root, run:

```bash
python main.py
```

An interactive menu appears at startup. The available commands are:

| Command | Operation |
| --- | --- |
| `h` | Show the menu again |
| `1` | Index a new folder |
| `2` | Search the index for a word or phrase |
| `3` | View all indexed files |
| `4` | Remove a folder from the index |
| `5` | Update the index |
| `6` | Save the index to disk |
| `7` | Clear the index |
| `8` | Exit the application |

Example usage:

1. Run `python main.py`.
2. Choose `1`.
3. Enter the path to the folder you want to index.
4. Choose `2` and enter the search terms.

## Configuration

Configuration is stored in `config.ini`:

```ini
[parsers]
folder = parser

[index]
index = index.json
inverted_index = inverted_index.json

[logging]
level = DEBUG
file = log/indexer.log
```

The main keys are:

- `parsers.folder`: directory from which parsers are dynamically loaded;
- `index.index`: JSON file containing the indexed documents;
- `index.inverted_index`: JSON file used for word-based searches;
- `logging.file`: application log file;
- `logging.level`: logging level, such as `DEBUG`, `INFO`, or `WARNING`.

The `index.json`, `inverted_index.json`, and `log/indexer.log` files are created
or updated when the application runs and should not be edited manually.

## Parsers

The `parser/` directory contains implementations based on
`model.parser.DocumentParser`. The available parsers support:

- `.txt` text files;
- `.md` Markdown files;
- CSV/TSV files through `CSVParser`.

To add support for another format, create a Python module in `parser/`, define a
class that inherits from `DocumentParser`, set the supported extension, and
implement the `parse` method.
