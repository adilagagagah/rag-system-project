import fitz
from typing import List, Dict

# cek data
# doc = fitz.open("data/raw/Skripsi Cetak_Gagah Pusoko Adilaga.pdf")
# print(doc.page_count)

# fungsi ekstrak pdf
def extract_pdf(path:str) -> List[Dict]:
    doc = fitz.open(path)
    pages = []

    for i, page in enumerate(doc):
        text = page.get_text("text")

        pages.append({
            "page" : i+1,
            "text" : text
        })

    doc.close()
    return pages

if __name__ == "__main__":
    pdf_path = "data/raw/Skripsi Cetak_Gagah Pusoko Adilaga.pdf"

    pages = extract_pdf(pdf_path)

    print(f"Total pages extracted: {len(pages)}")
    print(pages[0])
    print(pages[20])
