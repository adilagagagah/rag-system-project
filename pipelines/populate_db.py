import sys
import os

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(ROOT_DIR)

import pandas as pd
from src.embedding import EmbeddingModel
from src.vector_store import VectorStore

def main():
    # 1. Load data hasil ETL Minggu 1
    print("Loading processed data...")
    parquet_path = os.path.normpath(os.path.join(ROOT_DIR, "data", "processed", "processed_data.parquet"))
    df = pd.read_parquet(parquet_path)

    # 2. Inisialisasi Model & DB
    embed_model = EmbeddingModel()
    v_store = VectorStore()

    # 3. Generate Embeddings
    print("Generating embeddings (ini mungkin butuh waktu)...")
    embeddings = embed_model.get_embeddings(df['content'].tolist())

    # 4. Simpan ke Vector DB
    print("Upserting to Vector DB...")
    v_store.upsert_chunks(df, embeddings.tolist())
    print("✅ Vector Database berhasil dibuat!")

if __name__ == "__main__":
    main()