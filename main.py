import asyncio
import base64
import queue
import shutil
import tempfile
import threading
import numpy as np
from pathlib import Path

from fastapi import FastAPI, HTTPException, UploadFile, File, Form, Body, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from search_function import search_top_similarities, compare_vectors
from model_loader import get_model
from os_functions.file_operator import read_from, convert_file_dict_to_dict_metadata
from converter_functions.metadata_to_vector import metadata_to_vector, embed_chunks_and_query
import json

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:3000", "https://muhammad-romli.github.io/Oculus/index.html"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Guardrails so a big/careless upload can't choke a free-tier server.
MAX_FILE_SIZE = 5 * 1024 * 1024    # 5 MB per file
MAX_TOTAL_SIZE = 20 * 1024 * 1024  # 20 MB per upload

model_lock = threading.Lock()


def load_metadata():
    with open("embeddings.json", "r", encoding="utf-8") as json_file:
        return json.load(json_file)


metadata = load_metadata()


# /search-demo just search through my shared folder which is about animals
@app.get("/search-demo")
def search(q: str, n: int = 5):
    with model_lock:
        results = search_top_similarities(q, metadata, n)
    return results


@app.post("/search-by-vector")
def search_by_vector(vector: list[float] = Body(...), n: int = 5):
    expected_dim = get_model().get_embedding_dimension()
    if len(vector) != expected_dim:
        raise HTTPException(400, f"vector must have {expected_dim} dimensions, got {len(vector)}")
    embedded_query = np.array(vector)
    with model_lock:
        results = compare_vectors(embedded_query, metadata, n)
    return results


@app.post("/search-by-file")
def search_by_file(file: UploadFile = File(...), q: str = Form(...), n: int = 5):
    data = file.file.read()
    if len(data) > MAX_FILE_SIZE:
        raise HTTPException(400, f"{file.filename} exceeds the {MAX_FILE_SIZE // (1024 * 1024)} MB limit")

    tmp_dir = tempfile.mkdtemp(prefix="vector-seek-search-")
    try:
        if file.filename is None:
            raise HTTPException(400, "File is no where to be found")
        (Path(tmp_dir) / file.filename).write_bytes(data)
        file_package = read_from(tmp_dir)

        if file_package is None:
            raise HTTPException(400, "No usable content found in upload")

        package_of_metadatas = convert_file_dict_to_dict_metadata(file_package)

        with model_lock:
            chunk_metadatas, query_vector = embed_chunks_and_query(package_of_metadatas, q)
            results = compare_vectors(query_vector, chunk_metadatas, n)

        return results
    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)


@app.post("/build")
def build():
    """Admin's tool: build from shared 'src' folder and overwrite the
    shared embeddings.json. Don't wire the public build.html page to
    this endpoint; see /ws/build-preview below for the visitor-facing
    version.
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
    """Kept for backwards compatibility / non-JS clients.
    The progress-reporting version build.html actually uses is
    /ws/build-preview below.
    """
    total_size = 0
    file_bytes = []

    for f in files:
        data = f.file.read()
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

        return embeddings
    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)


def _write_upload_to_tmp(tmp_dir: str, filename: str, content_b64: str):
    data = base64.b64decode(content_b64)
    if len(data) > MAX_FILE_SIZE:
        raise ValueError(f"{filename} exceeds the {MAX_FILE_SIZE // (1024 * 1024)} MB per-file limit")
    (Path(tmp_dir) / filename).write_bytes(data)
    return len(data)


@app.websocket("/ws/build-preview")
async def build_preview_ws(websocket: WebSocket):
    """
    Client sends one JSON message to start:
        { "files": [ { "filename": "a.txt", "content_base64": "..." }, ... ] }
    Server sends zero or more:
        { "type": "progress", "current": N, "total": N }
    then exactly one of:
        { "type": "done", "result": [...] }
        { "type": "build_error", "detail": "..." }

    How the progress actually gets streamed: the blocking embedding
    work runs on a background thread, which only ever does
    queue.put(...) (thread-safe, no event loop involved). This async
    handler is the only thing that ever awaits — it just polls the
    queue and forwards whatever it finds to the browser.
    """
    await websocket.accept()
    payload = await websocket.receive_json()
    files = payload.get("files", [])

    tmp_dir = tempfile.mkdtemp(prefix="vector-seek-preview-")
    progress_queue: "queue.Queue" = queue.Queue()

    def on_progress(current, total):
        progress_queue.put({"type": "progress", "current": current, "total": total})

    def worker():
        try:
            total_size = 0
            for f in files:
                total_size += _write_upload_to_tmp(tmp_dir, f["filename"], f["content_base64"])
                if total_size > MAX_TOTAL_SIZE:
                    raise ValueError(f"Upload exceeds the {MAX_TOTAL_SIZE // (1024 * 1024)} MB total limit")

            file_package = read_from(tmp_dir)
            if file_package is None:
                raise ValueError("No usable files found in upload")

            package_of_metadatas = convert_file_dict_to_dict_metadata(file_package)

            with model_lock:
                result = metadata_to_vector(package_of_metadatas, output_path=None, on_progress=on_progress)

            progress_queue.put({"type": "done", "result": result})
        except Exception as e:
            progress_queue.put({"type": "build_error", "detail": str(e)})

    thread = threading.Thread(target=worker, daemon=True)
    thread.start()

    try:
        while True:
            try:
                msg = progress_queue.get_nowait()
            except queue.Empty:
                await asyncio.sleep(0.1)
                continue
            await websocket.send_json(msg)
            if msg["type"] in ("done", "build_error"):
                break
        thread.join()
    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)
        await websocket.close()