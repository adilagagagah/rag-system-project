import re

# membersihkan teks dari hasil ingest_pdf.py
def clean_text(text: str) -> str:
    # remove multiple newlines
    text = re.sub(r'\n+', '\n', text)

    # remove excessive spaces
    text = re.sub(r'[ \t]+', ' ', text)

    # remove page numbers (simple heuristic)
    text = re.sub(r'\d+\n\n\n', '\n', text)
    text = re.sub(r'^\s*\d+\s*\n+', '\n', text, flags=re.MULTILINE)

    # strip
    text = text.strip()

    return text
