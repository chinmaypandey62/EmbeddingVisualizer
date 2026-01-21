"""
Embedding Visualization Page

Interactive 2D visualization of word embeddings with progressive loading.
"""
import streamlit as st
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from components.sidebar import render_sidebar
from components.visualization import plot_embeddings_scatter
from components.styles import GLOBAL_STYLES, ICONS, render_page_header, render_loading
from utils.api_client import get_api_client

# Page config
st.set_page_config(
    page_title="Embedding Visualization",
    page_icon="✦",
    layout="wide"
)

# Apply styles
st.markdown(GLOBAL_STYLES, unsafe_allow_html=True)


def main():
    """Main page function."""
    
    # Render sidebar and get parameters
    params = render_sidebar()
    
    # Page header
    st.markdown(render_page_header(
        title="Embedding Visualization",
        subtitle="Explore word embeddings in 2D space with interactive zoom and progressive loading",
        icon_html=f'<div style="color: var(--primary);">{ICONS["chart"]}</div>'
    ), unsafe_allow_html=True)
    
    # API client
    api = get_api_client()
    
    # Main layout
    col_main, col_side = st.columns([3, 1])
    
    with col_side:
        # Highlight Words section using native expander for proper styling
        with st.expander("🎯 Highlight Words", expanded=True):
            highlight_input = st.text_area(
                "Words",
                placeholder="Enter words (one per line)\ne.g.:\ntechnology\nscience\npolitics",
                height=100,
                label_visibility="collapsed"
            )
            highlight_words = [w.strip() for w in highlight_input.split("\n") if w.strip()]
        
        # Display options using native expander
        with st.expander("⚙️ Display Options", expanded=True):
            show_labels = st.checkbox("Show word labels", value=True, key="show_labels")
        
        # Top words section using native expander
        with st.expander("📚 Top Words in Model", expanded=True):
            sample_data = api.get_vocabulary_sample(params["model_type"], 12)
            if sample_data and "sample_words" in sample_data:
                words = sample_data["sample_words"][:12]
                # Display as styled word chips
                chips_html = "".join([f'<span class="word-chip">{word}</span>' for word in words])
                st.markdown(f'<div style="display: flex; flex-wrap: wrap; gap: 0.25rem;">{chips_html}</div>', unsafe_allow_html=True)
    
    with col_main:
        # Progressive loading controls
        col1, col2, col3 = st.columns([2, 2, 1])
        
        with col1:
            current_words = st.session_state.get("current_word_count", params["initial_words"])
            st.markdown(f"""
            <div style="color: var(--text-secondary); font-size: 0.9rem;">
                Showing <span style="color: var(--primary); font-weight: 600;">{current_words}</span> words
                (max: {params["max_words"]})
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            load_more_col, reset_col = st.columns(2)
            with load_more_col:
                if st.button("Load More Points", key="load_more", use_container_width=True):
                    new_count = min(current_words + 200, params["max_words"])
                    st.session_state.current_word_count = new_count
                    st.rerun()
            with reset_col:
                if st.button("Reset View", key="reset", use_container_width=True):
                    st.session_state.current_word_count = params["initial_words"]
                    st.rerun()
        
        # Determine number of words to load
        num_words = st.session_state.get("current_word_count", params["initial_words"])
        
        # Show loading state
        loading_placeholder = st.empty()
        chart_placeholder = st.empty()
        
        # Display loading animation
        with loading_placeholder:
            st.markdown(render_loading(f"Loading {num_words} word embeddings..."), unsafe_allow_html=True)
        
        # Fetch embeddings
        data = api.get_embeddings(
            model_type=params["model_type"],
            method=params["reduction_method"],
            num_words=num_words,
            perplexity=params["perplexity"]
        )
        
        # Clear loading
        loading_placeholder.empty()
        
        if data and "points" in data:
            # Store current count
            st.session_state.current_word_count = len(data['points'])
            
            # Success message
            st.markdown(f"""
            <div class="badge badge-success" style="margin-bottom: 1rem;">
                {ICONS['check']}
                Loaded {len(data['points'])} words
            </div>
            """, unsafe_allow_html=True)
            
            # Create visualization
            with chart_placeholder:
                fig = plot_embeddings_scatter(
                    data,
                    highlight_words=highlight_words if highlight_words else None,
                    show_labels=show_labels
                )
                st.plotly_chart(fig, use_container_width=True, config={
                    'displayModeBar': True,
                    'displaylogo': False,
                    'modeBarButtonsToRemove': ['lasso2d', 'select2d'],
                    'scrollZoom': True,
                })
            
            # Info section
            with st.expander("About this visualization"):
                st.markdown(f"""
                **Model:** {params['model_type'].upper()}  
                **Reduction:** {params['reduction_method'].upper()}  
                **Points:** {len(data['points'])}
                
                **Interaction Tips:**
                - **Scroll** to zoom in/out
                - **Drag** to pan around
                - **Double-click** to reset view
                - **Hover** over points for details
                - **Box zoom** by clicking the zoom tool
                
                **Color Meaning:**
                - Darker colors = less frequent words
                - Brighter colors = more frequent words
                - Red stars = highlighted words
                """)
        else:
            chart_placeholder.markdown("""
            <div class="empty-state">
                <p style="color: var(--danger);">Failed to load embeddings</p>
                <p style="font-size: 0.9rem; color: var(--text-muted);">
                    Make sure the backend is running at http://127.0.0.1:8000
                </p>
            </div>
            """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
