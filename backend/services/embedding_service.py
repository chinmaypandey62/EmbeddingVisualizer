"""
Embedding service for similarity calculations and vector operations.
"""
import logging
from typing import List, Tuple, Optional

import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

from backend.services.model_loader import model_loader

logger = logging.getLogger(__name__)


class EmbeddingService:
    """
    Service for embedding operations including similarity lookup.
    """
    
    def __init__(self):
        self.loader = model_loader
    
    def get_similar_words_tfidf(
        self, 
        word: str, 
        topn: int = 10
    ) -> Tuple[List[Tuple[str, float]], bool, Optional[str]]:
        """
        Get similar words using TF-IDF LSA embeddings.
        
        Returns:
            Tuple of (similar_words, in_vocabulary, error_message)
        """
        word = word.lower().strip()
        
        try:
            vocab = self.loader.get_tfidf_vocab()
            embeddings = self.loader.get_tfidf_embeddings()
            idx_to_word = self.loader.get_tfidf_idx_to_word()
            
            if word not in vocab:
                return [], False, f"Word '{word}' not found in TF-IDF vocabulary"
            
            word_idx = vocab[word]
            word_vector = embeddings[word_idx].reshape(1, -1)
            
            # Calculate cosine similarity with all words
            similarities = cosine_similarity(word_vector, embeddings)[0]
            
            # Get top N similar words (excluding the word itself)
            top_indices = similarities.argsort()[::-1]
            
            results = []
            for idx in top_indices:
                if len(results) >= topn:
                    break
                if idx != word_idx:
                    similar_word = idx_to_word[idx]
                    similarity_score = float(similarities[idx])
                    results.append((similar_word, similarity_score))
            
            return results, True, None
            
        except Exception as e:
            logger.error(f"Error in TF-IDF similarity: {e}")
            return [], False, str(e)
    
    def get_similar_words_word2vec(
        self, 
        word: str, 
        model_type: str = "word2vec_cbow",
        topn: int = 10
    ) -> Tuple[List[Tuple[str, float]], bool, Optional[str]]:
        """
        Get similar words using Word2Vec model.
        
        Args:
            word: Query word
            model_type: "word2vec_cbow" or "word2vec_skipgram"
            topn: Number of similar words to return
            
        Returns:
            Tuple of (similar_words, in_vocabulary, error_message)
        """
        word = word.lower().strip()
        
        try:
            if model_type == "word2vec_cbow":
                model = self.loader.get_word2vec_cbow()
            elif model_type == "word2vec_skipgram":
                model = self.loader.get_word2vec_skipgram()
            else:
                return [], False, f"Unknown model type: {model_type}"
            
            if word not in model.wv:
                return [], False, f"Word '{word}' not found in {model_type} vocabulary"
            
            # Get most similar words
            similar = model.wv.most_similar(word, topn=topn)
            results = [(w, float(score)) for w, score in similar]
            
            return results, True, None
            
        except Exception as e:
            logger.error(f"Error in Word2Vec similarity: {e}")
            return [], False, str(e)
    
    def get_similar_words(
        self, 
        word: str, 
        model_type: str = "tfidf",
        topn: int = 10
    ) -> Tuple[List[Tuple[str, float]], bool, Optional[str]]:
        """
        Get similar words for any model type.
        
        Args:
            word: Query word
            model_type: "tfidf", "word2vec_cbow", or "word2vec_skipgram"
            topn: Number of similar words to return
            
        Returns:
            Tuple of (similar_words, in_vocabulary, error_message)
        """
        if model_type == "tfidf":
            return self.get_similar_words_tfidf(word, topn)
        elif model_type in ["word2vec_cbow", "word2vec_skipgram"]:
            return self.get_similar_words_word2vec(word, model_type, topn)
        else:
            return [], False, f"Unknown model type: {model_type}"
    
    def get_word_vector(
        self, 
        word: str, 
        model_type: str = "tfidf"
    ) -> Optional[np.ndarray]:
        """
        Get the embedding vector for a word.
        
        Args:
            word: The word to get vector for
            model_type: Model type
            
        Returns:
            Numpy array of the word vector, or None if not found
        """
        word = word.lower().strip()
        
        try:
            if model_type == "tfidf":
                vocab = self.loader.get_tfidf_vocab()
                embeddings = self.loader.get_tfidf_embeddings()
                
                if word not in vocab:
                    return None
                
                return embeddings[vocab[word]]
                
            elif model_type == "word2vec_cbow":
                model = self.loader.get_word2vec_cbow()
                if word not in model.wv:
                    return None
                return model.wv[word]
                
            elif model_type == "word2vec_skipgram":
                model = self.loader.get_word2vec_skipgram()
                if word not in model.wv:
                    return None
                return model.wv[word]
                
        except Exception as e:
            logger.error(f"Error getting word vector: {e}")
            return None
        
        return None
    
    def get_all_embeddings(
        self, 
        model_type: str = "tfidf",
        num_words: int = 500
    ) -> Tuple[np.ndarray, List[str]]:
        """
        Get embeddings for top N most frequent words.
        
        Args:
            model_type: Model type
            num_words: Number of words to include
            
        Returns:
            Tuple of (embeddings matrix, list of words)
        """
        frequencies = self.loader.get_word_frequencies()
        
        if model_type == "tfidf":
            vocab = self.loader.get_tfidf_vocab()
            embeddings = self.loader.get_tfidf_embeddings()
            
            # Get top words by frequency
            vocab_with_freq = [(w, frequencies.get(w, 0)) for w in vocab.keys()]
            vocab_with_freq.sort(key=lambda x: x[1], reverse=True)
            top_words = [w for w, _ in vocab_with_freq[:num_words]]
            
            # Get embeddings for these words
            indices = [vocab[w] for w in top_words]
            selected_embeddings = embeddings[indices]
            
            return selected_embeddings, top_words
            
        elif model_type in ["word2vec_cbow", "word2vec_skipgram"]:
            if model_type == "word2vec_cbow":
                model = self.loader.get_word2vec_cbow()
            else:
                model = self.loader.get_word2vec_skipgram()
            
            # Get top words by frequency that are in the model
            all_words = list(model.wv.key_to_index.keys())
            vocab_with_freq = [(w, frequencies.get(w, 0)) for w in all_words]
            vocab_with_freq.sort(key=lambda x: x[1], reverse=True)
            top_words = [w for w, _ in vocab_with_freq[:num_words]]
            
            # Get embeddings
            selected_embeddings = np.array([model.wv[w] for w in top_words])
            
            return selected_embeddings, top_words
        
        return np.array([]), []
    
    def compare_similarity(
        self, 
        word: str, 
        topn: int = 10
    ) -> dict:
        """
        Compare similarity results across all models.
        
        Args:
            word: Query word
            topn: Number of similar words per model
            
        Returns:
            Dictionary with results per model
        """
        results = {}
        
        for model_type in ["tfidf", "word2vec_cbow", "word2vec_skipgram"]:
            similar, in_vocab, message = self.get_similar_words(word, model_type, topn)
            results[model_type] = {
                "similar_words": [{"word": w, "similarity": s} for w, s in similar],
                "in_vocabulary": in_vocab,
                "message": message,
            }
        
        return results


# Global instance
embedding_service = EmbeddingService()
