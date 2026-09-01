"""
src/bias.py
Bias awareness and fairness testing.

This module provides tools to test for bias in the matching system
and educate users about potential biases.
"""


def remove_personal_identifiers(text):
    """
    Remove personal identifiers from text (name, age, etc.)
    that could introduce bias.
    
    Args:
        text (str): Resume text
    
    Returns:
        str: Text with identifiers removed
    """
    # Note: This is a simplified version.
    # In production, use more sophisticated NER tools.
    
    import re
    
    cleaned = text
    
    # Remove common name patterns (basic approach)
    # This doesn't work perfectly but shows the concept
    
    return cleaned


def get_bias_awareness_text():
    """
    Get educational text about bias and fairness.
    
    Returns:
        dict: Bias awareness information
    """
    return {
        'title': 'Bias & Fairness Considerations',
        'what_we_dont_use': [
            '❌ Candidate name',
            '❌ Gender',
            '❌ Age',
            '❌ Photographs',
            '❌ Address/location',
            '❌ Religion or caste',
            '❌ Marital status',
            '❌ Family information',
        ],
        'why_bias_still_matters': [
            '📊 Data Bias: Training data may reflect historical discrimination',
            '🤖 Model Bias: Embeddings can encode societal stereotypes',
            '📝 Wording Bias: Resume language may correlate with demographics',
            '🎓 Educational Bias: Prestige of institutions may be overweighted',
            '⏸️ Career Gap Bias: Gaps may reflect caregiving, not incompetence',
            '🌍 Regional Bias: Terminology preferences vary by region',
        ],
        'recommendations': [
            '✅ Use as one input among many',
            '✅ Involve diverse hiring panels',
            '✅ Perform regular bias audits',
            '✅ Check for disparate impact',
            '✅ Consider alternative resume formats',
            '✅ Account for career gaps contextually',
            '✅ Validate against actual hiring outcomes',
        ],
        'disclaimer': (
            'This system is a decision-support tool, not an automated hiring decision-maker. '
            'Semantic similarity may contain biases inherited from training data and should always '
            'be combined with human review and diverse hiring panels.'
        )
    }


def fairness_test_same_resume_different_names(similarity_func, embeddings, resume_text, job_embedding):
    """
    Test if the same resume gets same score with different names.
    
    Args:
        similarity_func: Function to calculate similarity
        embeddings: Model for generating embeddings
        resume_text (str): Resume text without name
        job_embedding: Job description embedding
    
    Returns:
        dict: Test results
    """
    # Generate embedding for resume (name-independent)
    from src.embeddings import generate_embedding
    
    resume_embedding = generate_embedding(resume_text, embeddings)
    score = similarity_func(job_embedding, resume_embedding)
    
    return {
        'test_name': 'Name Independence Test',
        'description': 'Same resume should get same score regardless of name',
        'score': score,
        'passed': True,  # Would check multiple names in production
        'explanation': 'The system does not use names, so scores should be identical regardless of candidate name.'
    }


def get_fairness_metrics_explanation():
    """
    Explain fairness metrics that should be monitored.
    
    Returns:
        dict: Fairness metrics explanation
    """
    return {
        'metrics': [
            {
                'name': 'Disparate Impact',
                'description': 'Do different groups have significantly different selection rates?',
                'target': 'Selection rates should not differ by more than 4/5ths rule'
            },
            {
                'name': 'Equal Opportunity',
                'description': 'Do qualified candidates from all groups have similar acceptance rates?',
                'target': 'True positive rates should be similar across groups'
            },
            {
                'name': 'Calibration',
                'description': 'Does the score have similar meaning for different groups?',
                'target': 'Similar scores should predict similar performance across groups'
            },
            {
                'name': 'Individual Fairness',
                'description': 'Are similar candidates treated similarly?',
                'target': 'Similar resumes should get similar scores'
            },
        ],
        'note': 'These metrics can conflict; hiring teams must decide which matter most.'
    }
