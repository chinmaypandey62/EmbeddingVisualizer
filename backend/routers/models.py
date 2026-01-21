"""
API router for model information endpoints.
"""
from fastapi import APIRouter, HTTPException
from typing import List

from backend.schemas import ModelInfo, VocabularyInfo
from backend.services.model_loader import model_loader
from backend.config import MODEL_TYPES

router = APIRouter(prefix="/models", tags=["Models"])


@router.get("", response_model=List[ModelInfo])
async def list_models():
    """
    List all available embedding models with their information.
    """
    return model_loader.get_all_models_info()


@router.get("/{model_type}", response_model=ModelInfo)
async def get_model_info(model_type: str):
    """
    Get information about a specific model.
    
    Args:
        model_type: One of "tfidf", "word2vec_cbow", "word2vec_skipgram"
    """
    if model_type not in MODEL_TYPES:
        raise HTTPException(
            status_code=404,
            detail=f"Model type '{model_type}' not found. Available: {list(MODEL_TYPES.keys())}"
        )
    
    info = model_loader.get_model_info(model_type)
    return info


@router.get("/{model_type}/vocabulary", response_model=VocabularyInfo)
async def get_vocabulary_sample(model_type: str, sample_size: int = 50):
    """
    Get a sample of words from the model's vocabulary.
    
    Args:
        model_type: Model type
        sample_size: Number of sample words to return (sorted by frequency)
    """
    if model_type not in MODEL_TYPES:
        raise HTTPException(
            status_code=404,
            detail=f"Model type '{model_type}' not found"
        )
    
    info = model_loader.get_model_info(model_type)
    sample_words = model_loader.get_vocabulary_sample(model_type, sample_size)
    
    return VocabularyInfo(
        model_type=model_type,
        vocab_size=info["vocab_size"],
        sample_words=sample_words
    )


@router.get("/{model_type}/check-word")
async def check_word_in_vocabulary(model_type: str, word: str):
    """
    Check if a word exists in the model's vocabulary.
    
    Args:
        model_type: Model type
        word: Word to check
    """
    if model_type not in MODEL_TYPES:
        raise HTTPException(
            status_code=404,
            detail=f"Model type '{model_type}' not found"
        )
    
    in_vocab = model_loader.is_word_in_vocab(word, model_type)
    
    return {
        "word": word,
        "model_type": model_type,
        "in_vocabulary": in_vocab
    }
