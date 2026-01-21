"""
Dimensionality reduction service for PCA and t-SNE.
"""
import logging
from typing import List, Tuple, Optional
import hashlib

import numpy as np
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE

from backend.services.embedding_service import embedding_service
from backend.services.model_loader import model_loader
from backend.config import DEFAULT_PERPLEXITY

logger = logging.getLogger(__name__)


class DimensionalityReductionService:
    """
    Service for reducing high-dimensional embeddings to 2D for visualization.
    Includes caching for performance.
    """
    
    def __init__(self):
        self.embedding_service = embedding_service
        self.loader = model_loader
        self._cache = {}  # Cache for reduced embeddings
    
    def _get_cache_key(
        self, 
        model_type: str, 
        method: str, 
        num_words: int,
        perplexity: int = DEFAULT_PERPLEXITY
    ) -> str:
        """Generate a cache key for the reduction parameters."""
        key_str = f"{model_type}_{method}_{num_words}_{perplexity}"
        return hashlib.md5(key_str.encode()).hexdigest()
    
    def reduce_pca(
        self, 
        embeddings: np.ndarray,
        n_components: int = 2
    ) -> np.ndarray:
        """
        Reduce embeddings using PCA.
        
        Args:
            embeddings: High-dimensional embeddings matrix
            n_components: Number of output dimensions
            
        Returns:
            Reduced embeddings
        """
        logger.info(f"Applying PCA reduction: {embeddings.shape} -> {n_components}D")
        
        pca = PCA(n_components=n_components, random_state=42)
        reduced = pca.fit_transform(embeddings)
        
        logger.info(f"PCA explained variance ratio: {pca.explained_variance_ratio_.sum():.4f}")
        
        return reduced
    
    def reduce_tsne(
        self, 
        embeddings: np.ndarray,
        n_components: int = 2,
        perplexity: int = DEFAULT_PERPLEXITY
    ) -> np.ndarray:
        """
        Reduce embeddings using t-SNE.
        
        Args:
            embeddings: High-dimensional embeddings matrix
            n_components: Number of output dimensions
            perplexity: t-SNE perplexity parameter
            
        Returns:
            Reduced embeddings
        """
        # Adjust perplexity if needed (must be < n_samples)
        n_samples = embeddings.shape[0]
        adjusted_perplexity = min(perplexity, max(5, (n_samples - 1) // 3))
        
        logger.info(f"Applying t-SNE reduction: {embeddings.shape} -> {n_components}D (perplexity={adjusted_perplexity})")
        
        try:
            # Try newer sklearn API first
            tsne = TSNE(
                n_components=n_components,
                perplexity=adjusted_perplexity,
                random_state=42,
                n_iter=1000,
                init='random'  # 'pca' can fail with some data
            )
            reduced = tsne.fit_transform(embeddings)
        except Exception as e:
            logger.error(f"t-SNE failed: {e}")
            # Fallback to PCA if t-SNE fails
            logger.info("Falling back to PCA")
            reduced = self.reduce_pca(embeddings, n_components)
        
        return reduced
    
    def get_reduced_embeddings(
        self,
        model_type: str = "tfidf",
        method: str = "pca",
        num_words: int = 500,
        perplexity: int = DEFAULT_PERPLEXITY,
        use_cache: bool = True
    ) -> Tuple[np.ndarray, List[str], List[int]]:
        """
        Get reduced 2D embeddings for visualization.
        
        Args:
            model_type: Model type ("tfidf", "word2vec_cbow", "word2vec_skipgram")
            method: Reduction method ("pca" or "tsne")
            num_words: Number of words to include
            perplexity: t-SNE perplexity (only used if method="tsne")
            use_cache: Whether to use cached results
            
        Returns:
            Tuple of (2D coordinates, word list, frequencies)
        """
        cache_key = self._get_cache_key(model_type, method, num_words, perplexity)
        
        # Check cache
        if use_cache and cache_key in self._cache:
            logger.info(f"Using cached reduction for {model_type}/{method}/{num_words}")
            return self._cache[cache_key]
        
        # Get embeddings
        embeddings, words = self.embedding_service.get_all_embeddings(model_type, num_words)
        
        if len(words) == 0:
            logger.warning(f"No embeddings found for {model_type}")
            return np.array([]), [], []
        
        # Apply dimensionality reduction
        if method == "pca":
            reduced = self.reduce_pca(embeddings)
        elif method == "tsne":
            reduced = self.reduce_tsne(embeddings, perplexity=perplexity)
        else:
            raise ValueError(f"Unknown reduction method: {method}")
        
        # Get word frequencies
        frequencies = self.loader.get_word_frequencies()
        word_freqs = [frequencies.get(w, 0) for w in words]
        
        # Cache result
        result = (reduced, words, word_freqs)
        self._cache[cache_key] = result
        
        return result
    
    def get_word_neighborhood(
        self,
        word: str,
        model_type: str = "tfidf",
        method: str = "pca",
        num_neighbors: int = 20,
        perplexity: int = DEFAULT_PERPLEXITY
    ) -> Tuple[np.ndarray, List[str], List[float]]:
        """
        Get 2D coordinates for a word and its nearest neighbors.
        
        Args:
            word: Query word
            model_type: Model type
            method: Reduction method
            num_neighbors: Number of neighbors to include
            perplexity: t-SNE perplexity
            
        Returns:
            Tuple of (2D coordinates, word list, similarity scores)
        """
        # Get similar words
        similar_words, in_vocab, _ = self.embedding_service.get_similar_words(
            word, model_type, num_neighbors
        )
        
        if not in_vocab:
            return np.array([]), [], []
        
        # Get the word itself plus neighbors
        words = [word] + [w for w, _ in similar_words]
        similarities = [1.0] + [s for _, s in similar_words]
        
        # Get vectors for all words
        vectors = []
        valid_words = []
        valid_similarities = []
        
        for w, sim in zip(words, similarities):
            vec = self.embedding_service.get_word_vector(w, model_type)
            if vec is not None:
                vectors.append(vec)
                valid_words.append(w)
                valid_similarities.append(sim)
        
        if len(vectors) < 2:
            return np.array([]), [], []
        
        embeddings = np.array(vectors)
        
        # Apply reduction
        if method == "pca":
            reduced = self.reduce_pca(embeddings)
        else:
            # For small sets, use lower perplexity
            adj_perplexity = min(perplexity, max(2, len(vectors) // 3))
            reduced = self.reduce_tsne(embeddings, perplexity=adj_perplexity)
        
        return reduced, valid_words, valid_similarities
    
    def clear_cache(self) -> None:
        """Clear the reduction cache."""
        self._cache.clear()
        logger.info("Dimensionality reduction cache cleared")


# Global instance
dimensionality_service = DimensionalityReductionService()
