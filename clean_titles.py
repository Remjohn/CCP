import argparse
from pathlib import Path

def clean_titles(directory):
    path = Path(directory)
    if not path.exists():
        print(f"Directory {directory} does not exist.")
        return

    print(f"Cleaning titles in: {directory}")
    prefixes = ["_OceanofPDF.com_", "dokumen.pub_"]
    count = 0

    for item in path.iterdir():
        if not item.is_file():
            continue

        name = item.name

        # Remove common prefixes
        for prefix in prefixes:
            if name.startswith(prefix):
                name = name[len(prefix):]
                break

        # Replace underscores with spaces in the stem only
        stem = Path(name).stem.replace("_", " ").strip()
        # Clean up any double spaces that resulted from double underscores
        import re
        stem = re.sub(r'\s+', ' ', stem)
        suffix = Path(name).suffix
        new_name = stem + suffix

        new_path = item.parent / new_name

        if new_path == item:
            continue

        if new_path.exists():
            print(f"Skipping '{item.name}', '{new_name}' already exists.")
            continue

        item.rename(new_path)
        print(f"Renamed: {item.name} -> {new_name}")
        count += 1

    print(f"Finished cleaning {count} files in {directory}.\n")

if __name__ == "__main__":
    import sys
    parser = argparse.ArgumentParser(description="Clean file titles in a directory.")
    parser.add_argument(
        "paths",
        nargs="*",
        default=["lab/Ai Engineering books", "lab/Public Speeaking Coaching"],
        help="Directories to clean (default: the two standard lab dirs)."
    )
    args = parser.parse_args()
    for p in args.paths:
        clean_titles(p)
