"""Tests for the core ZipArchive functionality."""

import json
import pytest
from pathlib import Path
from typing import Dict, Any
from zipper import ZipArchive

@pytest.fixture
def test_file(temp_dir: Path) -> Path:
    """Create a test file."""
    test_file = temp_dir / "test.txt"
    test_file.write_text("test content")
    return test_file

@pytest.fixture
def archive_path(temp_dir: Path) -> Path:
    """Create a path for the test archive."""
    return temp_dir / "test.zip"

def test_create_archive(archive_path: Path, temp_dir: Path, test_files: tuple[Path, Dict[str, Any]]):
    """Test creating a new archive with files."""
    dir_path, metadata = test_files
    
    with ZipArchive(str(archive_path)) as archive:
        # Add files with metadata
        for filename, file_metadata in metadata.items():
            archive.add_file(str(dir_path / filename), metadata=file_metadata)
    
    # Verify archive exists
    assert archive_path.exists()
    assert archive_path.is_file()

def test_read_archive(archive_path: Path, temp_dir: Path, test_files: tuple[Path, Dict[str, Any]]):
    """Test reading from an existing archive."""
    dir_path, metadata = test_files
    
    # Create archive
    with ZipArchive(str(archive_path)) as archive:
        for filename, file_metadata in metadata.items():
            archive.add_file(str(dir_path / filename), metadata=file_metadata)
    
    # Read archive
    with ZipArchive(str(archive_path), "r") as archive:
        # Check each file's metadata
        for filename, expected_metadata in metadata.items():
            actual_metadata = archive.get_file_metadata(filename)
            assert actual_metadata == expected_metadata

def test_archive_metadata(archive_path: Path, archive_metadata: Dict[str, Any]):
    """Test setting and getting archive metadata."""
    with ZipArchive(str(archive_path)) as archive:
        archive.set_archive_metadata(archive_metadata)
    
    with ZipArchive(str(archive_path), "r") as archive:
        actual_metadata = archive.get_archive_metadata()
        assert actual_metadata == archive_metadata

def test_list_contents(archive_path: Path, temp_dir: Path, test_files: tuple[Path, Dict[str, Any]]):
    """Test listing archive contents."""
    dir_path, metadata = test_files
    
    # Create archive
    with ZipArchive(str(archive_path)) as archive:
        for filename, file_metadata in metadata.items():
            archive.add_file(str(dir_path / filename), metadata=file_metadata)
    
    # List contents
    with ZipArchive(str(archive_path), "r") as archive:
        contents = archive.list_contents()
        
        # Verify each file
        assert len(contents) == len(metadata)
        for item in contents:
            filename = item["filename"]
            assert filename in metadata
            assert item["metadata"] == metadata[filename]
            assert item["size"] > 0
            assert "compressed_size" in item

def test_invalid_operations(archive_path: Path, test_file: Path, temp_dir: Path):
    """Test invalid operations raise appropriate errors."""
    # Create test files
    test_file.write_text("test content")
    doc_file = temp_dir / "document.txt"
    doc_file.write_text("document content")
    
    # Create an empty archive first
    with ZipArchive(str(archive_path)) as archive:
        archive.add_file(str(test_file))
    
    # Test write operations on read-only archive
    with ZipArchive(str(archive_path), "r") as archive:
        with pytest.raises(RuntimeError):
            archive.add_file(str(doc_file))
        with pytest.raises(RuntimeError):
            archive.set_archive_metadata({"test": "data"})
    
    # Test reading non-existent file metadata
    with ZipArchive(str(archive_path), "w") as archive:
        archive.add_file(str(doc_file))
        with pytest.raises(KeyError):
            archive.get_file_metadata("nonexistent.txt")

def test_json_metadata_validation(archive_path: Path, test_file: Path):
    """Test JSON metadata validation."""
    with ZipArchive(str(archive_path)) as archive:
        # Test non-serializable metadata
        with pytest.raises((TypeError, ValueError)):
            archive.add_file(str(test_file), metadata={"key": object()})
        
        # Test valid but complex metadata
        valid_metadata = {
            "strings": "test",
            "numbers": [1, 2, 3],
            "nested": {"key": "value"},
            "null": None,
            "boolean": True
        }
        archive.add_file(str(test_file), metadata=valid_metadata)
        
        # Test empty metadata
        archive.add_file(str(test_file), metadata={})

