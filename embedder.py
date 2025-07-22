import os

# ✅ File extensions you want to index
ALLOWED_EXTENSIONS = {
    ".pdf", ".docx", ".txt", ".xlsx", ".pptx", ".csv",
    ".py", ".java", ".ipynb", ".db", ".sqlite"
}

# 🚫 Folder names (partial matches) to skip
EXCLUDED_DIRS = [
    "recycle", "system volume information", "windows", "program files",
    "programdata", "appdata", "temp", "logs", "venv", ".venv", "env", ".env",
    ".git", "node_modules", "__pycache__", ".cache", ".idea", ".vscode"
]

def is_valid_file(file_path):
    _, ext = os.path.splitext(file_path)
    return ext.lower() in ALLOWED_EXTENSIONS

def should_skip_folder(folder_path):
    folder_path_lower = folder_path.lower()
    return any(excl in folder_path_lower for excl in EXCLUDED_DIRS)

def scan_and_parse_documents(root_dir, external_exclude_func=None):
    parsed_docs = {}

    for dirpath, dirnames, filenames in os.walk(root_dir):
        # Modify the list in-place to skip unwanted folders
        dirnames[:] = [d for d in dirnames if not should_skip_folder(os.path.join(dirpath, d))]

        for file in filenames:
            file_path = os.path.join(dirpath, file)
            if external_exclude_func and external_exclude_func(file_path):
                continue
            if is_valid_file(file_path):
                parsed_docs[file_path] = {
                    "filename": file,
                    "path": file_path,
                    "modified": os.path.getmtime(file_path),
                    "type": os.path.splitext(file)[1][1:]
                }

    return parsed_docs
