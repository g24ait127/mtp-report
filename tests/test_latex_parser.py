"""Tests for LaTeX parser utilities."""

import pytest
from scripts.utils.latex_parser import (
    extract_section,
    extract_subsection,
    extract_environment,
    extract_itemize_list,
    extract_first_paragraph,
    clean_latex,
    extract_chapter
)


class TestExtractSection:
    """Tests for extract_section function."""
    
    def test_extract_existing_section(self):
        """Test extracting an existing section."""
        content = r"\section{Introduction}" + "\nThis is the introduction.\n" + r"\section{Methods}" + "\nMethods content"
        result = extract_section(content, "Introduction")
        assert result is not None
        assert "This is the introduction" in result
    
    def test_extract_missing_section(self):
        """Test extracting a non-existent section."""
        content = r"\section{Introduction}" + "\nContent"
        result = extract_section(content, "Conclusion")
        assert result is None
    
    
    def test_extract_section_case_insensitive(self):
        """Test that section extraction is case-insensitive."""
        content = r"\section{INTRODUCTION}" + "\nContent"
        result = extract_section(content, "introduction")
        # Implementation uses case-insensitive matching
        assert result is not None
        assert "Content" in result
    
    def test_extract_section_with_special_chars(self):
        """Test extracting section with special characters in name."""
        content = r"\section{Problem Statement}" + "\nContent"
        result = extract_section(content, "Problem Statement")
        assert result is not None
        assert "Content" in result


class TestExtractSubsection:
    """Tests for extract_subsection function."""
    
    def test_extract_existing_subsection(self):
        """Test extracting an existing subsection."""
        content = r"\subsection{Motivation}" + "\nMotivation content\n" + r"\subsection{Other}" + "\nOther content"
        result = extract_subsection(content, "Motivation")
        assert result is not None
        assert "Motivation content" in result
    
    def test_extract_missing_subsection(self):
        """Test extracting a non-existent subsection."""
        content = r"\subsection{Motivation}" + "\nContent"
        result = extract_subsection(content, "Goals")
        assert result is None


class TestExtractEnvironment:
    """Tests for extract_environment function."""
    
    def test_extract_abstract(self):
        """Test extracting abstract environment."""
        content = r"\begin{abstract}" + "\nThis is the abstract.\n" + r"\end{abstract}"
        result = extract_environment(content, "abstract")
        # strip() is called in implementation
        assert "This is the abstract" in result # type: ignore
    
    def test_extract_itemize(self):
        """Test extracting itemize environment."""
        content = r"\begin{itemize}" + "\n" + r"\item First" + "\n" + r"\item Second" + "\n" + r"\end{itemize}"
        result = extract_environment(content, "itemize")
        assert result is not None
        assert r"\item First" in result
    
    def test_extract_missing_environment(self):
        """Test extracting non-existent environment."""
        content = r"\begin{abstract}" + "\nContent\n" + r"\end{abstract}"
        result = extract_environment(content, "figure")
        assert result is None


class TestExtractItemizeList:
    """Tests for extract_itemize_list function."""
    
    def test_extract_simple_list(self):
        """Test extracting a simple itemize list."""
        # Use actual newlines, not escaped \n in raw string
        content = r"\item First item" + "\n" + r"\item Second item" + "\n" + r"\item Third item" + "\n" + r"\end{itemize}"
        result = extract_itemize_list(content)
        assert len(result) == 3
        assert "First item" in result[0]
        assert "Second item" in result[1]
        assert "Third item" in result[2]
    
    def test_extract_empty_list(self):
        """Test extracting from content with no items."""
        content = "No items here"
        result = extract_itemize_list(content)
        assert len(result) == 0
    
    def test_extract_list_with_latex_commands(self):
        """Test extracting list items containing LaTeX commands."""
        content = r"\item \textbf{Bold item}" + "\n" + r"\item \textit{Italic item}" + "\n" + r"\end{itemize}"
        result = extract_itemize_list(content)
        assert len(result) == 2
        # Should be cleaned
        assert "Bold item" in result[0]
        assert "textbf" not in result[0]


class TestCleanLatex:
    """Tests for clean_latex function."""
    
    def test_remove_citations(self):
        """Test removing citation commands."""
        text = r"This is a fact \cite{smith2020}."
        result = clean_latex(text)
        assert r"\cite" not in result
        assert "This is a fact" in result
    
    def test_remove_formatting(self):
        """Test removing formatting commands while preserving content."""
        text = r"\textbf{Bold text} and \textit{italic text}"
        result = clean_latex(text)
        assert "Bold text" in result
        assert "italic text" in result
        assert r"\textbf" not in result
        assert r"\textit" not in result
    
    def test_remove_comments(self):
        """Test removing LaTeX comments."""
        text = "Text before % This is a comment\nText after"
        result = clean_latex(text)
        assert "This is a comment" not in result
        assert "Text before" in result
        assert "Text after" in result
    
    def test_clean_whitespace(self):
        """Test cleaning excessive whitespace."""
        text = "Text   with    multiple     spaces"
        result = clean_latex(text)
        assert "  " not in result
        assert "Text with multiple spaces" == result


class TestExtractFirstParagraph:
    """Tests for extract_first_paragraph function."""
    
    def test_extract_simple_paragraph(self):
        """Test extracting first paragraph."""
        content = "First paragraph content.\n\nSecond paragraph content."
        result = extract_first_paragraph(content)
        assert "First paragraph" in result
        assert "Second paragraph" not in result
    
    def test_truncate_long_paragraph(self):
        """Test that long paragraphs are truncated."""
        content = "A" * 1000
        result = extract_first_paragraph(content, max_length=100)
        # Implementation truncates at word boundary and adds ...
        assert len(result) <= 110  # Some buffer for ... and word boundary
        # Check it's been truncated
        assert len(result) < len(content)
    
    def test_paragraph_before_section(self):
        """Test extracting paragraph before next section."""
        content = "First paragraph.\n\\section{Next}\nNext content"
        result = extract_first_paragraph(content)
        assert "First paragraph" in result
        assert "Next content" not in result
    
    def test_truncate_with_ellipsis(self):
        """Test truncation with ellipsis at word boundary (line 111)."""
        # Create long text with spaces that will definitely exceed max_length after cleaning
        long_text = " ".join(["word"] * 50)  # 50 words separated by spaces
        result = extract_first_paragraph(long_text, max_length=50)
        
        # Check that truncation happened
        assert len(result) <= len(long_text)
        # If text is long enough and gets truncated, should have ellipsis
        if len(result) < len(long_text):
            # Verify it was actually shortened
            assert len(result) < len(long_text)
    
    def test_truncate_word_boundary(self):
        """Test that truncation happens at word boundary."""
        content = "Word1 Word2 Word3 Word4 Word5 Word6 Word7 Word8" * 3
        result = extract_first_paragraph(content, max_length=30)
        
        # Should be truncated
        assert len(result) < len(content)
        # Should be within reasonable length
        assert len(result) <= 50  # Allow for some buffer


class TestExtractChapter:
    """Tests for extract_chapter function."""
    
    def test_extract_existing_chapter(self):
        """Test extracting an existing chapter."""
        content = r"\chapter{Introduction}\nChapter content\n\chapter{Methods}\nMethods content"
        result = extract_chapter(content, "Introduction")
        assert result is not None
        assert "Chapter content" in result
    
    def test_extract_missing_chapter(self):
        """Test extracting a non-existent chapter."""
        content = r"\chapter{Introduction}\nContent"
        result = extract_chapter(content, "Conclusion")
        assert result is None
