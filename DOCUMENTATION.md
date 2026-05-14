# Care Platform Documentation Site

## 🎉 Documentation Site is Live!

Your Care Platform documentation is now available online at:

**https://care-ecosystem.github.io/care_product/**

---

## 📚 What's Been Set Up

### Documentation Site Features

✅ **Beautiful Material Design Theme**
- Modern, professional appearance
- Light and dark mode toggle
- Fully responsive (mobile, tablet, desktop)
- Fast search functionality

✅ **Organized Structure**
- 47 SOPs & guides organized into 9 categories
- Intuitive navigation with tabs and sections
- Index pages for each category
- Breadcrumb navigation

✅ **Rich Content**
- 188 images (11MB) locally hosted
- Loom video tutorials linked
- Mermaid diagrams for workflows
- Interactive cards and grids

✅ **Developer Features**
- "Edit on GitHub" links on every page
- Automatic deployment via GitHub Actions
- Version control integration
- Social media links

---

## 📁 Repository Structure

```
care_product/
├── .github/
│   └── workflows/
│       └── docs.yml (Auto-deployment workflow)
├── docs/
│   ├── index.md (Home page)
│   ├── overview.md (Original wiki overview)
│   ├── facility-management/ (9 guides)
│   ├── appointments/ (3 guides)
│   ├── patient-registration/ (5 guides)
│   ├── encounters/ (11 guides)
│   ├── clinical/ (9 guides)
│   ├── laboratory/ (2 guides)
│   ├── billing/ (2 guides)
│   ├── pharmacy/ (1 guide)
│   ├── miscellaneous/ (4 guides)
│   ├── images/ (188 images, 11MB)
│   └── stylesheets/
│       └── extra.css (Custom styling)
├── scripts/
│   ├── README.md
│   ├── fetch_wiki_docs.py
│   ├── download_external_images.py
│   └── fix_image_links.py
├── mkdocs.yml (Site configuration)
└── requirements.txt (Python dependencies)
```

---

## 🚀 How It Works

### Automatic Deployment

Every time you push changes to the `main` branch that affect:
- `docs/**` (any documentation file)
- `mkdocs.yml` (configuration)
- `.github/workflows/docs.yml` (workflow)

GitHub Actions will automatically:
1. Build the documentation site
2. Deploy to GitHub Pages
3. Make it live at the URL above

**Typical deployment time: 2-3 minutes**

---

## 🔄 Updating Documentation

### Method 1: Update from Confluence Wiki

```bash
# Fetch latest content from Confluence
python3 scripts/fetch_wiki_docs.py

# Download external images
python3 scripts/download_external_images.py

# Fix image links (if needed)
python3 scripts/fix_image_links.py

# Commit and push
git add docs/
git commit -m "Update documentation from Confluence"
git push origin main

# GitHub Actions will auto-deploy in ~2 minutes
```

### Method 2: Edit Directly in GitHub

1. Navigate to any page on the documentation site
2. Click "Edit on GitHub" (pencil icon)
3. Make your changes in the GitHub web editor
4. Commit the changes
5. GitHub Actions auto-deploys the update

### Method 3: Local Development

```bash
# Serve documentation locally with live reload
mkdocs serve

# Open browser to http://127.0.0.1:8000
# Edit files and see changes instantly

# When ready, commit and push
git add .
git commit -m "Update documentation"
git push origin main
```

---

## 🎨 Customization

### Colors & Branding

Edit `mkdocs.yml` to customize:
- Primary color (currently: teal)
- Accent color
- Logo
- Favicon
- Social links

### Custom Styles

Edit `docs/stylesheets/extra.css` to:
- Adjust spacing and layout
- Customize card designs
- Modify typography
- Add custom components

### Navigation

Edit the `nav:` section in `mkdocs.yml` to:
- Reorder pages
- Add new sections
- Remove pages
- Create nested structures

---

## 🛠️ Local Development Setup

### Prerequisites

