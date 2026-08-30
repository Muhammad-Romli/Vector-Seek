import shutil
import tempfile
import threading
from pathlib import Path

from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from search_function import search_top_similarities, compare_vectors
from os_functions.file_operator import read_from, convert_file_dict_to_dict_metadata
from converter_functions.metadata_to_vector import metadata_to_vector, embed_chunks_and_query
import json

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "https://muhammad-romli.github.io/Oculus/index.html"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Guardrails so a big/careless upload can't choke a free-tier server.
# (What i even thinking making semantic-search on free-tier server)
MAX_FILE_SIZE = 5 * 1024 * 1024    # 5 MB per file
MAX_TOTAL_SIZE = 20 * 1024 * 1024  # 20 MB per upload

# If we use plain def FastAPI
model_lock = threading.Lock()


def load_metadata():
    with open("embeddings.json", "r", encoding="utf-8") as json_file:
        return json.load(json_file)


metadata = load_metadata()


@app.get("/search")
def search(q: str, n: int = 5):
    with model_lock:
        results = search_top_similarities(q, metadata, n)
    return results


@app.post("/build")
def build():
    """This is admin's tool is build from shared 'src' folder
    and then overwrite the shared embeddings.json.
    Don't wire the public build.html page to this endpoint; see
    /build-preview below for the visitor-facing version.
    """
    global metadata
    file_package = read_from()
    if file_package is None:
        raise HTTPException(status_code=400, detail="No files found to build from")
    package_of_metadatas = convert_file_dict_to_dict_metadata(file_package)
    with model_lock:
        metadata_to_vector(package_of_metadatas)
    metadata = load_metadata()
    return {"status": "index built successfully"}


@app.post("/build-preview")
def build_preview(files: list[UploadFile] = File(...)):
    """Visitor-facing 'try it yourself' build.

    Writes the upload into a throwaway temp folder, reuses read_from()
    (which already recurses into subfolders on its own) pointed at
    that folder, and returns the embeddings directly in the response.
    Never touches embeddings.json or the shared `metadata` used by
    /search, and the temp folder is always deleted afterward.
    """
    total_size = 0
    file_bytes = []

    for f in files:
        data = f.file.read()  # sync read — fine here since this is a sync `def` endpoint
        if len(data) > MAX_FILE_SIZE:
            raise HTTPException(400, f"{f.filename} exceeds the {MAX_FILE_SIZE // (1024 * 1024)} MB per-file limit")
        total_size += len(data)
        if total_size > MAX_TOTAL_SIZE:
            raise HTTPException(400, f"Upload exceeds the {MAX_TOTAL_SIZE // (1024 * 1024)} MB total limit")
        file_bytes.append((f.filename, data))

    tmp_dir = tempfile.mkdtemp(prefix="vector-seek-preview-")
    try:
        for filename, data in file_bytes:
            (Path(tmp_dir) / filename).write_bytes(data)

        file_package = read_from(tmp_dir)
        if file_package is None:
            raise HTTPException(status_code=400, detail="No usable files found in upload")

        package_of_metadatas = convert_file_dict_to_dict_metadata(file_package)

        with model_lock:
            embeddings = metadata_to_vector(package_of_metadatas, output_path=None)

        return embeddings  # goes straight back to the browser, saved nowhere on the server

    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)