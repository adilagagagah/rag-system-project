from typing import List, Dict


def create_chunks(cleaned_pages: List[Dict], chunk_size: int = 800) -> List[Dict]:
    """
    Memotong teks menjadi bagian kecil (chunks) berdasarkan paragraf dan jumlah kata, 
    dengan tetap mempertahankan konteks halaman serta metadata BAB.
    """
    final_chunks = []
    
    for item in cleaned_pages:
        # 1. Logika split_paragraphs (filter paragraf pendek)
        paragraphs = [p.strip() for p in item["text"].split('\n') if len(p.strip()) > 50]
        
        # 2. Logika chunk_text
        current_chunk = ""
        chunk_index = 0
        
        for para in paragraphs:
            candidate = current_chunk + "\n" + para if current_chunk else para
            
            if len(candidate.split()) < chunk_size:
                current_chunk = candidate
            else:
                final_chunks.append({
                    "chunk_id": f"p{item['page']}-c{chunk_index}",
                    "page": item["page"],
                    "bab": item.get("bab", "Unknown"),
                    "sub_bab": item.get("sub_bab", ""),
                    "sub_sub_bab": item.get("sub_sub_bab", ""),
                    "content": current_chunk.strip()
                })
                chunk_index += 1
                current_chunk = para
                
        if current_chunk:
            final_chunks.append({
                "chunk_id": f"p{item['page']}-c{chunk_index}",
                "page": item["page"],
                "bab": item.get("bab", "Unknown"),
                "sub_bab": item.get("sub_bab", ""),
                "sub_sub_bab": item.get("sub_sub_bab", ""),
                "content": current_chunk.strip()
            })
            
    return final_chunks