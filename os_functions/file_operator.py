import os
import json
from converter_functions.markdown_converter import markdown_to_dict_metadata

def read_from(path: str="src") -> list[dict[str, str]] | None:
    list_of_file_dict = []

    if not os.path.exists(path):
        raise FileNotFoundError
    
    if os.path.isfile(path):
        file_package = read_from_file(path) 
        list_of_file_dict.append(file_package)
        return list_of_file_dict

    # the path is guaranteed to be directory at this point, so we can run os.listdir safely
    all_files = os.listdir(path)
    if len(all_files) == 0:
        return None 

    for file_in_dir in all_files:
        item_path = os.path.join(path, file_in_dir)
        if os.path.isdir(item_path):
            nested_files =  read_from(item_path)
            if not nested_files:
                continue # because the folder empty we may as well just go to next file/folder
            list_of_file_dict.extend(nested_files)

        elif os.path.isfile(item_path):
            file_package = read_from_file(item_path)
            list_of_file_dict.append(file_package)
    return list_of_file_dict

def read_from_file(file_path: str) -> dict[str, str]:
    with open(file_path, "r", encoding="utf-8") as file:
        file_content =  file.read()
    file_package = {
        "from_file": file_path,
        "content": file_content,
    }
    return file_package

def convert_file_dict_to_dict_metadata(list_of_file_dict: list[dict[str,str | None]]) -> list[list[dict[str | None, str | list[str] | None]]]:
    # each dict that gonna be returned is list of dict that that contain from_file, from_title, and splitted content
    list_of_dict_metadata = []
    for dict in list_of_file_dict:
        file_name = dict["from_file"]
        file_content = dict["content"]
        dict_metadata = markdown_to_dict_metadata(file_name, file_content)
        dict_metadata: list[dict[str, list[str] | None]]
        list_of_dict_metadata.append(dict_metadata)
    return list_of_dict_metadata