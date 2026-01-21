# Embedding Explorer

An interactive web application for exploring and comparing TF-IDF and Word2Vec embeddings using Streamlit (frontend) and FastAPI (backend).

## Features

- **📊 Embedding Visualization**: Visualize word embeddings in 2D space using PCA or t-SNE
- **🔍 Similarity Lookup**: Find semantically similar words based on cosine similarity
- **⚖️ Model Comparison**: Compare results across TF-IDF, Word2Vec CBOW, and Skip-Gram

## Project Structure

```
Assignment1/
├── backend/
│   ├── main.py              # FastAPI application
│   ├── config.py            # Configuration settings
│   ├── routers/             # API endpoints
│   │   ├── models.py        # Model info endpoints
│   │   ├── embeddings.py    # Visualization endpoints
│   │   └── similarity.py    # Similarity lookup endpoints
│   ├── services/            # Business logic
│   │   ├── model_loader.py  # Model loading & caching
│   │   ├── embedding_service.py  # Similarity calculations
│   │   └── dimensionality.py     # PCA/t-SNE reduction
│   └── schemas/             # Pydantic models
├── frontend/
│   ├── app.py               # Main Streamlit app
│   ├── pages/               # Multi-page app
│   │   ├── 1_Embedding_Visualization.py
│   │   ├── 2_Similarity_Lookup.py
│   │   └── 3_Model_Comparison.py
│   ├── components/          # Reusable UI components
│   └── utils/               # API client
├── models/                  # Pre-trained model files
├── requirements.txt
└── README.md
```

## Installation

1. **Create virtual environment** (recommended):
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   # or
   source venv/bin/activate  # Linux/Mac
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Download NLTK data** (if not already done):
   ```python
   import nltk
   nltk.download('stopwords')
   nltk.download('wordnet')
   nltk.download('punkt')
   nltk.download('punkt_tab')
   ```

## Model Files

Ensure the following files are in the `models/` directory:

| File | Description |
|------|-------------|
| `tfidf_vectorizer.pkl` | TF-IDF vectorizer |
| `tfidf_word_embeddings.npy` | LSA word embeddings (200d) |
| `tfidf_svd.pkl` | TruncatedSVD model |
| `tfidf_vocab.pkl` | Word-to-index mapping |
| `word2vec_cbow.model` | Word2Vec CBOW model |
| `word2vec_skipgram.model` | Word2Vec Skip-Gram model |
| `word_frequencies.pkl` | Word frequency counts |

## Running the Application

### 1. Start the Backend (FastAPI)

```bash
# From the project root directory
cd backend
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

The API will be available at `http://127.0.0.1:8000`

- Swagger docs: `http://127.0.0.1:8000/docs`
- Health check: `http://127.0.0.1:8000/health`

### 2. Start the Frontend (Streamlit)

In a new terminal:

```bash
# From the project root directory
cd frontend
streamlit run app.py
```

The app will open at `http://localhost:8501`

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/models` | GET | List available models |
| `/api/models/{type}` | GET | Get model info |
| `/api/similarity/word/{word}` | GET | Find similar words |
| `/api/similarity/compare/{word}` | GET | Compare across models |
| `/api/embeddings/{type}` | GET | Get 2D embeddings |

## Key Concepts

### Word Embeddings vs TF-IDF

| Aspect | TF-IDF + LSA | Word2Vec |
|--------|--------------|----------|
| Type | Sparse → Dense via SVD | Dense (neural) |
| Context | Document-level | Window-based |
| Semantics | Limited | Captures meaning |

### CBOW vs Skip-Gram

| Aspect | CBOW | Skip-Gram |
|--------|------|-----------|
| Task | Predict word from context | Predict context from word |
| Speed | Faster | Slower |
| Rare words | Less accurate | More accurate |

### Dimensionality Reduction

- **PCA**: Fast, linear, preserves global structure
- **t-SNE**: Slower, non-linear, preserves local clusters

## Training Details

Models were trained on the **News Category Dataset** from Kaggle:
- ~210,000 news headlines and descriptions
- Word2Vec: 200 dimensions, window=8, 15 epochs
- TF-IDF: 20,000 features, reduced to 200 via TruncatedSVD

## License

MIT License
