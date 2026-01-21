"""
Pydantic response models for the API.
"""
from typing import List, Optional
from pydantic import BaseModel, Field


class ModelInfo(BaseModel):
    """Information about a loaded model."""
    model_type: str = Field(..., description="Type of the model")
    display_name: str = Field(..., description="Human-readable model name")
    vocab_size: int = Field(..., description="Size of the vocabulary")
    vector_dimensions: int = Field(..., description="Dimensionality of word vectors")
    is_loaded: bool = Field(..., description="Whether the model is loaded")


class SimilarWord(BaseModel):
    """A word with its similarity score."""
    word: str = Field(..., description="The similar word")
    similarity: float = Field(..., description="Cosine similarity score (0-1)")


class SimilarityResponse(BaseModel):
    """Response for similarity lookup."""
    query_word: str = Field(..., description="The input query word")
    model_type: str = Field(..., description="Model used for similarity")
    similar_words: List[SimilarWord] = Field(..., description="List of similar words")
    in_vocabulary: bool = Field(..., description="Whether query word is in vocabulary")
    message: Optional[str] = Field(None, description="Additional message or error")


class EmbeddingPoint(BaseModel):
    """A word with its 2D coordinates for visualization."""
    word: str = Field(..., description="The word")
    x: float = Field(..., description="X coordinate (after dimensionality reduction)")
    y: float = Field(..., description="Y coordinate (after dimensionality reduction)")
    frequency: Optional[int] = Field(None, description="Word frequency in corpus")


class EmbeddingsResponse(BaseModel):
    """Response containing embeddings for visualization."""
    model_type: str = Field(..., description="Model used for embeddings")
    reduction_method: str = Field(..., description="Dimensionality reduction method (pca/tsne)")
    num_words: int = Field(..., description="Number of words included")
    points: List[EmbeddingPoint] = Field(..., description="List of embedding points")


class VocabularyInfo(BaseModel):
    """Information about the vocabulary."""
    model_type: str = Field(..., description="Model type")
    vocab_size: int = Field(..., description="Total vocabulary size")
    sample_words: List[str] = Field(..., description="Sample words from vocabulary")


class ComparisonResult(BaseModel):
    """Comparison of similarity results across models."""
    query_word: str = Field(..., description="The input query word")
    results: dict = Field(..., description="Results per model type")
