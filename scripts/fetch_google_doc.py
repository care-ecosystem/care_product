#!/usr/bin/env python3
"""
Fetch Google Docs and convert to Markdown
"""

import os
import re
import requests
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urljoin

class GoogleDocToMarkdown(HTMLParser):
    def __init__(self):
        super().__init__()
        self.markdown = []
        self.current_tag = None
        self.list_level = 0
        self.in_bold = False
        self.in_italic = False
        self.in_list = False
        self.list_item_buffer = []

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)

        if tag in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
            level = int(tag[1])
            self.current_tag = '#' * level + ' '
        elif tag == 'p':
            self.current_tag = 'p'
        elif tag in ['ul', 'ol']:
            self.in_list = True
            self.list_level += 1
        elif tag == 'li':
            indent = '  ' * (self.list_level - 1)
            self.list_item_buffer = [f"{indent}- "]
        elif tag == 'strong' or tag == 'b':
            self.in_bold = True
            self.list_item_buffer.append('**') if self.in_list else self.markdown.append('**')
        elif tag == 'em' or tag == 'i':
            self.in_italic = True
            self.list_item_buffer.append('*') if self.in_list else self.markdown.append('*')
        elif tag == 'a':
            href = attrs_dict.get('href', '')
            self.current_tag = f'[LINK:{href}]'
        elif tag == 'img':
            src = attrs_dict.get('src', '')
            alt = attrs_dict.get('alt', 'image')
            if src:
                self.markdown.append(f'\n![{alt}]({src})\n')
        elif tag == 'br':
            self.markdown.append('\n')
        elif tag == 'code':
            self.markdown.append('`')
        elif tag == 'pre':
            self.markdown.append('\n```\n')

    def handle_endtag(self, tag):
        if tag in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
            self.markdown.append('\n\n')
            self.current_tag = None
        elif tag == 'p':
            self.markdown.append('\n\n')
            self.current_tag = None
        elif tag in ['ul', 'ol']:
            self.list_level -= 1
            if self.list_level == 0:
                self.in_list = False
                self.markdown.append('\n')
        elif tag == 'li':
            self.markdown.extend(self.list_item_buffer)
            self.markdown.append('\n')
            self.list_item_buffer = []
        elif tag == 'strong' or tag == 'b':
            self.in_bold = False
            self.list_item_buffer.append('**') if self.in_list else self.markdown.append('**')
        elif tag == 'em' or tag == 'i':
            self.in_italic = False
            self.list_item_buffer.append('*') if self.in_list else self.markdown.append('*')
        elif tag == 'a':
            self.current_tag = None
        elif tag == 'code':
            self.markdown.append('`')
        elif tag == 'pre':
            self.markdown.append('\n```\n\n')

    def handle_data(self, data):
        data = data.strip()
        if not data:
            return

        if self.current_tag and self.current_tag.startswith('#'):
            self.markdown.append(self.current_tag + data)
        elif self.current_tag and self.current_tag.startswith('[LINK:'):
            href = self.current_tag[6:-1]
            self.markdown.append(f'[{data}]({href})')
        elif self.in_list:
            self.list_item_buffer.append(data)
        else:
            self.markdown.append(data)

    def get_markdown(self):
        result = ''.join(self.markdown)
        # Clean up extra whitespace
        result = re.sub(r'\n{3,}', '\n\n', result)
        return result.strip()

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

def convert_html_to_markdown(html_content):
    """Convert HTML to Markdown"""
    parser = GoogleDocToMarkdown()
    parser.feed(html_content)
    markdown = parser.get_markdown()

    # Additional cleanup
    # Fix multiple spaces
    markdown = re.sub(r' {2,}', ' ', markdown)

    # Ensure proper spacing after headings
    markdown = re.sub(r'(#{1,6} .+)\n([^\n])', r'\1\n\n\2', markdown)

    # Clean up list formatting
    markdown = re.sub(r'\n\n-', r'\n-', markdown)

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

    # Convert to markdown
    print("Converting to markdown...")
    markdown_content = convert_html_to_markdown(html_content)

    # Save to file
    output_file = output_dir / "pharmacy-setup-guide.md"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(markdown_content)

    print(f"\n✓ Document saved to: {output_file}")
    print(f"  File size: {len(markdown_content)} characters")

    # Show preview
    lines = markdown_content.split('\n')
    print(f"\nPreview (first 20 lines):")
    print("-" * 60)
    for line in lines[:20]:
        print(line)
    print("-" * 60)

if __name__ == "__main__":
    main()
