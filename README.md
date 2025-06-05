# Zipper

A Python package for creating and reading ZIP archives with metadata support. Zipper allows you to attach JSON metadata to both individual files and the archive itself.

## Features

- Create ZIP archives with multiple files
- Add JSON metadata to individual files
- Add JSON metadata to the entire archive
- Interactive metadata input for each file
- Read metadata from files and archives
- List archive contents with metadata
- Clean and simple API with type hints
- Command-line interface (CLI)

## Installation

### Using Poetry (recommended)
```bash
# Install Poetry if you haven't already
curl -sSL https://install.python-poetry.org | python3 -

# Install the package
poetry install
```

### Using pip
```bash
pip install zipper
```

## Development

This project uses Poetry for dependency management. To set up the development environment:

```bash
# Clone the repository
git clone https://github.com/yourusername/zipper
cd zipper

# Install dependencies
poetry install

# Run tests
poetry run pytest
```

## Usage

### Python API

```python
from zipper import ZipArchive

# Create a new archive with metadata
with ZipArchive("example.zip") as archive:
    # Add files with metadata
    archive.add_file("document.txt", metadata={"type": "text", "version": "1.0"})
    archive.add_file("image.png", metadata={"type": "image", "author": "John"})
    
    # Add metadata to the entire archive
    archive.set_archive_metadata({
        "description": "Example archive",
        "created": "2024-03-15"
    })

# Read metadata from an archive
with ZipArchive("example.zip", "r") as archive:
    # Get archive metadata
    archive_metadata = archive.get_archive_metadata()
    print(f"Archive metadata: {archive_metadata}")
    
    # Get file metadata
    file_metadata = archive.get_file_metadata("document.txt")
    print(f"File metadata: {file_metadata}")
    
    # List all contents with metadata
    contents = archive.list_contents()
    for item in contents:
        print(f"File: {item['filename']}")
        print(f"Size: {item['size']} bytes")
        print(f"Metadata: {item['metadata']}")
```

### Command Line Interface

Create an archive:
```bash
# Create a simple archive
zipper create archive.zip file1.txt file2.txt

# Create with interactive metadata input (default)
zipper create archive.zip file1.txt file2.txt
# The CLI will prompt for metadata for each file and the archive

# Create with archive metadata
zipper create archive.zip file1.txt --archive-metadata '{"description": "My archive"}'

# Create with default file metadata
zipper create archive.zip file1.txt file2.txt --file-metadata '{"type": "document"}'
# In interactive mode, you can still override the default for specific files

# Create with both archive and file metadata
zipper create archive.zip file1.txt \
    --archive-metadata metadata.json \
    --file-metadata '{"type": "document"}'

# Disable interactive mode
zipper create archive.zip file1.txt --no-interactive
```

View metadata and contents:
```bash
# List archive contents
zipper list-contents archive.zip

# Get all metadata
zipper get-metadata archive.zip

# Get metadata for a specific file
zipper get-metadata archive.zip -f file1.txt
```

## Interactive Metadata Input

By default, the CLI runs in interactive mode, which allows you to:

1. Add different metadata for each file:
   - The CLI will prompt you for each file
   - Enter metadata as JSON or path to a JSON file
   - Press Enter to skip metadata for a file

2. Override default metadata:
   - When using `--file-metadata`, you can still customize metadata for specific files
   - The CLI will show the default metadata and ask if you want to use different metadata

3. Add archive metadata:
   - After adding files, you can add metadata to the archive itself
   - Skip by pressing Enter when prompted

Example interactive session:
```
$ zipper create archive.zip doc1.txt doc2.txt

Add metadata for doc1.txt?
> y

Enter metadata as JSON or path to JSON file
Example: {"type": "document", "version": "1.0"}
Or just press Enter to skip

Metadata> {"type": "document", "author": "John"}
Added doc1.txt to archive with metadata

Add metadata for doc2.txt?
> y

Enter metadata as JSON or path to JSON file
Example: {"type": "document", "version": "1.0"}
Or just press Enter to skip

Metadata> metadata.json
Added doc2.txt to archive with metadata

Add metadata to the archive?
> y

Enter metadata as JSON or path to JSON file
Example: {"type": "document", "version": "1.0"}
Or just press Enter to skip

Metadata> {"created": "2024-03-15", "project": "Documentation"}
Added metadata to archive
```

## API Reference

### ZipArchive

```python
class ZipArchive:
    def __init__(self, filename: str, mode: str = "w"):
        """
        Initialize a new ZIP archive.
        
        Args:
            filename (str): Path to the ZIP file
            mode (str): Mode to open the file in ('w' for write, 'r' for read)
        """

    def add_file(self, filepath: str, metadata: Optional[Dict[str, Any]] = None):
        """
        Add a file to the archive with optional metadata.
        
        Args:
            filepath (str): Path to the file to add
            metadata (dict, optional): Metadata to associate with the file
        """

    def set_archive_metadata(self, metadata: Dict[str, Any]):
        """
        Set metadata for the entire archive.
        
        Args:
            metadata (dict): Metadata for the archive
        """

    def get_archive_metadata(self) -> Dict[str, Any]:
        """
        Get the archive's metadata.
        
        Returns:
            dict: The archive's metadata
        """

    def get_file_metadata(self, filename: str) -> Dict[str, Any]:
        """
        Get a file's metadata.
        
        Args:
            filename (str): Name of the file in the archive
        
        Returns:
            dict: The file's metadata
        """

    def list_contents(self) -> List[Dict[str, Any]]:
        """
        List all files in the archive with their metadata.
        
        Returns:
            list: List of dictionaries containing file information and metadata
        """
```

## Metadata Format

Metadata must be valid JSON. Both archive and file metadata are stored as JSON strings in the ZIP file comments. Example metadata:

```json
{
    "description": "Project documentation",
    "author": "John Doe",
    "version": "1.0.0",
    "tags": ["docs", "project"],
    "created": "2024-03-15",
    "custom": {
        "department": "Engineering",
        "priority": "high"
    }
}
```

## Error Handling

The package raises the following exceptions:

- `ValueError`: When an invalid mode is specified (must be 'w' or 'r')
- `RuntimeError`: When trying to modify an archive in read mode
- `FileNotFoundError`: When a file to be added doesn't exist
- `KeyError`: When trying to get metadata for a non-existent file
- `json.JSONDecodeError`: When invalid JSON metadata is provided

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.