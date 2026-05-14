# Documentation Scripts

This folder contains scripts for managing the Care platform documentation.

## Scripts

### `fetch_wiki_docs.py`

Fetches all pages from the Atlassian Confluence wiki space and converts them to markdown format.

**Usage:**
```bash
# Run from the repository root
python3 scripts/fetch_wiki_docs.py
```

**What it does:**
- Connects to Atlassian Confluence API
- Fetches all pages from the configured wiki space
- Converts Confluence HTML storage format to Markdown
- Downloads attached images and videos
- Saves markdown files to `docs/` directory
- Organizes media files in `docs/images/` and `docs/videos/`

**Configuration:**
Edit the script to update these variables:
- `ATLASSIAN_DOMAIN`: Your Atlassian domain
- `SPACE_KEY`: The wiki space key
- `API_TOKEN`: Your Atlassian API token

---

### `download_external_images.py`

Downloads external images (like Loom video thumbnails) referenced in the documentation and updates markdown files to use local copies.

**Usage:**
```bash
# Run from the repository root
python3 scripts/download_external_images.py
```

**What it does:**
- Scans all markdown files in `docs/` directory
- Finds external image references (HTTP/HTTPS URLs)
- Downloads images to `docs/images/`
- Updates markdown files to reference local copies
- Generates consistent filenames using URL hashes

---

## Workflow for Updating Documentation

1. **Update source pages** in the Atlassian Confluence wiki

2. **Fetch updated content:**
   ```bash
   python3 scripts/fetch_wiki_docs.py
   ```

3. **Download external images:**
   ```bash
   python3 scripts/download_external_images.py
   ```

4. **Review changes:**
   ```bash
   git status
   git diff
   ```

5. **Commit and push:**
   ```bash
   git add docs/
   git commit -m "Update documentation from Confluence wiki"
   git push
   ```

---

## Requirements

```bash
pip install requests
```

Both scripts require the `requests` library for HTTP operations.

---

## Notes

- Scripts must be run from the repository root directory
- Both scripts automatically create necessary directories
- API token is stored in the script - consider using environment variables for security
- External images are cached locally to reduce dependencies on external services
- Loom video thumbnails are downloaded but video links remain as external URLs
