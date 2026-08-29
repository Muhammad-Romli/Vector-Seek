from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from search_function import search_top_similarities
from os_functions.file_operator import read_from, convert_file_dict_to_dict_metadata
from converter_functions.metadata_to_vector import metadata_to_vector
import json

app = FastAPI()

with open("embeddings.json", "r", encoding="utf-8") as json_file:
    metadata = json.load(json_file)

@app.get("/search")
def search(q: str, n: int = 5):
    results = search_top_similarities(q, metadata, n)
    return results

@app.post("/build")
def build():
    global metadata
    file_package = read_from() #if you dont want to use src_folder, just put the path of your folder relative to the root of project directory
    if file_package == None:
        raise HTTPException(status_code=400, detail="No files found to build from")
    package_of_metadatas = convert_file_dict_to_dict_metadata(file_package)
    metadata_to_vector(package_of_metadatas)
    with open("embeddings.json", "r", encoding="utf-8") as json_file:
        metadata = json.load(json_file)
    return {"status": "index built successfully"}


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "https://your-oculus-domain.com"],
    allow_methods=["*"],
    allow_headers=["*"],
)