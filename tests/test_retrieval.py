import sys
import os

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(ROOT_DIR)

from src.retrieval import Retriever


retriever = Retriever()

query = "Apa itu regresi spline truncated?"

results = retriever.retrieve(query)

for i, doc in enumerate(results["documents"][0]):
    metadata = results["metadatas"][0][i]

    print("=" * 50)

    print(f"RESULT {i+1} | BAB: {metadata.get('bab', 'Unknown')} | PAGE: {metadata.get('page', 'Unknown')}")

    print(doc[:1000])