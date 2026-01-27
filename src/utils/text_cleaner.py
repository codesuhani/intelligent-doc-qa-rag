import re

def clean_text(text: str) -> str:
    """
    Cleans extracted PDF text by removing excessive whitespace
    and non-printable characters.
    """
    text = re.sub(r'\s+', ' ', text)
    text = text.replace('\x00', '')
    return text.strip()
