"""
Greenwashing Detector - Text Cleaning Module

This module provides utilities for cleaning and preprocessing text data
for greenwashing detection analysis.
"""

import re
import nltk
from typing import List, Optional

# Download required NLTK data (run once)
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt', quiet=True)

try:
    nltk.data.find('tokenizers/punkt_tab')
except LookupError:
    nltk.download('punkt_tab', quiet=True)

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords', quiet=True)

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize


def clean_text(text: str, remove_stopwords: bool = False, lowercase: bool = True) -> str:
    """
    Clean and preprocess text data.
    
    Args:
        text: Input text to clean
        remove_stopwords: Whether to remove common stopwords (default: False)
        lowercase: Whether to convert text to lowercase (default: True)
    
    Returns:
        Cleaned text string
    """
    if not isinstance(text, str):
        return ""
    
    # Remove URLs
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
    
    # Remove email addresses
    text = re.sub(r'\S+@\S+', '', text)
    
    # Remove special characters and digits, keep letters and spaces
    text = re.sub(r'[^a-zA-Z\s]', ' ', text)
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    
    # Convert to lowercase
    if lowercase:
        text = text.lower()
    
    # Remove stopwords if requested
    if remove_stopwords:
        stop_words = set(stopwords.words('english'))
        words = word_tokenize(text)
        text = ' '.join([word for word in words if word not in stop_words])
    
    return text


def tokenize_text(text: str) -> List[str]:
    """
    Tokenize text into individual words.
    
    Args:
        text: Input text to tokenize
    
    Returns:
        List of tokens (words)
    """
    if not isinstance(text, str):
        return []
    
    return word_tokenize(text.lower())


def extract_keywords(text: str, min_length: int = 3) -> List[str]:
    """
    Extract meaningful keywords from text.
    
    Args:
        text: Input text
        min_length: Minimum word length to consider (default: 3)
    
    Returns:
        List of keywords
    """
    if not isinstance(text, str):
        return []
    
    # Clean the text first
    cleaned = clean_text(text, remove_stopwords=True)
    
    # Tokenize
    tokens = word_tokenize(cleaned)
    
    # Filter by minimum length
    keywords = [token for token in tokens if len(token) >= min_length]
    
    return keywords
