"""
FastAPI application entry point for Embedding Explorer backend.
"""
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.config import API_PREFIX, CORS_ORIGINS
from backend.routers import models_router, embeddings_router, similarity_router

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler for startup and shutdown events."""
    # Startup
    logger.info("Starting Embedding Explorer API...")
    logger.info("Models will be loaded lazily on first access")
    yield
    # Shutdown
    logger.info("Shutting down Embedding Explorer API...")


# Create FastAPI application
app = FastAPI(
    title="Embedding Explorer API",
    description="""
    API for exploring and comparing TF-IDF and Word2Vec embeddings.
    
    ## Features
    - **Model Information**: Get details about available embedding models
    - **Similarity Lookup**: Find semantically similar words
    - **Embedding Visualization**: Get 2D coordinates for plotting word embeddings
    - **Model Comparison**: Compare results across TF-IDF, Word2Vec CBOW, and Skip-Gram
    
    ## Models Available
    - **TF-IDF (LSA)**: Sparse embeddings reduced via TruncatedSVD to 200 dimensions
    - **Word2Vec CBOW**: Dense embeddings trained with Continuous Bag of Words
    - **Word2Vec Skip-Gram**: Dense embeddings trained with Skip-Gram architecture
    """,
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(models_router, prefix=API_PREFIX)
app.include_router(similarity_router, prefix=API_PREFIX)
app.include_router(embeddings_router, prefix=API_PREFIX)


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "name": "Embedding Explorer API",
        "version": "1.0.0",
        "docs_url": "/docs",
        "endpoints": {
            "models": f"{API_PREFIX}/models",
            "similarity": f"{API_PREFIX}/similarity",
            "embeddings": f"{API_PREFIX}/embeddings"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    from backend.config import API_HOST, API_PORT
    
    uvicorn.run(
        "backend.main:app",
        host=API_HOST,
        port=API_PORT,
        reload=True
    )
