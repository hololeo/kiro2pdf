# Kiro2PDF: Convert Kiro specs into printable pdf

A command-line utility to convert one or more Kiro markdown spec files into a single, consolidated PDF document. The script automatically generates a Table of Contents (TOC) with an entry for each input file, making it easy to navigate large documents.

## Features

-   **Combine Multiple Files**: Merge several Markdown files into one PDF.
-   **Automatic Table of Contents**: Each input file gets its own top-level entry in the PDF's TOC.

## Prerequisites

Before running the script, you need to install the `markdown-pdf` library:

```bash
pip install markdown-pdf
```

## Usage

Run the script from your terminal, providing the input Markdown files and specifying an output file.

### Basic Example

This command combines `requirement.md` and `design.md` into a single `output.pdf`.

```bash
python kiro2pdf.py requirements.md design.md -o output.pdf
```
