# IITJ MTP Template Generator

Generate professional LaTeX academic reports with ease

[Simple guide (beginners)](beginners_guide){: .btn .btn-primary .fs-5 .mb-4 .mb-md-0 .mr-2 }
[Quick Start](quickstart){: .btn .fs-5 .mb-4 .mb-md-0 .mr-2 }
[View on GitHub](https://github.com/satishjhanwer/IITJ-MTP-Template-Generator){: .btn .fs-5 .mb-4 .mb-md-0 }

---

## What is IITJ MTP Template Generator?

A Python-based tool that builds a **structured LaTeX project** from simple configuration files: your title, name, supervisor, and other settings, plus **section shells** you must fill in (abstract, chapters, acknowledgments, and more). It does **not** write your report content for you. Perfect for students and researchers who need to create:

- 📄 **Proposal Reports** (MTP1/Research Proposals)
- 📚 **Major Project Reports** (Full Thesis/Dissertation)
- 🎤 **Presentation Slides** (Beamer)

## Key Features

✅ **Easy to Use** - Interactive CLI or YAML configuration  
✅ **Professional Templates** - IEEE-style formatting  
✅ **Fully Customizable** - Modify templates to match your needs  
✅ **Well Documented** - Comprehensive guides and examples  
✅ **Zero Dependencies Option** - Works without pip  

## Quick Example

```bash
# Install dependencies
pip install -r scripts/requirements.txt

# Generate a proposal report
python scripts/generate.py --config examples/sample-proposal/config.yaml

# Compile to PDF
cd output/your-project
pdflatex proposal.tex
```

## What You Get

### Proposal Report Template

- Title page with university branding
- Abstract and table of contents
- Introduction with objectives
- Literature review with comparison tables
- Methodology with architecture diagrams
- Project timeline
- IEEE-style bibliography

### Major Project Report Template

- Complete front matter (declaration, certificate, acknowledgments)
- 7 comprehensive chapters
- Professional formatting
- Automatic table of contents, figures, and tables
- IEEE-style citations

### Presentation Slides (Beamer)

- Title, introduction, methodology, results, and conclusion sections
- Configurable theme and aspect ratio via YAML
- Optional content extraction from an existing LaTeX report

## Getting Started

1. [Simple guide for beginners](beginners_guide) - Plain language: what you install, what you get, template PDF vs final PDF
2. [Quick Start Guide](quickstart) - Get up and running in 5 minutes
3. [CI/CD Auto-Compilation](ci-cd) - Automatic PDF generation with GitHub Actions
4. [Input Schema](input-schema) - Learn about configuration options
5. [Customization Guide](customization) - Personalize your templates
6. [FAQ](faq) - Common questions and troubleshooting

## Example Output

The generator creates a complete LaTeX project with:

- All necessary `.tex` files
- Bibliography with example entries
- `[TODO]` / `% TODO` markers where **you** add real content
- Compilation instructions
- Template-specific README

**Note:** Building a PDF immediately after generation shows **formatting and layout**; the text is still placeholder until you edit every section. That early PDF is a **preview**, not your final submission.

## Requirements

- Python 3.9+
- LaTeX distribution (TeX Live, MiKTeX, or MacTeX)
- Optional: Jinja2 and PyYAML (or use zero-dependency version)

## License

MIT License - Free to use for academic and commercial purposes

---

**Ready to create your academic report?** [Simple guide →](beginners_guide) &nbsp;·&nbsp; [Quick Start →](quickstart)
