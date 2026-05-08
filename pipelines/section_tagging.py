import re
from typing import List, Dict


def detect_section(text: str) -> str:

    text_upper = text.upper()

    if re.search(r'BAB\s+I\b', text_upper):
        return "Pendahuluan"

    elif re.search(r'BAB\s+II\b', text_upper):
        return "Tinjauan Pustaka"

    elif re.search(r'BAB\s+III\b', text_upper):
        return "Metodologi"

    elif re.search(r'BAB\s+IV\b', text_upper):
        return "Hasil dan Pembahasan"

    elif re.search(r'BAB\s+V\b', text_upper):
        return "Kesimpulan"

    else:
        return "Unknown"


def assign_sections(pages: List[Dict]):

    current_section = "Unknown"

    for page in pages:

        detected = detect_section(page["text"])

        if detected != "Unknown":
            current_section = detected

        page["section"] = current_section

    return pages