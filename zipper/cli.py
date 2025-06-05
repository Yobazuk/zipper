"""
Command-line interface for the Zipper package.

This module provides a modern, user-friendly command-line interface for working with
ZIP archives and their metadata. The interface uses rich formatting and colors for
better readability and provides helpful error messages and progress indicators.

Available commands:
- create: Create a new ZIP archive with optional metadata
- get-metadata: Read metadata from an archive or specific file
- list-contents: List archive contents with details

Example usage:
    # Create an archive with metadata
    zipper create archive.zip file1.txt --archive-metadata '{"description": "My files"}'
    
    # List contents
    zipper list-contents archive.zip
    
    # Get metadata
    zipper get-metadata archive.zip -f file1.txt
"""

import json
from pathlib import Path
from typing import List, Optional, Dict, Any
import sys
import typer
from rich import print
from rich.console import Console
from rich.table import Table
from rich.syntax import Syntax
from rich.prompt import Prompt, Confirm
from .core import ZipArchive

app = typer.Typer(
    help="Create and manage ZIP archives with metadata",
    add_completion=False
)
console = Console()


def validate_archive(archive_path: Path):
    """Validate that the archive path has a .zip extension."""
    if archive_path.suffix.lower() != '.zip':
        typer.secho(
            f"Error: Archive file must have .zip extension, got: {archive_path}",
            fg=typer.colors.RED,
            err=True
        )
        raise typer.Exit(1)


def parse_metadata(metadata_str: str) -> dict:
    """Parse metadata string into a dictionary."""
    try:
        # Check if the string is a path to a JSON file
        if metadata_str.endswith('.json') and Path(metadata_str).exists():
            with open(metadata_str, 'r') as f:
                return json.load(f)
        
        # Remove any PowerShell escaping
        metadata_str = metadata_str.strip('`"\' ')
        
        # First try parsing as is
        try:
            return json.loads(metadata_str)
        except json.JSONDecodeError:
            # Try replacing single quotes with double quotes and handle PowerShell escaping
            metadata_str = metadata_str.replace("'", '"').replace('`"', '"')
            return json.loads(metadata_str)
    except json.JSONDecodeError as e:
        typer.secho(
            'Error: Invalid JSON metadata format. Please use valid JSON with double quotes.\n'
            'Examples:\n'
            '  1. Direct JSON: \'{"key": "value"}\'\n'
            '  2. JSON file: metadata.json',
            fg=typer.colors.RED,
            err=True
        )
        raise typer.Exit(1)


def prompt_for_metadata(file: Path) -> Optional[Dict[str, Any]]:
    """Interactively prompt for file metadata."""
    if Confirm.ask(f"\nAdd metadata for {file.name}?"):
        print("\n[bold blue]Enter metadata as JSON or path to JSON file[/]")
        print("Example: {\"type\": \"document\", \"version\": \"1.0\"}")
        print("Or just press Enter to skip\n")
        
        metadata_str = Prompt.ask("Metadata")
        if metadata_str:
            try:
                return parse_metadata(metadata_str)
            except typer.Exit:
                if Confirm.ask("Invalid JSON. Try again?"):
                    return prompt_for_metadata(file)
    return None


