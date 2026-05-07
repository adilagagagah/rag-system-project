import re

# membersihkan teks dari hasil ingest_pdf.py
def clean_text(text: str) -> str:
    # remove multiple newlines
    text = re.sub(r'\n+', '\n', text)

    # remove excessive spaces
    text = re.sub(r'[ \t]+', ' ', text)

    # remove page numbers (simple heuristic)
    text = re.sub(r'^\s*\d+\s*\n+', '\n', text, flags=re.MULTILINE)

    # --- Formula removal ---

    # Define patterns for various mathematical components
    # Mathematical Alphanumeric Symbols (e.g., 𝛽, 𝜀, 𝜎, 𝑛, 𝑑, 𝑦, 𝑥, 𝑿, 𝒀, 𝜺, 𝜷)
    # Greek letters (e.g., α, β, γ)
    # Mathematical Operators (e.g., +, -, *, /, =, ~, ⋮)
    # Fullwidth Parentheses (൦, ൪)
    # Parts of Large Delimiters (e.g., ⎡, ⎣, ⎤, ⎦, ⎢, ⎥)
    # Common mathematical punctuation and operators (., ,, +, -, *, /, (, ), [, ], {, }, ;)
    pure_math_line_pattern = r'[\U0001D400-\U0001D7FF\u0370-\u03FF\u2200-\u22FF\uFF08-\uFF09\u23A0-\u23FF=.,+\-*/()\[\]\{\};]'

    # 1. Remove lines that are purely equation numbers (e.g., "(2)", "(3)") or single digits.
    # This helps in cleaning up standalone equation labels or numbers within formula blocks.
    text = re.sub(r'^[ \t]*\(\d+\)[ \t]*$', '', text, flags=re.MULTILINE)
    text = re.sub(r'^[ \t]*\d+[ \t]*$', '', text, flags=re.MULTILINE)

    # 2. Remove lines that are predominantly mathematical formulas.
    # This regex targets lines that start with a mathematical character (or space then math char)
    # and then contain mostly mathematical characters, digits, and common math punctuation,
    # with optional spaces. This should capture full lines of equations or matrix rows.
    # The `+` after the first `pure_math_line_pattern` ensures at least one math character is present.
    text = re.sub(r'^[ \t]*' + pure_math_line_pattern + r'[ \t\d' + pure_math_line_pattern + r']*[ \t]*$', '', text, flags=re.MULTILINE)

    # After removing formula lines, there might be new empty lines or lines with only spaces.
    # Re-run newline and space cleaning to consolidate.
    text = re.sub(r'\n+', '\n', text)
    text = re.sub(r'[ \t]+', ' ', text)

    # strip
    text = text.strip()

    return text
