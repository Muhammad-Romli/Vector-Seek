# Vector-Seek

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Status](https://img.shields.io/badge/status-complete-brightgreen)
![License](https://img.shields.io/badge/license-MIT-lightgrey)

A semantic search engine that embeds text into vectors and retrieves results by **meaning**, not keyword matching.

## Table of Contents
- [Introduction](#introduction)
- [What I Learned](#what-i-learned)
- [Dependencies](#dependencies)
- [Installation](#installation)
- [Project Structure](#project-structure)
- [How to Use](#how-to-use)
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

## Installation

Clone the repo and set up a virtual environment:

```bash
git clone https://github.com/<your-username>/vector-seek.git
cd vector-seek
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

Install PyTorch as a **CPU-only build first**, before installing `sentence-transformers`. If you skip this step, `pip` will pull the default PyTorch build with CUDA/GPU dependencies bundled in — several GB of packages you don't need on a CPU-only setup:

```bash
pip install torch --index-url https://download.pytorch.org/whl/cpu
pip install sentence-transformers
pip install pytest
```

## Project Structure

The project splits cleanly into two halves: **Building** (turning raw files into searchable vectors) and **Searching** (querying those vectors). Keeping these mentally separate made debugging significantly easier.

```
vector-seek/
├── src/                  # Drop your input files/data here
├── build.sh              # Runs the Building pipeline
├── search.sh             # Runs the Searching pipeline
├── file_operator.py      # read_from, convert_file_dict_to_dict_metadata
├── embeddings.json        # Stored vector embeddings (output of Building)
└── tests/                # pytest test suite
```

**Building pipeline:**
1. `read_from` — reads raw files from `src/`
2. `convert_file_dict_to_dict_metadata` — parses files into metadata chunks
3. `metadata_to_vector` — embeds each chunk and stores it

**Searching pipeline:**
1. Get user input (the search query)
2. `search_top_similarities` — compares the query embedding against stored vectors
3. `format_top_similarities` — formats and prints the results

## How to Use

1. Put the files/data you want to search into `src/`.
2. Run the build step to generate embeddings:
   ```bash
   ./build.sh
   ```
3. Run a search:
   ```bash
   ./search.sh "your query here"
   ```
   Use the `-n` flag to control how many results are returned (default varies — check your `argparse` setup):
   ```bash
   ./search.sh "your query here" -n 3
   ```

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
