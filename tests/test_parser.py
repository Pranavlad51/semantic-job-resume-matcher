"""
tests/test_parser.py
Unit tests for resume parser module
"""

import pytest
import os
from pathlib import Path
from src.parser import extract_resume_text, clean_text, extract_text_from_txt


def test_clean_text():
    """Test text cleaning function."""
    raw_text = "Hello    world\n\n  This  is   a  test"
    cleaned = clean_text(raw_text)
    assert "    " not in cleaned  # Multiple spaces removed
    assert cleaned == "Hello world This is a test"


def test_extract_text_from_txt():
    """Test TXT file extraction."""
    # Create temporary test file
    test_content = "This is a test resume\nWith multiple lines"
    test_file = "test_resume.txt"
    
    with open(test_file, "w") as f:
        f.write(test_content)
    
    try:
        extracted = extract_text_from_txt(test_file)
        assert "test resume" in extracted.lower()
        assert "multiple lines" in extracted.lower()
    finally:
        os.remove(test_file)


def test_extract_resume_text_txt():
    """Test main extraction function with TXT."""
    test_content = "Python developer with 5 years experience"
    test_file = "test_resume.txt"
    
    with open(test_file, "w") as f:
        f.write(test_content)
    
    try:
        extracted = extract_resume_text(test_file)
        assert "Python" in extracted
        assert "5 years" in extracted
    finally:
        os.remove(test_file)


def test_extract_resume_empty_file():
    """Test extraction with empty file."""
    test_file = "empty_resume.txt"
    
    with open(test_file, "w") as f:
        f.write("")
    
    try:
        with pytest.raises(Exception):
            extract_resume_text(test_file)
    finally:
        os.remove(test_file)
