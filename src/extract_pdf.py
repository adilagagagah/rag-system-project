#! pip install pymupdf
import fitz  

doc = fitz.open("data/raw/Skripsi Cetak_Gagah Pusoko Adilaga.pdf")
print(doc.page_count)

