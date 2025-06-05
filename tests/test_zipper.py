"""
Integration tests for the Zipper package.
"""

import os
import json
import pytest
from pathlib import Path
from zipper.core import ZipArchive

def test_create_archive(temp_dir: Path, sample_files: list[Path]):
    """Test creating a new archive."""
    archive_path = str(temp_dir / "test.zip")
    test_files = [str(f) for f in sample_files]
    
    with ZipArchive(archive_path) as archive:
        archive.add_file(test_files[0])
    
    assert os.path.exists(archive_path)
    assert os.path.getsize(archive_path) > 0

def test_archive_metadata(temp_dir: Path, sample_files: list[Path]):
    """Test adding and retrieving archive metadata."""
    archive_path = str(temp_dir / "test.zip")
    test_files = [str(f) for f in sample_files]
    test_metadata = {"description": "Test archive", "version": "1.0.0"}
    
    with ZipArchive(archive_path) as archive:
        archive.add_file(test_files[0])
        archive.set_archive_metadata(test_metadata)
    
    with ZipArchive(archive_path, 'r') as archive:
        metadata = archive.get_archive_metadata()
        assert metadata == test_metadata

def test_file_metadata(temp_dir: Path, sample_files: list[Path]):
    """Test adding and retrieving file metadata."""
    archive_path = str(temp_dir / "test.zip")
    test_files = [str(f) for f in sample_files]
    test_metadata = {"type": "test", "version": "1.0.0"}
    test_file = os.path.basename(test_files[0])
    
    with ZipArchive(archive_path) as archive:
        archive.add_file(test_files[0], metadata=test_metadata)
    
    with ZipArchive(archive_path, 'r') as archive:
        metadata = archive.get_file_metadata(test_file)
        assert metadata == test_metadata

def test_list_contents(temp_dir: Path, sample_files: list[Path]):
    """Test listing archive contents."""
    archive_path = str(temp_dir / "test.zip")
    test_files = [str(f) for f in sample_files]
    file_metadata = {"type": "test"}
    
    with ZipArchive(archive_path) as archive:
        archive.add_file(test_files[0], metadata=file_metadata)
        archive.add_file(test_files[1])
    
    with ZipArchive(archive_path, 'r') as archive:
        contents = archive.list_contents()
        assert len(contents) == 2
        
        # Check first file has metadata
        first_file = next(item for item in contents if item['filename'] == os.path.basename(test_files[0]))
        assert first_file['metadata'] == file_metadata
        
        # Check second file has no metadata
        second_file = next(item for item in contents if item['filename'] == os.path.basename(test_files[1]))
        assert not second_file['metadata']

def test_read_only_mode(temp_dir: Path, sample_files: list[Path]):
    """Test read-only mode operations."""
    archive_path = str(temp_dir / "test.zip")
    test_files = [str(f) for f in sample_files]
    test_metadata = {"type": "test"}
    
    # Create archive in write mode
    with ZipArchive(archive_path) as archive:
        archive.add_file(test_files[0], metadata=test_metadata)
    
    # Try to modify in read mode
    with pytest.raises(RuntimeError, match="Archive must be opened in write mode"):
        with ZipArchive(archive_path, 'r') as archive:
            archive.add_file(test_files[1])
    
    # Verify original content is unchanged
    with ZipArchive(archive_path, 'r') as archive:
        contents = archive.list_contents()
        assert len(contents) == 1
        assert contents[0]['metadata'] == test_metadata


if __name__ == "__main__":
    pytest.main() 