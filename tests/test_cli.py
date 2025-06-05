"""Tests for the command-line interface."""

import json
import pytest
from pathlib import Path
from typer.testing import CliRunner
from zipper.cli import app
from zipper import ZipArchive
from typing import Dict, Any

@pytest.fixture
def runner() -> CliRunner:
    """Create a CLI runner."""
    return CliRunner()

@pytest.fixture
def test_file(temp_dir: Path) -> Path:
    """Create a test file."""
    test_file = temp_dir / "document.txt"
    test_file.write_text("test content")
    return test_file

@pytest.fixture
def archive_path(temp_dir: Path) -> Path:
    """Create a path for the test archive."""
    return temp_dir / "test.zip"

def test_create_basic(runner: CliRunner, archive_path: Path, temp_dir: Path, test_files: tuple[Path, Dict[str, Any]]):
    """Test basic archive creation."""
    dir_path, metadata = test_files
    files = list(dir_path.glob("*.*"))
    
    result = runner.invoke(app, [
        "create",
        str(archive_path),
        *[str(f) for f in files],
        "--no-interactive"
    ])
    
    assert result.exit_code == 0
    assert archive_path.exists()
    
    # Verify contents
    with ZipArchive(str(archive_path), "r") as archive:
        contents = archive.list_contents()
        assert len(contents) == len(files)
        assert all(any(f.name == item["filename"] for f in files) for item in contents)

def test_create_with_metadata(runner: CliRunner, archive_path: Path, temp_dir: Path, test_file: Path, archive_metadata: Dict[str, Any], test_files: tuple[Path, Dict[str, Any]]):
    """Test archive creation with metadata."""
    dir_path, metadata = test_files
    
    # Create metadata JSON files
    archive_meta_file = temp_dir / "archive_meta.json"
    file_meta_file = temp_dir / "file_meta.json"
    
    archive_meta_file.write_text(json.dumps(archive_metadata))
    file_meta_file.write_text(json.dumps(metadata["document.txt"]))
    
    result = runner.invoke(app, [
        "create",
        str(archive_path),
        str(test_file),
        "--archive-metadata", str(archive_meta_file),
        "--file-metadata", str(file_meta_file),
        "--no-interactive"
    ])
    
    assert result.exit_code == 0
    
    # Verify metadata
    with ZipArchive(str(archive_path), "r") as archive:
        assert archive.get_archive_metadata() == archive_metadata
        assert archive.get_file_metadata("document.txt") == metadata["document.txt"]

def test_get_metadata(runner: CliRunner, archive_path: Path, temp_dir: Path, test_files: tuple[Path, Dict[str, Any]]):
    """Test getting metadata from archive and files."""
    dir_path, metadata = test_files
    
    # Create archive with metadata
    with ZipArchive(str(archive_path)) as archive:
        for filename, file_metadata in metadata.items():
            archive.add_file(str(dir_path / filename), metadata=file_metadata)
        archive.set_archive_metadata({"project": "test"})
    
    # Test getting archive metadata
    result = runner.invoke(app, ["get-metadata", str(archive_path)])
    assert result.exit_code == 0
    assert "project" in result.stdout
    
    # Test getting file metadata
    result = runner.invoke(app, [
        "get-metadata",
        str(archive_path),
        "-f", "document.txt"
    ])
    assert result.exit_code == 0
    assert "text" in result.stdout
    assert "1.0" in result.stdout

def test_list_contents(runner: CliRunner, archive_path: Path, temp_dir: Path, test_files: tuple[Path, Dict[str, Any]]):
    """Test listing archive contents."""
    dir_path, metadata = test_files
    
    # Create archive
    with ZipArchive(str(archive_path)) as archive:
        for filename, file_metadata in metadata.items():
            archive.add_file(str(dir_path / filename), metadata=file_metadata)
    
    result = runner.invoke(app, ["list-contents", str(archive_path)])
    assert result.exit_code == 0
    
    # Check all files are listed
    for filename in metadata:
        assert filename in result.stdout

def test_interactive_mode(runner: CliRunner, archive_path: Path, test_file: Path):
    """Test interactive mode for metadata input."""
    # Create test file first
    test_file.write_text("test content")
    
    # Simulate interactive input with proper newlines
    input_data = (
        "y\n"  # Yes to add metadata for file
        '{"type": "test"}\n'  # File metadata
        "y\n"  # Yes to add archive metadata
        "y\n"  # Yes to add metadata for archive
        '{"project": "test"}\n'  # Archive metadata
    )
    
    result = runner.invoke(app, [
        "create",
        str(archive_path),
        str(test_file)
    ], input=input_data)
    
    # Print result for debugging
    if result.exit_code != 0:
        print(f"Exit code: {result.exit_code}")
        print(f"Output: {result.stdout}")
        print(f"Exception: {result.exception}")
    
    assert result.exit_code == 0
    
    # Verify metadata
    with ZipArchive(str(archive_path), "r") as archive:
        assert archive.get_file_metadata(test_file.name) == {"type": "test"}
        assert archive.get_archive_metadata() == {"project": "test"}

def test_error_handling(runner: CliRunner, archive_path: Path, temp_dir: Path, test_file: Path):
    """Test CLI error handling."""
    nonexistent = temp_dir / "nonexistent.txt"
    
    # Test non-existent file
    result = runner.invoke(app, [
        "create",
        str(archive_path),
        str(nonexistent),
        "--no-interactive"  # Disable interactive mode
    ])
    assert result.exit_code == 0  # CLI continues even if file not found
    assert "file not found" in result.stdout.lower()
    
    # Test invalid JSON metadata
    result = runner.invoke(app, [
        "create",
        str(archive_path),
        str(test_file),
        "--archive-metadata", "{invalid}",
        "--no-interactive"  # Disable interactive mode
    ])
    assert result.exit_code == 1
    assert "invalid json" in result.stdout.lower()
    
    # Test invalid archive extension
    invalid_path = temp_dir / "test.txt"
    result = runner.invoke(app, [
        "create",
        str(invalid_path),
        str(test_file),
        "--no-interactive"  # Disable interactive mode
    ])
    assert result.exit_code == 1
    assert "zip extension" in result.stdout.lower()

def test_help_messages(runner: CliRunner):
    """Test help messages for all commands."""
    # Main help
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "Usage:" in result.stdout
    
    # Command-specific help
    commands = ["create", "get-metadata", "list-contents"]
    for cmd in commands:
        result = runner.invoke(app, [cmd, "--help"])
        assert result.exit_code == 0
        assert "Usage:" in result.stdout

def test_json_file_handling(runner: CliRunner, archive_path: Path, test_file: Path, json_file: Path):
    """Test handling of JSON files for metadata."""
    result = runner.invoke(app, [
        "create",
        str(archive_path),
        str(test_file),
        "--file-metadata", str(json_file),
        "--no-interactive"
    ])
    
    assert result.exit_code == 0
    
    # Verify metadata was read from file
    with ZipArchive(str(archive_path), "r") as archive:
        metadata = archive.get_file_metadata("document.txt")
        assert metadata["type"] == "document"
        assert metadata["version"] == "1.0" 