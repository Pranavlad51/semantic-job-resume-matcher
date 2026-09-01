"""
tests/test_skills.py
Unit tests for skills extraction and matching
"""

import pytest
from src.skills import (
    extract_skills,
    get_matched_skills,
    get_missing_skills,
    calculate_skill_match_percentage
)


def test_extract_skills_basic():
    """Test basic skill extraction."""
    text = "Experience with Python, SQL, and Machine Learning"
    skills = extract_skills(text)
    assert "Python" in skills
    assert "SQL" in skills
    assert "Machine Learning" in skills


def test_extract_skills_case_insensitive():
    """Test that skill extraction is case insensitive."""
    text1 = "I know python"
    text2 = "I know PYTHON"
    text3 = "I know Python"
    skills1 = extract_skills(text1)
    skills2 = extract_skills(text2)
    skills3 = extract_skills(text3)
    assert "Python" in skills1
    assert "Python" in skills2
    assert "Python" in skills3


def test_extract_skills_no_match():
    """Test extraction with no skills."""
    text = "Lorem ipsum dolor sit amet"
    skills = extract_skills(text)
    assert len(skills) == 0


def test_get_matched_skills():
    """Test finding matched skills."""
    job_skills = ["Python", "SQL", "Machine Learning"]
    resume_skills = ["Python", "Java", "SQL"]
    matched = get_matched_skills(job_skills, resume_skills)
    assert set(matched) == {"Python", "SQL"}


def test_get_missing_skills():
    """Test finding missing skills."""
    job_skills = ["Python", "SQL", "Machine Learning"]
    resume_skills = ["Python", "Java", "SQL"]
    missing = get_missing_skills(job_skills, resume_skills)
    assert missing == ["Machine Learning"]


def test_calculate_skill_match_percentage():
    """Test percentage calculation."""
    job_skills = ["Python", "SQL", "Machine Learning", "Docker"]
    resume_skills = ["Python", "SQL"]
    percentage = calculate_skill_match_percentage(job_skills, resume_skills)
    assert percentage == 50.0  # 2 out of 4


def test_calculate_skill_match_percentage_no_skills():
    """Test with empty job skills."""
    percentage = calculate_skill_match_percentage([], ["Python"])
    assert percentage == 0.0
