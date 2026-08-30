from model_loader import get_model
import numpy as np


def encode_query(query: str):
    model = get_model()
    return model.encode(query)


def compare_vectors(embedded_query, stored_metadatas: list[dict], n: int) -> list[dict]:
    all_comparisons = []
    for metadata in stored_metadatas:
        metadata_embedding = metadata["embedding"]
        comparison = cosine_similarity(embedded_query, metadata_embedding)
        all_comparisons.append(comparison)
    sorted_indices = np.argsort(all_comparisons)[::-1]
    top_indices = sorted_indices[:n]
    return [stored_metadatas[i] for i in top_indices]


def search_top_similarities(query: str, stored_metadatas: list[dict], n: int) -> list[dict]:
    embedded_query = encode_query(query)
    return compare_vectors(embedded_query, stored_metadatas, n)


def cosine_similarity(chunk1, chunk2):
    dot_product = np.dot(chunk1, chunk2)
    return dot_product / (np.linalg.norm(chunk1) * np.linalg.norm(chunk2))


# search_top_similarities function return what in README.md Flow Of Data, number 3