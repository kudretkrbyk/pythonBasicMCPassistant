# utils.py
import re

def extract_first_json_block(text):
    """
    LLM yanıtından ilk geçerli JSON nesnesini çıkarır.
    """
    match = re.search(r'{.*}', text, re.DOTALL)
    return match.group(0) if match else None
