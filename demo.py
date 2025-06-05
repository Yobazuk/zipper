from zipper import ZipArchive
import os
from pathlib import Path

# Create some sample files and directories
def create_sample_files():
    # Create directories
    Path("dir1").mkdir(exist_ok=True)
    Path("dir2").mkdir(exist_ok=True)
    
    # Create files
    files = [
        "file1.txt",
        "file2.json",
        "file3.py",
        "file4.md",
        "file5.csv",
        "dir1/inside_dir1.txt",
        "dir2/inside_dir2.log"
    ]
    
    for file_path in files:
        # Create parent directories if they don't exist
        Path(file_path).parent.mkdir(parents=True, exist_ok=True)
        # Write some sample content
        with open(file_path, 'w') as f:
            f.write(f"Sample content for {file_path}")
    
    return files

def get_file_metadata(file_path):
    """Generate metadata for a file."""
    path = Path(file_path)
    return {
        "name": path.name,
        "size": path.stat().st_size,
        "type": path.suffix.lstrip('.') or 'txt',  # If no extension, assume txt
        "directory": str(path.parent) if str(path.parent) != '.' else 'root'
    }

def main():
    # First create our sample files
    print("Creating sample files...")
    files = create_sample_files()
    
    # Create the archive with metadata
    print("\nCreating archive with metadata...")
    with ZipArchive("demo_archive.zip") as archive:
        # Add each file with its metadata
        for file_path in files:
            metadata = get_file_metadata(file_path)
            archive.add_file(file_path, metadata=metadata)
            print(f"Added {file_path} with metadata: {metadata}")
        
        # Set archive-level metadata
        archive_metadata = {
            "total_files": len(files),
            "directories": ["dir1", "dir2"],
            "created": "2024-03-20",
            "description": "Demo archive with metadata"
        }
        archive.set_archive_metadata(archive_metadata)
        print(f"\nSet archive metadata: {archive_metadata}")
    
    # Verify the contents
    print("\nVerifying archive contents:")
    with ZipArchive("demo_archive.zip", "r") as archive:
        contents = archive.list_contents()
        print("\nFiles in archive:")
        for item in contents:
            print(f"\nFile: {item['filename']}")
            print(f"Size: {item['size']} bytes")
            print(f"Metadata: {item['metadata']}")
        
        print("\nArchive metadata:")
        print(archive.get_archive_metadata())

if __name__ == "__main__":
    main() 