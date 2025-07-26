import os
import pickle
import faiss
import sqlite3
from embedder import Embedder
from datetime import datetime

INDEX_PATH = "Aaryan_store/index.faiss"
META_PATH = "Aaryan_store/meta.pkl"
DB_PATH = "Aaryan_database.db"

embedder = Embedder()

def fts_search(query, top_k=5):
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute('''
            SELECT filename, path FROM documents_fts
            WHERE documents_fts MATCH ?
            LIMIT ?
        ''', (query, top_k))
        rows = c.fetchall()

    results = []
    for filename, path in rows:
        if os.path.exists(path):
            modified_time = os.path.getmtime(path)
            results.append({
                "filename": filename,
                "path": path,
                "modified": datetime.fromtimestamp(modified_time).strftime("%Y-%m-%d %H:%M:%S"),
                "score": "FTS5"
            })
    return results

def search_documents(query, top_k=5):
    if not os.path.exists(INDEX_PATH) or not os.path.exists(META_PATH):
        return fts_search(query, top_k)

    index = faiss.read_index(INDEX_PATH)
    with open(META_PATH, "rb") as f:
        paths = pickle.load(f)

    vector = embedder.embed_texts([query])
    faiss.normalize_L2(vector)

    D, I = index.search(vector, top_k * 2)

    results = []
    for i, score in zip(I[0], D[0]):
        if i < len(paths):
            path = paths[i]
            if os.path.exists(path):
                modified_time = os.path.getmtime(path)
                results.append({
                    "filename": os.path.basename(path),
                    "path": path,
                    "modified": datetime.fromtimestamp(modified_time).strftime("%Y-%m-%d %H:%M:%S"),
                    "score": round(float(1 - score), 4)  # similarity instead of distance
                })
        if len(results) == top_k:
            break

    if not results:
        print("⚠️ No FAISS results found. Falling back to FTS5...")
        return fts_search(query, top_k)

    return results
