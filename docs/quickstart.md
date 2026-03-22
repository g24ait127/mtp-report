# Quick Start Guide

Get started with the IITJ MTP Template Generator in 5 minutes!

**New to terminals or Python?** Start with the [Simple guide for beginners](beginners_guide).

## What you get (important)

The generator creates a **LaTeX project** under `output/` with your **metadata** and **section files** (abstract, acknowledgments, declaration, certificate, chapters, etc.). Most **paragraphs are placeholders**—search for `[TODO]` and `% TODO`. Compiling to PDF **before** you replace that text produces a **layout preview**, not your finished submission. See [examples/README](../examples/README.md) for how sample configs relate to this.

## Prerequisites

Before you begin, make sure you have:

1. **Python 3.9+** installed

   ```bash
   python --version  # Should show 3.9 or higher
   ```

2. **LaTeX distribution** installed
   - **Windows**: [MiKTeX](https://miktex.org/download)
   - **macOS**: [MacTeX](https://www.tug.org/mactex/)
   - **Linux**: TeX Live

     ```bash
     sudo apt-get install texlive-full  # Ubuntu/Debian
     ```

## Installation

### Step 1: Get the Code

```bash
git clone https://github.com/satishjhanwer/IITJ-MTP-Template-Generator.git
cd IITJ-MTP-Template-Generator
```

### Step 2: Install Dependencies

```bash
pip install -r scripts/requirements.txt
```

This installs:

- `jinja2` - Template rendering
- `pyyaml` - YAML configuration parsing

## Generate Your First Report

### Option 1: Interactive Mode (Recommended for First-Time Users)

```bash
python scripts/generate.py
```

The generator will ask you questions like:

- Report type (proposal, major project, or presentation)
- Project title
- Your name and roll number
- Supervisor details
- University and department
- Submission date

Answer each question and the generator will create your report!

### Option 2: Using a Config File (Faster for Repeated Use)

1. Create a `config.yaml` file (or use an example):

   ```bash
   cp examples/sample-proposal/config.yaml my-config.yaml
   ```

2. Edit `my-config.yaml` with your details

3. Generate the report:

   ```bash
   python scripts/generate.py --config my-config.yaml
   ```

## Edit Your Report

After generation, you'll find your report in the `output/` directory:

```bash
cd output/your-project-name
```

Edit the `.tex` files to add your content:

- Search for `[TODO]` markers
- Replace placeholders with your actual content
- Add references to the `.bib` file

## Compile to PDF

### Method 1: Using pdflatex (Recommended)

```bash
# For proposal reports
pdflatex proposal.tex
bibtex proposal
pdflatex proposal.tex
pdflatex proposal.tex

# For major project reports
pdflatex main.tex
bibtex main
pdflatex main.tex
pdflatex main.tex
```

### Method 2: Using latexmk (If Available)

```bash
latexmk -pdf proposal.tex  # or main.tex
```

## View Your PDF

Open the generated PDF file:

- `proposal.pdf` (for proposals)
- `main.pdf` (for major projects)

## Next Steps

- 📖 Read the [Input Schema](input-schema) to understand all configuration options
- 🎨 Check the [Customization Guide](customization) to personalize your report
- ❓ See the [FAQ](faq) for common questions and issues

## Common Issues

### Issue: "Command not found: python"

**Solution**: Try `python3` instead of `python`

### Issue: "pdflatex: command not found"

**Solution**: Install a LaTeX distribution (see Prerequisites)

### Issue: "No module named 'jinja2'"

**Solution**: Run `pip install -r scripts/requirements.txt`

### Issue: Bibliography not showing

**Solution**: Make sure you:

1. Added references to the `.bib` file
2. Cited at least one reference using `\cite{key}` in your text
3. Ran bibtex and pdflatex multiple times

## Getting Help

- Check the [FAQ](faq)
- Open an issue on [GitHub](https://github.com/satishjhanwer/IITJ-MTP-Template-Generator/issues)
- Read the full documentation in the `docs/` directory

---

Happy report writing! 📝
