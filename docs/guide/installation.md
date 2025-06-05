# Installation

Zipper requires Python 3.11 or higher. You can install it using either Poetry (recommended) or pip.

## Using Poetry (Recommended)

[Poetry](https://python-poetry.org/) is a modern dependency management and packaging tool for Python. To install Zipper using Poetry:

1. First, install Poetry if you haven't already:

::: code-group
```bash [Linux/macOS]
curl -sSL https://install.python-poetry.org | python3 -
```

```powershell [Windows]
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -
```
:::

2. Create a new project or navigate to your existing project:

```bash
cd your-project
```

3. Add Zipper as a dependency:

```bash
poetry add zipper
```

## Using pip

You can also install Zipper using pip:

```bash
pip install zipper
```

## Development Installation

If you want to contribute to Zipper or install it from source:

1. Clone the repository:

```bash
git clone https://github.com/yourusername/zipper
cd zipper
```

2. Install dependencies using Poetry:

```bash
poetry install
```

This will install all dependencies, including development dependencies.

## Verifying the Installation

To verify that Zipper is installed correctly:

1. Using Poetry:

```bash
poetry run zipper --help
```

2. Using pip:

```bash
zipper --help
```

You should see the help message with available commands:

```
Usage: zipper [OPTIONS] COMMAND [ARGS]...

  Create and manage ZIP archives with metadata

Options:
  --help  Show this message and exit.

Commands:
  create        Create a new ZIP archive with the specified files
  get-metadata  Read metadata from archive or files
  list         List archive contents with details
  set-metadata  Add metadata to archive or files
```

## Requirements

- Python 3.11 or higher
- Poetry (recommended) or pip
- Operating System: Windows, macOS, or Linux

## Next Steps

- [Getting Started](./getting-started.md) - Learn how to use Zipper
- [API Reference](/reference/api.md) - Explore the Python API and CLI
- [Implementation Details](/reference/implementation.md) - Learn about the internals 