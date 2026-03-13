import os
import argparse
import pymupdf4llm
from pathlib import Path

def convert_pdf_to_md(pdf_path, output_path=None):
    """
    Converts a single PDF file to a Markdown file.
    """
    pdf_path = Path(pdf_path)
    if not pdf_path.exists():
        print(f"Error: File {pdf_path} does not exist.")
        return False

    if output_path is None:
        output_path = pdf_path.with_suffix(".md")
    else:
        output_path = Path(output_path)

    print(f"Converting {pdf_path} to {output_path}...")
    
    try:
        # Extract markdown content
        md_text = pymupdf4llm.to_markdown(str(pdf_path))
        
        # Write to file
        output_path.write_text(md_text, encoding="utf-8")
        print(f"Successfully converted: {output_path}")
        return True
    except Exception as e:
        print(f"An error occurred while converting {pdf_path}: {e}")
        return False

def batch_convert(directory_path):
    """
    Converts all PDF files in a directory to Markdown.
    """
    directory = Path(directory_path)
    if not directory.is_dir():
        print(f"Error: {directory_path} is not a directory.")
        return

    pdf_files = list(directory.glob("*.pdf"))
    if not pdf_files:
        print(f"No PDF files found in {directory_path}.")
        return

    print(f"Found {len(pdf_files)} PDF files. Starting batch conversion...")
    success_count = 0
    for pdf_file in pdf_files:
        if convert_pdf_to_md(pdf_file):
            success_count += 1
    
    print(f"Batch conversion complete. Successfully converted {success_count}/{len(pdf_files)} files.")

def main():
    parser = argparse.ArgumentParser(description="Convert PDF files to Markdown.")
    parser.add_argument("path", nargs="?", default=".", help="Path to a PDF file or a directory containing PDFs (default: current directory).")
    parser.add_argument("-o", "--output", help="Output path for a single file conversion.")
    args = parser.parse_args()

    target_path = Path(args.path)

    if target_path.is_file():
        convert_pdf_to_md(target_path, args.output)
    elif target_path.is_dir():
        batch_convert(target_path)
    else:
        print(f"Error: Path {target_path} not found.")

if __name__ == "__main__":
    main()
