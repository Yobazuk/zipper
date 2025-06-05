# Getting Started with Zipper

Zipper is a modern Python package that allows you to create and manage ZIP archives with structured metadata support. Unlike traditional ZIP tools, Zipper enables you to attach rich, structured metadata to both the archive itself and individual files within it.

## Overview

Zipper provides two main ways to interact with ZIP archives:

1. **Command Line Interface (CLI)**: A modern, user-friendly interface with rich formatting and helpful feedback.
2. **Python API**: A clean and intuitive API for programmatic usage.

## Key Features

- Store structured metadata as JSON in ZIP archives
- Add metadata to both archives and individual files
- Update metadata with smart merging capabilities
- Modern CLI with rich formatting and progress indicators
- Clean Python API with type hints and context managers
- Comprehensive documentation and examples

## Quick Example

Here's a quick example of using Zipper to create an archive with metadata:

::: code-group
```python [Python API]
from zipper import ZipArchive

# Create a new archive with metadata
with ZipArchive("project.zip") as archive:
    # Add a file with metadata
    archive.add_file(
        "config.json",
        metadata={
            "type": "configuration",
            "version": "1.0",
            "environment": "production"
        }
    )
    
    # Set archive-level metadata
    archive.set_archive_metadata({
        "project": "MyProject",
        "version": "2.0.0",
        "created": "2024-03-14"
    })
```

```bash [CLI]
# Create a new archive
zipper create project.zip config.json

# Add metadata to the file
zipper set-metadata project.zip -f config.json -m '{
    "type": "configuration",
    "version": "1.0",
    "environment": "production"
}'

# Add metadata to the archive
zipper set-metadata project.zip -m '{
    "project": "MyProject",
    "version": "2.0.0",
    "created": "2024-03-14"
}'
```
:::

## Next Steps

- [Installation Guide](./installation.md) - Learn how to install Zipper
- [API Reference](/reference/api.md) - Explore the Python API and CLI
- [Implementation Details](/reference/implementation.md) - Learn about the internals 