from query_sender import send_query
from utils import format_results

def cli():
    print("\n🧠 Welcome to Document Finder CLI!")
    while True:
        q = input("🔍 Enter search query (or 'exit'): ").strip()
        if q.lower() == "exit":
            break
        results = send_query(q)
        print(format_results(results))

if __name__ == "__main__":
    cli()