# db_api.py

from flask import Flask, request, jsonify
import os
import sqlite3
from datetime import datetime

app = Flask(__name__)
DB_PATH = "doc_metadata.db"

def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            CREATE VIRTUAL TABLE IF NOT EXISTS documents USING fts5(
                filename,
                path,
                extension,
                size,
                indexed_on UNINDEXED
            )
        """)

def insert_metadata(documents: dict):
    inserted = 0
    with sqlite3.connect(DB_PATH) as conn:
        for path in documents.keys():
            if not os.path.exists(path):
                print(f"[DB SKIP] File not found: {path}")
                continue

            metadata = {
                "filename": os.path.basename(path),
                "path": path,
                "extension": os.path.splitext(path)[1],
                "size": os.path.getsize(path),
                "indexed_on": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }

            conn.execute(
                "INSERT INTO documents (filename, path, extension, size, indexed_on) VALUES (?, ?, ?, ?, ?)",
                (metadata["filename"], metadata["path"], metadata["extension"], metadata["size"], metadata["indexed_on"])
            )
            inserted += 1

        conn.commit()
    return inserted

@app.route("/add_metadata", methods=["POST"])
def add_metadata():
    data = request.json
    documents = data.get("documents", {})

    if not documents:
        return jsonify({"error": "No documents received"}), 400

    inserted_count = insert_metadata(documents)
    return jsonify({"message": f"{inserted_count} documents inserted."}), 200

if __name__ == "__main__":
    init_db()
    app.run(port=5004)
