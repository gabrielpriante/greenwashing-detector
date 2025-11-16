"""
Greenwashing Detector - Scoring Module

This module provides a simple keyword-based scoring system to detect
potential greenwashing in text.
"""

from typing import Dict, List, Tuple
from .text_cleaner import clean_text, tokenize_text


# Common greenwashing keywords and phrases (weighted by suspicion level)
GREENWASHING_KEYWORDS = {
    # High suspicion (weight: 3)
    'eco friendly': 3,
    'ecofriendly': 3,
    'green': 3,
    'natural': 3,
    'sustainable': 3,
    'organic': 3,
    'environmentally friendly': 3,
    
    # Medium suspicion (weight: 2)
    'recyclable': 2,
    'biodegradable': 2,
    'renewable': 2,
    'clean': 2,
    'pure': 2,
    'earth friendly': 2,
    'planet friendly': 2,
    'carbon neutral': 2,
    'zero waste': 2,
    
    # Lower suspicion (weight: 1)
    'conscious': 1,
    'responsible': 1,
    'ethical': 1,
    'better': 1,
    'improved': 1,
}

# Vague or misleading terms that often indicate greenwashing
VAGUE_TERMS = {
    'all natural': 2,
    'chemical free': 3,  # Everything is chemicals!
    'non toxic': 2,
    'safe': 1,
    'good for environment': 2,
    'helps planet': 2,
}


def calculate_greenwashing_score(text: str) -> Dict[str, any]:
    """
    Calculate a greenwashing score for the given text based on keyword matching.
    
    Args:
        text: Input text to analyze
    
    Returns:
        Dictionary containing:
            - score: numerical score (higher = more suspicious)
            - matched_keywords: list of matched keywords with their weights
            - risk_level: categorization (Low/Medium/High)
            - word_count: total words in text
    """
    if not isinstance(text, str) or not text.strip():
        return {
            'score': 0,
            'matched_keywords': [],
            'risk_level': 'Low',
            'word_count': 0
        }
    
    # Clean and prepare text
    cleaned_text = clean_text(text, remove_stopwords=False, lowercase=True)
    
    # Count words for normalization
    word_count = len(cleaned_text.split())
    
    # Track matched keywords and calculate score
    matched_keywords = []
    total_score = 0
    
    # Check for greenwashing keywords
    for keyword, weight in GREENWASHING_KEYWORDS.items():
        if keyword in cleaned_text:
            count = cleaned_text.count(keyword)
            matched_keywords.append({
                'keyword': keyword,
                'weight': weight,
                'count': count,
                'contribution': weight * count
            })
            total_score += weight * count
    
    # Check for vague terms (higher penalty)
    for term, weight in VAGUE_TERMS.items():
        if term in cleaned_text:
            count = cleaned_text.count(term)
            matched_keywords.append({
                'keyword': term,
                'weight': weight,
                'count': count,
                'contribution': weight * count,
                'type': 'vague'
            })
            total_score += weight * count
    
    # Normalize score by word count (to avoid penalizing longer texts)
    normalized_score = (total_score / word_count * 100) if word_count > 0 else 0
    
    # Determine risk level
    if normalized_score >= 15:
        risk_level = 'High'
    elif normalized_score >= 5:
        risk_level = 'Medium'
    else:
        risk_level = 'Low'
    
    return {
        'score': round(normalized_score, 2),
        'raw_score': total_score,
        'matched_keywords': matched_keywords,
        'risk_level': risk_level,
        'word_count': word_count
    }


def analyze_text(text: str) -> str:
    """
    Perform a complete greenwashing analysis and return a formatted report.
    
    Args:
        text: Input text to analyze
    
    Returns:
        Formatted string report of the analysis
    """
    result = calculate_greenwashing_score(text)
    
    report = f"""
Greenwashing Detection Report
{'=' * 50}

Text Length: {result['word_count']} words
Greenwashing Score: {result['score']}/100
Risk Level: {result['risk_level']}

Matched Keywords ({len(result['matched_keywords'])}):
"""
    
    if result['matched_keywords']:
        for match in result['matched_keywords']:
            keyword_type = f" [{match.get('type', 'standard').upper()}]" if 'type' in match else ""
            report += f"  - '{match['keyword']}': appeared {match['count']}x (weight: {match['weight']}, contribution: {match['contribution']}){keyword_type}\n"
    else:
        report += "  No greenwashing keywords detected.\n"
    
    report += f"\nTotal Raw Score: {result['raw_score']}\n"
    
    return report


def get_keyword_list() -> Dict[str, Dict[str, int]]:
    """
    Get the complete list of keywords used for greenwashing detection.
    
    Returns:
        Dictionary with 'greenwashing' and 'vague' keyword categories
    """
    return {
        'greenwashing': GREENWASHING_KEYWORDS,
        'vague': VAGUE_TERMS
    }
