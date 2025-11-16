"""
Greenwashing Detector Package

A simple keyword-based greenwashing detection tool for analyzing text.
"""

from .text_cleaner import clean_text, tokenize_text, extract_keywords
from .scoring import calculate_greenwashing_score, analyze_text, get_keyword_list

__version__ = '0.1.0'
__all__ = [
    'clean_text',
    'tokenize_text', 
    'extract_keywords',
    'calculate_greenwashing_score',
    'analyze_text',
    'get_keyword_list'
]
