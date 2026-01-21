"""
API router for similarity lookup endpoints.
"""
from fastapi import APIRouter, HTTPException, Query
from typing import Optional

from backend.schemas import SimilarityResponse, SimilarWord, ComparisonResult
from backend.services.embedding_service import embedding_service
from backend.config import MODEL_TYPES, DEFAULT_SIMILAR_WORDS

router = APIRouter(prefix="/similarity", tags=["Similarity"])


@router.get("/word/{word}", response_model=SimilarityResponse)
async def get_similar_words(
    word: str,
    model_type: str = Query(default="tfidf", description="Model type to use"),
    topn: int = Query(default=DEFAULT_SIMILAR_WORDS, ge=1, le=50, description="Number of similar words")
):
    """
    Get semantically similar words for a given input word.
    
    Args:
        word: The query word
        model_type: Model to use ("tfidf", "word2vec_cbow", "word2vec_skipgram")
        topn: Number of similar words to return
    """
    if model_type not in MODEL_TYPES:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid model type. Available: {list(MODEL_TYPES.keys())}"
        )
    
    similar_words, in_vocab, message = embedding_service.get_similar_words(
        word, model_type, topn
    )
    
    return SimilarityResponse(
        query_word=word.lower().strip(),
        model_type=model_type,
        similar_words=[
            SimilarWord(word=w, similarity=round(s, 4))
            for w, s in similar_words
        ],
        in_vocabulary=in_vocab,
        message=message
    )


@router.get("/compare/{word}", response_model=ComparisonResult)
async def compare_similarity_across_models(
    word: str,
    topn: int = Query(default=DEFAULT_SIMILAR_WORDS, ge=1, le=50)
):
    """
    Compare similarity results for a word across all embedding models.
    
    Args:
        word: The query word
        topn: Number of similar words per model
    """
    results = embedding_service.compare_similarity(word, topn)
    
    return ComparisonResult(
        query_word=word.lower().strip(),
        results=results
    )


@router.post("/batch")
async def get_similar_words_batch(
    words: list[str],
    model_type: str = Query(default="tfidf"),
    topn: int = Query(default=5, ge=1, le=20)
):
    """
    Get similar words for multiple input words (batch operation).
    
    Args:
        words: List of query words
        model_type: Model to use
        topn: Number of similar words per query
    """
    if model_type not in MODEL_TYPES:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid model type. Available: {list(MODEL_TYPES.keys())}"
        )
    
    if len(words) > 20:
        raise HTTPException(
            status_code=400,
            detail="Maximum 20 words per batch"
        )
    
    results = []
    for word in words:
        similar_words, in_vocab, message = embedding_service.get_similar_words(
            word, model_type, topn
        )
        results.append({
            "query_word": word.lower().strip(),
            "similar_words": [{"word": w, "similarity": round(s, 4)} for w, s in similar_words],
            "in_vocabulary": in_vocab,
            "message": message
        })
    
    return {"model_type": model_type, "results": results}
