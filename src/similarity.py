"""
src/similarity.py
Calculate semantic similarity between job descriptions and resumes.

This module computes cosine similarity between embeddings.
Cosine similarity measures the angle between two vectors:
- 1.0 = identical direction (perfect match)
- 0.5 = 60° angle (moderate similarity)
- 0.0 = perpendicular (no similarity)
"""

from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


def calculate_cosine_similarity(embedding1, embedding2):
    """
    Calculate cosine similarity between two embeddings.
    
    Cosine similarity measures how similar two vectors are based on the
    angle between them. It's normalized to range [0, 1].
    
    Args:
        embedding1 (np.ndarray): First embedding vector
        embedding2 (np.ndarray): Second embedding vector
    
    Returns:
        float: Similarity score between 0 and 1
    """
    if embedding1 is None or embedding2 is None:
        return 0.0
    
    # Reshape if needed for sklearn
    if len(embedding1.shape) == 1:
        embedding1 = embedding1.reshape(1, -1)
    if len(embedding2.shape) == 1:
        embedding2 = embedding2.reshape(1, -1)
    
    similarity = cosine_similarity(embedding1, embedding2)[0][0]
    
    # Clamp to [0, 1] range
    similarity = max(0.0, min(1.0, similarity))
    
    return float(similarity)


def calculate_similarities_batch(job_embedding, resume_embeddings):
    """
    Calculate similarity between one job description and multiple resumes.
    
    Args:
        job_embedding (np.ndarray): Job description embedding
        resume_embeddings (np.ndarray): Array of resume embeddings
    
    Returns:
        np.ndarray: Array of similarity scores
    """
    if len(job_embedding.shape) == 1:
        job_embedding = job_embedding.reshape(1, -1)
    
    # Calculate similarity for each resume against job
    similarities = cosine_similarity(job_embedding, resume_embeddings)[0]
    
    # Clamp to [0, 1] range
    similarities = np.clip(similarities, 0.0, 1.0)
    
    return similarities


def similarity_to_percentage(similarity_score):
    """
    Convert similarity score (0-1) to percentage (0-100).
    
    Args:
        similarity_score (float): Score between 0 and 1
    
    Returns:
        float: Percentage between 0 and 100
    """
    return round(similarity_score * 100, 1)


def get_similarity_level(percentage):
    """
    Convert percentage score to qualitative level.
    
    Args:
        percentage (float): Score between 0 and 100
    
    Returns:
        str: Qualitative assessment
    """
    if percentage >= 85:
        return "Excellent Match"
    elif percentage >= 70:
        return "Good Match"
    elif percentage >= 55:
        return "Moderate Match"
    elif percentage >= 40:
        return "Weak Match"
    else:
        return "Poor Match"


"""
Cosine Similarity Explained:

In semantic embeddings space, each word/sentence is a point.
Similar meanings are close together.

Example:
Job: "machine learning engineer" → embedding [0.5, 0.3, 0.8, ...]
Resume1: "ML engineer" → embedding [0.49, 0.31, 0.79, ...] → 98% similar
Resume2: "JavaScript developer" → embedding [-0.2, 0.9, 0.1, ...] → 25% similar

Cosine similarity = dot product / (norm1 × norm2)
                  = how "aligned" are the vectors

High alignment = high similarity = good match
Low alignment = low similarity = poor match
"""
