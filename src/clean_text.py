import re

NOISE_PATTERNS = r'[൦⎣⎢⎥⎦⋮⋯⋱]'
MATH_LINE_PATTERN = r'[\U0001D400-\U0001D7FF\u0370-\u03FF\u2200-\u22FF\uFF08-\uFF09\u23A0-\u23FF=.,+\-*/()\[\]\{\};]'

def remove_math_noise(text: str) -> str:
    text = re.sub(NOISE_PATTERNS, ' ', text)
    text = re.sub(r'^[ \t]*\(\d+\)[ \t]*$', '', text, flags=re.MULTILINE)
    text = re.sub(r'^[ \t]*' + MATH_LINE_PATTERN + r'[ \t\d' + MATH_LINE_PATTERN + r']*[ \t]*$', '', text, flags=re.MULTILINE)
    return text

def remove_page_numbers(text: str) -> str:
    return re.sub(r'^\s*\d+\s*$', '', text, flags=re.MULTILINE)

def remove_short_lines(text: str) -> str:
    return '\n'.join(line.strip() for line in text.split('\n') if len(line.strip()) > 2)

def normalize_whitespace(text: str) -> str:
    text = re.sub(r'[ \t]+', ' ', text)
    return re.sub(r'\n+', '\n', text).strip()


def clean_text(text: str) -> str:
    text = remove_math_noise(text)
    text = remove_page_numbers(text)
    text = remove_short_lines(text)
    text = normalize_whitespace(text)
    return text
