import re

def clean_text(text):
    """
    Clean the raw extracted text (remove unnecessary characters, etc.)
    """
    cleaned_text = re.sub(r'\n+', '\n', text)  # Remove unnecessary newlines
    cleaned_text = re.sub(r'\s{2,}', ' ', cleaned_text)  # Remove extra spaces
    return cleaned_text

