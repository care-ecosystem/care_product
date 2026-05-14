#!/usr/bin/env python3
"""
Script to fetch Atlassian Confluence wiki pages and convert them to markdown.
Downloads all images and videos referenced in the pages.
"""

import json
import os
import re
import requests
from pathlib import Path
from urllib.parse import urlparse, unquote
import html

# Configuration
ATLASSIAN_DOMAIN = "openhealthcarenetwork.atlassian.net"
SPACE_KEY = "~7120200a236b5c77374eedad7da15fad96ac25"
API_TOKEN = "ATATT3xFfGF01_hSzv3Qbkk-2c1UzxQH3tGkc5PBXpyFBYtVGgBsHnKv7GgjSF7LDSZQd1Hh8g5Sz4RD8YJXSKxInvlZ7zDVoPShT5DocH_n-FHxt4VShlPX2AZpjm6XAnHazY7DwlwtZwP-1yPDk44Cw9DuYw7F5ZTOdiGZyYRxP0gzGDriJBo=7C66E51A"
BASE_URL = f"https://{ATLASSIAN_DOMAIN}/wiki"
API_URL = f"{BASE_URL}/rest/api"

HEADERS = {
    "Authorization": f"Bearer {API_TOKEN}",
    "Accept": "application/json"
}

# Get the project root directory (parent of scripts/)
PROJECT_ROOT = Path(__file__).parent.parent
DOCS_DIR = PROJECT_ROOT / "docs"
IMAGES_DIR = DOCS_DIR / "images"
VIDEOS_DIR = DOCS_DIR / "videos"

# Create directories
DOCS_DIR.mkdir(exist_ok=True)
IMAGES_DIR.mkdir(exist_ok=True)
VIDEOS_DIR.mkdir(exist_ok=True)


def sanitize_filename(name):
    """Convert a page title to a valid filename."""
    # Remove or replace invalid characters
    name = re.sub(r'[<>:"/\\|?*]', '', name)
    # Replace spaces and special chars with hyphens
    name = re.sub(r'[\s]+', '-', name)
    # Remove multiple consecutive hyphens
    name = re.sub(r'-+', '-', name)
    # Remove leading/trailing hyphens
    name = name.strip('-')
    return name.lower()


def download_attachment(page_id, attachment_id, filename, file_type='image'):
    """Download an attachment (image or video) from a page."""
    try:
        # Get attachment download URL
        attach_url = f"{API_URL}/content/{page_id}/child/attachment/{attachment_id}/download"
        response = requests.get(attach_url, headers=HEADERS, stream=True)

        if response.status_code == 200:
            target_dir = IMAGES_DIR if file_type == 'image' else VIDEOS_DIR
            filepath = target_dir / filename

            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)

            print(f"  ✓ Downloaded {file_type}: {filename}")
            return str(filepath.relative_to(DOCS_DIR))
        else:
            print(f"  ✗ Failed to download {filename}: {response.status_code}")
            return None
    except Exception as e:
        print(f"  ✗ Error downloading {filename}: {e}")
        return None


def get_attachments(page_id):
    """Get all attachments for a page."""
    try:
        url = f"{API_URL}/content/{page_id}/child/attachment?limit=100"
        response = requests.get(url, headers=HEADERS)

        if response.status_code == 200:
            data = response.json()
            return data.get('results', [])
        return []
    except Exception as e:
        print(f"  ✗ Error fetching attachments: {e}")
        return []


