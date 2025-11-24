import re

def clean_text(text):
    if not isinstance(text, str):
        return ""
    text = text.lower()
    text = text.replace("\\n", " ").replace("\\r", " ")
    text = re.sub(r"\s+", " ", text).strip()
    text = re.sub(r"[^a-z0-9\\s]", "", text)
    return text

def tokenize_words(text):
    text = clean_text(text)
    if text=="":
        return []
    return text.split()