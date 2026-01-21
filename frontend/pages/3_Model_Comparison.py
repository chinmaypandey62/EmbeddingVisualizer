"""
Model Comparison Page

Compare embedding results across TF-IDF, Word2Vec CBOW, and Skip-Gram with polished UI.
"""
import streamlit as st
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from components.visualization import plot_embeddings_scatter
from components.similarity_panel import render_comparison_results
from components.styles import GLOBAL_STYLES, ICONS, render_page_header, render_loading
from utils.api_client import get_api_client

# Page config
st.set_page_config(
    page_title="Model Comparison",
    page_icon="✦",
    layout="wide"
)

# Apply styles
st.markdown(GLOBAL_STYLES, unsafe_allow_html=True)


def main():
    """Main page function."""
    
    api = get_api_client()
    
    # Page header
    st.markdown(render_page_header(
        title="Model Comparison",
        subtitle="Compare embeddings and similarity results across different models",
        icon_html=f'<div style="color: var(--warning);">{ICONS["compare"]}</div>'
    ), unsafe_allow_html=True)
    
    # Tabs for different comparisons
    tab1, tab2, tab3 = st.tabs([
        "Similarity Comparison",
        "TF-IDF vs Word2Vec",
        "CBOW vs Skip-Gram"
    ])
    
    with tab1:
        st.markdown(f"""
        <div style="display: flex; align-items: center; gap: 0.75rem; margin-bottom: 1.5rem;">
            <div style="color: var(--accent);">{ICONS['search']}</div>
            <span style="color: var(--text-primary); font-weight: 600;">Compare Similar Words Across Models</span>
        </div>
        """, unsafe_allow_html=True)
        
        col_input, col_results = st.columns([1, 3])
        
        with col_input:
            st.markdown(f"""
            <div class="control-panel">
                <div class="control-panel-header">
                    {ICONS['search']}
                    <span class="control-panel-title">Search Word</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            query_word = st.text_input(
                "Word",
                placeholder="e.g., technology",
                key="compare_word",
                label_visibility="collapsed"
            )
            
            topn = st.slider(
                "Results per model",
                min_value=5,
                max_value=15,
                value=8,
                key="compare_topn"
            )
            
            compare_clicked = st.button(
                "Compare Models",
                type="primary",
                use_container_width=True,
                key="compare_btn"
            )
        
        with col_results:
            if query_word and compare_clicked:
                loading_placeholder = st.empty()
                results_placeholder = st.empty()
                
                with loading_placeholder:
                    st.markdown(render_loading(f"Comparing '{query_word}' across all models..."), unsafe_allow_html=True)
                
                comparison_data = api.compare_similarity(query_word, topn)
                
                loading_placeholder.empty()
                
                with results_placeholder.container():
                    if comparison_data:
                        render_comparison_results(comparison_data)
            else:
                st.markdown(f"""
                <div class="empty-state" style="padding: 4rem;">
                    <div style="color: var(--text-muted); margin-bottom: 1rem;">{ICONS['compare']}</div>
                    <p>Enter a word and click "Compare Models" to see results</p>
                </div>
                """, unsafe_allow_html=True)
    
    with tab2:
        st.markdown(f"""
        <div style="display: flex; align-items: center; gap: 0.75rem; margin-bottom: 1rem;">
            <div style="color: var(--primary);">{ICONS['layers']}</div>
            <span style="color: var(--text-primary); font-weight: 600;">TF-IDF (LSA) vs Word2Vec</span>
        </div>
        <p style="color: var(--text-secondary); margin-bottom: 1.5rem;">
            Compare sparse document-based embeddings with dense neural embeddings
        </p>
        """, unsafe_allow_html=True)
        
        # Controls
        st.markdown(f"""
        <div class="control-panel">
            <div class="control-panel-header">
                {ICONS['settings']}
                <span class="control-panel-title">Settings</span>
            </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            method = st.radio(
                "Reduction",
                ["pca", "tsne"],
                format_func=lambda x: "PCA" if x == "pca" else "t-SNE",
                key="tfidf_w2v_method",
                horizontal=True
            )
        with col2:
            num_words = st.select_slider(
                "Points",
                options=[100, 200, 300, 500],
                value=200,
                key="tfidf_w2v_words"
            )
        with col3:
            w2v_model = st.radio(
                "Word2Vec",
                ["word2vec_cbow", "word2vec_skipgram"],
                format_func=lambda x: "CBOW" if x == "word2vec_cbow" else "Skip-Gram",
                key="w2v_model_select",
                horizontal=True
            )
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        if st.button("Load Comparison", key="load_tfidf_w2v", use_container_width=False):
            col_left, col_right = st.columns(2)
            
            with col_left:
                loading_left = st.empty()
                chart_left = st.empty()
                
                with loading_left:
                    st.markdown(render_loading("Loading TF-IDF..."), unsafe_allow_html=True)
                
                tfidf_data = api.get_embeddings(
                    model_type="tfidf",
                    method=method,
                    num_words=num_words
                )
                
                loading_left.empty()
                
                if tfidf_data and "points" in tfidf_data:
                    with chart_left:
                        fig_tfidf = plot_embeddings_scatter(
                            tfidf_data,
                            title="<b>TF-IDF (LSA)</b>",
                            show_labels=False
                        )
                        fig_tfidf.update_layout(height=450, showlegend=False)
                        fig_tfidf.update_traces(marker=dict(showscale=False), selector=dict(name="Words"))
                        st.plotly_chart(fig_tfidf, use_container_width=True, config={'displayModeBar': False})
            
            with col_right:
                loading_right = st.empty()
                chart_right = st.empty()
                
                with loading_right:
                    st.markdown(render_loading("Loading Word2Vec..."), unsafe_allow_html=True)
                
                w2v_data = api.get_embeddings(
                    model_type=w2v_model,
                    method=method,
                    num_words=num_words
                )
                
                loading_right.empty()
                
                if w2v_data and "points" in w2v_data:
                    model_name = "CBOW" if w2v_model == "word2vec_cbow" else "Skip-Gram"
                    with chart_right:
                        fig_w2v = plot_embeddings_scatter(
                            w2v_data,
                            title=f"<b>Word2Vec ({model_name})</b>",
                            show_labels=False
                        )
                        fig_w2v.update_layout(height=450, showlegend=False)
                        fig_w2v.update_traces(marker=dict(showscale=False), selector=dict(name="Words"))
                        st.plotly_chart(fig_w2v, use_container_width=True, config={'displayModeBar': False})
        
        with st.expander("Key Differences"):
            st.markdown("""
            | Aspect | TF-IDF + LSA | Word2Vec |
            |--------|--------------|----------|
            | **Training** | Statistical (document frequency) | Neural network |
            | **Context** | Document-level co-occurrence | Window-based (local) |
            | **Semantics** | Limited understanding | Rich relationships |
            | **Analogy** | Cannot do analogies | king - man + woman ≈ queen |
            """)
    
    with tab3:
        st.markdown(f"""
        <div style="display: flex; align-items: center; gap: 0.75rem; margin-bottom: 1rem;">
            <div style="color: var(--secondary);">{ICONS['layers']}</div>
            <span style="color: var(--text-primary); font-weight: 600;">CBOW vs Skip-Gram</span>
        </div>
        <p style="color: var(--text-secondary); margin-bottom: 1.5rem;">
            Compare Word2Vec architectures: predict word from context vs context from word
        </p>
        """, unsafe_allow_html=True)
        
        # Controls
        st.markdown(f"""
        <div class="control-panel">
            <div class="control-panel-header">
                {ICONS['settings']}
                <span class="control-panel-title">Settings</span>
            </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            cbow_sg_method = st.radio(
                "Reduction",
                ["pca", "tsne"],
                format_func=lambda x: "PCA" if x == "pca" else "t-SNE",
                key="cbow_sg_method",
                horizontal=True
            )
        with col2:
            cbow_sg_words = st.select_slider(
                "Points",
                options=[100, 200, 300, 500],
                value=200,
                key="cbow_sg_words"
            )
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        if st.button("Load Comparison", key="load_cbow_sg", use_container_width=False):
            col_left, col_right = st.columns(2)
            
            with col_left:
                loading_left = st.empty()
                chart_left = st.empty()
                
                with loading_left:
                    st.markdown(render_loading("Loading CBOW..."), unsafe_allow_html=True)
                
                cbow_data = api.get_embeddings(
                    model_type="word2vec_cbow",
                    method=cbow_sg_method,
                    num_words=cbow_sg_words
                )
                
                loading_left.empty()
                
                if cbow_data and "points" in cbow_data:
                    with chart_left:
                        fig_cbow = plot_embeddings_scatter(
                            cbow_data,
                            title="<b>Word2Vec CBOW</b>",
                            show_labels=False
                        )
                        fig_cbow.update_layout(height=450, showlegend=False)
                        fig_cbow.update_traces(marker=dict(showscale=False), selector=dict(name="Words"))
                        st.plotly_chart(fig_cbow, use_container_width=True, config={'displayModeBar': False})
            
            with col_right:
                loading_right = st.empty()
                chart_right = st.empty()
                
                with loading_right:
                    st.markdown(render_loading("Loading Skip-Gram..."), unsafe_allow_html=True)
                
                sg_data = api.get_embeddings(
                    model_type="word2vec_skipgram",
                    method=cbow_sg_method,
                    num_words=cbow_sg_words
                )
                
                loading_right.empty()
                
                if sg_data and "points" in sg_data:
                    with chart_right:
                        fig_sg = plot_embeddings_scatter(
                            sg_data,
                            title="<b>Word2Vec Skip-Gram</b>",
                            show_labels=False
                        )
                        fig_sg.update_layout(height=450, showlegend=False)
                        fig_sg.update_traces(marker=dict(showscale=False), selector=dict(name="Words"))
                        st.plotly_chart(fig_sg, use_container_width=True, config={'displayModeBar': False})
        
        with st.expander("CBOW vs Skip-Gram Details"):
            st.markdown("""
            | Aspect | CBOW | Skip-Gram |
            |--------|------|-----------|
            | **Objective** | Predict target from context | Predict context from target |
            | **Speed** | Faster training | Slower training |
            | **Common Words** | Better representations | Good representations |
            | **Rare Words** | Less accurate | More accurate |
            | **Best For** | Large datasets | Smaller datasets |
            
            **Our Training:** 200 dimensions, window=8, min_count=5, 15 epochs
            """)


if __name__ == "__main__":
    main()
