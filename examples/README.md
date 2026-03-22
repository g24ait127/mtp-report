# Example configuration files

This folder contains **sample configs** you can copy and edit. They are **inputs** to the generator, not pre-written reports.

## What is included

| Folder | Config files | Report type |
|--------|----------------|-------------|
| [sample-proposal/](sample-proposal/) | `config.yaml`, `config.json` | Proposal (MTP1-style) |
| [sample-major-project/](sample-major-project/) | `config.yaml` | Major project / thesis-style |
| [sample-presentation/](sample-presentation/) | `config.yaml`, `config.json` | Beamer slides |

- **`config.yaml`** — Use with `python scripts/generate.py --config ...` (full generator).
- **`config.json`** — Use with `python scripts/generate_simple.py --config ...` (zero-dependency generator; limited features).

## What running the generator does

Running generate with one of these files (or your own copy) **creates a new project under `output/`** with:

- LaTeX files for all standard sections (e.g. abstract, acknowledgments, declaration, certificate, title page, chapters such as introduction, literature, methodology, results, discussion, conclusion—depending on type).
- **Placeholder text** and **`[TODO]` / `% TODO` markers** where you must add real content.
- Example bibliography entries you should replace with your own references.

It does **not** produce your final written report—only a **structured template**.

## Important: PDF you get right after generating

If you compile LaTeX **before** replacing placeholders, the PDF will look **professionally formatted** but will still read like a **draft shell**, not your completed work. Treat early PDFs as **layout previews** until every section contains your actual text.

## Try an example

```bash
pip install -r scripts/requirements.txt
python scripts/generate.py --config examples/sample-proposal/config.yaml
```

Then open the new folder under `output/`, search for `[TODO]`, and start editing.

For a gentler introduction, see [Simple guide for beginners](../docs/beginners_guide.md).
