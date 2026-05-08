from src.embedding import EmbeddingModel
from src.vector_store import VectorStore


class Retriever:

    def __init__(self):
        self.embedding_model = EmbeddingModel()
        self.vector_store = VectorStore()

    def retrieve(
        self,
        query,
        top_k=5
    ):
        # get_embeddings mengembalikan sebuah list berisi embedding (numpy array)
        query_embedding_list = self.embedding_model.get_embeddings(
            [query]
        )
        # Ambil embedding pertama (dan satu-satunya) dari list
        query_embedding = query_embedding_list[0]

        results = self.vector_store.query(
            # Embedding perlu diubah ke format list untuk metode query
            query_embedding=query_embedding.tolist(),
            n_results=top_k
        )

        return results