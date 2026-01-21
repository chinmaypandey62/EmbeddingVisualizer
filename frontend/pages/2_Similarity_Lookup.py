"""
Similarity Lookup Page

Find semantically similar words with polished UI and loading states.
"""
import streamlit as st
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from components.sidebar import render_sidebar
from components.visualization import plot_word_neighborhood, create_similarity_bar_chart
from components.similarity_panel import render_similarity_results, render_word_chips
from components.styles import GLOBAL_STYLES, ICONS, render_page_header, render_loading
from utils.api_client import get_api_client

# Page config
st.set_page_config(
    page_title="Similarity Lookup",
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
        title="Similarity Lookup",
        subtitle="Find semantically similar words using cosine similarity across embedding models",
        icon_html=f'<div style="color: var(--accent);">{ICONS["search"]}</div>'
    ), unsafe_allow_html=True)
    
    # API client
    api = get_api_client()
    
    # Check if a suggestion was selected (before widget instantiation)
    selected_suggestion = st.session_state.pop("selected_suggestion", None)
    
    # Main layout
    col_input, col_results = st.columns([1, 2])
    
    with col_input:
        # Search panel using native expander for proper styling
        with st.expander("🔍 Search Word", expanded=True):
            # Use selected suggestion as default value if available
            default_value = selected_suggestion if selected_suggestion else ""
            
            query_word = st.text_input(
                "Word",
                value=default_value,
                placeholder="e.g., technology",
                label_visibility="collapsed"
            )
            
            topn = st.slider(
                "Number of results",
                min_value=5,
                max_value=30,
                value=10,
                key="topn"
            )
            
            # Auto-trigger search if suggestion was selected
            search_clicked = st.button(
                "Find Similar Words",
                type="primary",
                use_container_width=True,
                key="search_btn"
            ) or (selected_suggestion is not None)
        
        # Suggestions panel using native expander
        with st.expander("⚡ Try These Words", expanded=True):
            sample_words = api.get_vocabulary_sample(params["model_type"], 12)
            if sample_words and "sample_words" in sample_words:
                words = sample_words["sample_words"][:12]
                
                # Display in rows of 3 using columns (wider to avoid text wrapping)
                for i in range(0, len(words), 3):
                    row_words = words[i:i+3]
                    cols = st.columns(3)
                    for j, word in enumerate(row_words):
                        with cols[j]:
                            if st.button(word, key=f"sug_{i}_{j}", use_container_width=True):
                                st.session_state.selected_suggestion = word
                                st.rerun()
    
    with col_results:
        if query_word and search_clicked:
            # Loading state
            loading_placeholder = st.empty()
            results_placeholder = st.empty()
            
            with loading_placeholder:
                st.markdown(render_loading(f"Finding words similar to '{query_word}'..."), unsafe_allow_html=True)
            
            # Fetch results
            results = api.get_similar_words(
                word=query_word,
                model_type=params["model_type"],
                topn=topn
            )
            
            # Clear loading
            loading_placeholder.empty()
            
            with results_placeholder.container():
                if results:
                    render_similarity_results(results)
                    
                    # Show bar chart
                    if results.get("similar_words"):
                        st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
                        fig = create_similarity_bar_chart(
                            results["similar_words"],
                            results["query_word"]
                        )
                        st.plotly_chart(fig, use_container_width=True, config={
                            'displayModeBar': False
                        })
                        
                        # Store for neighborhood vis
                        st.session_state.last_search_word = query_word
        elif query_word:
            # Show initial state with hint
            st.markdown(f"""
            <div class="empty-state" style="padding: 4rem 2rem;">
                <div style="color: var(--primary); margin-bottom: 1rem;">{ICONS['search']}</div>
                <p>Click "Find Similar Words" to search</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="empty-state" style="padding: 4rem 2rem;">
                <div style="color: var(--text-muted); margin-bottom: 1rem;">{ICONS['search']}</div>
                <p>Enter a word to find similar words</p>
                <p style="font-size: 0.85rem; color: var(--text-muted);">Or click one of the suggestions</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Neighborhood visualization section
    st.markdown("<hr>", unsafe_allow_html=True)
    
    st.markdown(f"""
    <div style="display: flex; align-items: center; gap: 0.75rem; margin-bottom: 1rem;">
        <div style="color: var(--secondary);">{ICONS['target']}</div>
        <span style="color: var(--text-primary); font-weight: 600; font-size: 1.1rem;">Word Neighborhood</span>
    </div>
    """, unsafe_allow_html=True)
    
    # Get the word for neighborhood (use last searched word)
    neighborhood_word = st.session_state.get("last_search_word", query_word if search_clicked else None)
    
    if neighborhood_word:
        neighborhood_loading = st.empty()
        neighborhood_chart = st.empty()
        
        with neighborhood_loading:
            st.markdown(render_loading("Generating neighborhood visualization..."), unsafe_allow_html=True)
        
        neighborhood_data = api.get_word_neighborhood(
            word=neighborhood_word,
            model_type=params["model_type"],
            method=params["reduction_method"],
            num_neighbors=topn
        )
        
        neighborhood_loading.empty()
        
        if neighborhood_data and "points" in neighborhood_data:
            with neighborhood_chart:
                fig = plot_word_neighborhood(neighborhood_data)
                st.plotly_chart(fig, use_container_width=True, config={
                    'displayModeBar': True,
                    'displaylogo': False,
                    'scrollZoom': True,
                })
            
            with st.expander("About this visualization"):
                st.markdown(f"""
                This shows **{neighborhood_word}** (★) and its {topn} nearest neighbors in 2D space.
                
                **How to read:**
                - The query word appears as a red star
                - Neighbors are colored by similarity (green = most similar)
                - Lines connect the query to each neighbor
                - Line thickness indicates similarity strength
                
                **Note:** Positions are computed using {params['reduction_method'].upper()} on the neighborhood subset.
                """)
        else:
            with neighborhood_chart:
                st.markdown(f"""
                <div class="empty-state">
                    <p>Could not generate neighborhood for "{neighborhood_word}"</p>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="empty-state" style="padding: 3rem;">
            <p>Search for a word to see its neighborhood</p>
        </div>
        """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
