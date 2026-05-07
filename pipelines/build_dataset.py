import os
import pandas as pd
from tqdm import tqdm

from pipelines.ingest_pdf import extract_pdf
from pipelines.clean_text import clean_text


pdf_path = "data/raw/Skripsi Cetak_Gagah Pusoko Adilaga.pdf"

print("1. Extracting PDF...")
pages = extract_pdf(pdf_path)

print("2. Cleaning text...")
print(pages[20])
pages[20]["text"] = clean_text(pages[20]["text"])
