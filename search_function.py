from sentence_transformers import SentenceTransformer
from model_loader import get_model
import numpy as np

def search_top_similarities(query: str, stored_metadatas: list[dict], num_similarities_shown: int) -> list[dict]: #im very terrible at naming lol
    all_comparisons = []
    model = get_model()
    embedded_query = model.encode(query)
    for metadata in stored_metadatas:
        metadata_embedding = metadata["embedding"]
        comparison = cosine_similarity(embedded_query, metadata_embedding)
        all_comparisons.append(comparison)
    sorted_indices = np.argsort(all_comparisons)[::-1]
    top_indices = sorted_indices[:num_similarities_shown]
    return [stored_metadatas[i] for i in top_indices]


def cosine_similarity(chunk1, chunk2):
    dot_product = np.dot(chunk1, chunk2)
    return dot_product / (np.linalg.norm(chunk1) * np.linalg.norm(chunk2))


# search_top_similarities function return what in README.md Flow Of Data, number 3