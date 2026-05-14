#!/usr/bin/env python3
"""
Script to fix markdown formatting issues from Confluence conversion.
Adds proper spacing and line breaks where missing.
"""

from pathlib import Path
import re

# Get the project root directory
PROJECT_ROOT = Path(__file__).parent.parent
DOCS_DIR = PROJECT_ROOT / "docs"

# Folders to process
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

def fix_formatting(content):
    """Fix common markdown formatting issues."""

    # Fix heading concatenation (### ObjectiveThis -> ### Objective\n\nThis)
    content = re.sub(r'(###?\s+[A-Z][a-z]+)([A-Z])', r'\1\n\n\2', content)

    # Fix Key Steps formatting (Key Steps**Step -> Key Steps\n\n**Step)
    content = re.sub(r'(Key Steps)(\*\*)', r'\1\n\n\2', content)

    # Fix bold start of sentences after headings
    content = re.sub(r'(###\s+.+?)(\*\*[A-Z])', r'\1\n\n\2', content)

    # Add proper spacing after link timestamps like [0:00](url)text -> [0:00](url)\n\ntext
    content = re.sub(r'(\]\([^)]+\))([A-Z][a-z])', r'\1\n\n\2', content)

    # Fix double asterisks without spaces (**text** something -> **text**\n\nsomething)
    content = re.sub(r'(\*\*\s+[0-9]+:)', r'\n\n\1', content)

    # Fix "Cautionary Notes" and "Tips" sections
    content = re.sub(r'(Cautionary Notes)([A-Z-])', r'\1\n\n\2', content)
    content = re.sub(r'(Tips for Efficiency)([A-Z-])', r'\1\n\n\2', content)

    # Fix "Link to Loom" sections
    content = re.sub(r'(Link to Loom)(\[?https?://)', r'\1\n\n\2', content)

    # Ensure double line breaks after headers
    content = re.sub(r'(###\s+.+?)\n([A-Z][a-z])', r'\1\n\n\2', content)

    # Clean up multiple consecutive blank lines (more than 2)
    content = re.sub(r'\n{4,}', '\n\n\n', content)

    return content

def process_file(file_path):
    """Process a single markdown file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Skip if no frontmatter
        if not content.startswith('---'):
            return False

        original = content
        fixed = fix_formatting(content)

        if fixed != original:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(fixed)
            return True

        return False
    except Exception as e:
        print(f"  ✗ Error processing {file_path.name}: {e}")
        return False

def main():
    print("=" * 60)
    print("Fixing Markdown Formatting Issues")
    print("=" * 60)

    fixed_count = 0
    total_files = 0

    # Process all content folders
    for folder in CONTENT_FOLDERS:
        folder_path = DOCS_DIR / folder
        if not folder_path.exists():
            continue

        print(f"\nProcessing: {folder}/")

        for md_file in folder_path.glob("*.md"):
            total_files += 1
            if process_file(md_file):
                fixed_count += 1
                print(f"  ✓ Fixed: {md_file.name}")

    # Also process root level docs
    print(f"\nProcessing: root level docs")
    for md_file in DOCS_DIR.glob("*.md"):
        if md_file.name not in ['index.md', 'README.md', 'QUICK_START.md']:
            total_files += 1
            if process_file(md_file):
                fixed_count += 1
                print(f"  ✓ Fixed: {md_file.name}")

    print("\n" + "=" * 60)
    print(f"✓ Processed {total_files} files")
    print(f"✓ Fixed formatting in {fixed_count} files")
    print("=" * 60)

if __name__ == "__main__":
    main()
