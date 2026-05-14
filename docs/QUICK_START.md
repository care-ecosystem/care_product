# Quick Start Guide

Get started with the Care Platform documentation site in minutes.

## 🌐 Access the Documentation

**Live URL**: https://care-ecosystem.github.io/care_product/

Simply visit the URL above to access the full documentation site with all 47 guides.

---

## 📖 Find What You Need

### Using Search
1. Click the search icon (🔍) in the top navigation bar
2. Type your query (e.g., "register patient", "prescribe medication")
3. Results appear instantly with highlighting

### Browse by Category
Navigate using the tabs at the top:
- **Facility Management** - Setup & configuration
- **Appointments** - Scheduling system
- **Patient Registration** - Onboarding
- **Encounters** - Episode management
- **Clinical** - Documentation & treatment
- **Laboratory** - Diagnostics
- **Billing** - Finance
- **Pharmacy** - Medication
- **Miscellaneous** - Other guides

---

## 🎨 Customize Your View

### Dark Mode
- Click the theme toggle (☀️/🌙) in the top-right corner
- Your preference is saved automatically

### Navigation
- Use the sidebar to browse within a section
- Click section headings to expand/collapse
- Use breadcrumbs to navigate back

---

## ✏️ Edit Documentation

Every page has an "Edit on GitHub" button:
1. Click the pencil icon on any page
2. Make your changes in GitHub
3. Submit the changes
4. Site updates automatically in 2-3 minutes

---

## 🔄 Keep Documentation Updated

### From Confluence Wiki

```bash
python3 scripts/fetch_wiki_docs.py
python3 scripts/download_external_images.py
git add docs/ && git commit -m "Update from wiki" && git push
```

### Direct Edits

```bash
# Edit markdown files in docs/ folder
git add docs/ && git commit -m "Update documentation" && git push
```

---

## 💡 Tips & Tricks

- **Keyboard shortcuts**: Press `/` to focus search
- **Print**: Use browser print for offline copies
- **Share**: Copy page URL to share specific guides
- **Mobile**: Site works perfectly on mobile devices
- **Offline**: Download PDF versions (coming soon)

---

## 🆘 Need Help?

- **Can't find something?** Use the search function
- **Broken link?** File an issue on GitHub
- **Have suggestions?** Contact the documentation team
- **Technical issues?** Check GitHub Actions logs

---

**Quick Links**:
- [Home](index.md) | [Overview](overview.md) | [All Categories](#)
