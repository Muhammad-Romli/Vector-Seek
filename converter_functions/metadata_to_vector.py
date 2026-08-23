from sentence_transformers import SentenceTransformer
import json

def metadata_to_vector(list_of_metadatas: list[list[dict[str, str | list[str] | None]]]):
    contents = [] 
    all_embed_metadatas = []
    metadatas_without_content = []


    for metadatas in list_of_metadatas:
        for data in metadatas:
            content = data["content"]
            if isinstance(content, str):
                contents.append(content)
                metadata_wo_content = {k: v for k, v in data.items() if k != "content"}
                metadatas_without_content.append(metadata_wo_content)


            elif isinstance(content, list):
                for content_str in content:
                    contents.append(content_str)
                    metadata_wo_content = {k: v for k, v in data.items() if k != "content"}
                    metadatas_without_content.append(metadata_wo_content)
            else:
                raise Exception("what type are you even are?")

    model = SentenceTransformer("all-MiniLM-L6-v2")
    embeddings = model.encode(
        contents,
        batch_size = 4,
        show_progress_bar=True
    )

    for i in range(len(embeddings)):
        print(i)
        print(metadatas_without_content[i])
        embed_metadata = format_embed_metadata(i, contents[i], embeddings[i], metadatas_without_content[i])
        all_embed_metadatas.append(embed_metadata)

    with open("embeddings.json", "w", encoding="utf-8") as f:
        json.dump(all_embed_metadatas, f)


def format_embed_metadata(id, content, embedding, metadata) -> dict[str, str]:
    embed_metadata = {
        "id": id,
        "content": content,
        "embedding": embedding.tolist(),
        "metadata": metadata
    }
    return embed_metadata