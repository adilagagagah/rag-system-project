import os
import sys
import pandas as pd
from tqdm import tqdm

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(ROOT_DIR)

from src.ingest_pdf import extract_pdf
from src.clean_text import clean_text
from src.section_tagging import assign_sections
from src.chunking import create_chunks

ALLOWED_BABS = {
    "BAB I Pendahuluan",
    "BAB II Tinjauan Pustaka",
    "BAB III Metodologi",
    "BAB IV Hasil dan Pembahasan",
    "BAB V Kesimpulan"
}

# Konfigurasi path sesuai struktur folder baru
RAW_DATA_PATH = os.path.normpath(os.path.join(ROOT_DIR, "data", "raw", "Skripsi Cetak_Gagah Pusoko Adilaga.pdf"))
PROCESSED_DATA_PATH = os.path.normpath(os.path.join(ROOT_DIR, "data", "processed", "processed_data.parquet"))

def main():
    # 1. Ingestion 
    print("--- Tahap 1: Ingesting PDF ---")
    pages = extract_pdf(RAW_DATA_PATH)
    if pages:
        print(f"\n[DEBUG] Contoh Ingestion (Page {pages[20]['page']}):\n{pages[20]['text']}\n")
    if pages and len(pages) > 0:
        idx = min(20, len(pages) - 1)
        print(f"\n[DEBUG] Contoh Ingestion (Page {pages[idx]['page']}):\n{pages[idx]['text'][:200]}...\n")
    
    # 2. Cleaning 
    print("--- Tahap 2: Cleaning Text ---")
    cleaned_pages = []
    for p in tqdm(pages):
        cleaned_content = clean_text(p["text"])
        if cleaned_content:
            cleaned_pages.append({"page": p["page"], "text": cleaned_content})
            
    if cleaned_pages:
        print(f"\n[DEBUG] Contoh Cleaning (Page {cleaned_pages[18]['page']}):\n{cleaned_pages[18]['text']}\n")
    if cleaned_pages and len(cleaned_pages) > 0:
        idx = min(18, len(cleaned_pages) - 1)
        print(f"\n[DEBUG] Contoh Cleaning (Page {cleaned_pages[idx]['page']}):\n{cleaned_pages[idx]['text'][:200]}...\n")
            
    # 3. Section Tagging
    print("--- Tahap 3: Section Tagging ---")
    cleaned_pages = assign_sections(cleaned_pages)
    cleaned_pages = [page for page in cleaned_pages if page["bab"] in ALLOWED_BABS]
    if cleaned_pages:
        print(f"\n[DEBUG] Contoh Section Tagging (Page {cleaned_pages[18]['page']}): BAB -> {cleaned_pages[18].get('bab', 'Unknown')} | Sub-bab -> {cleaned_pages[18].get('sub_bab', '')}\n")
    if cleaned_pages and len(cleaned_pages) > 0:
        idx = min(18, len(cleaned_pages) - 1)
        print(f"\n[DEBUG] Contoh Section Tagging (Page {cleaned_pages[idx]['page']}): BAB -> {cleaned_pages[idx].get('bab', 'Unknown')} | Sub-bab -> {cleaned_pages[idx].get('sub_bab', '')}\n")

    # 4. Chunking 
    print("--- Tahap 4 Creating Chunks ---")
    chunks = create_chunks(cleaned_pages)
    if chunks:
        print(f"\n[DEBUG] Contoh Chunking (Chunk {chunks[20]['chunk_id']}):\n{chunks[20]['content']}\n")
    if chunks and len(chunks) > 0:
        idx = min(20, len(chunks) - 1)
        print(f"\n[DEBUG] Contoh Chunking (Chunk {chunks[idx]['chunk_id']}):\n{chunks[idx]['content'][:200]}...\n")
    
    # 5. Storage (Data Layer) 
    print(f"--- Tahap 5: Saving {len(chunks)} chunks to Parquet ---")
    df = pd.DataFrame(chunks)
    
    os.makedirs(os.path.dirname(PROCESSED_DATA_PATH), exist_ok=True)
    df.to_parquet(PROCESSED_DATA_PATH, index=False)
    
    print(f"✅ ETL Selesai! Data siap di: {PROCESSED_DATA_PATH}")

if __name__ == "__main__":
    main()