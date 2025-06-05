"""
Pytest configuration and fixtures.
"""

import os
import json
import pytest
from pathlib import Path
from typing import Dict, Any, Generator, Tuple

@pytest.fixture
def temp_dir(tmp_path: Path) -> Path:
    """Create a temporary directory for tests."""
    return tmp_path

@pytest.fixture
def test_files(temp_dir: Path) -> Tuple[Path, Dict[str, Any]]:
    """Create test files with content and return their metadata."""
    # Create test files
    file1 = temp_dir / "document.txt"
    file2 = temp_dir / "image.png"
    file3 = temp_dir / "data.json"
    
    # Write content
    file1.write_text("This is a test document")
    file2.write_bytes(b"Fake PNG content")
    file3.write_text('{"key": "value"}')
    
    # Create metadata
    metadata = {
        "document.txt": {
            "type": "text",
            "version": "1.0",
            "author": "Test User"
        },
        "image.png": {
            "type": "image",
            "format": "png",
            "dimensions": "100x100"
        },
        "data.json": {
            "type": "data",
            "format": "json",
            "schema_version": "1.0"
        }
    }
    
    return temp_dir, metadata

@pytest.fixture
def archive_metadata() -> Dict[str, Any]:
    """Return test archive metadata."""
    return {
        "project": "Test Project",
        "version": "1.0.0",
        "created": "2024-03-20",
        "description": "Test archive for Zipper tests"
    }

@pytest.fixture
def cleanup_files() -> Generator[None, None, None]:
    """Clean up any test files after tests."""
    yield
    # Clean up any .zip files in the current directory
    for file in Path().glob("*.zip"):
        file.unlink(missing_ok=True)

@pytest.fixture
def json_file(temp_dir: Path) -> Path:
    """Create a JSON file with test metadata."""
    json_path = temp_dir / "metadata.json"
    metadata = {
        "type": "document",
        "version": "1.0",
        "tags": ["test", "fixture"]
    }
    json_path.write_text(json.dumps(metadata))
    return json_path

@pytest.fixture
def sample_file(temp_dir):
    """Create a sample file for testing."""
    file_path = temp_dir / "sample.txt"
    content = "This is a test file."
    file_path.write_text(content)
    return file_path

@pytest.fixture
def sample_files(temp_dir):
    """Create multiple sample files for testing."""
    files = []
    for i in range(3):
        file_path = temp_dir / f"sample_{i}.txt"
        content = f"This is test file {i}."
        file_path.write_text(content)
        files.append(file_path)
    return files

@pytest.fixture
def sample_metadata():
    """Create sample metadata for testing."""
    return {
        "author": "Test User",
        "version": "1.0.0",
        "description": "Test file",
        "tags": ["test", "sample"]
    }

@pytest.fixture
def archive_path(temp_dir):
    """Create a path for the test archive."""
    return temp_dir / "test_archive.zip" 