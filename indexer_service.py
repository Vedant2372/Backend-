from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/index", methods=["POST"])
def index_documents():
    try:
        data = request.get_json()
        parsed_docs = data.get("parsed_docs", {})

        print(f"[INDEXER] Received {len(parsed_docs)} docs")

        # ▶ Place your indexing logic here
        # For example:
        from indexer import index_documents
        index_documents(parsed_docs)

        return jsonify({"message": "Indexed successfully", "count": len(parsed_docs)}), 200

    except Exception as e:
        import traceback
        print("[INDEXER ERROR]", str(e))
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    print("⚙️ Indexer Service running on port 5002")
    app.run(port=5002)
