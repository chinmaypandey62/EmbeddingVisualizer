"""
Embedding Explorer - Main Streamlit Application

An interactive web application for exploring and comparing
TF-IDF and Word2Vec embeddings.
"""
import streamlit as st

# Page configuration
st.set_page_config(
    page_title="Embedding Explorer",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for polished UI
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Root variables */
    :root {
        --primary: #6366f1;
        --primary-dark: #4f46e5;
        --secondary: #8b5cf6;
        --accent: #06b6d4;
        --success: #10b981;
        --warning: #f59e0b;
        --danger: #ef4444;
        --bg-dark: #0f172a;
        --bg-card: #1e293b;
        --bg-hover: #334155;
        --text-primary: #f8fafc;
        --text-secondary: #94a3b8;
        --text-muted: #64748b;
        --border: #334155;
        --gradient-1: linear-gradient(135deg, #6366f1 0%, #8b5cf6 50%, #06b6d4 100%);
        --gradient-2: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
    }
    
    /* Global styles */
    .stApp {
        background: var(--bg-dark);
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Hide Streamlit branding */
    #MainMenu, footer, header {visibility: hidden;}
    
    /* Main container */
    .main .block-container {
        padding: 2rem 3rem;
        max-width: 1400px;
    }
    
    /* Headers */
    h1, h2, h3 {
        font-family: 'Inter', sans-serif;
        font-weight: 600;
        color: var(--text-primary);
    }
    
    /* Hero section */
    .hero-container {
        background: var(--gradient-2);
        border: 1px solid var(--border);
        border-radius: 16px;
        padding: 3rem;
        margin-bottom: 2rem;
        text-align: center;
        position: relative;
        overflow: hidden;
    }
    
    .hero-container::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: var(--gradient-1);
    }
    
    .hero-title {
        font-size: 2.5rem;
        font-weight: 700;
        background: var(--gradient-1);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.5rem;
    }
    
    .hero-subtitle {
        color: var(--text-secondary);
        font-size: 1.1rem;
        font-weight: 400;
    }
    
    /* Feature cards */
    .feature-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 1.5rem;
        margin: 2rem 0;
    }
    
    .feature-card {
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: 12px;
        padding: 1.5rem;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        cursor: pointer;
    }
    
    .feature-card:hover {
        transform: translateY(-4px);
        border-color: var(--primary);
        box-shadow: 0 20px 40px -12px rgba(99, 102, 241, 0.25);
    }
    
    .feature-icon {
        width: 48px;
        height: 48px;
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-bottom: 1rem;
        font-size: 1.5rem;
    }
    
    .feature-icon.viz { background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%); }
    .feature-icon.sim { background: linear-gradient(135deg, #06b6d4 0%, #0891b2 100%); }
    .feature-icon.cmp { background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%); }
    
    .feature-title {
        color: var(--text-primary);
        font-size: 1.1rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
    
    .feature-desc {
        color: var(--text-secondary);
        font-size: 0.9rem;
        line-height: 1.5;
    }
    
    /* Buttons */
    .stButton > button {
        background: var(--gradient-1);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.75rem 1.5rem;
        font-weight: 500;
        font-family: 'Inter', sans-serif;
        transition: all 0.3s ease;
        box-shadow: 0 4px 14px -4px rgba(99, 102, 241, 0.4);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px -4px rgba(99, 102, 241, 0.5);
    }
    
    /* Info boxes */
    .info-box {
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: 12px;
        padding: 1.25rem;
        margin: 1rem 0;
    }
    
    .info-box.gradient-border {
        border: none;
        position: relative;
    }
    
    .info-box.gradient-border::before {
        content: '';
        position: absolute;
        inset: 0;
        border-radius: 12px;
        padding: 1px;
        background: var(--gradient-1);
        -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
        mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
        -webkit-mask-composite: xor;
        mask-composite: exclude;
    }
    
    /* Concept cards */
    .concept-grid {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 1.5rem;
    }
    
    .concept-card {
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: 12px;
        padding: 1.5rem;
    }
    
    .concept-header {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        margin-bottom: 1rem;
    }
    
    .concept-badge {
        background: var(--primary);
        color: white;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
    }
    
    /* Tables */
    .styled-table {
        width: 100%;
        border-collapse: collapse;
        margin: 1rem 0;
    }
    
    .styled-table th {
        background: var(--bg-hover);
        color: var(--text-primary);
        padding: 0.75rem 1rem;
        text-align: left;
        font-weight: 600;
        font-size: 0.85rem;
    }
    
    .styled-table td {
        padding: 0.75rem 1rem;
        border-bottom: 1px solid var(--border);
        color: var(--text-secondary);
        font-size: 0.9rem;
    }
    
    .styled-table tr:hover td {
        background: var(--bg-hover);
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 2rem;
        color: var(--text-muted);
        border-top: 1px solid var(--border);
        margin-top: 3rem;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: var(--bg-card);
        border-right: 1px solid var(--border);
    }
    
    [data-testid="stSidebar"] .stSelectbox label,
    [data-testid="stSidebar"] .stRadio label,
    [data-testid="stSidebar"] .stSlider label {
        color: var(--text-secondary);
        font-weight: 500;
    }
    
    /* Form elements */
    .stTextInput > div > div > input,
    .stSelectbox > div > div {
        background: var(--bg-dark);
        border: 1px solid var(--border);
        border-radius: 8px;
        color: var(--text-primary);
    }
    
    .stTextInput > div > div > input:focus {
        border-color: var(--primary);
        box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.2);
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: 8px;
        color: var(--text-primary);
    }
    
    /* Metrics */
    [data-testid="stMetric"] {
        background: var(--bg-card);
        padding: 1rem;
        border-radius: 12px;
        border: 1px solid var(--border);
    }
    
    [data-testid="stMetricValue"] {
        color: var(--text-primary);
    }
    
    [data-testid="stMetricLabel"] {
        color: var(--text-secondary);
    }
    
    /* Loading animation */
    .loading-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: 3rem;
    }
    
    .loading-spinner {
        width: 48px;
        height: 48px;
        border: 3px solid var(--border);
        border-top-color: var(--primary);
        border-radius: 50%;
        animation: spin 1s linear infinite;
    }
    
    @keyframes spin {
        to { transform: rotate(360deg); }
    }
    
    .loading-text {
        margin-top: 1rem;
        color: var(--text-secondary);
        font-size: 0.9rem;
    }
    
    /* Divider */
    hr {
        border: none;
        height: 1px;
        background: var(--border);
        margin: 2rem 0;
    }
    
    /* Progress bar animation */
    .progress-container {
        background: var(--bg-card);
        border-radius: 8px;
        overflow: hidden;
        height: 8px;
    }
    
    .progress-bar {
        height: 100%;
        background: var(--gradient-1);
        border-radius: 8px;
        animation: progress 2s ease-in-out;
    }
    
    @keyframes progress {
        from { width: 0%; }
    }
