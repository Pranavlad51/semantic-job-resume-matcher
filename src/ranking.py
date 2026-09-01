"""
src/ranking.py
Rank candidates based on semantic similarity scores.

This module handles sorting and ranking of candidates.
"""

import pandas as pd
from src.similarity import similarity_to_percentage, get_similarity_level


def rank_candidates(candidates_data):
    """
    Rank candidates based on similarity scores.
    
    Args:
        candidates_data (list): List of dicts with 'name', 'similarity', 'skills_matched', etc.
    
    Returns:
        pd.DataFrame: Ranked candidates DataFrame
    """
    df = pd.DataFrame(candidates_data)
    
    # Sort by similarity in descending order
    df = df.sort_values('similarity_score', ascending=False).reset_index(drop=True)
    
    # Add rank column
    df.insert(0, 'rank', range(1, len(df) + 1))
    
    return df


def get_ranked_candidates_summary(ranked_df):
    """
    Get a summary of ranked candidates for display.
    
    Args:
        ranked_df (pd.DataFrame): Ranked candidates
    
    Returns:
        list: List of summary dicts
    """
    summary = []
    
    for idx, row in ranked_df.iterrows():
        summary.append({
            'rank': row['rank'],
            'name': row['candidate_name'],
            'similarity_percentage': similarity_to_percentage(row['similarity_score']),
            'similarity_level': get_similarity_level(similarity_to_percentage(row['similarity_score'])),
            'matched_skills_count': len(row['matched_skills']),
            'missing_skills_count': len(row['missing_skills']),
            'matched_skills': row['matched_skills'],
            'missing_skills': row['missing_skills'],
            'keyword_score': row.get('keyword_score', 0),
        })
    
    return summary
