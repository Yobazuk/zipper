#!/usr/bin/env python3
"""
Demonstration: Reading only ZIP archive metadata without extracting files

This script shows different ways to read only the archive-level metadata
from a ZIP file without reading or extracting any of the inner files.
"""

import json
from zipper.core import ZipArchive

def demo_read_archive_metadata_only():
    """
    Demonstrate reading only archive metadata without touching inner files.
    """
    
    # First, let's create a sample archive with metadata for demonstration
    print("🔧 Creating sample archive with metadata...")
    
    sample_archive = "sample_with_metadata.zip"
    archive_metadata = {
        "title": "My Document Collection",
        "author": "John Doe", 
        "created": "2024-03-15",
        "version": "1.0",
        "description": "A collection of important documents",
        "tags": ["documents", "important", "work"]
    }
    
    # Create archive with some files and metadata
    with ZipArchive(sample_archive, "w") as archive:
        # Add some files (we won't read these later)
        archive.add_file("file1.txt", metadata={"type": "text", "category": "notes"})
        archive.add_file("file2.json", metadata={"type": "data", "format": "json"})
        
        # Set archive-level metadata
        archive.set_archive_metadata(archive_metadata)
    
    print(f"✅ Created {sample_archive} with archive metadata and 2 files\n")
    
    # Now demonstrate reading ONLY the archive metadata
    print("📖 Reading ONLY archive metadata (no file extraction):")
    print("=" * 60)
    
    # Method 1: Using the ZipArchive class
    with ZipArchive(sample_archive, "r") as archive:
        # This reads ONLY the archive comment, not any file contents
        metadata = archive.get_archive_metadata()
        
        print("📋 Archive Metadata:")
        print(json.dumps(metadata, indent=2))
        print()
        
        # Show that we can access metadata without listing or reading files
        print("🔍 Archive metadata details:")
        for key, value in metadata.items():
            print(f"  • {key}: {value}")
    
    print("\n" + "=" * 60)
    print("✨ Key Points:")
    print("  • Only the ZIP archive comment was read")
    print("  • No files were extracted or read from the archive") 
    print("  • This is very fast even for large archives")
    print("  • File contents remain untouched and secure")

def demo_using_standard_zipfile():
    """
    Show how the same can be done with standard zipfile module.
    """
    print("\n" + "=" * 60)
    print("🔧 Alternative: Using standard zipfile module directly")
    print("=" * 60)
    
    import zipfile
    
    # Read only archive comment using standard zipfile
    with zipfile.ZipFile("sample_with_metadata.zip", "r") as zf:
        # Get raw comment bytes
        raw_comment = zf.comment
        
        if raw_comment:
            try:
                # Decode JSON metadata
                metadata = json.loads(raw_comment.decode('utf-8'))
                print("📋 Archive metadata (via standard zipfile):")
                print(json.dumps(metadata, indent=2))
            except json.JSONDecodeError:
                print(f"📋 Raw archive comment: {raw_comment.decode('utf-8', errors='replace')}")
        else:
            print("❌ No archive comment found")

def demo_cli_usage():
    """
    Show CLI usage for reading archive metadata only.
    """
    print("\n" + "=" * 60)
    print("💻 CLI Usage Examples")
    print("=" * 60)
    
    print("To read ONLY archive metadata using the CLI:")
    print()
    print("  # Read archive metadata only (no file-specific metadata)")
    print("  python -m zipper get-metadata sample_with_metadata.zip")
    print()
    print("  # This will show:")
    print("  #   - Archive-level metadata in JSON format")
    print("  #   - File metadata table (but files aren't extracted)")
    print()
    print("To read metadata of a specific file (still no extraction):")
    print("  python -m zipper get-metadata sample_with_metadata.zip -f file1.txt")

if __name__ == "__main__":
    print("🚀 ZIP Archive Metadata Reader Demo")
    print("=" * 60)
    
    # Run demonstrations
    demo_read_archive_metadata_only()
    demo_using_standard_zipfile()
    demo_cli_usage()
    
    print("\n✅ Demo completed!")
    print("📁 Sample archive 'sample_with_metadata.zip' created for testing") 