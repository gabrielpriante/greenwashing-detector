from typing import Dict, List
from text_cleaning import basic_clean_text

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

def simple_greenwashing_score(text: str) -> Dict[str, object]:
    cleaned = basic_clean_text(text)
    
    total_weight = 0
    matched: List[str] = []

    for phrase, weight in GREENWASHING_KEYWORDS.items():
        if phrase in cleaned:
            matched.append(phrase)
            total_weight += weight

    score = max(0, min(100, total_weight * 10))

    if score >= 60:
        risk = "High"
    elif score >= 30:
        risk = "Medium"
    else:
        risk = "Low"

    return {
        "score": score,
        "risk_level": risk,
        "matched_keywords": matched,
    }
