"""
Sidebar component for model selection and parameters.
"""
import streamlit as st
from frontend.utils.api_client import get_api_client
from frontend.components.styles import GLOBAL_STYLES, ICONS


def render_sidebar():
    """
    Render the sidebar with model selection and parameters.
    
    Returns:
        dict: Selected parameters
    """
    # Apply global styles
    st.markdown(GLOBAL_STYLES, unsafe_allow_html=True)
    
    # Sidebar header
    st.sidebar.markdown(f"""
    <div style="display: flex; align-items: center; gap: 0.75rem; margin-bottom: 1.5rem; padding-bottom: 1rem; border-bottom: 1px solid var(--border);">
        <div style="color: var(--primary);">{ICONS['settings']}</div>
        <span style="color: var(--text-primary); font-weight: 600; font-size: 1.1rem;">Settings</span>
    </div>
    """, unsafe_allow_html=True)
    
    # Model selection
    st.sidebar.markdown(f"""
    <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.5rem;">
        <div style="color: var(--accent); width: 18px;">{ICONS['layers']}</div>
        <span style="color: var(--text-secondary); font-weight: 500; font-size: 0.85rem;">Model Selection</span>
    </div>
    """, unsafe_allow_html=True)
    
    model_options = {
        "tfidf": "TF-IDF (LSA)",
        "word2vec_cbow": "Word2Vec CBOW",
        "word2vec_skipgram": "Word2Vec Skip-Gram"
    }
    
    selected_model = st.sidebar.selectbox(
        "Embedding Model",
        options=list(model_options.keys()),
        format_func=lambda x: model_options[x],
        key="model_selection",
        label_visibility="collapsed"
    )
    
    st.sidebar.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
    
    # Visualization settings
    st.sidebar.markdown(f"""
    <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.5rem;">
        <div style="color: var(--secondary); width: 18px;">{ICONS['chart']}</div>
        <span style="color: var(--text-secondary); font-weight: 500; font-size: 0.85rem;">Visualization</span>
    </div>
    """, unsafe_allow_html=True)
    
    reduction_method = st.sidebar.radio(
        "Reduction Method",
        options=["pca", "tsne"],
        format_func=lambda x: "PCA (Fast)" if x == "pca" else "t-SNE (Detailed)",
        key="reduction_method",
        horizontal=True,
        label_visibility="collapsed"
    )
    
    st.sidebar.markdown("<div style='height: 0.5rem;'></div>", unsafe_allow_html=True)
    
    # Initial word count (for progressive loading)
    initial_words = st.sidebar.select_slider(
        "Initial Points",
        options=[50, 100, 200, 300, 500],
        value=100,
        key="initial_words",
        help="Start with fewer points and load more as needed"
    )
    
    # Maximum words
    max_words = st.sidebar.select_slider(
        "Maximum Points",
        options=[200, 500, 1000, 1500, 2000],
        value=500,
        key="max_words",
        help="Maximum points when fully loaded"
    )
    
    # t-SNE perplexity (only show if t-SNE selected)
    perplexity = 30
    if reduction_method == "tsne":
        perplexity = st.sidebar.slider(
            "t-SNE Perplexity",
            min_value=5,
            max_value=50,
            value=30,
            key="perplexity",
            help="Higher = more global structure"
        )
    
    st.sidebar.markdown("<hr style='margin: 1.5rem 0;'>", unsafe_allow_html=True)
    
    # Model info
    st.sidebar.markdown(f"""
    <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.75rem;">
        <div style="color: var(--warning); width: 18px;">{ICONS['info']}</div>
        <span style="color: var(--text-secondary); font-weight: 500; font-size: 0.85rem;">Model Info</span>
    </div>
    """, unsafe_allow_html=True)
    
    api = get_api_client()
    model_info = api.get_model_info(selected_model)
    
    if model_info:
        col1, col2 = st.sidebar.columns(2)
        with col1:
            st.metric("Vocabulary", f"{model_info.get('vocab_size', 0):,}")
        with col2:
            st.metric("Dimensions", model_info.get('vector_dimensions', 0))
        
        if model_info.get('is_loaded'):
            st.sidebar.markdown("""
            <div class="badge badge-success" style="margin-top: 0.5rem;">
                <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20 6 9 17l-5-5"/></svg>
                Model loaded
            </div>
            """, unsafe_allow_html=True)
    else:
        st.sidebar.warning("Could not connect to backend")
    
    return {
        "model_type": selected_model,
        "reduction_method": reduction_method,
        "initial_words": initial_words,
        "max_words": max_words,
        "num_words": initial_words,  # Start with initial
        "perplexity": perplexity
    }
