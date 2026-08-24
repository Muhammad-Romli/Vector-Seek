# Vector-Seek

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Status](https://img.shields.io/badge/status-complete-brightgreen)
![License](https://img.shields.io/badge/license-MIT-lightgrey)

A semantic search engine that embeds text into vectors and retrieves results by **meaning**, not keyword matching.

## Table of Contents
- [Introduction](#introduction)
- [What I Learned](#what-i-learned)
- [Dependencies](#dependencies)
- [Data Flow](#data-flow)
- [Preview](#preview)

## Introduction

Vector-Seek does two things:

1. **Embeds** your text — turns raw content into vectors.
2. **Searches** by context and meaning, instead of exact keyword matches.

## What I Learned

- Working with external libraries (`sentence-transformers`, `numpy`)
- Designing custom data structures that carry metadata through a pipeline
- Building multi-stage data pipelines
- Structuring and documenting a real project

## Dependencies

| Library | Purpose |
|---|---|
| `pytest` | Testing |
| `sentence-transformers` | Generating embeddings |
| `numpy` | Cosine similarity math |

## Data Flow

<details>
<summary><strong>1. Read files from <code>src/</code></strong></summary>

```python
file_package = {
    "from_file": file_path,
    "content": file_content,
}
# list[dict[str, str]]
```
</details>

<details>
<summary><strong>2. Parse into metadata chunks</strong></summary>

`convert_file_dict_to_dict_metadata()` (in `file_operator.py`) wraps `markdown_to_metadata`, since the lower-level function only accepts raw markdown content:

```python
chunk = {
    "from_file": file_name,
    "from_title": from_title,
    "chunk_id": index_num,
    "content": content.split("\n\n"),  # split by paragraph
}
# list[list[dict[str, str]]]
```
</details>

<details>
<summary><strong>3. Embed and store</strong></summary>

```python
embed_metadata = {
    "id": id,
    "content": content,
    "embedding": embedding.tolist(),
    "metadata": metadata,  # chunk without content
}
```
</details>

## Preview

#### Video

*(coming soon)*

#### Screenshots

*(coming soon)*
