import numpy as np

class MusicRetriever:
    """
    Simulates a vector database for musical retrieval.
    Stores embeddings and performs similarity search.
    """
    def __init__(self):
        # In-memory storage for our "vectors"
        # Maps ID (filename) -> Vector (numpy array)
        self.index = {}
        
    def add_item(self, item_id, vector):
        """
        Adds a musical item to the index.
        
        Args:
            item_id (str): Unique identifier (e.g., filename).
            vector (np.array): Embedding vector.
        """
        self.index[item_id] = vector
        
    def search(self, query_vector, k=3):
        """
        Finds the k most similar items to the query vector.
        
        Args:
            query_vector (np.array): The embedding of the query input.
            k (int): Number of results to return.
            
        Returns:
            list: List of tuples (item_id, similarity_score).
        """
        results = []
        
        # Iterate through every item in our "database"
        # In a real system (FAISS, Pinecone), this would be optimized
        for item_id, vector in self.index.items():
            # Calculate Cosine Similarity
            # Since vectors are already normalized (length=1) in the Embedder,
            # Cosine Similarity is just the Dot Product.
            # a . b = |a||b|cos(theta) -> if |a|=|b|=1 -> a . b = cos(theta)
            similarity = np.dot(query_vector, vector)
            
            results.append((item_id, similarity))
            
        # Sort results by similarity score in descending order (highest match first)
        results.sort(key=lambda x: x[1], reverse=True)
        
        # Return the top k results
        return results[:k]
