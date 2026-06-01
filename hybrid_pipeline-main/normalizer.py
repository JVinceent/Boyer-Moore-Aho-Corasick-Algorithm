import re

def normalize(text: str) -> str:
    if not text:
        return ""
    
    t = text.lower()
    
    # === Expanded Leetspeak Mapping ===
    leet_map = {
        '4': 'a', '@': 'a',
        '3': 'e', '€': 'e',
        '1': 'i', '!': 'i', '7': 'i',
        '0': 'o', '*': 'o',
        '5': 's', '$': 's',
        '7': 't', '+': 't',
        '9': 'g', '6': 'b', '8': 'b',
        '2': 'z', 'v': 'v',  # sometimes used for 'v'
    }
    
    for k, v in leet_map.items():
        t = t.replace(k, v)
    
    # Remove punctuation but keep spaces
    t = re.sub(r'[^a-z\s]', ' ', t)
    t = re.sub(r'\s+', ' ', t).strip()
    
    # Common multi-word / variant fixes
    t = t.replace('putang ina', 'putangina')
    t = t.replace('p tang ina', 'putangina')
    t = t.replace('tang ina', 'tangina')
    
    return t