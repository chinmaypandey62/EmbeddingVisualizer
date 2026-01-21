"""
Model loading service with lazy loading and caching.
"""
import logging
from typing import Optional, Dict, Any
from pathlib import Path

import numpy as np
import joblib
from gensim.models import Word2Vec

from backend.config import MODEL_PATHS, MODEL_TYPES

logger = logging.getLogger(__name__)


class ModelLoader:
    """
    Singleton service for loading and caching embedding models.
    Uses lazy loading to only load models when first accessed.
    """
    
    _instance: Optional["ModelLoader"] = None
    
    def __new__(cls) -> "ModelLoader":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        
        self._initialized = True
        self._models: Dict[str, Any] = {}
        self._tfidf_vocab: Optional[Dict[str, int]] = None
        self._tfidf_idx_to_word: Optional[Dict[int, str]] = None
        self._tfidf_embeddings: Optional[np.ndarray] = None
        self._word_frequencies: Optional[Dict[str, int]] = None
        
        logger.info("ModelLoader initialized")
    
    def _load_tfidf_models(self) -> None:
        """Load TF-IDF related models and embeddings."""
        if self._tfidf_embeddings is not None:
            return
        
        logger.info("Loading TF-IDF models...")
        
        # Load word embeddings (LSA reduced)
        embeddings_path = MODEL_PATHS["tfidf_word_embeddings"]
        if embeddings_path.exists():
            self._tfidf_embeddings = np.load(str(embeddings_path))
            logger.info(f"Loaded TF-IDF embeddings: {self._tfidf_embeddings.shape}")
        else:
            raise FileNotFoundError(f"TF-IDF embeddings not found: {embeddings_path}")
        
        # Load vocabulary mapping
        vocab_path = MODEL_PATHS["tfidf_vocab"]
        if vocab_path.exists():
            self._tfidf_vocab = joblib.load(str(vocab_path))
            self._tfidf_idx_to_word = {idx: word for word, idx in self._tfidf_vocab.items()}
            logger.info(f"Loaded TF-IDF vocabulary: {len(self._tfidf_vocab)} words")
        else:
            raise FileNotFoundError(f"TF-IDF vocabulary not found: {vocab_path}")
    
    def _load_word2vec_model(self, model_type: str) -> Word2Vec:
        """Load a Word2Vec model (CBOW or Skip-Gram)."""
        if model_type in self._models:
            return self._models[model_type]
        
        logger.info(f"Loading {model_type} model...")
        
        model_path = MODEL_PATHS[model_type]
        if model_path.exists():
            model = Word2Vec.load(str(model_path))
            self._models[model_type] = model
            logger.info(f"Loaded {model_type}: {len(model.wv)} words, {model.wv.vector_size} dimensions")
            return model
        else:
            raise FileNotFoundError(f"Word2Vec model not found: {model_path}")
    
    def _load_word_frequencies(self) -> Dict[str, int]:
        """Load word frequency counts."""
        if self._word_frequencies is not None:
            return self._word_frequencies
        
        freq_path = MODEL_PATHS["word_frequencies"]
        if freq_path.exists():
            self._word_frequencies = joblib.load(str(freq_path))
            logger.info(f"Loaded word frequencies: {len(self._word_frequencies)} words")
            return self._word_frequencies
        else:
            logger.warning(f"Word frequencies not found: {freq_path}")
            return {}
    
    def get_tfidf_embeddings(self) -> np.ndarray:
        """Get TF-IDF word embeddings matrix."""
        self._load_tfidf_models()
        return self._tfidf_embeddings
    
    def get_tfidf_vocab(self) -> Dict[str, int]:
        """Get TF-IDF word-to-index vocabulary."""
        self._load_tfidf_models()
        return self._tfidf_vocab
    
    def get_tfidf_idx_to_word(self) -> Dict[int, str]:
        """Get TF-IDF index-to-word mapping."""
        self._load_tfidf_models()
        return self._tfidf_idx_to_word
    
    def get_word2vec_cbow(self) -> Word2Vec:
        """Get Word2Vec CBOW model."""
        return self._load_word2vec_model("word2vec_cbow")
    
    def get_word2vec_skipgram(self) -> Word2Vec:
        """Get Word2Vec Skip-Gram model."""
        return self._load_word2vec_model("word2vec_skipgram")
    
    def get_word_frequencies(self) -> Dict[str, int]:
        """Get word frequency counts."""
        return self._load_word_frequencies()
    
    def get_model_info(self, model_type: str) -> Dict[str, Any]:
        """Get information about a specific model."""
        try:
            if model_type == "tfidf":
                self._load_tfidf_models()
                return {
                    "model_type": model_type,
                    "display_name": MODEL_TYPES[model_type],
                    "vocab_size": len(self._tfidf_vocab),
                    "vector_dimensions": self._tfidf_embeddings.shape[1],
                    "is_loaded": True,
                }
            elif model_type in ["word2vec_cbow", "word2vec_skipgram"]:
                model = self._load_word2vec_model(model_type)
                return {
                    "model_type": model_type,
                    "display_name": MODEL_TYPES[model_type],
                    "vocab_size": len(model.wv),
                    "vector_dimensions": model.wv.vector_size,
                    "is_loaded": True,
                }
            else:
                return {
                    "model_type": model_type,
                    "display_name": "Unknown",
                    "vocab_size": 0,
                    "vector_dimensions": 0,
                    "is_loaded": False,
                }
        except FileNotFoundError as e:
            logger.error(f"Model not found: {e}")
            return {
                "model_type": model_type,
                "display_name": MODEL_TYPES.get(model_type, "Unknown"),
                "vocab_size": 0,
                "vector_dimensions": 0,
                "is_loaded": False,
            }
    
    def get_all_models_info(self) -> list:
        """Get information about all available models."""
        return [self.get_model_info(model_type) for model_type in MODEL_TYPES.keys()]
    
    def is_word_in_vocab(self, word: str, model_type: str) -> bool:
        """Check if a word is in the vocabulary of a model."""
        word = word.lower().strip()
        
        if model_type == "tfidf":
            self._load_tfidf_models()
            return word in self._tfidf_vocab
        elif model_type == "word2vec_cbow":
            model = self.get_word2vec_cbow()
            return word in model.wv
        elif model_type == "word2vec_skipgram":
            model = self.get_word2vec_skipgram()
            return word in model.wv
        
        return False
    
    def get_vocabulary_sample(self, model_type: str, n: int = 50) -> list:
        """Get a sample of words from the vocabulary."""
        frequencies = self.get_word_frequencies()
        
        if model_type == "tfidf":
            self._load_tfidf_models()
            vocab = list(self._tfidf_vocab.keys())
        elif model_type in ["word2vec_cbow", "word2vec_skipgram"]:
            model = self._load_word2vec_model(model_type)
            vocab = list(model.wv.key_to_index.keys())
        else:
            return []
        
        # Sort by frequency if available, otherwise return first N
        if frequencies:
            vocab_with_freq = [(w, frequencies.get(w, 0)) for w in vocab]
            vocab_with_freq.sort(key=lambda x: x[1], reverse=True)
            return [w for w, _ in vocab_with_freq[:n]]
        
        return vocab[:n]


# Global instance
model_loader = ModelLoader()
