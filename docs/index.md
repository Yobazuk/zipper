---
layout: home

hero:
  name: "Zipper"
  text: "ZIP Archives with Structured Metadata"
  tagline: A modern Python package for creating and managing ZIP archives with rich metadata support
  actions:
    - theme: brand
      text: Get Started
      link: /guide/getting-started
    - theme: alt
      text: View on GitHub
      link: https://github.com/yourusername/zipper

features:
  - icon: 📦
    title: Metadata Support
    details: Attach structured JSON metadata to both individual files and entire archives. Perfect for organizing and cataloging your data.
  - icon: 🎯
    title: Focused Design
    details: Streamlined for create and read operations, making it simple and reliable for your archiving needs.
  - icon: 💻
    title: Interactive CLI
    details: Beautiful command-line interface with interactive metadata input, rich formatting, and progress indicators.
  - icon: 🐍
    title: Clean Python API
    details: Type-hinted Python API with context managers and comprehensive error handling for robust integration.
  - icon: 🎨
    title: Rich Output
    details: Beautiful output with syntax highlighting, tables, and progress bars powered by the Rich library.
  - icon: 🔍
    title: Smart Metadata
    details: Load metadata from JSON files or input directly, with interactive prompts and validation.

highlights:
  - title: Simple Yet Powerful
    details: Create archives with just a few lines of code
    code: |
      ```python
      from zipper import ZipArchive
      
      with ZipArchive("docs.zip") as archive:
          archive.add_file("readme.md", metadata={"type": "documentation"})
          archive.set_archive_metadata({"project": "MyApp"})
      ```
  
  - title: Interactive CLI
    details: Easy to use command-line interface
    code: |
      ```bash
      # Create archive with interactive metadata prompts
      zipper create archive.zip file1.txt file2.txt
      
      # View contents and metadata
      zipper list-contents archive.zip
      ```
  
  - title: Rich Metadata Support
    details: Attach and manage structured metadata
    code: |
      ```json
      {
        "type": "document",
        "version": "1.0",
        "author": "John Doe",
        "tags": ["draft", "review"]
      }
      ```
--- 