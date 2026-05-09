import chromadb
import pandas as pd
import os

class VectorStore:
    def __init__(self, db_path: str = "storage/vector_db"):
        # Konversi ke path absolut & normalkan slashes untuk mencegah [WinError 123] di Windows
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        full_db_path = os.path.normpath(os.path.join(base_dir, db_path))
        
        self.client = chromadb.PersistentClient(path=full_db_path)
        self.collection = self.client.get_or_create_collection(name="skripsi_rag")

    def upsert_chunks(self, df: pd.DataFrame, embeddings: list):
        """Menyimpan chunks dan metadata ke ChromaDB"""
        ids = df['chunk_id'].tolist()
        documents = df['content'].tolist()
        
        # Menyertakan page, bab, sub_bab, dan sub_sub_bab ke dalam metadata
        babs = df.get('bab', ['Unknown'] * len(df)).tolist()
        sub_babs = df.get('sub_bab', [''] * len(df)).tolist()
        sub_sub_babs = df.get('sub_sub_bab', [''] * len(df)).tolist()

        metadatas = [
            {"page": int(p), "bab": str(b), "sub_bab": str(sb), "sub_sub_bab": str(ssb)}
            for p, b, sb, ssb in zip(df['page'].tolist(), babs, sub_babs, sub_sub_babs)
        ]

        self.collection.upsert(
            ids=ids,
            embeddings=embeddings,
            documents=documents,
            metadatas=metadatas
        )

    def query(self, query_embedding: list, n_results: int = 3):
        return self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results
        )