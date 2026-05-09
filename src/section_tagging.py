import re
from typing import List, Dict


def detect_section(text: str) -> dict:

    # 1. Bagian Front Matter & Back Matter
    if re.search(r'^\s*(HALAMAN\s+JUDUL|JUDUL)\b', text, re.IGNORECASE | re.MULTILINE):
        return {"type": "bab", "title": "Judul"}
    if re.search(r'^\s*(ABSTRAK|ABSTRACT)\b', text, re.IGNORECASE | re.MULTILINE):
        return {"type": "bab", "title": "Abstrak"}
    if re.search(r'^\s*KATA\s+PENGANTAR\b', text, re.IGNORECASE | re.MULTILINE):
        return {"type": "bab", "title": "Kata Pengantar"}
    if re.search(r'^\s*DAFTAR\s+ISI\b', text, re.IGNORECASE | re.MULTILINE):
        return {"type": "bab", "title": "Daftar Isi"}
    
    match_daftar = re.search(r'^\s*DAFTAR\s+(TABEL|GAMBAR)\b', text, re.IGNORECASE | re.MULTILINE)
    if match_daftar:
        return {"type": "bab", "title": f"Daftar {match_daftar.group(1).capitalize()}"}
        
    if re.search(r'^\s*DAFTAR\s+PUSTAKA\b', text, re.IGNORECASE | re.MULTILINE):
        return {"type": "bab", "title": "Daftar Pustaka"}
    if re.search(r'^\s*LAMPIRAN\b', text, re.IGNORECASE | re.MULTILINE):
        return {"type": "bab", "title": "Lampiran"}

    # 2. BAB Utama
    if re.search(r'^\s*BAB\s+I\b', text, re.IGNORECASE | re.MULTILINE):
        return {"type": "bab", "title": "BAB I Pendahuluan"}
    if re.search(r'^\s*BAB\s+II\b', text, re.IGNORECASE | re.MULTILINE):
        return {"type": "bab", "title": "BAB II Tinjauan Pustaka"}
    if re.search(r'^\s*BAB\s+III\b', text, re.IGNORECASE | re.MULTILINE):
        return {"type": "bab", "title": "BAB III Metodologi"}
    if re.search(r'^\s*BAB\s+IV\b', text, re.IGNORECASE | re.MULTILINE):
        return {"type": "bab", "title": "BAB IV Hasil dan Pembahasan"}
    if re.search(r'^\s*BAB\s+V\b', text, re.IGNORECASE | re.MULTILINE):
        return {"type": "bab", "title": "BAB V Kesimpulan"}

    # 3. Sub-sub-bab (Misal: 1.1.1 Latar Belakang Khusus)
    # Deteksi format digit berjenjang 3 tingkat di awal baris
    sub_sub_bab_match = re.search(r'^\s*([1-9]\.\d+\.\d+)\s+([A-Za-z][^\n\r]*)', text, re.MULTILINE)
    if sub_sub_bab_match:
        nomor = sub_sub_bab_match.group(1)
        judul = sub_sub_bab_match.group(2).strip()
        # Membatasi panjang judul agar ukuran metadata ideal
        if len(judul) > 60: judul = judul[:60] + "..."
        return {"type": "sub_sub_bab", "title": f"{nomor} {judul}"}

    # 4. Sub-bab (Misal: 1.1 Latar Belakang)
    # Deteksi format digit berjenjang 2 tingkat di awal baris
    sub_bab_match = re.search(r'^\s*([1-9]\.\d+)\s+([A-Za-z][^\n\r]*)', text, re.MULTILINE)
    if sub_bab_match:
        nomor = sub_bab_match.group(1)
        judul = sub_bab_match.group(2).strip()
        if len(judul) > 60: judul = judul[:60] + "..."
        return {"type": "sub_bab", "title": f"{nomor} {judul}"}

    return {"type": "unknown", "title": "Unknown"}


def assign_sections(pages: List[Dict]):

    current_bab = "Unknown"
    current_sub_bab = ""
    current_sub_sub_bab = ""

    for page in pages:

        detected = detect_section(page["text"])

        if detected["type"] == "bab":
            current_bab = detected["title"]
            current_sub_bab = ""      # Reset saat ganti bab
            current_sub_sub_bab = ""  # Reset saat ganti bab
        elif detected["type"] == "sub_bab":
            current_sub_bab = detected["title"]
            current_sub_sub_bab = ""  # Reset saat ganti sub bab
        elif detected["type"] == "sub_sub_bab":
            current_sub_sub_bab = detected["title"]

        page["bab"] = current_bab
        page["sub_bab"] = current_sub_bab
        page["sub_sub_bab"] = current_sub_sub_bab

    return pages