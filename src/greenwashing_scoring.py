from typing import Dict, List, Optional
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
}

def simple_greenwashing_score(text: str, config_path: Optional[str] = None) -> Dict[str, object]:
    """
    Calculate greenwashing score for given text.
    
    Args:
        text: The text to analyze for greenwashing keywords.
        config_path: Optional path to YAML config file. If None, uses hardcoded defaults.
    
    Returns:
        Dictionary with 'score', 'risk_level', and 'matched_keywords'.
    
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

    for phrase, weight in keywords.items():
        if phrase in cleaned:
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
        "matched_keywords": matched,
    }
