from langchain_text_splitters import RecursiveCharacterTextSplitter
from typing import List, Dict

def create_chunks(cleaned_pages: List[Dict], chunk_size: int = 1000, chunk_overlap: int = 150) -> List[Dict]:
    """
    Memotong teks menjadi bagian kecil (chunks) dengan tetap mempertahankan konteks halaman.
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
        separators=["\n\n", "\n", " ", ""]
    )

    final_chunks = []
    for item in cleaned_pages:
        chunks = text_splitter.split_text(item["text"])
        for i, chunk in enumerate(chunks):
            final_chunks.append({
                "chunk_id": f"p{item['page']}-c{i}",
                "page": item["page"],
                "section": item.get("section", "Unknown"),
                "content": chunk
            })
    return final_chunks