import re
import string

def basic_clean_text(text: str) -> str:
    text = text.lower()
    text = text.replace("-", " ")
    text = text.translate(str.maketrans("", "", string.punctuation))
    text = re.sub(r"\s+", " ", text).strip()
    return text

def tokenize(text: str):
    cleaned = basic_clean_text(text)
    return cleaned.split()
