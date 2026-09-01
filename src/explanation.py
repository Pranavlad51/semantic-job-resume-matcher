"""
src/explanation.py
Generate detailed explanations for candidate scores.

This module creates human-readable explanations of why a candidate
received a particular similarity score.
"""

from src.similarity import similarity_to_percentage, get_similarity_level


def extract_experience_keywords(text):
    """
    Extract experience-related keywords from text.
    
    Args:
        text (str): Resume or job text
    
    Returns:
        list: Experience keywords
    """
    experience_keywords = [
        'experience', 'worked', 'built', 'developed', 'created', 'managed',
        'led', 'designed', 'implemented', 'deployed', 'optimized', 'architected',
        'years', 'project', 'projects', 'product', 'feature', 'features'
    ]
    
    text_lower = text.lower()
    found = [kw for kw in experience_keywords if kw in text_lower]
    return found


def extract_education_keywords(text):
    """
    Extract education-related keywords from text.
    
    Args:
        text (str): Resume or job text
    
    Returns:
        list: Education keywords
    """
    education_keywords = [
        'bachelor', 'master', 'phd', 'degree', 'diploma', 'certificate',
        'university', 'college', 'school', 'graduated', 'graduation',
        'computer science', 'engineering', 'it', 'information technology'
    ]
    
    text_lower = text.lower()
    found = [kw for kw in education_keywords if kw in text_lower]
    return found


def generate_explanation(candidate_name, similarity_score, matched_skills, 
                       missing_skills, job_text, resume_text):
    """
    Generate a detailed explanation for a candidate.
    
    Args:
        candidate_name (str): Candidate identifier
        similarity_score (float): Similarity score (0-1)
        matched_skills (list): Skills present in both
        missing_skills (list): Skills in job but not resume
        job_text (str): Job description
        resume_text (str): Resume text
    
    Returns:
        dict: Explanation components
    """
    percentage = similarity_to_percentage(similarity_score)
    level = get_similarity_level(percentage)
    
    experience_found = extract_experience_keywords(resume_text)
    education_found = extract_education_keywords(resume_text)
    
    # Generate explanation text
    explanation = f"This resume has {level.lower()} with the job description."
    
    if matched_skills:
        explanation += f" The candidate demonstrates expertise in {', '.join(matched_skills[:3])}"
        if len(matched_skills) > 3:
            explanation += f" and {len(matched_skills) - 3} more required skills."
        else:
            explanation += "."
    
    if missing_skills:
        explanation += f" However, experience with {', '.join(missing_skills[:2])}"
        if len(missing_skills) > 2:
            explanation += f" and {len(missing_skills) - 2} other skills is missing."
        else:
            explanation += " is missing."
    
    if experience_found:
        explanation += f" The resume mentions relevant experience keywords: {', '.join(experience_found[:3])}."
    
    explanation += " This ranking is based on semantic similarity—a deep understanding of meaning—not just keyword matching."
    
    return {
        'candidate_name': candidate_name,
        'similarity_percentage': percentage,
        'similarity_level': level,
        'matched_skills': matched_skills,
        'missing_skills': missing_skills,
        'experience_indicators': experience_found[:5],
        'education_indicators': education_found[:3],
        'explanation': explanation
    }


def generate_bulk_explanations(ranked_candidates, job_text, resume_texts):
    """
    Generate explanations for all candidates.
    
    Args:
        ranked_candidates (list): List of ranked candidate dicts
        job_text (str): Job description
        resume_texts (dict): Dict of candidate_name -> resume_text
    
    Returns:
        list: List of explanation dicts
    """
    explanations = []
    
    for candidate in ranked_candidates:
        exp = generate_explanation(
            candidate_name=candidate['name'],
            similarity_score=candidate['similarity_score'],
            matched_skills=candidate['matched_skills'],
            missing_skills=candidate['missing_skills'],
            job_text=job_text,
            resume_text=resume_texts.get(candidate['name'], '')
        )
        explanations.append(exp)
    
    return explanations
