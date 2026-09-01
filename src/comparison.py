"""
src/comparison.py
Compare semantic matching vs keyword matching.

Demonstrates why semantic similarity outperforms simple keyword matching.
"""

from src.skills import keyword_matching_score


def compare_matching_methods(job_text, resume_text, semantic_score, keyword_score=None):
    """
    Compare semantic and keyword matching scores.
    
    Args:
        job_text (str): Job description
        resume_text (str): Resume text
        semantic_score (float): Semantic similarity (0-1)
        keyword_score (float): Optional keyword score
    
    Returns:
        dict: Comparison results
    """
    if keyword_score is None:
        keyword_score = keyword_matching_score(job_text, resume_text) / 100.0
    
    semantic_pct = round(semantic_score * 100, 1)
    keyword_pct = round(keyword_score * 100, 1)
    
    difference = semantic_pct - keyword_pct
    
    return {
        'semantic_score': semantic_pct,
        'keyword_score': keyword_pct,
        'difference': round(difference, 1),
        'semantic_better': semantic_score > keyword_score,
        'comparison_text': generate_comparison_text(semantic_pct, keyword_pct, difference)
    }


def generate_comparison_text(semantic_pct, keyword_pct, difference):
    """
    Generate explanation text for the comparison.
    
    Args:
        semantic_pct (float): Semantic score percentage
        keyword_pct (float): Keyword score percentage
        difference (float): Difference between them
    
    Returns:
        str: Explanation text
    """
    if abs(difference) < 5:
        return (
            "Semantic and keyword matching agree: "
            "Both methods identify this as a similar match."
        )
    elif difference > 0:
        return (
            f"Semantic matching is {abs(difference):.1f}% higher than keyword matching. "
            "This suggests the resume uses different wording but similar concepts to the job description. "
            "Semantic similarity catches this; keyword matching would miss it."
        )
    else:
        return (
            f"Keyword matching is {abs(difference):.1f}% higher than semantic matching. "
            "This suggests many exact words match, but the contexts might differ. "
            "Semantic similarity avoids false positives from coincidental word matches."
        )


def get_comparison_insights():
    """
    Get insights about when each method works better.
    
    Returns:
        dict: Comparison insights
    """
    return {
        'when_semantic_wins': [
            'Resume uses different terminology (e.g., "ML" vs "Machine Learning")',
            'Similar concepts expressed differently (e.g., "predictive systems" vs "statistical models")',
            'Job description vague but resume specific (or vice versa)',
            'Different synonyms used (e.g., "code" vs "implement")',
        ],
        'when_keyword_wins': [
            'Exact specialized terms matter (e.g., "TensorFlow", "Kubernetes")',
            'Resume too generic without specific tool names',
            'Job description includes uncommon terminology',
        ],
        'best_practice': 'Use both methods together. High semantic + high keyword = strong match. '
                        'High semantic but low keyword = good fit with different wording. '
                        'High keyword but low semantic = possibly coincidental match.',
    }
