"""
Semantic similarity service module.
Handles semantic similarity calculations between messages.
"""

import logging
from typing import Optional

import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

logger = logging.getLogger(__name__)

class SemanticSimilarityService:
    """Service for calculating semantic similarity between text using embeddings."""
    
    def __init__(self, model_name: str = 'all-MiniLM-L6-v2'):
        """
        Initialize the semantic similarity service.
        
        Args:
            model_name: Name of the sentence transformer model to use
        """
        try:
            self.model = SentenceTransformer(model_name)
            logger.info(f"Loaded semantic similarity model: {model_name}")
        except Exception as e:
            logger.error(f"Failed to load semantic similarity model: {e}")
            self.model = None
    
    def calculate_similarity(self, text1: str, text2: str) -> Optional[float]:
        """
        Calculate semantic similarity between two texts using cosine similarity.
        
        Args:
            text1: First text to compare
            text2: Second text to compare
            
        Returns:
            Similarity score between 0 and 1, or None if calculation fails
        """
        if not self.model:
            logger.error("Semantic similarity model not loaded")
            return None
        
        try:
            # Encode the texts to get their embeddings
            embeddings = self.model.encode([text1, text2], convert_to_tensor=True)
            
            # Convert to numpy and calculate cosine similarity
            embedding1 = embeddings[0].cpu().numpy().reshape(1, -1)
            embedding2 = embeddings[1].cpu().numpy().reshape(1, -1)
            
            sim_score = cosine_similarity(embedding1, embedding2)[0][0]
            return float(sim_score)
        except Exception as e:
            logger.error(f"Error calculating semantic similarity: {e}")
            return None
    
    def check_message_diversity(self, new_message: str, previous_messages: list) -> dict:
        """
        Check how diverse a new message is compared to previous messages.
        
        Args:
            new_message: The new message to check
            previous_messages: List of previous messages to compare against
            
        Returns:
            Dictionary containing similarity scores and diversity assessment
        """
        if not previous_messages:
            return {
                "is_diverse": True,
                "similarity_scores": [],
                "average_similarity": 0.0,
                "max_similarity": 0.0
            }
        
        similarity_scores = []
        for prev_msg in previous_messages:
            sim_score = self.calculate_similarity(new_message, prev_msg)
            if sim_score is not None:
                similarity_scores.append(sim_score)
        
        if not similarity_scores:
            return {
                "is_diverse": True,
                "similarity_scores": [],
                "average_similarity": 0.0,
                "max_similarity": 0.0
            }
        
        avg_similarity = np.mean(similarity_scores)
        max_similarity = max(similarity_scores)
        
        # Consider message diverse if maximum similarity is below threshold
        # Typical threshold values range from 0.7-0.85 depending on desired diversity
        is_diverse = max_similarity < 0.75
        
        return {
            "is_diverse": is_diverse,
            "similarity_scores": similarity_scores,
            "average_similarity": float(avg_similarity),
            "max_similarity": float(max_similarity)
        }