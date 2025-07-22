import os
import json
import requests
import time
from flask import Flask
from embedder import scan_and_parse_documents

USER_HOME = os.path.expanduser("~")
FOLDERS_TO_SCAN = [
    "C:\\",   # ✅ Full C drive scan with filtering
    "D:\\"    # ✅ Full D drive scan with filtering
]

# ✅ Skip these absolute root folders
EXCLUDE_DIRS = [
    "C:\\Windows",
    "C:\\Program Files",
    "C:\\Program Files (x86)",
    "C:\\$Recycle.Bin",
    os.path.join(USER_HOME, "AppData")
]

SCAN_STATUS_PATH = "../signals/scan_status.json"
INDEXER_API_URL = "http://127.0.0.1:5002/index"

app = Flask(__name__)

# ✅ Check if path starts with any excluded root dir
def is_excluded(path):
    return any(path.startswith(ex_dir) for ex_dir in EXCLUDE_DIRS)

def write_scan_status(status):
    os.makedirs(os.path.dirname(SCAN_STATUS_PATH), exist_ok=True)
    with open(SCAN_STATUS_PATH, "w") as f:
        json.dump({"status": status}, f)

def run_auto_scan():
    print("📡 Auto-scan started...")
    start = time.time()
    total_files = {}

    for folder in FOLDERS_TO_SCAN:
        if os.path.exists(folder):
            print(f"🔍 Scanning {folder}...")
            parsed = scan_and_parse_documents(folder, is_excluded)
            total_files.update(parsed)
        else:
            print(f"[!] Folder not found: {folder}")

    print(f"✅ Auto-scan complete. {len(total_files)} files found.")
    print(f"⏱ Scan took {round(time.time() - start, 2)}s")
    write_scan_status("complete")

    try:
        print("📤 Sending documents to indexer service...")
        response = requests.post(INDEXER_API_URL, json={"parsed_docs": total_files})
        print(f"🧠 Indexer response: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"[!] Failed to connect to indexer: {e}")

# 🚀 Auto-scan when Flask starts
run_auto_scan()

@app.route("/")
def index():
    return "📁 Reader Service is running and sent documents to indexer."

if __name__ == "__main__":
    app.run(port=5001)
