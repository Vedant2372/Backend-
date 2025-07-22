import requests

def send_query_to_api(query):
    try:
        response = requests.get(f"http://127.0.0.1:5005/search?q={query}")
        response.raise_for_status()
        data = response.json()
        return data.get("results", [])
    except Exception as e:
        print(f"[ERROR] Failed to get results from search API: {e}")
        return []
