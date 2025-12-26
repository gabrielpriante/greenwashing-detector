import re
from typing import Dict, List, Optional, Tuple
from text_cleaning import basic_clean_text
from config_loader import load_config, get_default_config, ConfigError

# Default hardcoded keywords for backward compatibility
GREENWASHING_KEYWORDS: Dict[str, int] = {
    "eco friendly": 2,
    "environmentally friendly": 2,
    "green": 1,
    "planet friendly": 2,
    "sustainable": 2,
    "sustainably sourced": 3,
    "responsibly sourced": 3,
    "carbon neutral": 4,
    "net zero": 4,
    "zero emissions": 4,
    "climate positive": 4,
    "100 natural": 3,
    "all natural": 3,
    "chemical free": 3,
    "non toxic": 2,
    "plastic free": 3,
    "biodegradable": 2,
}

# Negation words to detect
NEGATION_WORDS = {"not", "no", "never"}

# Maximum distance (in tokens) for negation detection
MAX_NEGATION_DISTANCE = 3

def _create_phrase_pattern(phrase: str) -> re.Pattern:
    """
    Create a regex pattern for phrase matching with word boundaries.
    
    Args:
        phrase: The phrase to create a pattern for (e.g., "carbon neutral")
    
    Returns:
        Compiled regex pattern with word boundaries
    """
    # Escape special regex characters and use word boundaries
    escaped = re.escape(phrase)
    # Use word boundaries to ensure we match complete phrases
    return re.compile(r'\b' + escaped + r'\b', re.IGNORECASE)

def _is_negated(text: str, match_start: int) -> bool:
    """
    Check if a matched phrase is negated by a negation word within MAX_NEGATION_DISTANCE tokens before it.
    
    Args:
        text: The full cleaned text being analyzed (already lowercased)
        match_start: The start position of the matched phrase
    
    Returns:
        True if the phrase is negated, False otherwise
    """
    # Get text before the match (text is already lowercased from basic_clean_text)
    before_text = text[:match_start]
    
    # Tokenize the text before the match
    tokens = before_text.split()
    
    # Check the last MAX_NEGATION_DISTANCE tokens for negation words
    last_tokens = tokens[-MAX_NEGATION_DISTANCE:] if len(tokens) >= MAX_NEGATION_DISTANCE else tokens
    
    for token in last_tokens:
        # Remove punctuation from token for comparison
        clean_token = re.sub(r'[^\w]', '', token)
        if clean_token in NEGATION_WORDS:
            return True
    
    return False

def _find_phrase_matches(text: str, phrase: str) -> List[Tuple[int, int]]:
    """
    Find all matches of a phrase in text using word boundaries.
    
    Args:
        text: The text to search in
        phrase: The phrase to search for
    
    Returns:
        List of (start, end) positions for each match
    """
    pattern = _create_phrase_pattern(phrase)
    matches = []
    for match in pattern.finditer(text):
        matches.append((match.start(), match.end()))
    return matches

def simple_greenwashing_score(text: str, config_path: Optional[str] = None) -> Dict[str, object]:
    """
    Calculate greenwashing score for given text.
    
    Args:
        text: The text to analyze for greenwashing keywords.
        config_path: Optional path to YAML config file. If None, uses hardcoded defaults.
    
    Returns:
        Dictionary with 'score', 'risk_level', 'matched_terms', and 'negated_terms'.
    
    Raises:
        ConfigError: If config file is provided but invalid.
    """
    cleaned = basic_clean_text(text)
    
    # Load configuration
    if config_path is not None:
        try:
            config = load_config(config_path)
            keywords = config['keywords']
            thresholds = config['thresholds']
        except ConfigError:
            # Re-raise config errors
            raise
    else:
        # Use hardcoded defaults (backward compatibility)
        keywords = GREENWASHING_KEYWORDS
        thresholds = {'low': 0, 'medium': 30, 'high': 60}
    
    total_weight = 0
    matched: List[str] = []
    negated: List[str] = []

    for phrase, weight in keywords.items():
        # Find all matches of this phrase with word boundaries
        matches = _find_phrase_matches(cleaned, phrase)
        
        if matches:
            # Check each match for negation
            for match_start, match_end in matches:
                if _is_negated(cleaned, match_start):
                    # This match is negated, add to negated list but don't count toward score
                    if phrase not in negated:
                        negated.append(phrase)
                else:
                    # Valid match, add to matched list and count toward score
                    if phrase not in matched:
                        matched.append(phrase)
                        total_weight += weight

    score = max(0, min(100, total_weight * 10))

    # Determine risk level based on thresholds
    if score >= thresholds['high']:
        risk = "High"
    elif score >= thresholds['medium']:
        risk = "Medium"
    else:
        risk = "Low"

    return {
        "score": score,
        "risk_level": risk,
        "matched_terms": matched,
        "negated_terms": negated,
        # Keep matched_keywords for backward compatibility
        "matched_keywords": matched,
    }