@app.command()
def create(
    archive: Path = typer.Argument(..., help="Name of the archive to create"),
    files: List[Path] = typer.Argument(..., help="Files to add to the archive"),
    archive_metadata: Optional[str] = typer.Option(None, "--archive-metadata", help="JSON metadata for the archive"),
    file_metadata: Optional[str] = typer.Option(None, "--file-metadata", help="Default JSON metadata for all files"),
    interactive: bool = typer.Option(True, "--interactive/--no-interactive", help="Enable/disable interactive metadata input")
):
    """Create a new ZIP archive with the specified files and optional metadata."""
    validate_archive(archive)
    
    # Parse default metadata if provided
    archive_metadata_dict = parse_metadata(archive_metadata) if archive_metadata else None
    default_file_metadata = parse_metadata(file_metadata) if file_metadata else None
    
    # Collect all metadata first in interactive mode
    files_metadata = {}
    if interactive:
        for file in files:
            # Get file-specific metadata if in interactive mode
            metadata = None
            if not file_metadata:
                metadata = prompt_for_metadata(file)
            elif default_file_metadata:
                print(f"\n[bold blue]Default metadata for {file.name}:[/]")
                syntax = Syntax(
                    json.dumps(default_file_metadata, indent=2),
                    "json",
                    theme="monokai",
                    word_wrap=True
                )
                console.print(syntax)
                if Confirm.ask("Use different metadata for this file?"):
                    metadata = prompt_for_metadata(file)
                else:
                    metadata = default_file_metadata
            files_metadata[str(file)] = metadata
        
        # Prompt for archive metadata if not provided
        if not archive_metadata_dict and Confirm.ask("\nAdd metadata to the archive?"):
            archive_metadata_dict = prompt_for_metadata(archive)
    
    # Now create the archive with the collected metadata
    with console.status(f"Creating archive {archive}..."):
        with ZipArchive(str(archive)) as zip_archive:
            # Add files
            for file in files:
                try:
                    metadata = files_metadata.get(str(file)) if interactive else default_file_metadata
                    zip_archive.add_file(str(file), metadata=metadata)
                    if metadata:
                        typer.secho(f"Added {file} to archive with metadata", fg=typer.colors.GREEN)
                    else:
                        typer.secho(f"Added {file} to archive", fg=typer.colors.GREEN)
                except FileNotFoundError:
                    typer.secho(f"Error: File not found: {file}", fg=typer.colors.RED, err=True)
                    continue
            
            # Set archive metadata if provided
            if archive_metadata_dict:
                zip_archive.set_archive_metadata(archive_metadata_dict)
                typer.secho("Added metadata to archive", fg=typer.colors.GREEN)


@app.command(name="get-metadata")
def get_metadata(
    archive: Path = typer.Argument(..., help="Target archive"),
    file: Optional[Path] = typer.Option(None, "-f", "--file", help="Specific file to read metadata from")
):
    """Read metadata from archive or files."""
    validate_archive(archive)
    
    with ZipArchive(str(archive), 'r') as zip_archive:
        if file:
            try:
                metadata = zip_archive.get_file_metadata(str(file))
                if metadata:
                    print(f"\n[bold blue]Metadata for {file}:[/]")
                    syntax = Syntax(
                        json.dumps(metadata, indent=2),
                        "json",
                        theme="monokai",
                        word_wrap=True
                    )
                    console.print(syntax)
                else:
                    print(f"[yellow]No metadata found for {file}[/]")
            except KeyError:
                typer.secho(f"Error: File not found in archive: {file}", fg=typer.colors.RED, err=True)
                raise typer.Exit(1)
        else:
            # Read all metadata
            archive_metadata = zip_archive.get_archive_metadata()
            if archive_metadata:
                print("\n[bold green]Archive Metadata:[/]")
                syntax = Syntax(
                    json.dumps(archive_metadata, indent=2),
                    "json",
                    theme="monokai",
                    word_wrap=True
                )
                console.print(syntax)
            
            print("\n[bold blue]File Metadata:[/]")
            table = Table(show_header=True, header_style="bold magenta")
            table.add_column("File")
            table.add_column("Metadata")
            
            for item in zip_archive.list_contents():
                if item['metadata']:
                    table.add_row(
                        item['filename'],
                        json.dumps(item['metadata'], indent=2)
                    )
            
            if table.row_count > 0:
                console.print(table)
            else:
                print("[yellow]No file metadata found[/]")


@app.command()
def list_contents(
    archive: Path = typer.Argument(..., help="Archive to list contents of")
):
    """List archive contents with details."""
    validate_archive(archive)
    
    with ZipArchive(str(archive), 'r') as zip_archive:
        print(f"\n[bold blue]Archive:[/] {archive}")
        
        metadata = zip_archive.get_archive_metadata()
        if metadata:
            print("\n[bold green]Archive Metadata:[/]")
            syntax = Syntax(
                json.dumps(metadata, indent=2),
                "json",
                theme="monokai",
                word_wrap=True
            )
            console.print(syntax)
        
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("File")
        table.add_column("Size")
        table.add_column("Compressed")
        table.add_column("Metadata")
        
        for item in zip_archive.list_contents():
            table.add_row(
                item['filename'],
                f"{item['size']} bytes",
                f"{item['compressed_size']} bytes",
                json.dumps(item['metadata'], indent=2) if item['metadata'] else "[dim]No metadata[/]"
            )
        
        console.print(table)


if __name__ == "__main__":
    app() 