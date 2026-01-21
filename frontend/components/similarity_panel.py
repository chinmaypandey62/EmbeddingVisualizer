"""
Similarity results panel component with polished styling.
"""
import streamlit as st
from typing import Dict, List
from frontend.components.styles import ICONS, get_score_color


def render_similarity_results(data: Dict, show_chart: bool = True):
    """
    Render similarity results with styled components.
    
    Args:
        data: API response with similarity data
        show_chart: Whether to show the bar chart
    """
    if not data:
        st.markdown("""
        <div class="empty-state">
            <p>No results to display</p>
        </div>
        """, unsafe_allow_html=True)
        return
    
    query_word = data.get("query_word", "")
    in_vocab = data.get("in_vocabulary", False)
    similar_words = data.get("similar_words", [])
    message = data.get("message")
    model_type = data.get("model_type", "unknown")
    
    # Model display names
    model_names = {
        "tfidf": "TF-IDF (LSA)",
        "word2vec_cbow": "Word2Vec CBOW",
        "word2vec_skipgram": "Word2Vec Skip-Gram"
    }
    
    # Results card
    st.markdown(f"""
    <div class="results-card">
        <div class="results-header">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <span style="color: var(--text-primary); font-weight: 600; font-size: 1.1rem;">
                        Results for "{query_word}"
                    </span>
                    <div style="color: var(--text-muted); font-size: 0.85rem; margin-top: 0.25rem;">
                        {model_names.get(model_type, model_type)}
                    </div>
                </div>
                <div>
                    {"<span class='badge badge-success'>" + ICONS['check'] + " In vocabulary</span>" if in_vocab else "<span class='badge badge-warning'>" + ICONS['alert'] + " Not found</span>"}
                </div>
            </div>
        </div>
        <div class="results-body">
    """, unsafe_allow_html=True)
    
    if not in_vocab:
        st.markdown(f"""
            <div style="text-align: center; padding: 2rem; color: var(--text-secondary);">
                <div style="color: var(--warning); margin-bottom: 0.5rem;">{ICONS['alert']}</div>
                <p>{message or 'Word not found in vocabulary'}</p>
            </div>
        """, unsafe_allow_html=True)
        st.markdown("</div></div>", unsafe_allow_html=True)
        return
    
    if not similar_words:
        st.markdown("""
            <div style="text-align: center; padding: 2rem; color: var(--text-secondary);">
                <p>No similar words found</p>
            </div>
        """, unsafe_allow_html=True)
        st.markdown("</div></div>", unsafe_allow_html=True)
        return
    
    # Render score bars
    for i, item in enumerate(similar_words, 1):
        word = item["word"]
        score = item["similarity"]
        color = get_score_color(score)
        width_pct = score * 100
        
        st.markdown(f"""
        <div class="score-bar-container" style="animation: slideIn 0.3s ease forwards; animation-delay: {i * 0.05}s; opacity: 0;">
            <span class="score-rank">{i}.</span>
            <span class="score-word">{word}</span>
            <div class="score-bar">
                <div class="score-bar-fill" style="width: {width_pct}%; background: {color};"></div>
            </div>
            <span class="score-value">{score:.4f}</span>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("</div></div>", unsafe_allow_html=True)
    
    # Add animation keyframes
    st.markdown("""
    <style>
        @keyframes slideIn {
            from { opacity: 0; transform: translateX(-10px); }
            to { opacity: 1; transform: translateX(0); }
        }
    </style>
    """, unsafe_allow_html=True)


def render_comparison_results(data: Dict):
    """
    Render comparison results across multiple models.
    
    Args:
        data: API response with comparison data
    """
    if not data:
        st.info("No comparison results")
        return
    
    query_word = data.get("query_word", "")
    results = data.get("results", {})
    
    st.markdown(f"""
    <div class="page-header" style="margin-bottom: 1.5rem;">
        <div class="page-title">
            <h2 style="margin: 0; font-size: 1.25rem;">Comparison for "{query_word}"</h2>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Model display names and colors
    model_config = {
        "tfidf": {"name": "TF-IDF (LSA)", "color": "#6366f1"},
        "word2vec_cbow": {"name": "Word2Vec CBOW", "color": "#06b6d4"},
        "word2vec_skipgram": {"name": "Word2Vec Skip-Gram", "color": "#10b981"}
    }
    
    # Create columns for each model
    cols = st.columns(3)
    
    for i, (model_type, model_results) in enumerate(results.items()):
        config = model_config.get(model_type, {"name": model_type, "color": "#6366f1"})
        
        with cols[i]:
            in_vocab = model_results.get("in_vocabulary", False)
            similar_words = model_results.get("similar_words", [])
            message = model_results.get("message")
            
            # Card header
            st.markdown(f"""
            <div class="card" style="border-top: 3px solid {config['color']};">
                <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 1rem;">
                    <div style="width: 8px; height: 8px; border-radius: 50%; background: {config['color']};"></div>
                    <span style="color: var(--text-primary); font-weight: 600;">{config['name']}</span>
                </div>
            """, unsafe_allow_html=True)
            
            if not in_vocab:
                st.markdown(f"""
                <div style="text-align: center; padding: 1rem; color: var(--warning);">
                    <small>{message or 'Not in vocabulary'}</small>
                </div>
                """, unsafe_allow_html=True)
            elif not similar_words:
                st.markdown("""
                <div style="text-align: center; padding: 1rem; color: var(--text-muted);">
                    <small>No results</small>
                </div>
                """, unsafe_allow_html=True)
            else:
                # Display words with scores
                for j, item in enumerate(similar_words[:8], 1):
                    score = item["similarity"]
                    color = get_score_color(score)
                    
                    st.markdown(f"""
                    <div style="display: flex; justify-content: space-between; align-items: center; padding: 0.5rem 0; border-bottom: 1px solid var(--border);">
                        <span style="color: var(--text-primary); font-size: 0.9rem;">{j}. {item['word']}</span>
                        <span style="color: {color}; font-size: 0.8rem; font-family: monospace;">{score:.3f}</span>
                    </div>
                    """, unsafe_allow_html=True)
            
            st.markdown("</div>", unsafe_allow_html=True)


def render_word_chips(words: List[str], on_click_key: str = None):
    """
    Render a list of words as clickable chips.
    
    Args:
        words: List of words to display
        on_click_key: Session state key to store clicked word
    """
    if not words:
        return
    
    # Create chip HTML
    chips_html = ""
    for word in words:
        chips_html += f'<span class="word-chip">{word}</span>'
    
    st.markdown(f"""
    <div style="margin: 0.5rem 0;">
        {chips_html}
    </div>
    """, unsafe_allow_html=True)
