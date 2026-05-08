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
        
        # Menyertakan page dan section ke dalam metadata
        sections = df.get('section', ['Unknown'] * len(df)).tolist()
        metadatas = [{"page": int(p), "section": str(s)} for p, s in zip(df['page'].tolist(), sections)]

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