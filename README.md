# Kiro2PDF: Convert Kiro specs into printable pdf

A command-line utility to convert one or more Kiro markdown spec files into a single, consolidated PDF document. The script automatically generates a Table of Contents (TOC) with an entry for each input file, making it easy to navigate large documents.

## Features

-   **Combine Multiple Files**: Merge several Markdown files into one PDF.
-   **Automatic Table of Contents**: Each input file gets its own top-level entry in the PDF's TOC.
-   **Default Behavior**: If run without arguments, the script will search for markdown files in the `.kiro/specs` directory and offer to create a PDF from them.

## Prerequisites

Before running the script, you need to install the `markdown-pdf` library:

```bash
pip install markdown-pdf
```

## Usage

### Default Behavior

If you have your markdown files in a `.kiro/specs` directory, you can run the script without any arguments:

```bash
python kiro2pdf.py
```

The script will find the files and ask for confirmation before creating the PDF.

### Specific Document Generation

You can generate specific documents (todo, requirements, design) directly from the `.kiro/specs/` directory using dedicated flags. This will create individual PDF files named `kiro_todo.pdf`, `kiro_requirements.pdf`, and `kiro_design.pdf` respectively.

```bash
kiro2pdf --todo
kiro2pdf --requirements --design
```

### Basic Example

This command combines `requirement.md` and `design.md` into a single `output.pdf`.

```bash
python kiro2pdf.py requirements.md design.md -o output.pdf
```
