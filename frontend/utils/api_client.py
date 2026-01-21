"""
API client for communicating with the FastAPI backend.
"""
import requests
from typing import Optional, Dict, Any, List
import streamlit as st

# Backend API URL
API_BASE_URL = "http://127.0.0.1:8000/api"


class APIClient:
    """Client for interacting with the Embedding Explorer API."""
    
    def __init__(self, base_url: str = API_BASE_URL):
        self.base_url = base_url
    
    def _get(self, endpoint: str, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Make a GET request to the API."""
        try:
            response = requests.get(
                f"{self.base_url}{endpoint}",
                params=params,
                timeout=60
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.ConnectionError:
            st.error("❌ Cannot connect to backend. Make sure the FastAPI server is running.")
            return {}
        except requests.exceptions.Timeout:
            st.error("⏱️ Request timed out. The operation took too long.")
            return {}
        except requests.exceptions.RequestException as e:
            st.error(f"🚫 API Error: {str(e)}")
            return {}
    
    def _post(self, endpoint: str, data: Any, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Make a POST request to the API."""
        try:
            response = requests.post(
                f"{self.base_url}{endpoint}",
                json=data,
                params=params,
                timeout=60
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.ConnectionError:
            st.error("❌ Cannot connect to backend. Make sure the FastAPI server is running.")
            return {}
        except requests.exceptions.RequestException as e:
            st.error(f"🚫 API Error: {str(e)}")
            return {}
    
    # Model endpoints
    def get_models(self) -> List[Dict]:
        """Get list of available models."""
        return self._get("/models") or []
    
    def get_model_info(self, model_type: str) -> Dict:
        """Get information about a specific model."""
        return self._get(f"/models/{model_type}")
    
    def get_vocabulary_sample(self, model_type: str, sample_size: int = 50) -> Dict:
        """Get sample words from vocabulary."""
        return self._get(f"/models/{model_type}/vocabulary", {"sample_size": sample_size})
    
    def check_word(self, model_type: str, word: str) -> Dict:
        """Check if word exists in vocabulary."""
        return self._get(f"/models/{model_type}/check-word", {"word": word})
    
    # Similarity endpoints
    def get_similar_words(
        self, 
        word: str, 
        model_type: str = "tfidf", 
        topn: int = 10
    ) -> Dict:
        """Get similar words for a query word."""
        return self._get(
            f"/similarity/word/{word}",
            {"model_type": model_type, "topn": topn}
        )
    
    def compare_similarity(self, word: str, topn: int = 10) -> Dict:
        """Compare similarity across all models."""
        return self._get(f"/similarity/compare/{word}", {"topn": topn})
    
    # Embedding endpoints
    def get_embeddings(
        self,
        model_type: str = "tfidf",
        method: str = "pca",
        num_words: int = 500,
        perplexity: int = 30
    ) -> Dict:
        """Get 2D embeddings for visualization."""
        return self._get(
            f"/embeddings/{model_type}",
            {
                "method": method,
                "num_words": num_words,
                "perplexity": perplexity
            }
        )
    
    def get_word_neighborhood(
        self,
        word: str,
        model_type: str = "tfidf",
        method: str = "pca",
        num_neighbors: int = 20
    ) -> Dict:
        """Get word neighborhood for visualization."""
        return self._get(
            f"/embeddings/{model_type}/neighborhood/{word}",
            {"method": method, "num_neighbors": num_neighbors}
        )


# Cached API client instance
@st.cache_resource
def get_api_client() -> APIClient:
    """Get cached API client instance."""
    return APIClient()