def test_context_manager(archive_path: Path, test_file: Path):
    """Test context manager behavior."""
    # Test normal exit
    with ZipArchive(str(archive_path)) as archive:
        archive.add_file(str(test_file))
    assert archive_path.exists()
    
    # Test exception handling
    with pytest.raises(ValueError):
        with ZipArchive(str(archive_path)) as archive:
            archive.add_file(str(test_file))
            raise ValueError("Test exception")
    
    # Archive should still exist and be valid
    assert archive_path.exists()
    with ZipArchive(str(archive_path), "r") as archive:
        contents = archive.list_contents()
        assert len(contents) == 1

def test_large_metadata(archive_path: Path, test_file: Path):
    """Test handling of large metadata."""
    # Create large nested metadata
    large_metadata = {
        "level1": {
            f"key{i}": {
                f"subkey{j}": f"value{i}{j}"
                for j in range(10)
            }
            for i in range(10)
        }
    }
    
    with ZipArchive(str(archive_path)) as archive:
        archive.add_file(str(test_file), metadata=large_metadata)
    
    with ZipArchive(str(archive_path), "r") as archive:
        read_metadata = archive.get_file_metadata(test_file.name)
        assert read_metadata == large_metadata

def test_multiple_files_same_name(archive_path: Path, temp_dir: Path, test_file: Path):
    """Test adding multiple files with the same name from different directories."""
    # Create two directories with same-named files
    dir1 = temp_dir / "dir1"
    dir2 = temp_dir / "dir2"
    dir1.mkdir()
    dir2.mkdir()
    
    file1 = dir1 / "test.txt"
    file2 = dir2 / "test.txt"
    file1.write_text("content1")
    file2.write_text("content2")
    
    with ZipArchive(str(archive_path)) as archive:
        # Add files with different metadata
        archive.add_file(str(file1), metadata={"source": "dir1"}, arcname="test.txt")
        # Second file should overwrite the first
        archive.add_file(str(file2), metadata={"source": "dir2"}, arcname="test.txt")
        # Add a different file to ensure proper counting
        archive.add_file(str(test_file), metadata={"source": "root"}, arcname="other.txt")
    
    with ZipArchive(str(archive_path), "r") as archive:
        contents = archive.list_contents()
        # We should have two files: test.txt (last added) and other.txt
        assert len(contents) == 2
        test_txt = next(item for item in contents if item["filename"] == "test.txt")
        assert test_txt["metadata"]["source"] == "dir2"

def test_invalid_mode(archive_path: Path):
    """Test opening archive with invalid mode."""
    with pytest.raises(ValueError, match="Mode must be 'w' for write or 'r' for read"):
        ZipArchive(str(archive_path), mode='a')

def test_write_to_read_only_archive(archive_path: Path, test_file: Path):
    """Test attempting to write to a read-only archive."""
    # First create an empty archive
    with ZipArchive(str(archive_path)) as archive:
        archive.add_file(str(test_file))
    
    # Try to write to it in read mode
    with pytest.raises(RuntimeError, match="Archive must be opened in write mode"):
        with ZipArchive(str(archive_path), 'r') as archive:
            archive.add_file(str(test_file))

def test_set_metadata_on_read_only_archive(archive_path: Path, test_file: Path, archive_metadata: Dict[str, Any]):
    """Test attempting to set metadata on a read-only archive."""
    # First create an empty archive
    with ZipArchive(str(archive_path)) as archive:
        archive.add_file(str(test_file))
    
    # Try to set metadata in read mode
    with pytest.raises(RuntimeError, match="Archive must be opened in write mode"):
        with ZipArchive(str(archive_path), 'r') as archive:
            archive.set_archive_metadata(archive_metadata) 