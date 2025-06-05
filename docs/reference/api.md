# API Reference

This section provides detailed documentation for Zipper's Python API and command-line interface.

## Overview

Zipper provides two main interfaces:

1. **Python API**: A programmatic interface centered around the `ZipArchive` class
2. **Command Line Interface**: A set of commands for working with archives from the terminal

## Python API Structure

The main components of the Python API are:

- `ZipArchive`: The main class for working with ZIP archives
  - Archive operations (create, read, update)
  - File management (add, read)
  - Metadata management (get, set, update)

## CLI Structure

The command-line interface provides the following commands:

- `create`: Create new ZIP archives
- `set-metadata`: Add or update metadata
- `get-metadata`: Read metadata from archives or files
- `list`: Display archive contents and metadata

## Quick Links

### Python API
- [Implementation Details](./implementation.md) - Technical implementation details

### Command Line Interface
- [Getting Started](/guide/getting-started.md) - Basic usage examples
- [Installation](/guide/installation.md) - Installation instructions

## Type Hints

Zipper uses Python type hints throughout its codebase. Here are the main types you'll encounter:

```python
from typing import Dict, List, Optional, Any

# Metadata type
Metadata = Dict[str, Any]

# Archive contents type
ArchiveItem = Dict[str, Any]  # Contains 'filename', 'size', 'compressed_size', 'metadata'
ArchiveContents = List[ArchiveItem]
```

## Error Handling

Zipper provides several custom exceptions:

```python
# File operations
FileNotFoundError    # When a file doesn't exist
KeyError            # When a file is not found in the archive
RuntimeError        # When using ZipArchive outside a context manager

# Metadata operations
json.JSONDecodeError  # When metadata JSON is invalid
UnicodeDecodeError   # When comment encoding is invalid
```

## Best Practices

1. Always use context managers with `ZipArchive`:
```python
with ZipArchive("archive.zip") as archive:
    # Work with the archive
    pass
```

2. Handle metadata errors:
```python
try:
    metadata = archive.get_file_metadata("file.txt")
except KeyError:
    # Handle missing file
except json.JSONDecodeError:
    # Handle invalid metadata
```

3. Use type hints in your code:
```python
from zipper import ZipArchive
from typing import Dict, Any

def process_archive(metadata: Dict[str, Any]) -> None:
    with ZipArchive("archive.zip") as archive:
        archive.set_archive_metadata(metadata)
```

## Next Steps

- [Implementation Details](./implementation.md) - Technical implementation details
- [Getting Started](/guide/getting-started.md) - Basic usage examples 