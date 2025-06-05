"""
Core functionality for the Zipper package.

This module provides the core functionality for creating and reading ZIP archives with metadata
support. The metadata is stored as JSON in ZIP comments, allowing for structured data to be
associated with both individual files and the entire archive.

The main class, ZipArchive, provides a clean and simple API for working with ZIP archives
in either write ('w') or read ('r') mode. Write mode is used for creating new archives and
adding files with metadata, while read mode is used for reading existing archives and their
metadata.
"""

import os
import json
import zipfile
from typing import Optional, Dict, List, Any
from functools import wraps

def requires_open_archive(func):
    """
    Decorator to ensure the archive is open before executing a method.
    Raises RuntimeError if the archive is not open.
    """
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        if not self.archive:
            raise RuntimeError("Archive not opened. Use with context manager.")
        return func(self, *args, **kwargs)
    return wrapper

class ZipArchive:
    """
    A class for creating and reading ZIP archives with metadata support.
    
    This class provides functionality to:
    - Create new ZIP archives
    - Add files with optional JSON metadata
    - Set JSON metadata for the entire archive
    - Read metadata from files and the archive
    - List archive contents with their metadata
    
    The class uses a context manager pattern for safe file handling:
    
    Write mode example:
        with ZipArchive("example.zip") as archive:
            archive.add_file("document.txt", metadata={"type": "text"})
            archive.set_archive_metadata({"created": "2024-03-15"})
    
    Read mode example:
        with ZipArchive("example.zip", "r") as archive:
            metadata = archive.get_file_metadata("document.txt")
            contents = archive.list_contents()
    
    All metadata is stored as JSON in ZIP comments, ensuring compatibility
    with standard ZIP tools while providing structured data capabilities.
    """

    def __init__(self, filename: str, mode: str = "w"):
        """
        Initialize a new ZIP archive.

        Args:
            filename (str): Path to the ZIP file
            mode (str): Mode to open the file in ('w' for write, 'r' for read)
        """
        if mode not in ('w', 'r'):
            raise ValueError("Mode must be 'w' for write or 'r' for read")
        
        self.filename = filename
        self.mode = mode
        self.archive = None

    def __enter__(self):
        """Context manager entry point."""
        self.archive = zipfile.ZipFile(self.filename, self.mode)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit point."""
        if self.archive:
            self.archive.close()

    def _encode_metadata(self, metadata: Dict[str, Any]) -> bytes:
        """Encode metadata dictionary to bytes for ZIP comment."""
        return json.dumps(metadata, ensure_ascii=True).encode('utf-8')

    def _decode_metadata(self, comment: bytes) -> Dict[str, Any]:
        """Decode ZIP comment bytes to metadata dictionary."""
        if not comment:
            return {}
        try:
            return json.loads(comment.decode('utf-8'))
        except (json.JSONDecodeError, UnicodeDecodeError):
            # If the comment is not valid JSON, treat it as a legacy plain text comment
            return {"comment": comment.decode('utf-8', errors='replace')}

    @requires_open_archive
    def add_file(self, filepath: str, metadata: Optional[Dict[str, Any]] = None, arcname: Optional[str] = None) -> None:
        """
        Add a file to the archive with optional metadata.

        Args:
            filepath (str): Path to the file to add
            metadata (dict, optional): Metadata to associate with the file
            arcname (str, optional): Alternative name for the file in the archive
        """
        if self.mode != 'w':
            raise RuntimeError("Archive must be opened in write mode to add files")

        if not os.path.exists(filepath):
            raise FileNotFoundError(f"File not found: {filepath}")

        # Use provided arcname or basename of filepath
        name_in_archive = arcname or os.path.basename(filepath)

        # Create ZipInfo object for the file
        zinfo = zipfile.ZipInfo.from_file(filepath, name_in_archive)
        
        # Store and encode metadata if provided
        if metadata:
            zinfo.comment = self._encode_metadata(metadata)
        
        # Read file contents and write to archive with ZipInfo
        with open(filepath, 'rb') as f:
            self.archive.writestr(zinfo, f.read())

    @requires_open_archive
    def set_archive_metadata(self, metadata: Dict[str, Any]) -> None:
        """
        Set metadata for the entire archive.

        Args:
            metadata (dict): Metadata for the archive
        """
        if self.mode != 'w':
            raise RuntimeError("Archive must be opened in write mode to set metadata")
        
        self.archive.comment = self._encode_metadata(metadata)

    @requires_open_archive
    def get_archive_metadata(self) -> Dict[str, Any]:
        """
        Get the archive's metadata.

        Returns:
            dict: The archive's metadata
        """
        return self._decode_metadata(self.archive.comment)

    @requires_open_archive
    def get_file_metadata(self, filename: str) -> Dict[str, Any]:
        """
        Get a file's metadata.

        Args:
            filename (str): Name of the file in the archive

        Returns:
            dict: The file's metadata
        """
        # Normalize filename to match what's in the archive
        filename = os.path.basename(filename)
        
        try:
            info = self.archive.getinfo(filename)
            return self._decode_metadata(info.comment)
        except KeyError:
            raise KeyError(f"File not found in archive: {filename}")

    @requires_open_archive
    def list_contents(self) -> List[Dict[str, Any]]:
        """
        List all files in the archive with their metadata.

        Returns:
            list: List of dictionaries containing file information and metadata
        """
        contents = []
        for info in self.archive.filelist:
            contents.append({
                'filename': info.filename,
                'size': info.file_size,
                'compressed_size': info.compress_size,
                'metadata': self._decode_metadata(info.comment)
            })
        return contents 