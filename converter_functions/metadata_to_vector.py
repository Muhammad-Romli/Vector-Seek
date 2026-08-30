from model_loader import get_model
import numpy as np # The numpy is already imported somewhere in the infrastructure, so this cost nothing
import json

# This function is the one that the CLI build.sh run from
def metadata_to_vector(
    list_of_metadatas: list[list[dict[str, str | list[str] | None]]],
    output_path: str | None = "embeddings.json"
) -> list[dict[str, str]]:
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

    model = get_model()
    embeddings = model.encode(
        contents,
        batch_size=4,
        show_progress_bar=True
    )

    for i in range(len(embeddings)):
        print(i)
        print(metadatas_without_content[i])
        embed_metadata = format_embed_metadata(i, contents[i], embeddings[i], metadatas_without_content[i])
        all_embed_metadatas.append(embed_metadata)

    # output_path=None means "don't touch disk" — used by the
    # visitor-facing preview build so it never writes to the
    # server's shared embeddings.json.
    if output_path is not None:
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(all_embed_metadatas, f)

    return all_embed_metadatas


# This function is made for the web version specifically for search-by-text-file option
def embed_chunks_and_query(
    list_of_metadatas: list[list[dict[str, str | list[str] | None]]],
    query: str
) -> tuple[list[dict[str, str]], np.ndarray]:
    
    contents = []
    metadatas_without_content = [] 

    for metadatas in list_of_metadatas:
        for data in metadatas:
            content = data["content"]
            if isinstance(content, str):
                contents.append(content)
                metadatas_without_content.append({k: v for k, v in data.items() if k != "content"})
            elif isinstance(content, list):
                for content_str in content:
                    contents.append(content_str)
                    metadatas_without_content.append({k: v for k, v in data.items() if k != "content"})

    contents.append(query)  # appending the qwery to contents so is get embedding at one go

    model = get_model()
    embeddings = model.encode(contents, batch_size=4, show_progress_bar=True)

    query_embedding = embeddings[-1]
    chunk_embeddings = embeddings[:-1]

    all_embed_metadatas = [
        format_embed_metadata(i, contents[i], chunk_embeddings[i], metadatas_without_content[i])
        for i in range(len(chunk_embeddings))
    ]

    return all_embed_metadatas, query_embedding


def format_embed_metadata(id, content, embedding, metadata) -> dict[str, str]:
    embed_metadata = {
        "id": id,
        "content": content,
        "embedding": embedding.tolist(),
        "metadata": metadata
    }
    return embed_metadata