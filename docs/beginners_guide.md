---
layout: default
title: Simple guide for beginners
---

# Simple guide for beginners

This page is for you if you are **not** used to terminals, Python, or LaTeX jargon. The [Quick Start](quickstart) guide has the exact commands once you are ready.

## What this tool does

This program **does not** write your thesis or proposal for you. It **creates a starter LaTeX project** on your computer:

- Your **metadata** is filled in where possible (title, your name, supervisor, dates, and similar fields from the questions or config file).
- **Sections and files** are created for you (for example abstract, acknowledgments, declaration, certificate, chapters such as introduction, literature, methodology, results, conclusion, and more depending on report type).
- Most **body text starts as placeholders**—look for `[TODO]` and `% TODO` comments in the `.tex` files and example lines in the `.bib` file.

**You** must replace those placeholders with your real writing, figures, and references. That is your actual report.

## What this tool does *not* do

- It does not guarantee that your department or supervisor will accept every section title or wording—you may still need small edits.
- It does not run research or fill in technical content for you.

## What you need on your computer

1. **Python** (3.9 or newer)—used once to run the generator script.
2. **A LaTeX system** (MiKTeX, TeX Live, MacTeX, etc.)—needed when you want to turn `.tex` files into a **PDF**.
3. **This project’s folder**—from `git clone` or by downloading the repository as a ZIP from GitHub (ZIP means you update manually when the project releases new versions).

For a step-by-step checklist, see [Setup Checklist](setup_checklist).

## Choose a path

| If you… | Then… |
|--------|--------|
| Prefer answering questions | Use **interactive** mode: `python scripts/generate.py` (after installing dependencies—see [Quick Start](quickstart)). |
| Already have a filled `config.yaml` | Run `python scripts/generate.py --config your-config.yaml`. |
| Cannot use `pip` / Jinja2 | Try `python scripts/generate_simple.py` with a JSON config (fewer features). |

## After generation: template PDF vs your real PDF

When you run the generator, it writes files under `output/your-project-name/`.

- If you **compile to PDF immediately**, you will get a PDF that shows **correct formatting and layout**, but the **content is still mostly placeholders**. Think of it as a **template or preview**, not your final submission.
- Your **real** submission PDF is the **same build process**, but **after** you have edited every section (abstract, chapters, acknowledgments, declaration, certificate text, bibliography, etc.).

Search the generated folder for `[TODO]` and `% TODO` so nothing important is left as dummy text.

## Typical next steps (short)

1. Open the folder under `output/` that the tool printed.
2. Edit the `.tex` files (and `.bib` if you use citations) with your real content.
3. Compile with LaTeX (see [Quick Start](quickstart) for `pdflatex` / `bibtex` commands, or use your editor’s build button).
4. When the PDF reads like **your** work—not example text—you are much closer to done.

## Tiny glossary

- **LaTeX** — A system for writing structured documents; `.tex` files are source files.
- **PDF** — The printable file you submit; produced by compiling `.tex` files.
- **Terminal / command prompt** — The text window where you type `python scripts/generate.py`.
- **YAML config** — A text file (often `config.yaml`) listing your project settings for non-interactive runs.
- **`output/`** — Default folder where generated projects are stored (ignored by Git so your drafts are not committed by mistake).

## Where to get help

- [FAQ](faq) — Common errors and questions.
- [Input schema](input_schema) — All configuration fields explained.
- [GitHub Issues](https://github.com/satishjhanwer/IITJ-MTP-Template-Generator/issues) — Bugs and feature requests.

If someone in your lab already has Python and LaTeX working, asking them to verify your install can save a lot of time.
