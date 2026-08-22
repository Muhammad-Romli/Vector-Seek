import re

def markdown_to_dict_metadata(file_name: str, markdown: str) -> list[dict[str | None, str | list[str] | None]]:
    # Turning markdown into dict that contain the original
    list_of_chunk =  []
    pattern = r"^(#\s+.+)$"
    matches = re.split(pattern, markdown, flags=re.MULTILINE) # we will allow empty content so its doesn't break indexing for now
    if len(matches) ==  0 or matches == [""]:
        raise Exception("markdown is super empty")

    if matches[0].strip() != "":
        chunk = {
            "from_file": file_name,
            "from_title": None,
            "chunk_id": 0,
            "content": matches[0].split("\n\n") # get splitted for paragraph
        }
        chunk["content"] = content_cleansing(chunk["content"])
        list_of_chunk.append(chunk)


    index_num = 1
    for i in range(1, len(matches), 2): #we start iterating from index 1 because index 0 is already getting taken care of

        from_title = matches[i].strip()
        content = matches[i+1] if i + 1 < len(matches) else ""  #if it "" it will get turned to None later

        chunk = {
            "from_file": file_name,
            "from_title": from_title,
            "chunk_id": index_num,
            "content": content.split("\n\n") # get splitted for paragraph
        }

        index_num += 1
        chunk["content"] = content_cleansing(chunk["content"])
        if not chunk["content"]:
            chunk["content"] = [None]
        list_of_chunk.append(chunk)

    return list_of_chunk


def content_cleansing(contents: list[str])  -> list[str | None]:
    list_of_content = []
    for content in contents:
        content = content.strip()
        
        if not content or not any(c.isalnum for c in content): #this will skip if none of the content in the chunk id real word
            continue
        else:
            list_of_content.append(content)
    return list_of_content