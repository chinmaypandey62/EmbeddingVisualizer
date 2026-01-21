"""
API router for embedding visualization endpoints.
"""
from fastapi import APIRouter, HTTPException, Query
from typing import List

from backend.schemas import EmbeddingsResponse, EmbeddingPoint
from backend.services.dimensionality import dimensionality_service
from backend.services.model_loader import model_loader
from backend.config import (
    MODEL_TYPES, 
    DEFAULT_REDUCTION_METHOD, 
    DEFAULT_NUM_WORDS,
    MAX_NUM_WORDS,
    DEFAULT_PERPLEXITY
)

router = APIRouter(prefix="/embeddings", tags=["Embeddings"])


@router.get("/{model_type}", response_model=EmbeddingsResponse)
async def get_embeddings_for_visualization(
    model_type: str,
    method: str = Query(
        default=DEFAULT_REDUCTION_METHOD,
        description="Dimensionality reduction method (pca or tsne)"
    ),
    num_words: int = Query(
        default=DEFAULT_NUM_WORDS,
        ge=50,
        le=MAX_NUM_WORDS,
        description="Number of words to include"
    ),
    perplexity: int = Query(
        default=DEFAULT_PERPLEXITY,
        ge=5,
        le=100,
        description="t-SNE perplexity (only used if method=tsne)"
    )
):
    """
    Get 2D reduced embeddings for visualization.
    
    Returns the top N most frequent words with their 2D coordinates
    after applying PCA or t-SNE dimensionality reduction.
    
    Args:
        model_type: Model type ("tfidf", "word2vec_cbow", "word2vec_skipgram")
        method: Reduction method ("pca" or "tsne")
        num_words: Number of words to include (sorted by frequency)
        perplexity: t-SNE perplexity parameter
    """
    if model_type not in MODEL_TYPES:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid model type. Available: {list(MODEL_TYPES.keys())}"
        )
    
    if method not in ["pca", "tsne"]:
        raise HTTPException(
            status_code=400,
            detail="Method must be 'pca' or 'tsne'"
        )
    
    try:
        reduced, words, frequencies = dimensionality_service.get_reduced_embeddings(
            model_type=model_type,
            method=method,
            num_words=num_words,
            perplexity=perplexity
        )
        
        if len(words) == 0:
            raise HTTPException(
                status_code=500,
                detail="Failed to load embeddings"
            )
        
        points = [
            EmbeddingPoint(
                word=word,
                x=float(reduced[i, 0]),
                y=float(reduced[i, 1]),
                frequency=freq
            )
            for i, (word, freq) in enumerate(zip(words, frequencies))
        ]
        
        return EmbeddingsResponse(
            model_type=model_type,
            reduction_method=method,
            num_words=len(points),
            points=points
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error generating embeddings: {str(e)}"
        )


@router.get("/{model_type}/neighborhood/{word}")
async def get_word_neighborhood(
    model_type: str,
    word: str,
    method: str = Query(default=DEFAULT_REDUCTION_METHOD),
    num_neighbors: int = Query(default=20, ge=5, le=50),
    perplexity: int = Query(default=DEFAULT_PERPLEXITY)
):
    """
    Get 2D visualization of a word and its nearest neighbors.
    
    Args:
        model_type: Model type
        word: Query word
        method: Reduction method
        num_neighbors: Number of neighbors to include
        perplexity: t-SNE perplexity
    """
    if model_type not in MODEL_TYPES:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid model type. Available: {list(MODEL_TYPES.keys())}"
        )
    
    try:
        reduced, words, similarities = dimensionality_service.get_word_neighborhood(
            word=word,
            model_type=model_type,
            method=method,
            num_neighbors=num_neighbors,
            perplexity=perplexity
        )
        
        if len(words) == 0:
            raise HTTPException(
                status_code=404,
                detail=f"Word '{word}' not found in vocabulary"
            )
        
        points = []
        for i, (w, sim) in enumerate(zip(words, similarities)):
            points.append({
                "word": w,
                "x": float(reduced[i, 0]),
                "y": float(reduced[i, 1]),
                "similarity": round(sim, 4),
                "is_query": w == word.lower().strip()
            })
        
        return {
            "query_word": word.lower().strip(),
            "model_type": model_type,
            "reduction_method": method,
            "points": points
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error generating neighborhood: {str(e)}"
        )


@router.delete("/cache")
async def clear_embeddings_cache():
    """
    Clear the cached dimensionality reductions.
    Useful when memory is constrained or to force recalculation.
    """
    dimensionality_service.clear_cache()
    return {"message": "Cache cleared successfully"}