</style>
""", unsafe_allow_html=True)

# SVG Icons
ICONS = {
    "chart": '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M12 2a14.5 14.5 0 0 0 0 20 14.5 14.5 0 0 0 0-20"/><path d="M2 12h20"/></svg>',
    "search": '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/></svg>',
    "compare": '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M16 3h5v5"/><path d="M8 3H3v5"/><path d="M21 3l-8.5 8.5"/><path d="M3 3l8.5 8.5"/><path d="M16 21h5v-5"/><path d="M8 21H3v-5"/><path d="M21 21l-8.5-8.5"/><path d="M3 21l8.5-8.5"/></svg>',
    "layers": '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m12.83 2.18a2 2 0 0 0-1.66 0L2.6 6.08a1 1 0 0 0 0 1.83l8.58 3.91a2 2 0 0 0 1.66 0l8.58-3.9a1 1 0 0 0 0-1.83Z"/><path d="m22 12.65-9.17 4.16a2 2 0 0 1-1.66 0L2 12.65"/><path d="m22 17.65-9.17 4.16a2 2 0 0 1-1.66 0L2 17.65"/></svg>',
    "book": '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/></svg>',
}


def main():
    """Main application entry point."""
    
    # Hero section
    st.markdown("""
    <div class="hero-container">
        <h1 class="hero-title">Embedding Explorer</h1>
        <p class="hero-subtitle">Interactive visualization and comparison of TF-IDF and Word2Vec embeddings</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Feature cards using Streamlit columns
    st.markdown("### Features")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style="background: #1e293b; border: 1px solid #334155; border-radius: 12px; padding: 1.5rem; border-top: 3px solid #6366f1;">
            <h4 style="color: #f8fafc; margin-top: 0;">Embedding Visualization</h4>
            <p style="color: #94a3b8; font-size: 0.9rem;">Visualize word embeddings in 2D space using PCA or t-SNE dimensionality reduction.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Open Visualization", key="btn_viz", use_container_width=True):
            st.switch_page("pages/1_Embedding_Visualization.py")
    
    with col2:
        st.markdown("""
        <div style="background: #1e293b; border: 1px solid #334155; border-radius: 12px; padding: 1.5rem; border-top: 3px solid #06b6d4;">
            <h4 style="color: #f8fafc; margin-top: 0;">Similarity Lookup</h4>
            <p style="color: #94a3b8; font-size: 0.9rem;">Find semantically similar words for any input using cosine similarity.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Open Similarity", key="btn_sim", use_container_width=True):
            st.switch_page("pages/2_Similarity_Lookup.py")
    
    with col3:
        st.markdown("""
        <div style="background: #1e293b; border: 1px solid #334155; border-radius: 12px; padding: 1.5rem; border-top: 3px solid #f59e0b;">
            <h4 style="color: #f8fafc; margin-top: 0;">Model Comparison</h4>
            <p style="color: #94a3b8; font-size: 0.9rem;">Compare results across TF-IDF, Word2Vec CBOW, and Skip-Gram models.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Open Comparison", key="btn_comp", use_container_width=True):
            st.switch_page("pages/3_Model_Comparison.py")
    
    st.markdown("<hr>", unsafe_allow_html=True)
    
    # Concepts section
    st.markdown("### Key Concepts")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="concept-card">
            <div class="concept-header">
                <span class="concept-badge">EMBEDDINGS</span>
                <span style="color: var(--text-primary); font-weight: 600;">Word Embeddings vs TF-IDF</span>
            </div>
            <table class="styled-table">
                <tr><th>Aspect</th><th>TF-IDF</th><th>Word2Vec</th></tr>
                <tr><td>Type</td><td>Sparse</td><td>Dense</td></tr>
                <tr><td>Dimensions</td><td>Vocab size</td><td>100-300</td></tr>
                <tr><td>Semantic</td><td>Limited</td><td>Rich</td></tr>
                <tr><td>Context</td><td>Document</td><td>Window</td></tr>
            </table>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="concept-card">
            <div class="concept-header">
                <span class="concept-badge">ARCHITECTURE</span>
                <span style="color: var(--text-primary); font-weight: 600;">CBOW vs Skip-Gram</span>
            </div>
            <table class="styled-table">
                <tr><th>Aspect</th><th>CBOW</th><th>Skip-Gram</th></tr>
                <tr><td>Task</td><td>Word from context</td><td>Context from word</td></tr>
                <tr><td>Speed</td><td>Faster</td><td>Slower</td></tr>
                <tr><td>Rare words</td><td>Less accurate</td><td>More accurate</td></tr>
            </table>
        </div>
        """, unsafe_allow_html=True)
    
    with st.expander("Dimensionality Reduction Methods"):
        st.markdown("""
        **PCA (Principal Component Analysis)**
        - Linear transformation preserving global variance
        - Fast computation, ideal for exploration
        - Best for: Quick overview, linear relationships
        
        **t-SNE (t-Distributed Stochastic Neighbor Embedding)**
        - Non-linear transformation preserving local structure
        - Slower but reveals clusters effectively
        - Best for: Finding semantic clusters, detailed analysis
        """)
    
    # Footer
    st.markdown("""
    <div class="footer">
        <p>Built with FastAPI + Streamlit • News Category Dataset</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
