"""
Configuration settings for the Embedding Explorer backend.
"""
import os
from pathlib import Path

# Base paths
BASE_DIR = Path(__file__).resolve().parent.parent
MODELS_DIR = BASE_DIR / "models"

# Model file paths
MODEL_PATHS = {
    "tfidf_vectorizer": MODELS_DIR / "tfidf_vectorizer.pkl",
    "tfidf_word_embeddings": MODELS_DIR / "tfidf_word_embeddings.npy",
    "tfidf_svd": MODELS_DIR / "tfidf_svd.pkl",
    "tfidf_vocab": MODELS_DIR / "tfidf_vocab.pkl",
    "word2vec_cbow": MODELS_DIR / "word2vec_cbow.model",
    "word2vec_skipgram": MODELS_DIR / "word2vec_skipgram.model",
    "word_frequencies": MODELS_DIR / "word_frequencies.pkl",
}

# API Configuration
API_HOST = os.getenv("API_HOST", "127.0.0.1")
API_PORT = int(os.getenv("API_PORT", 8000))
API_PREFIX = "/api"

# CORS settings
# CORS settings - Allow Streamlit Cloud and local development
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "").split(",") if os.getenv("CORS_ORIGINS") else [
    "http://localhost:8501",  # Streamlit default
    "http://127.0.0.1:8501",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "https://*.streamlit.app",  # Streamlit Cloud
]

# Dimensionality reduction settings
DEFAULT_REDUCTION_METHOD = "pca"  # "pca" or "tsne"
DEFAULT_NUM_WORDS = 500  # Default number of words for visualization
MAX_NUM_WORDS = 2000  # Maximum words for visualization
DEFAULT_PERPLEXITY = 30  # t-SNE perplexity
DEFAULT_SIMILAR_WORDS = 10  # Default top-N similar words

# Model types
MODEL_TYPES = {
    "tfidf": "TF-IDF (LSA)",
    "word2vec_cbow": "Word2Vec (CBOW)",
    "word2vec_skipgram": "Word2Vec (Skip-Gram)",
}
