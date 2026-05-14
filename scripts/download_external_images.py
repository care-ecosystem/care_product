#!/usr/bin/env python3
"""
Script to download external images (like Loom thumbnails) from markdown files
and update the references to use local copies.
"""

import re
import requests
from pathlib import Path
from urllib.parse import urlparse
import hashlib

# Get the project root directory (parent of scripts/)
PROJECT_ROOT = Path(__file__).parent.parent
DOCS_DIR = PROJECT_ROOT / "docs"
IMAGES_DIR = DOCS_DIR / "images"

IMAGES_DIR.mkdir(exist_ok=True)


def download_image(url):
    """Download an image from URL and save it locally."""
    try:
        response = requests.get(url, timeout=30)
        if response.status_code == 200:
            # Generate filename from URL hash
            url_hash = hashlib.md5(url.encode()).hexdigest()[:12]

            # Try to get extension from URL or content type
            parsed = urlparse(url)
            ext = Path(parsed.path).suffix
            if not ext:
                content_type = response.headers.get('content-type', '')
                if 'png' in content_type:
                    ext = '.png'
                elif 'jpeg' in content_type or 'jpg' in content_type:
                    ext = '.jpg'
                elif 'gif' in content_type:
                    ext = '.gif'
                elif 'webp' in content_type:
                    ext = '.webp'
                else:
                    ext = '.png'  # default

            filename = f"external-{url_hash}{ext}"
            filepath = IMAGES_DIR / filename

            with open(filepath, 'wb') as f:
                f.write(response.content)

            print(f"  ✓ Downloaded: {filename} ({len(response.content)} bytes)")
            return filename
        else:
            print(f"  ✗ Failed to download {url}: HTTP {response.status_code}")
            return None
    except Exception as e:
        print(f"  ✗ Error downloading {url}: {e}")
        return None


def process_markdown_file(md_file):
    """Process a markdown file to download external images and update references."""
    print(f"\nProcessing: {md_file.name}")

    with open(md_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find all image markdown patterns: ![alt](url)
    pattern = r'!\[(.*?)\]\((https?://[^\)]+)\)'
    matches = list(re.finditer(pattern, content))

    if not matches:
        print("  No external images found")
        return False

    print(f"  Found {len(matches)} external images")

    modified = False
    for match in matches:
        alt_text = match.group(1)
        url = match.group(2)

        # Skip if already pointing to local images
        if url.startswith('images/'):
            continue

        print(f"    Downloading: {url}")
        filename = download_image(url)

        if filename:
            # Replace the URL with local path
            old_markdown = match.group(0)
            new_markdown = f"![{alt_text}](images/{filename})"
            content = content.replace(old_markdown, new_markdown)
            modified = True

    if modified:
        with open(md_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  ✓ Updated: {md_file.name}")
        return True

    return False


def main():
    print("=" * 60)
    print("External Images Downloader for Documentation")
    print("=" * 60)

    # Get all markdown files
    md_files = list(DOCS_DIR.glob("*.md"))
    print(f"\nFound {len(md_files)} markdown files")

    processed_count = 0
    for md_file in md_files:
        if process_markdown_file(md_file):
            processed_count += 1

    print("\n" + "=" * 60)
    print(f"✓ Processed {processed_count} files with external images")
    print(f"✓ Images saved in: {IMAGES_DIR.absolute()}")
    print("=" * 60)


if __name__ == "__main__":
    main()
