from sentence_transformers import SentenceTransformer
import numpy as np
import json

def metadata_to_vector(metadatas: list[dict[str | None, list[str] | None]]):
    contents = [] 
    all_embed_metadatas = []

    for data in metadatas:
        content = data["content"]
        contents.append(content)
    model = SentenceTransformer("all-MiniLM-L6-v2")
    embeddings = model.encode(
        contents,
        batch_size = 4,
        show_progress_bar=True
    )

    for i in range(len(embeddings) - 1):
        embed_metadata = format_embed_metadata(i, contents[i], embeddings[i])
        all_embed_metadatas.append(embed_metadata)
    
    with open("embeddings.json", "w", encoding="utf-8") as f:
        json.dump(all_embed_metadatas, f)


def format_embed_metadata(id, chunk, embedding) -> dict[str, str]:
    embed_metadata = {
        "id": id,
        "chunk": chunk,
        "embedding": embedding.tolist(),
    }
    return embed_metadata