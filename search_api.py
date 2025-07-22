# search_api.py
from flask import Flask, request, jsonify
from search import search_documents

app = Flask(__name__)

@app.route("/search")
def search():
    try:
        query = request.args.get("q", "")
        if not query:
            return jsonify({"error": "No query provided"}), 400

        print(f"🔍 Received query: {query}")
        results = search_documents(query)
        return jsonify({"results": results})
    
    except Exception as e:
        print("[SEARCH ERROR]", str(e))
        return jsonify({"error": "Internal Server Error", "details": str(e)}), 500

if __name__ == "__main__":
    print("🚀 Search Service is running...")
    app.run(port=5005)
