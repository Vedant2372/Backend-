# search_service/query_embedder.py

from sentence_transformers import SentenceTransformer
import numpy as np

class QueryEmbedder:
    """
    Converts a natural language search query into a vector using a sentence transformer.
    """

    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        """
        Initialize the embedding model.
        
        Args:
            model_name (str): Pretrained model name to load from sentence-transformers.
        """
        print(f"🔍 Loading embedding model: {model_name}")
        self.model = SentenceTransformer(model_name)

    def embed_query(self, query: str) -> np.ndarray:
        """
        Embed a single query string into a vector.

        Args:
            query (str): The search query text.
        
        Returns:
            np.ndarray: A (1, 384) shaped numpy array vector.
        """
        embedding = self.model.encode([query])
        return np.array(embedding)
