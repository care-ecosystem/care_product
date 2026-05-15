#!/usr/bin/env python3
"""
Fetch Google Docs and convert to clean Markdown
Uses BeautifulSoup for proper HTML parsing
"""

import os
import re
import requests
from pathlib import Path
from bs4 import BeautifulSoup
import html2text

def fetch_google_doc(doc_id):
    """Fetch Google Doc as HTML"""
    url = f"https://docs.google.com/document/d/{doc_id}/export?format=html"

    print(f"Fetching document from Google Docs...")
    response = requests.get(url, allow_redirects=True)

    if response.status_code == 200:
        print("✓ Document fetched successfully")
        return response.text
    else:
        print(f"✗ Failed to fetch document: {response.status_code}")
        return None

def clean_html(html_content):
    """Extract only body content, remove styles and scripts"""
    soup = BeautifulSoup(html_content, 'html.parser')

    # Remove style and script tags
    for tag in soup(['style', 'script', 'head']):
        tag.decompose()

    # Get body content
    body = soup.find('body')
    if body:
        return str(body)
    return str(soup)

def convert_to_markdown(html_content):
    """Convert HTML to Markdown using html2text"""
    h = html2text.HTML2Text()
    h.ignore_links = False
    h.ignore_images = False
    h.ignore_emphasis = False
    h.body_width = 0  # Don't wrap lines
    h.single_line_break = False

    markdown = h.handle(html_content)

    # Clean up
    # Remove excessive newlines
    markdown = re.sub(r'\n{3,}', '\n\n', markdown)

    # Fix heading spacing
    markdown = re.sub(r'(#{1,6} .+)\n([^\n#])', r'\1\n\n\2', markdown)

    # Clean up list formatting
    markdown = re.sub(r'\n\n(\s*[\*\-\+])', r'\n\1', markdown)

    return markdown.strip()

def download_images(html_content, output_dir):
    """Download images from the HTML content"""
    soup = BeautifulSoup(html_content, 'html.parser')
    images = soup.find_all('img')

    images_dir = output_dir / "images"
    images_dir.mkdir(exist_ok=True)

    image_mapping = {}
    for idx, img in enumerate(images, 1):
        src = img.get('src')
        if not src or src.startswith('data:'):
            continue

        try:
            print(f"  Downloading image {idx}/{len(images)}...")
            response = requests.get(src, timeout=30)
            if response.status_code == 200:
                # Get file extension from content-type
                content_type = response.headers.get('content-type', '')
                ext = '.png'
                if 'jpeg' in content_type or 'jpg' in content_type:
                    ext = '.jpg'
                elif 'png' in content_type:
                    ext = '.png'
                elif 'gif' in content_type:
                    ext = '.gif'

                filename = f"pharmacy-image-{idx}{ext}"
                filepath = images_dir / filename

                with open(filepath, 'wb') as f:
                    f.write(response.content)

                image_mapping[src] = f"images/{filename}"
                print(f"    ✓ Saved: {filename}")
        except Exception as e:
            print(f"    ✗ Failed to download image: {e}")

    return image_mapping

def replace_image_urls(markdown, image_mapping):
    """Replace external image URLs with local paths"""
    for old_url, new_path in image_mapping.items():
        markdown = markdown.replace(old_url, new_path)
    return markdown

def main():
    # Google Doc ID
    doc_id = "1RxwuTflKKsXWnc9Xyi7o81LkI8jmFmjKPYBMWOeqm7E"

    # Output directory
    output_dir = Path("/Users/jagankumar/Office/Work/repo/Care/care_product/docs/pharmacy")
    output_dir.mkdir(parents=True, exist_ok=True)

    # Fetch the document
    html_content = fetch_google_doc(doc_id)

    if not html_content:
        print("Failed to fetch document")
        return

    print("\nProcessing document...")

    # Clean HTML
    clean_content = clean_html(html_content)

    # Download images
    print("\nDownloading images...")
    image_mapping = download_images(html_content, output_dir)
    print(f"✓ Downloaded {len(image_mapping)} images")

    # Convert to markdown
    print("\nConverting to markdown...")
    markdown_content = convert_to_markdown(clean_content)

    # Replace image URLs
    if image_mapping:
        markdown_content = replace_image_urls(markdown_content, image_mapping)

    # Save to file
    output_file = output_dir / "pharmacy-setup-guide.md"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(markdown_content)

    print(f"\n✓ Document saved to: {output_file}")
    print(f"  File size: {len(markdown_content)} characters")
    print(f"  Lines: {len(markdown_content.split(chr(10)))}")

    # Show preview
    lines = markdown_content.split('\n')
    print(f"\nPreview (first 30 lines):")
    print("=" * 60)
    for line in lines[:30]:
        print(line)
    print("=" * 60)

if __name__ == "__main__":
    main()
