from sentence_transformers import SentenceTransformer

class EmbeddingModel:
    def __init__(self, model_name: str = "intfloat/multilingual-e5-base"):
        self.model = SentenceTransformer(model_name)

    def get_embeddings(self, texts, prefix: str = "passage: "):

        prefixed = [
            f"{prefix}{t}"
            for t in texts
        ]

        return self.model.encode(
            prefixed,
            convert_to_numpy=True,
            show_progress_bar=True
        )