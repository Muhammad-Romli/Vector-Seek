# Vector-Seek


![Python](https://img.shields.io/badge/Python-3.11-blue)




![Status](https://img.shields.io/badge/status-in--progress-yellow)



___

## Table of contents

- [Introduction]($introduction) 
- [What I Learned]($what-i-learned) 
- [Dependencies]($dependencies) 
- [Data Flow]($data-flow) 
- [Preview]($preview) 


## Introduction

Vector-Seek does two things:

1. **Embeds** your text — turns raw content into vectors.
2. **Searches** by context and meaning, instead of exact keyword matches.


## What I Learned

- Working with external libraries (`sentence-transformers`, `numpy`)
- Designing custom data structures that carry metadata through a pipeline
- Building multi-stage data pipelines
- Structuring and documenting a real project without guide


## Dependencies

| Library | Purpose |
|---|---|
| `pytest` | Testing |
| `sentence-transformers` | Generating embeddings |
| `numpy` | Cosine similarity math |

___
## Data Flow

<details>
<summary><strong>1. Read files from <code>src/</code></strong></summary>

`read_from()` returns a list of file packages:

```python
file_package = {
    "from_file": file_path,
    "content": file_content,
}
# list[dict[str, str]]


<details>
<summary><strong>1. Parse into metadata chunks</strong></scontent

convert_file_dict_to_dict_metadata() (in file_operator.py) wraps markdown_to_metadata, since the lower-level function only accepts raw markdown content:

        ```chunk = {
    "from_file": file_name,
    "from_title": from_title,
    "chunk_id": index_num,
    "content": content.split("\n\n"),  # split by paragraph
}
# list[list[dict[str, str]]]```


3. We gonna turn the list of list of metadata into embeddings and then stored it in embeddings.json
    embed_metadata = {
        "id": id,
        "content": content,
        "embedding": embedding.tolist(),
        "metadata": metadata
    }
    where metadata is chunk without content, an

___

## Preview:

##### *-Video:*


##### *-Screenshots:*