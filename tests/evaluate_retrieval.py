import sys
import os

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(ROOT_DIR)

from src.retrieval import Retriever


test_queries = [
    {
        "query": "Berapa rata-rata Angka Harapan Hidup di Indonesia pada tahun 2019-2023?",
        "expected_bab": "BAB I Pendahuluan"
    },
    {
        "query": "Apa yang dimaksud dengan Angka Harapan Hidup (AHH)?",
        "expected_bab": "BAB II Tinjauan Pustaka"
    },
    {
        "query": "Bagaimana kriteria kebaikan model berdasarkan nilai R-squared menurut Chin?",
        "expected_bab": "BAB II Tinjauan Pustaka"
    },
    {
        "query": "Berapa proporsi pembagian data in-sample dan out-sample yang digunakan dalam penelitian?",
        "expected_bab": "BAB III Metodologi"
    },
    {
        "query": "Apa saja variabel prediktor yang digunakan dalam penelitian ini?",
        "expected_bab": "BAB III Metodologi"
    },
    {
        "query": "Berapa nilai Cross Validation (CV) terkecil yang diperoleh dari model terbaik?",
        "expected_bab": "BAB IV Hasil dan Pembahasan"
    },
    {
        "query": "Berapa nilai koefisien determinasi dan MAPE dari model terbaik?",
        "expected_bab": "BAB IV Hasil dan Pembahasan"
    },
    {
        "query": "Apa kesimpulan dari penelitian mengenai model regresi nonparametrik campuran terbaik?",
        "expected_bab": "BAB V Kesimpulan"
    }
]

def main():
    retriever = Retriever()

    metrics = {
        "Hit@1": 0,
        "Hit@3": 0,
        "Hit@5": 0
    }

    print("=== Evaluasi Retrieval ===")
    
    for idx, test in enumerate(test_queries, 1):
        results = retriever.retrieve(test["query"], top_k=5)
        
        retrieved_metadatas = results.get("metadatas", [[]])[0]
        retrieved_babs = [meta.get("bab", "") for meta in retrieved_metadatas]
        
        expected = test["expected_bab"]
        
        hit_at_1 = expected in retrieved_babs[:1]
        hit_at_3 = expected in retrieved_babs[:3]
        hit_at_5 = expected in retrieved_babs[:5]
        
        if hit_at_1: metrics["Hit@1"] += 1
        if hit_at_3: metrics["Hit@3"] += 1
        if hit_at_5: metrics["Hit@5"] += 1
        
        print(f"\nQuery {idx}: {test['query']}")
        print(f"Expected: {expected}")
        print(f"Predicted Top 5: {retrieved_babs}")
        print(f"Match: Hit@1: {hit_at_1} | Hit@3: {hit_at_3} | Hit@5: {hit_at_5}")

    total_queries = len(test_queries)
    print("\n" + "="*50)
    print("=== SUMMARY METRICS ===")
    print(f"Total Queries: {total_queries}")
    print(f"Hit@1 Accuracy: {metrics['Hit@1'] / total_queries * 100:.2f}%")
    print(f"Hit@3 Accuracy: {metrics['Hit@3'] / total_queries * 100:.2f}%")
    print(f"Hit@5 Accuracy: {metrics['Hit@5'] / total_queries * 100:.2f}%")
    print("="*50)

if __name__ == "__main__":
    main()