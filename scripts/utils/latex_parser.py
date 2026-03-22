"""LaTeX parsing utilities for content extraction.

This module provides functions to parse LaTeX documents and extract
content from sections, environments, and lists.
"""

import re
from typing import Dict, List, Optional


def extract_section(content: str, section_name: str) -> Optional[str]:
    """Extract content from a LaTeX section.
    
    Args:
        content: Full LaTeX document content
        section_name: Name of the section to extract (e.g., 'Introduction')
    
    Returns:
        Section content or None if not found
    """
    # Try to match section with various patterns
    # Lookahead: next structural command, literal \end{document}, or end of string.
    # Note: \end{...} must use \\end in the pattern or \e is parsed as ESC in regex.
    _end_doc = r'\\end\{{document\}}'
    _after = rf'(?=\\section|\\chapter|{_end_doc}|\Z)'
    patterns = [
        rf'\\section\{{{section_name}\}}(.*?){_after}',
        rf'\\section\{{.*?{section_name}.*?\}}(.*?){_after}',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, content, re.DOTALL | re.IGNORECASE)
        if match:
            return match.group(1).strip()
    
    return None


def extract_subsection(content: str, subsection_name: str) -> Optional[str]:
    """Extract content from a LaTeX subsection.
    
    Args:
        content: Section or document content
        subsection_name: Name of the subsection to extract
    
    Returns:
        Subsection content or None if not found
    """
    _after_sub = r'(?=\\subsection|\\section|\\chapter|\Z)'
    patterns = [
        rf'\\subsection\{{{subsection_name}\}}(.*?){_after_sub}',
        rf'\\subsection\{{.*?{subsection_name}.*?\}}(.*?){_after_sub}',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, content, re.DOTALL | re.IGNORECASE)
        if match:
            return match.group(1).strip()
    
    return None


def extract_environment(content: str, env_name: str) -> Optional[str]:
    """Extract content from a LaTeX environment.
    
    Args:
        content: LaTeX document content
        env_name: Environment name (e.g., 'abstract', 'itemize')
    
    Returns:
        Environment content or None if not found
    """
    pattern = rf'\\begin\{{{env_name}\}}(.*?)\\end\{{{env_name}\}}'
    match = re.search(pattern, content, re.DOTALL)
    return match.group(1).strip() if match else None


def extract_itemize_list(content: str) -> List[str]:
    """Extract items from itemize or enumerate environment.
    
    Args:
        content: Content containing itemize/enumerate environment
    
    Returns:
        List of item texts
    """
    # Find all \item entries
    items = re.findall(r'\\item\s+(.*?)(?=\\item|\\end)', content, re.DOTALL)
    return [clean_latex(item.strip()) for item in items if item.strip()]


def extract_first_paragraph(content: str, max_length: int = 500) -> str:
    """Extract first paragraph from content.
    
    Args:
        content: Text content
        max_length: Maximum length of extracted text
    
    Returns:
        First paragraph, cleaned and truncated
    """
    # Remove leading whitespace and commands
    content = content.lstrip()
    
    # Find first paragraph (text before double newline or section)
    match = re.search(r'^(.*?)(?:\n\n|\\section|\\subsection)', content, re.DOTALL)
    if match:
        paragraph = match.group(1)
    else:
        paragraph = content[:max_length]
    
    cleaned = clean_latex(paragraph)
    
    # Truncate to max_length
    if len(cleaned) > max_length:
        cleaned = cleaned[:max_length].rsplit(' ', 1)[0] + '...'
    
    return cleaned


def clean_latex(text: str) -> str:
    """Remove LaTeX commands and simplify text.
    
    Args:
        text: LaTeX text to clean
    
    Returns:
        Cleaned text with LaTeX commands removed
    """
    # Remove citations
    text = re.sub(r'\\cite\{[^}]+\}', '', text)
    text = re.sub(r'\\citep?\{[^}]+\}', '', text)
    
    # Remove references
    text = re.sub(r'\\ref\{[^}]+\}', '', text)
    text = re.sub(r'\\label\{[^}]+\}', '', text)
    
    # Remove formatting commands (preserve content)
    text = re.sub(r'\\textbf\{([^}]+)\}', r'\1', text)
    text = re.sub(r'\\textit\{([^}]+)\}', r'\1', text)
    text = re.sub(r'\\emph\{([^}]+)\}', r'\1', text)
    text = re.sub(r'\\texttt\{([^}]+)\}', r'\1', text)
    
    # Remove URLs
    text = re.sub(r'\\url\{[^}]+\}', '', text)
    text = re.sub(r'\\href\{[^}]+\}\{([^}]+)\}', r'\1', text)
    
    # Remove comments
    text = re.sub(r'%.*$', '', text, flags=re.MULTILINE)
    
    # Remove figure/table references
    text = re.sub(r'\\includegraphics.*?\{[^}]+\}', '', text)
    text = re.sub(r'\\begin\{figure\}.*?\\end\{figure\}', '', text, flags=re.DOTALL)
    text = re.sub(r'\\begin\{table\}.*?\\end\{table\}', '', text, flags=re.DOTALL)
    
    # Clean whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text


def extract_chapter(content: str, chapter_name: str) -> Optional[str]:
    """Extract content from a LaTeX chapter.
    
    Args:
        content: Full LaTeX document content
        chapter_name: Name of the chapter to extract
    
    Returns:
        Chapter content or None if not found
    """
    _end_doc_ch = r'\\end\{{document\}}'
    _after_ch = rf'(?=\\chapter|{_end_doc_ch}|\Z)'
    patterns = [
        rf'\\chapter\{{{chapter_name}\}}(.*?){_after_ch}',
        rf'\\chapter\{{.*?{chapter_name}.*?\}}(.*?){_after_ch}',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, content, re.DOTALL | re.IGNORECASE)
        if match:
            return match.group(1).strip()
    
    return None
