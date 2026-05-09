import sys
import os

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(ROOT_DIR)

from src.retrieval import Retriever


test_queries = [
    {
        "query": "Apa itu regresi spline truncated?",
        "expected_bab": "BAB II Tinjauan Pustaka"
    },
    {
        "query": "Bagaimana pemilihan bandwidth dilakukan?",
        "expected_bab": "BAB III Metodologi"
    },
    {
        "query": "Apa kesimpualn penelitian?",
        "expected_bab": "BAB V Kesimpulan"
    }
]


retriever = Retriever()

correct = 0

for test in test_queries:

    results = retriever.retrieve(
        test["query"],
        top_k=1
    )

    metadata = results["metadatas"][0][0]

    predicted_bab = metadata.get("bab", "")

    print("=" * 50)
    print("QUERY:", test["query"])
    print("EXPECTED:", test["expected_bab"])
    print("PREDICTED:", predicted_bab)

    if predicted_bab == test["expected_bab"]:
        correct += 1

accuracy = correct / len(test_queries)

print("\nHit@1:", accuracy)