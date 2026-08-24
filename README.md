# Vector-Seek


___
## Introduction
Vector-Seek is program that allow you to do this 2 incredible things:

First, to embed your text and make it vector. 
Second, to search not based by matching keywords, and instead by context and the meaning of the words

___
## What i learn from this project:

- Using External Library
- Creating my own data structure that contain things l
- Creating advance Data Pipelines
- Formatting

___
## Dependency

- Pytest
- Pytorcg
- Sentence Transformer

___
##  Flow Of Data (Personal Note) 

1. The data get read from src folder by read_from function

   file_package = {
        "from_file": file_path,
        "content": file_content,
    }
    list[dict[str, str]]


2. The list of file_package get parse into chunk of metadata by convert_file_dict_to_dict_metadata(this was in file_operator.py and a higher level function because markdown_to_metadata only accept markdown the (content of the file))

        chunk = {
            "from_file": file_name,
            "from_title": from_title,
            "chunk_id": index_num,
            "content": content.split("\n\n") # get splitted for paragraph
        }
    list[list[dict[str, str]]]

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