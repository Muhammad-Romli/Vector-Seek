import re

import re

def markdown_to_dict_metadata(file_name: str, markdown: str) -> list[dict[str, str | list[str] | None]]:
    list_of_chunk = []
    pattern = r"^(#{1,2}\s+.+)$"  # Thus
    matches = re.split(pattern, markdown, flags=re.MULTILINE)
    if len(matches) == 0 or matches == [""]:
        raise Exception("markdown is super empty")

    if matches[0].strip() != "":
        chunk = {
            "from_file": file_name,
            "from_title": None,
            "sub_title": None,
            "chunk_id": 0,
            "content": matches[0].split("\n\n") # Get splitted for each double /n for more readability
        }
        chunk["content"] = content_cleansing(chunk["content"])
        list_of_chunk.append(chunk)

    index_num = 1
    current_title = None
    current_subtitle = None

    for i in range(1, len(matches), 2):
        header = matches[i].strip()
        content = matches[i + 1] if i + 1 < len(matches) else ""

        if header.startswith("##"):
            current_subtitle = header.strip()
        else:
            current_title = header.strip()
            current_subtitle = None  # new H1 resets any previous H2 scope

        chunk = {
            "from_file": file_name,
            "from_title": current_title,
            "sub_title": current_subtitle,
            "chunk_id": index_num,
            "content": content.split("\n\n") # Get splitted for each double /n for more readability
        }

        index_num += 1
        chunk["content"] = content_cleansing(chunk["content"])
        if not chunk["content"]:
            continue
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