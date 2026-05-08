import os
import pandas as pd
from tqdm import tqdm
from ingest_pdf import extract_pdf
from clean_text import clean_text
from chunking import create_chunks

# Konfigurasi path sesuai struktur folder baru
RAW_DATA_PATH = "data/raw/Skripsi Cetak_Gagah Pusoko Adilaga.pdf"
PROCESSED_DATA_PATH = "data/processed/processed_data.parquet"

def main():
    # 1. Ingestion 
    print("--- Tahap 1: Ingesting PDF ---")
    pages = extract_pdf(RAW_DATA_PATH)
    if pages:
        print(f"\n[DEBUG] Contoh Ingestion (Page {pages[20]['page']}):\n{pages[20]['text'][:200]}...\n")
    
    # 2. Cleaning 
    print("--- Tahap 2: Cleaning Text ---")
    cleaned_pages = []
    for p in tqdm(pages):
        cleaned_content = clean_text(p["text"])
        if cleaned_content:
            cleaned_pages.append({"page": p["page"], "text": cleaned_content})
            
    if cleaned_pages:
        print(f"\n[DEBUG] Contoh Cleaning (Page {cleaned_pages[18]['page']}):\n{cleaned_pages[18]['text'][:200]}...\n")
            
    # 3. Chunking 
    print("--- Tahap 3: Creating Chunks ---")
    chunks = create_chunks(cleaned_pages)
    if chunks:
        print(f"\n[DEBUG] Contoh Chunking (Chunk {chunks[20]['chunk_id']}):\n{chunks[20]['content'][:200]}...\n")
    
    # 4. Storage (Data Layer) 
    print(f"--- Tahap 4: Saving {len(chunks)} chunks to Parquet ---")
    df = pd.DataFrame(chunks)
    
    os.makedirs(os.path.dirname(PROCESSED_DATA_PATH), exist_ok=True)
    df.to_parquet(PROCESSED_DATA_PATH, index=False)
    
    print(f"✅ ETL Selesai! Data siap di: {PROCESSED_DATA_PATH}")

if __name__ == "__main__":
    main()