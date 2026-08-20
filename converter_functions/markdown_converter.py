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
            "title": None,
            "content": matches[0].split("\n\n") # get splitted for paragraph
        }
        chunk["content"] = content_cleansing(chunk["content"])
        list_of_chunk.append(chunk)


    for i in range(1, len(matches), 2): #we start iterating from index 1 because index 0 is already getting taken care of
        title = matches[i].strip()
        content = matches[i+1] if i + 1 < len(matches) else ""  #if it "" it will get turned to None later

        chunk = {
            "from_file": file_name,
            "title": title,
            "content": content.split("\n\n") # get splitted for paragraph
        }

        chunk["content"] = content_cleansing(chunk["content"])
        list_of_chunk.append(chunk)

    return list_of_chunk


def content_cleansing(contents: list[str])  -> list[str | None]:
    list_of_content = []
    for content in contents:
        stripped_content = content.strip()
        if not stripped_content:
            continue
        if not stripped_content:
            list_of_content.append(None)
        else:
            list_of_content.append(stripped_content)
    return list_of_content