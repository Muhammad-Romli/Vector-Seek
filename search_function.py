from sentence_transformers import SentenceTransformer
import numpy as np

def search_top_5(query: str, stored_metadatas: list[dict], num_of_top: int) -> list[dict]: #im very terrible at naming lol
    all_comparisons = []
    model = SentenceTransformer("all-MiniLM-L6-v2")
    embedded_query = model.encode(query)
    for metadata in stored_metadatas:
        comparison = cosine_similarity(embedded_query, metadata)
        all_comparisons.append(comparison)
    top_n_similarity = np.argsort(all_comparisons)[::-1]
    return top_n_similarity[num_of_top]


def cosine_similarity(chunk1, chunk2):
    dot_product = np.dot(chunk1, chunk2)
    return dot_product / (np.linalg.norm(chunk1) * np.linalg.norm(chunk2))