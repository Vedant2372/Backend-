import requests

def send_query(q):
    try:
        r = requests.get("http://127.0.0.1:5005/search", params={"q": q})
        return r.json().get("results", [])
    except Exception as e:
        print(f"[Query Error] {e}")
        return []