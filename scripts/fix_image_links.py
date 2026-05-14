#!/usr/bin/env python3
"""
Script to fix image links in organized documentation folders.
Changes 'images/' to '../images/' for proper linking from subdirectories.
"""

from pathlib import Path
import re

# Get the project root directory
PROJECT_ROOT = Path(__file__).parent.parent
DOCS_DIR = PROJECT_ROOT / "docs"

# Folders that contain markdown files with image links
CONTENT_FOLDERS = [
    "facility-management",
    "appointments",
    "patient-registration",
    "encounters",
    "clinical",
    "laboratory",
    "billing",
    "pharmacy",
    "miscellaneous"
]

def fix_image_links_in_file(file_path):
    """Fix image links in a single markdown file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Replace images/ with ../images/ but not ../images/ (already fixed)
    original = content
    content = re.sub(r'!\[([^\]]*)\]\(images/', r'![\1](../images/', content)

    if content != original:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def main():
    print("=" * 60)
    print("Fixing Image Links in Documentation")
    print("=" * 60)

    fixed_count = 0
    total_files = 0

    for folder in CONTENT_FOLDERS:
        folder_path = DOCS_DIR / folder
        if not folder_path.exists():
            continue

        print(f"\nProcessing folder: {folder}")

        for md_file in folder_path.glob("*.md"):
            if md_file.name == "index.md":
                continue

            total_files += 1
            if fix_image_links_in_file(md_file):
                fixed_count += 1
                print(f"  ✓ Fixed: {md_file.name}")

    print("\n" + "=" * 60)
    print(f"✓ Processed {total_files} files")
    print(f"✓ Fixed image links in {fixed_count} files")
    print("=" * 60)

if __name__ == "__main__":
    main()
