# Contributing to IITJ MTP Template Generator

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## 🤝 How to Contribute

### Reporting Bugs

If you find a bug, please open an issue with:

- Clear description of the problem
- Steps to reproduce
- Expected vs actual behavior
- Your environment (OS, Python version, LaTeX distribution)
- Error messages or logs

### Suggesting Features

Feature requests are welcome! Please:

- Check if the feature has already been requested
- Clearly describe the feature and its use case
- Explain why it would be valuable

### Contributing Code

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/your-feature-name`
3. **Make your changes**
4. **Test your changes**
5. **Commit with clear messages**: `git commit -m "Add feature: description"`
6. **Push to your fork**: `git push origin feature/your-feature-name`
7. **Open a Pull Request**

## 📝 Contribution Areas

### 1. University Templates

We welcome templates for different universities! To contribute:

1. Create a new directory: `templates/your-university-name/`
2. Follow the existing template structure
3. Include a README with university-specific instructions
4. Add example configurations
5. Document any special requirements

### 2. Report Types

Add support for new report types:

- Conference papers
- Journal articles
- Technical reports
- Course projects

### 3. Documentation

Improvements to documentation are always appreciated:

- Fix typos or unclear explanations
- Add examples
- Translate to other languages
- Create video tutorials

### 4. Bug Fixes

Bug fixes are welcome! Please:

- Reference the issue number in your PR
- Add tests if applicable
- Update documentation if needed

### 5. Features

Before working on major features:

- Open an issue to discuss the feature
- Get feedback from maintainers
- Ensure it aligns with project goals

## 🧪 Testing Guidelines

Before submitting a PR:

1. **Test the generator**:

   ```bash
   python scripts/generate.py --config examples/sample-proposal/config.yaml
   ```

2. **Test LaTeX compilation**:

   ```bash
   cd output/test-project
   pdflatex proposal.tex
   bibtex proposal
   pdflatex proposal.tex
   pdflatex proposal.tex
   ```

3. **Check for errors**:
   - Python syntax errors
   - LaTeX compilation errors
   - Broken links in documentation

## 📋 Code Style

### Python

- Follow PEP 8 style guide
- Use meaningful variable names
- Add docstrings to functions
- Keep functions focused and small
- Add type hints where helpful

### LaTeX

- Use consistent indentation
- Add comments for complex sections
- Follow standard LaTeX conventions
- Test with multiple LaTeX distributions

### Documentation

- Use clear, concise language
- Include code examples
- Keep formatting consistent
- Use proper markdown syntax

## 🔍 Pull Request Process

1. **Update documentation** if you've changed functionality
2. **Add examples** if you've added new features
3. **Update CHANGELOG** (if applicable)
4. **Ensure tests pass**
5. **Request review** from maintainers

### PR Title Format

Use clear, descriptive titles:

- `feat: Add support for APA citation style`
- `fix: Correct bibliography rendering issue`
- `docs: Update installation instructions`
- `refactor: Simplify template rendering logic`

### PR Description

Include:

- What changes were made
- Why the changes were needed
- How to test the changes
- Screenshots (if UI changes)
- Related issues

## 🎯 Priority Areas

Current priority areas for contributions:

1. **Phase 2**: Beamer presentation templates
2. **Testing**: Automated tests for generator
3. **Examples**: More example configurations
4. **Templates**: University-specific templates
5. **Documentation**: Video tutorials

## 📜 License

By contributing, you agree that your contributions will be licensed under the MIT License.

## 💬 Communication

- **Issues**: For bug reports and feature requests
- **Discussions**: For questions and general discussion
- **Pull Requests**: For code contributions

## 🙏 Recognition

Contributors will be recognized in:

- README.md acknowledgments section
- Release notes
- Project documentation

## ❓ Questions?

If you have questions about contributing:

- Check the [FAQ](docs/faq.md)
- Open a discussion on GitHub
- Review existing issues and PRs

---

Thank you for contributing to IITJ MTP Template Generator! 🎓
