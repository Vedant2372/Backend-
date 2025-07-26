import sqlite3
import os

DB_PATH = "Aaryan_database.db"

def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True) if os.path.dirname(DB_PATH) else None
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS documents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                filename TEXT,
                path TEXT UNIQUE,
                extension TEXT,
                size INTEGER,
                modified REAL
            )
        ''')
        conn.execute('''
            CREATE VIRTUAL TABLE IF NOT EXISTS documents_fts USING fts5(
                filename, path, content
            )
        ''')

def insert_documents(docs: dict):
    with sqlite3.connect(DB_PATH) as conn:
        inserted = 0
        for path, meta in docs.items():
            try:
                conn.execute('''
                    INSERT OR REPLACE INTO documents
                    (filename, path, extension, size, modified)
                    VALUES (?, ?, ?, ?, ?)
                ''', (
                    meta["filename"], path,
                    meta["extension"], meta["size"], meta["modified"]
                ))
                conn.execute('''
                    INSERT INTO documents_fts (filename, path, content)
                    VALUES (?, ?, ?)
                ''', (
                    meta["filename"], path, meta.get("content", "")
                ))
                inserted += 1
            except Exception as e:
                print(f"[DB ERROR] {e}")
        conn.commit()
    return inserted
