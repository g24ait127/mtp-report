# Frequently Asked Questions (FAQ)

Common questions and solutions for the IITJ MTP Template Generator.

## Understanding the output

### Q: Does the generator write my full report (abstract, chapters, acknowledgments, etc.)?

**A:** No. It creates a **LaTeX project** with the right **structure** and your **metadata** (title, name, supervisor, dates, and similar fields from the config or prompts). Sections such as abstract, declaration, certificate, acknowledgments, and each chapter still contain **placeholders**—search for `[TODO]` and `% TODO` in the `.tex` files. **You** must add your real writing, figures, and bibliography entries.

### Q: I compiled a PDF right after generating—why does it look like dummy or example text?

**A:** That is expected until you replace every placeholder. Compiling produces a PDF from whatever is in the `.tex` files **right now**. Early on, that is mostly **template text**, so the PDF shows **correct layout** but not your finished work. Treat that as a **preview**; your **submission-ready** PDF is the same compile step **after** you have filled all sections.

## Installation and Setup

### Q: I get "python: command not found"

**A:** Try using `python3` instead:

```bash
python3 scripts/generate.py
```

Or check if Python is installed:

```bash
python --version
python3 --version
```

### Q: How do I install Python?

**A:** Download from [python.org](https://www.python.org/downloads/). Make sure to check "Add Python to PATH" during installation.

### Q: I get "No module named 'jinja2'"

**A:** Install the required dependencies:

```bash
pip install -r scripts/requirements.txt
```

If `pip` doesn't work, try:

```bash
pip3 install -r scripts/requirements.txt
```

### Q: How do I install LaTeX?

**A:** Install a LaTeX distribution:

- **Windows**: [MiKTeX](https://miktex.org/download)
- **macOS**: [MacTeX](https://www.tug.org/mactex/)
- **Linux**:

  ```bash
  sudo apt-get install texlive-full  # Ubuntu/Debian
  sudo yum install texlive-scheme-full  # Fedora/RHEL
  ```

## Usage

### Q: Can I use this without installing dependencies?

**A:** Yes! Use the zero-dependency version:

```bash
python scripts/generate_simple.py
```

Note: This version has limited features (no YAML support, basic templating).

### Q: How do I save my configuration for reuse?

**A:** Create a YAML config file:

```yaml
project:
  title: "My Project"
  type: "proposal"
# ... rest of config
```

Then use it:

```bash
python scripts/generate.py --config my-config.yaml
```

### Q: Can I generate multiple reports with different configs?

**A:** Yes! Create separate config files and generate each:

```bash
python scripts/generate.py --config project1.yaml --output project1
python scripts/generate.py --config project2.yaml --output project2
```

### Q: Where is the generated report?

**A:** By default, in `output/your-project-name/`. You can specify a custom location:

```bash
python scripts/generate.py --config config.yaml --output /path/to/output
```

## LaTeX Compilation

### Q: Bibliography is not showing

**A:** Make sure you:

1. Added references to the `.bib` file
2. Cited at least one reference using `\cite{key}` in your text
3. Ran the compilation sequence:

   ```bash
   pdflatex main.tex
   bibtex main
   pdflatex main.tex
   pdflatex main.tex
   ```

### Q: Table of contents is empty or outdated

**A:** Run `pdflatex` multiple times (2-3 times) to resolve cross-references.

### Q: I get "File 'logo.png' not found"

**A:** Either:

1. Provide a custom logo in your config
2. Create a placeholder `logo.png` file
3. Comment out the logo line in `titlePage.tex`:

   ```latex
   % \includegraphics[width=0.3\textwidth]{logo.png}
   ```

### Q: Compilation takes a long time

**A:** This is normal for LaTeX. First compilation is slower. Subsequent compilations are faster.

### Q: I get "Undefined control sequence" error

**A:** This usually means:

1. Missing package - add `\usepackage{packagename}` to preamble
2. Typo in command name
3. Special character not escaped - use `\&`, `\%`, `\$`, etc.

### Q: How do I view compilation errors?

**A:** Check the `.log` file in your output directory. Look for lines starting with `!` or `Error`.

## Content and Formatting

### Q: How do I add images/figures?

**A:**

1. Create a `figures/` directory in your output folder
2. Add your image files (PNG, JPG, PDF)
3. Include in your `.tex` file:

   ```latex
   \begin{figure}[H]
   \centering
   \includegraphics[width=0.8\textwidth]{figures/myimage.png}
   \caption{My Image Caption}
   \label{fig:myimage}
   \end{figure}
   ```

### Q: How do I add tables?

**A:** Use the `tabular` environment:

```latex
\begin{table}[H]
\centering
\caption{My Table}
\label{tab:mytable}
\begin{tabular}{lcc}
\toprule
\textbf{Item} & \textbf{Value 1} & \textbf{Value 2} \\
\midrule
Row 1 & 10 & 20 \\
Row 2 & 30 & 40 \\
\bottomrule
\end{tabular}
\end{table}
```

### Q: How do I cite references?

**A:**

1. Add reference to `.bib` file:

   ```bibtex
   @article{smith2024,
       author = {Smith, John},
       title = {Example Article},
       journal = {Journal Name},
       year = {2024}
   }
   ```

2. Cite in text:

   ```latex
   According to Smith \cite{smith2024}, ...
   ```

### Q: How do I change font size?

**A:** In `main.tex` or `proposal.tex`:

```latex
\documentclass[12pt]{article}  % Change to 10pt or 11pt
```

### Q: How do I change line spacing?

**A:** Modify the `\setstretch` command:

```latex
\setstretch{1.5}  % Change to 1.0 or 2.0
```

### Q: Can I add more chapters/sections?

**A:** Yes! See the [Customization Guide](customization.md#adding-custom-sections).

## Customization

### Q: Can I use my university's logo?

**A:** Yes! Specify in your config:

```yaml
assets:
  logo_path: "./path/to/logo.png"
```

Or use the `--logo` flag:

```bash
python scripts/generate.py --config config.yaml --logo logo.png
```

### Q: Can I change the title page layout?

**A:** Yes! Edit `titlePage.tex` in the generated output or in the template directory.

### Q: Can I use a different citation style?

**A:** Yes! Change the bibliography style:

```latex
\bibliographystyle{apa}  % or acm, plain, etc.
```

You may need to download the corresponding `.bst` file.

### Q: Can I remove the declaration/certificate pages?

**A:** Yes! Set in your config:

```yaml
content:
  include_declaration: false
  include_certificate: false
```

## Troubleshooting

### Q: Generated PDF has placeholder text

**A:** This is expected! Search for `[TODO]` markers in the `.tex` files and replace with your content.

### Q: Special characters are not displaying correctly

**A:** Escape special LaTeX characters:

- `&` → `\&`
- `%` → `\%`
- `$` → `\$`
- `#` → `\#`
- `_` → `\_`
- `{` → `\{`
- `}` → `\}`

### Q: Figures/tables are in wrong position

**A:** Use placement specifiers:

```latex
\begin{figure}[H]  % H = exactly here (requires float package)
\begin{figure}[t]  % t = top of page
\begin{figure}[b]  % b = bottom of page
\begin{figure}[p]  # p = separate page
```

### Q: Page numbers are wrong

**A:** Run `pdflatex` multiple times to resolve cross-references.

### Q: I want to start page numbering from a specific page

**A:** Use:

```latex
\pagenumbering{roman}  % For front matter (i, ii, iii)
\pagenumbering{arabic} % For main content (1, 2, 3)
\setcounter{page}{1}   % Reset counter
```

## Advanced

### Q: Can I use this for other document types?

**A:** Yes! The templates can be adapted for:

- Research papers
- Technical reports
- Dissertations
- Course projects

### Q: Can I contribute my university's template?

**A:** Yes! Please:

1. Fork the repository
2. Add your template to `templates/`
3. Submit a pull request
4. Include documentation

### Q: Can I use this commercially?

**A:** Yes! This project is MIT licensed. See [LICENSE](../LICENSE) for details.

### Q: How do I report bugs?

**A:** Open an issue on [GitHub](https://github.com/satishjhanwer/IITJ-MTP-Template-Generator/issues) with:

- Description of the problem
- Steps to reproduce
- Error messages
- Your config file (if applicable)

### Q: Can I request new features?

**A:** Yes! Open a feature request on [GitHub Discussions](https://github.com/satishjhanwer/IITJ-MTP-Template-Generator/discussions).

## Still Need Help?

- Check the [Quick Start Guide](quickstart)
- Read the [Input Schema](input-schema)
- See the [Customization Guide](customization)
- Ask on [GitHub Discussions](https://github.com/satishjhanwer/IITJ-MTP-Template-Generator/discussions)
- Open an [Issue](https://github.com/satishjhanwer/IITJ-MTP-Template-Generator/issues)

---

**Can't find your question? Ask on GitHub Discussions!**
