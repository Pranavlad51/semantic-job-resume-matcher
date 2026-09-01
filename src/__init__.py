"""
src/__init__.py (updated)
Package initialization - ensuring all imports work
"""

__version__ = "1.0.0"
__author__ = "Pranav Lad"
__description__ = "AI-powered resume ranking using semantic similarity"

from src.parser import extract_resume_text
from src.embeddings import load_model, generate_embedding
from src.similarity import calculate_cosine_similarity, similarity_to_percentage
from src.skills import extract_skills, get_skill_summary
from src.ranking import rank_candidates
from src.explanation import generate_explanation
from src.bias import get_bias_awareness_text