def html_to_markdown(html_content, page_id):
    """Convert Confluence HTML storage format to Markdown."""
    # This is a simplified converter - handles common Confluence elements
    md = html_content

    # Get attachments to map filenames
    attachments = get_attachments(page_id)
    attachment_map = {att['title']: att for att in attachments}

    # Handle images
    # Confluence format: <ac:image><ri:attachment ri:filename="image.png" /></ac:image>
    img_pattern = r'<ac:image[^>]*>.*?<ri:attachment ri:filename="([^"]+)"[^>]*/>.*?</ac:image>'

    def replace_image(match):
        filename = match.group(1)
        if filename in attachment_map:
            att = attachment_map[filename]
            # Download the image
            local_path = download_attachment(page_id, att['id'], filename, 'image')
            if local_path:
                return f"![{filename}]({local_path})"
        return f"![{filename}](images/{filename})"

    md = re.sub(img_pattern, replace_image, md, flags=re.DOTALL)

    # Handle embedded images with ac:url
    img_url_pattern = r'<ac:image[^>]*>.*?<ri:url ri:value="([^"]+)"[^>]*/>.*?</ac:image>'
    md = re.sub(img_url_pattern, r'![\1](\1)', md, flags=re.DOTALL)

    # Handle videos/media
    media_pattern = r'<ac:structured-macro ac:name="multimedia"[^>]*>.*?<ri:attachment ri:filename="([^"]+)"[^>]*/>.*?</ac:structured-macro>'

    def replace_media(match):
        filename = match.group(1)
        if filename in attachment_map:
            att = attachment_map[filename]
            # Download the video
            local_path = download_attachment(page_id, att['id'], filename, 'video')
            if local_path:
                return f"\n[Video: {filename}]({local_path})\n"
        return f"\n[Video: {filename}](videos/{filename})\n"

    md = re.sub(media_pattern, replace_media, md, flags=re.DOTALL)

    # Convert headings
    md = re.sub(r'<h1[^>]*>(.*?)</h1>', r'# \1', md, flags=re.DOTALL)
    md = re.sub(r'<h2[^>]*>(.*?)</h2>', r'## \1', md, flags=re.DOTALL)
    md = re.sub(r'<h3[^>]*>(.*?)</h3>', r'### \1', md, flags=re.DOTALL)
    md = re.sub(r'<h4[^>]*>(.*?)</h4>', r'#### \1', md, flags=re.DOTALL)
    md = re.sub(r'<h5[^>]*>(.*?)</h5>', r'##### \1', md, flags=re.DOTALL)
    md = re.sub(r'<h6[^>]*>(.*?)</h6>', r'###### \1', md, flags=re.DOTALL)

    # Convert paragraphs
    md = re.sub(r'<p[^>]*>(.*?)</p>', r'\1\n\n', md, flags=re.DOTALL)

    # Convert bold and italic
    md = re.sub(r'<strong>(.*?)</strong>', r'**\1**', md, flags=re.DOTALL)
    md = re.sub(r'<em>(.*?)</em>', r'*\1*', md, flags=re.DOTALL)

    # Convert lists
    md = re.sub(r'<ul[^>]*>(.*?)</ul>', lambda m: '\n' + m.group(1) + '\n', md, flags=re.DOTALL)
    md = re.sub(r'<ol[^>]*>(.*?)</ol>', lambda m: '\n' + m.group(1) + '\n', md, flags=re.DOTALL)
    md = re.sub(r'<li[^>]*>(.*?)</li>', r'- \1\n', md, flags=re.DOTALL)

    # Convert code blocks
    md = re.sub(r'<ac:structured-macro ac:name="code"[^>]*>.*?<ac:plain-text-body><!\[CDATA\[(.*?)\]\]></ac:plain-text-body>.*?</ac:structured-macro>', r'```\n\1\n```', md, flags=re.DOTALL)
    md = re.sub(r'<code>(.*?)</code>', r'`\1`', md, flags=re.DOTALL)

    # Convert links
    md = re.sub(r'<a href="([^"]*)"[^>]*>(.*?)</a>', r'[\2](\1)', md, flags=re.DOTALL)

    # Convert horizontal rules
    md = re.sub(r'<hr[^>]*/?>', r'\n---\n', md)

    # Convert tables (basic support)
    md = re.sub(r'<table[^>]*>', r'\n', md)
    md = re.sub(r'</table>', r'\n', md)
    md = re.sub(r'<tbody[^>]*>', r'', md)
    md = re.sub(r'</tbody>', r'', md)
    md = re.sub(r'<tr[^>]*>', r'', md)
    md = re.sub(r'</tr>', r'\n', md)
    md = re.sub(r'<th[^>]*>(.*?)</th>', r'| **\1** ', md, flags=re.DOTALL)
    md = re.sub(r'<td[^>]*>(.*?)</td>', r'| \1 ', md, flags=re.DOTALL)

    # Convert line breaks
    md = re.sub(r'<br\s*/?>', r'\n', md)

    # Remove remaining HTML tags
    md = re.sub(r'<[^>]+>', '', md)

    # Decode HTML entities
    md = html.unescape(md)

    # Clean up excessive whitespace
    md = re.sub(r'\n{3,}', '\n\n', md)
    md = md.strip()

    return md


def fetch_page_content(page_id):
    """Fetch page content with body storage format."""
    try:
        url = f"{API_URL}/content/{page_id}?expand=body.storage,version"
        response = requests.get(url, headers=HEADERS)

        if response.status_code == 200:
            return response.json()
        else:
            print(f"  ✗ Error fetching page {page_id}: {response.status_code}")
            return None
    except Exception as e:
        print(f"  ✗ Error fetching page {page_id}: {e}")
        return None


def fetch_all_pages():
    """Fetch all pages from the wiki space."""
    try:
        url = f"{API_URL}/content?spaceKey={SPACE_KEY}&limit=100"
        response = requests.get(url, headers=HEADERS)

        if response.status_code == 200:
            data = response.json()
            return data.get('results', [])
        return []
    except Exception as e:
        print(f"✗ Error fetching pages: {e}")
        return []


def process_page(page_info):
    """Process a single page: fetch content, convert to markdown, save."""
    page_id = page_info['id']
    title = page_info['title']

    print(f"\nProcessing: {title}")

    # Fetch full page content
    page_data = fetch_page_content(page_id)
    if not page_data:
        return False

    # Get the HTML content
    html_content = page_data['body']['storage']['value']

    # Convert to markdown
    markdown_content = html_to_markdown(html_content, page_id)

    # Create markdown file
    filename = sanitize_filename(title)
    if not filename:
        filename = f"page-{page_id}"

    filepath = DOCS_DIR / f"{filename}.md"

    # Add frontmatter
    frontmatter = f"""---
title: {title}
page_id: {page_id}
source: {BASE_URL}/spaces/{SPACE_KEY}/pages/{page_id}
---

"""

    full_content = frontmatter + markdown_content

    # Write to file
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(full_content)

    print(f"  ✓ Saved: {filepath.name}")
    return True


def main():
    print("=" * 60)
    print("Atlassian Confluence Wiki Documentation Fetcher")
    print("=" * 60)

    # Fetch all pages
    print("\nFetching page list...")
    pages = fetch_all_pages()

    if not pages:
        print("✗ No pages found or error occurred")
        return

    print(f"✓ Found {len(pages)} pages")

    # Process each page
    success_count = 0
    for page in pages:
        if process_page(page):
            success_count += 1

    print("\n" + "=" * 60)
    print(f"✓ Successfully processed {success_count}/{len(pages)} pages")
    print(f"✓ Documentation saved in: {DOCS_DIR.absolute()}")
    print(f"✓ Images saved in: {IMAGES_DIR.absolute()}")
    print(f"✓ Videos saved in: {VIDEOS_DIR.absolute()}")
    print("=" * 60)


if __name__ == "__main__":
    main()
