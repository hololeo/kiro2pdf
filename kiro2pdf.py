#!/usr/bin/env python3
import argparse
import os
import sys
import glob
from markdown_pdf import MarkdownPdf, Section

def create_pdf_from_markdown_files(
    input_files: list[str],
    output_file: str,
    toc_level: int = 6,
    optimize: bool = False,
    css_file: str = None
):
    """
    Converts multiple Markdown files into a single PDF document.

    Each Markdown file is treated as a separate section in the PDF,
    and a top-level heading (H1) derived from its filename is
    prepended to its content to ensure an entry in the Table of Contents.

    Args:
        input_files: A list of paths to the input Markdown files.
        output_file: The path for the output PDF file.
        toc_level: The maximum heading level (1-6) to include in the PDF's
                   Table of Contents. Default is 6 (all headings).
        optimize: If True, the generated PDF will be optimized for size.
        css_file: Optional path to a CSS file for custom styling of the PDF.
    """
    pdf = MarkdownPdf(toc_level=toc_level, optimize=optimize)

    # Load custom CSS if a path is provided
    user_css = None
    if css_file:
        try:
            with open(css_file, 'r', encoding='utf-8') as f:
                user_css = f.read()
            print(f"Using custom CSS from: {css_file}")
        except FileNotFoundError:
            print(f"Error: Custom CSS file '{css_file}' not found. Proceeding without custom CSS.")
            user_css = None
        except Exception as e:
            print(f"Error reading CSS file '{css_file}': {e}. Proceeding without custom CSS.")
            user_css = None

    print(f"Processing {len(input_files)} Markdown files...")

    for md_file_path in input_files:
        try:
            with open(md_file_path, 'r', encoding='utf-8') as f:
                md_content = f.read()

            # Extract filename (without extension) to use as a default title for the TOC entry
            file_basename = os.path.basename(md_file_path)
            title_for_toc = os.path.splitext(file_basename)[0]

            # Prepend a top-level heading (H1) to the content to ensure each file
            # gets a distinct entry in the PDF's Table of Contents.
            # This ensures consistency even if the original markdown file doesn't start with an H1.
            section_content_with_title = f"# {title_for_toc}\n\n" + md_content

            # Add the section to the PDF. The 'toc=True' (default for Section)
            # ensures that headings within this section (including our prepended H1)
            # are considered for the Table of Contents.
            pdf.add_section(Section(section_content_with_title), user_css=user_css)
            print(f"Added '{md_file_path}' as a section.")

        except FileNotFoundError:
            print(f"Warning: Markdown file '{md_file_path}' not found. Skipping this file.")
            continue
        except Exception as e:
            print(f"Error processing '{md_file_path}': {e}. Skipping this file.")
            continue

    # Set overall PDF metadata
    pdf.meta["title"] = "Combined Markdown Document"
    pdf.meta["author"] = "Markdown to PDF CLI"

    try:
        pdf.save(output_file)
        print(f"\nSuccessfully created PDF: {output_file}")
    except Exception as e:
        print(f"\nError saving PDF to '{output_file}': {e}")

def main():
    """
    Main function to parse command-line arguments and initiate PDF creation.
    """
    # Check for the new default behavior: no arguments provided
    if len(sys.argv) == 1:
        kiro_dir = ".kiro/specs"
        if os.path.isdir(kiro_dir):
            md_files = glob.glob(os.path.join(kiro_dir, "*.md"))
            if md_files:
                print("Found the following spec files:")
                for f in md_files:
                    print(f"  - {f}")
                
                user_input = input("Create PDF from these files? (y/n): ").lower()
                if user_input == 'y':
                    output_file = "theplan.pdf"
                    print(f"Generating {output_file}...")
                    # Get absolute paths for the files
                    abs_md_files = [os.path.abspath(f) for f in md_files]
                    create_pdf_from_markdown_files(abs_md_files, output_file)
                    print("Done.")
                else:
                    print("To generate the PDF manually, run the following command:")
                    # Get absolute paths for the files
                    abs_md_files = [os.path.abspath(f) for f in md_files]
                    print(f"python {sys.argv[0]} {' '.join(abs_md_files)} -o theplan.pdf")
                return

    parser = argparse.ArgumentParser(
        description="Convert one or more Markdown files to a single PDF, "
                    "with each input file appearing as a separate section in the PDF's Table of Contents."
    )
    parser.add_argument(
        "input_files",
        nargs="*",  # Allow zero or more arguments
        help="One or more paths to input Markdown files (.md).",
    )
    parser.add_argument(
        "--todo",
        action="store_true",
        help="Generate PDF for the 'tasks.md' spec file.",
    )
    parser.add_argument(
        "--requirements",
        action="store_true",
        help="Generate PDF for the 'requirements.md' spec file.",
    )
    parser.add_argument(
        "--design",
        action="store_true",
        help="Generate PDF for the 'design.md' spec file.",
    )
    parser.add_argument(
        "-o",
        "--output",
        required=False, # Not required for the new default behavior
        help="The path for the output PDF file (e.g., output.pdf).",
    )
    parser.add_argument(
        "-t",
        "--toc-level",
        type=int,
        default=6,
        choices=range(1, 7), # TOC levels from H1 to H6
        metavar="{1-6}",
        help="Maximum heading level to include in the Table of Contents (1=H1 only, 6=H1-H6). Default is 6.",
    )
    parser.add_argument(
        "-z",
        "--optimize",
        action="store_true",
        help="Optimize the PDF file size for smaller output.",
    )
    parser.add_argument(
        "-c",
        "--css",
        help="Optional path to a CSS file for custom styling of the PDF content.",
    )

    args = parser.parse_args()

    # Handle specific flags: --todo, --requirements, --design
    specific_requests_made = False
    if args.todo:
        specific_requests_made = True
        md_file = os.path.abspath(os.path.join(".kiro", "specs", "tasks.md"))
        output_pdf = "kiro_todo.pdf"
        print(f"Generating {output_pdf} from {md_file}...")
        create_pdf_from_markdown_files([md_file], output_pdf, args.toc_level, args.optimize, args.css)

    if args.requirements:
        specific_requests_made = True
        md_file = os.path.abspath(os.path.join(".kiro", "specs", "requirements.md"))
        output_pdf = "kiro_requirements.pdf"
        print(f"Generating {output_pdf} from {md_file}...")
        create_pdf_from_markdown_files([md_file], output_pdf, args.toc_level, args.optimize, args.css)

    if args.design:
        specific_requests_made = True
        md_file = os.path.abspath(os.path.join(".kiro", "specs", "design.md"))
        output_pdf = "kiro_design.pdf"
        print(f"Generating {output_pdf} from {md_file}...")
        create_pdf_from_markdown_files([md_file], output_pdf, args.toc_level, args.optimize, args.css)

    if specific_requests_made:
        return # Exit after handling specific requests

    # Existing logic for general input_files and output
    if not args.input_files:
        parser.print_help()
        return

    if not args.output:
        print("Error: The --output argument is required when providing input files.")
        parser.print_help()
        return

    create_pdf_from_markdown_files(
        input_files=args.input_files,
        output_file=args.output,
        toc_level=args.toc_level,
        optimize=args.optimize,
        css_file=args.css
    )

if __name__ == "__main__":
    main()
