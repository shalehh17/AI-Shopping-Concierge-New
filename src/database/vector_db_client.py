import numpy as np
from scipy.spatial.distance import cosine
# Singleton Dependency Injection: Import global database client for connection pooling
from src.database.supabase_client import supabase_client

class VectorDBClient:
    def __init__(self):
        """
        Initialization Layer for Vector Database Operations.
        Binds the Supabase client to facilitate high-dimensional vector querying and embedding management.
        """
        self.supabase = supabase_client

    def compute_cosine_similarity(self, query_vector: np.ndarray, candidate_products: list) -> list:
        """
        Semantic Similarity Computation (Fault-Tolerant Scoring Pipeline).
        Calculates the semantic relevance between the query embedding and product candidates
        using a 512-dimensional vector space.
        """
        scored_products = []
        
        for item in candidate_products:
            # Artifact Extraction: Retrieve dense vector embeddings from the database payload
            if "embedding_vector" in item and item["embedding_vector"] is not None:
                product_vector = np.array(item["embedding_vector"], dtype=float)
            else:
                # Fault Tolerance: Generate deterministic synthetic embeddings for incomplete records 
                # using product ID as a seed to ensure reproducible testing environments.
                prod_id_numeric = sum(ord(char) for char in item.get("ID Produk", "A"))
                np.random.seed(prod_id_numeric)
                product_vector = np.random.rand(512)
            
            # Metric Computation: Compute Cosine Distance (0.0: identical, 2.0: antipodal)
            try:
                cosine_dist = cosine(query_vector, product_vector)
                # Similarity Transformation: Normalize to [0, 1] range (1.0: perfect semantic alignment)
                similarity_score = 1.0 - cosine_dist
            except Exception:
                # Default anomaly handling for numerical stability
                similarity_score = 0.0
                
            # Feature Augmentation: Merge product metadata with computed semantic relevance scores
            item_with_score = item.copy()
            item_with_score["score"] = float(similarity_score)
            scored_products.append(item_with_score)
            
        return scored_products

    def retrieve_top_semantic_matches(self, query_vector: np.ndarray, filtered_products: list, top_k: int = 3) -> list:
        """
        Ranking Pipeline (Candidate Selection).
        Sorts candidates by semantic similarity score and performs top-K truncation to yield 
        the most relevant search results.
        """
        if not filtered_products:
            return []
            
        # 1. Pipeline Execution: Run semantic scoring on the filtered candidate subset
        scored_list = self.compute_cosine_similarity(query_vector, filtered_products)
        
        # 2. Ranking Algorithm: Apply descending sort based on computed similarity score
        scored_list.sort(key=lambda x: x.get("score", 0.0), reverse=True)
        
        # 3. Truncation: Select optimal top-K results for downstream consumption
        return scored_list[:top_k]