```bash
# Python 3.8 or higher
python3 --version

# Install dependencies
pip install -r requirements.txt
```

### Commands

```bash
# Serve locally (live reload)
mkdocs serve

# Build static site
mkdocs build

# Deploy to GitHub Pages manually
mkdocs gh-deploy

# Clean build directory
mkdocs build --clean

# Strict mode (fail on warnings)
mkdocs build --strict
```

---

## 📊 Documentation Statistics

| Metric | Count |
|--------|-------|
| **Total Documents** | 47 SOPs & Guides |
| **Categories** | 9 functional areas |
| **Images** | 188 files (11MB) |
| **Videos** | Linked via Loom |
| **Lines of Documentation** | ~15,000+ |

### Category Breakdown

- Facility Management: 9 guides
- Patient Encounters: 11 guides
- Clinical Documentation: 9 guides
- Patient Registration: 5 guides
- Miscellaneous: 4 guides
- Appointments: 3 guides
- Laboratory: 2 guides
- Billing: 2 guides
- Pharmacy: 1 guide

---

## 🔗 Important Links

- **Live Site**: https://care-ecosystem.github.io/care_product/
- **Repository**: https://github.com/care-ecosystem/care_product
- **GitHub Actions**: https://github.com/care-ecosystem/care_product/actions
- **MkDocs**: https://www.mkdocs.org/
- **Material Theme**: https://squidfunk.github.io/mkdocs-material/

---

## 🆘 Troubleshooting

### Build Failures

```bash
# Check for errors
mkdocs build --strict

# Common issues:
# - Broken internal links
# - Missing images
# - Invalid markdown syntax
```

### Deployment Issues

1. Check GitHub Actions logs: https://github.com/care-ecosystem/care_product/actions
2. Verify GitHub Pages is enabled in repository settings
3. Ensure `gh-pages` branch exists
4. Check that GitHub Actions has write permissions

### Image Not Showing

- Verify image exists in `docs/images/`
- Check image path uses `../images/` from subdirectories
- Run `python3 scripts/fix_image_links.py`

---

## 📝 Best Practices

### Writing Documentation

1. **Use clear headings** - H1 for title, H2 for sections, H3 for subsections
2. **Add screenshots** - Visual guides are easier to follow
3. **Include video tutorials** - Link to Loom or YouTube
4. **Use admonitions** - Highlight tips, warnings, and notes
5. **Keep it concise** - Step-by-step instructions work best

### Organizing Content

1. **One topic per page** - Don't create mega-documents
2. **Logical categorization** - Group related guides together
3. **Consistent naming** - Use kebab-case for filenames
4. **Index pages** - Provide overview of each section

### Maintenance

1. **Regular updates** - Keep documentation in sync with features
2. **Review accuracy** - Verify steps match current UI
3. **Update screenshots** - Replace outdated images
4. **Version control** - Use meaningful commit messages

---

## 🎯 Next Steps

### Enhancements to Consider

- [ ] Add search keywords/tags for better discoverability
- [ ] Create video walkthrough of common workflows
- [ ] Add FAQ section
- [ ] Implement versioning for different Care releases
- [ ] Add API documentation (if applicable)
- [ ] Create printable PDF versions
- [ ] Add multi-language support
- [ ] Integrate feedback mechanism

### Custom Domain (Optional)

To use a custom domain (e.g., docs.care.com):

1. Add `CNAME` file in `docs/` with your domain
2. Configure DNS with your provider
3. Update `site_url` in `mkdocs.yml`
4. Commit and push changes

---

## 📞 Support

For documentation site issues:
- File an issue: https://github.com/care-ecosystem/care_product/issues
- Check GitHub Actions logs for deployment errors
- Review MkDocs documentation: https://www.mkdocs.org/

For Care platform support:
- Visit: Open Healthcare Network

---

**Last Updated**: 2024-05-14
**Site Version**: 1.0.0
**MkDocs Version**: 1.5+
**Material Theme Version**: 9.5+
