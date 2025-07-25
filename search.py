# search_service/search.py

import faiss
import numpy as np
import pickle
import os

from query_embedder import QueryEmbedder

# File paths for FAISS index and metadata
INDEX_PATH = "vector_storeAaru/index.faiss"
META_PATH = "vector_storeAaru/meta.pkl"

# Load embedding model
embedder = QueryEmbedder()

def load_faiss_index():
    if os.path.exists(INDEX_PATH):
        print("📦 Loading FAISS index...")
        return faiss.read_index(INDEX_PATH)
    else:
        raise FileNotFoundError(f"FAISS index not found at {INDEX_PATH}")

def load_metadata():
    if os.path.exists(META_PATH):
        with open(META_PATH, "rb") as f:
            return pickle.load(f)
    else:
        raise FileNotFoundError(f"Metadata not found at {META_PATH}")

def search_documents(query: str, top_k: int = 5):
    print(f"🔍 Searching for: '{query}'")
    
    query_vector = embedder.embed_query(query).astype("float32")
    index = load_faiss_index()
    metadata = load_metadata()

    print(f"📦 FAISS index has {index.ntotal} vectors")
    print(f"📂 Metadata entries: {len(metadata)}")

    if index.ntotal == 0 or len(metadata) == 0:
        print("[!] FAISS or Metadata is empty.")
        return []

    distances, indices = index.search(query_vector, top_k)

    results = []
    for idx in indices[0]:
        if idx < len(metadata):
            print(f"✅ Match index {idx}: {metadata[idx]}")
            results.append(metadata[idx])

    return results


if __name__ == "__main__":
    query = input("🔍 Enter your search query: ")
    results = search_documents(query)
    print("\n📄 Top Results:")
    for path in results:
        print("➤", path)
