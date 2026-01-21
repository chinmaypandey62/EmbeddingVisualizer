"""
Shared styles and theme configuration for the Embedding Explorer frontend.
"""

# CSS Styles for all pages
GLOBAL_STYLES = """
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
    
    /* Page header */
    .page-header {
        background: var(--gradient-2);
        border: 1px solid var(--border);
        border-radius: 16px;
        padding: 2rem;
        margin-bottom: 2rem;
        position: relative;
        overflow: hidden;
    }
    
    .page-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: var(--gradient-1);
    }
    
    .page-title {
        display: flex;
        align-items: center;
        gap: 1rem;
        margin-bottom: 0.5rem;
    }
    
    .page-title h1 {
        font-size: 1.75rem;
        margin: 0;
        background: var(--gradient-1);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .page-subtitle {
        color: var(--text-secondary);
        font-size: 0.95rem;
        margin: 0;
    }
    
    /* Control panel */
    .control-panel {
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
    }
    
    .control-panel-header {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        margin-bottom: 1rem;
        padding-bottom: 1rem;
        border-bottom: 1px solid var(--border);
    }
    
    .control-panel-title {
        color: var(--text-primary);
        font-weight: 600;
        font-size: 0.95rem;
        margin: 0;
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
    
    .stButton > button:active {
        transform: translateY(0);
    }
    
    /* Secondary button style */
    .secondary-btn button {
        background: transparent !important;
        border: 1px solid var(--border) !important;
        color: var(--text-primary) !important;
        box-shadow: none !important;
    }
    
    .secondary-btn button:hover {
        border-color: var(--primary) !important;
        background: var(--bg-hover) !important;
    }
    
    /* Card style */
    .card {
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: 12px;
        padding: 1.5rem;
        transition: all 0.3s ease;
    }
    
    .card:hover {
        border-color: var(--primary);
    }
    
    .card-title {
        color: var(--text-primary);
        font-weight: 600;
        font-size: 1rem;
        margin-bottom: 0.75rem;
    }
    
    /* Results card */
    .results-card {
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: 12px;
        overflow: hidden;
    }
    
    .results-header {
        background: var(--bg-hover);
        padding: 1rem 1.5rem;
        border-bottom: 1px solid var(--border);
    }
    
    .results-body {
        padding: 1.5rem;
    }
    
    /* Status badges */
    .badge {
        display: inline-flex;
        align-items: center;
        gap: 0.375rem;
        padding: 0.375rem 0.75rem;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
    }
    
    .badge-success {
        background: rgba(16, 185, 129, 0.15);
        color: #10b981;
    }
    
    .badge-warning {
        background: rgba(245, 158, 11, 0.15);
        color: #f59e0b;
    }
    
    .badge-error {
        background: rgba(239, 68, 68, 0.15);
        color: #ef4444;
    }
    
    .badge-info {
        background: rgba(99, 102, 241, 0.15);
        color: #6366f1;
    }
    
    /* Loading state */
    .loading-overlay {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: 4rem 2rem;
        background: var(--bg-card);
        border-radius: 12px;
        border: 1px solid var(--border);
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
    
    .loading-progress {
        width: 200px;
        height: 4px;
        background: var(--border);
        border-radius: 2px;
        margin-top: 1rem;
        overflow: hidden;
    }
    
    .loading-progress-bar {
        height: 100%;
        background: var(--gradient-1);
        border-radius: 2px;
        animation: progress-animation 2s ease-in-out infinite;
    }
    
    @keyframes progress-animation {
        0% { width: 0%; margin-left: 0%; }
        50% { width: 60%; margin-left: 20%; }
        100% { width: 0%; margin-left: 100%; }
    }
    
    /* Empty state */
    .empty-state {
        text-align: center;
        padding: 4rem 2rem;
        color: var(--text-secondary);
    }
    
    .empty-state-icon {
        width: 64px;
        height: 64px;
        margin: 0 auto 1rem;
        opacity: 0.5;
    }
    
    /* Word chips */
    .word-chip {
        display: inline-block;
        padding: 0.375rem 0.75rem;
        background: var(--bg-hover);
        border: 1px solid var(--border);
        border-radius: 20px;
        color: var(--text-secondary);
        font-size: 0.85rem;
        margin: 0.25rem;
        cursor: pointer;
        transition: all 0.2s ease;
    }
    
    .word-chip:hover {
        border-color: var(--primary);
        color: var(--primary);
        background: rgba(99, 102, 241, 0.1);
    }
    
    /* Similarity score bar */
    .score-bar-container {
        display: flex;
        align-items: center;
        gap: 1rem;
        padding: 0.75rem 0;
        border-bottom: 1px solid var(--border);
    }
    
    .score-bar-container:last-child {
        border-bottom: none;
    }
    
    .score-rank {
        width: 24px;
        color: var(--text-muted);
        font-size: 0.85rem;
    }
    
    .score-word {
        flex: 1;
        color: var(--text-primary);
        font-weight: 500;
    }
    
    .score-bar {
        width: 120px;
        height: 6px;
        background: var(--bg-hover);
        border-radius: 3px;
        overflow: hidden;
    }
    
    .score-bar-fill {
        height: 100%;
        border-radius: 3px;
        transition: width 0.5s ease;
    }
    
    .score-value {
        width: 60px;
        text-align: right;
        color: var(--text-secondary);
        font-size: 0.85rem;
        font-family: monospace;
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
    .stSelectbox > div > div,
    .stTextArea textarea {
        background: var(--bg-dark) !important;
        border: 1px solid var(--border) !important;
        border-radius: 8px !important;
        color: var(--text-primary) !important;
    }
    
    .stTextInput > div > div > input:focus,
    .stTextArea textarea:focus {
        border-color: var(--primary) !important;
        box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.2) !important;
    }
    
    /* Slider */
    .stSlider > div > div > div {
        background: var(--gradient-1);
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background: var(--bg-card) !important;
        border: 1px solid var(--border) !important;
        border-radius: 8px !important;
        color: var(--text-primary) !important;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0;
        background: var(--bg-card);
        border-radius: 12px 12px 0 0;
        padding: 0.5rem 0.5rem 0;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border-radius: 8px 8px 0 0;
        color: var(--text-secondary);
        padding: 0.75rem 1.5rem;
        font-weight: 500;
    }
    
    .stTabs [aria-selected="true"] {
        background: var(--bg-hover);
        color: var(--text-primary);
    }
    
    .stTabs [data-baseweb="tab-panel"] {
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-top: none;
        border-radius: 0 0 12px 12px;
        padding: 1.5rem;
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
    
    /* Divider */
    hr {
        border: none;
        height: 1px;
        background: var(--border);
        margin: 1.5rem 0;
    }
    
    /* Tooltips */
    .tooltip {
        position: relative;
    }
    
    .tooltip-text {
        visibility: hidden;
        background: var(--bg-dark);
        color: var(--text-primary);
        padding: 0.5rem 0.75rem;
        border-radius: 6px;
        font-size: 0.8rem;
        position: absolute;
        z-index: 100;
        bottom: 100%;
        left: 50%;
        transform: translateX(-50%);
        white-space: nowrap;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
    }
    
    .tooltip:hover .tooltip-text {
        visibility: visible;
    }
    
    /* Plotly chart container */
    .chart-container {
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: 12px;
        padding: 1rem;
        margin: 1rem 0;
    }
    
    /* Animation keyframes */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes slideIn {
        from { opacity: 0; transform: translateX(-20px); }
        to { opacity: 1; transform: translateX(0); }
    }
    
    .animate-fade-in {
        animation: fadeIn 0.3s ease forwards;
    }
    
    .animate-slide-in {
        animation: slideIn 0.3s ease forwards;
    }
</style>
"""

# SVG Icons
ICONS = {
    "chart": """<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M12 2a14.5 14.5 0 0 0 0 20 14.5 14.5 0 0 0 0-20"/><path d="M2 12h20"/></svg>""",
    "search": """<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/></svg>""",
    "compare": """<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M16 3h5v5"/><path d="M8 3H3v5"/><path d="M21 3l-8.5 8.5"/><path d="M3 3l8.5 8.5"/></svg>""",
    "settings": """<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12.22 2h-.44a2 2 0 0 0-2 2v.18a2 2 0 0 1-1 1.73l-.43.25a2 2 0 0 1-2 0l-.15-.08a2 2 0 0 0-2.73.73l-.22.38a2 2 0 0 0 .73 2.73l.15.1a2 2 0 0 1 1 1.72v.51a2 2 0 0 1-1 1.74l-.15.09a2 2 0 0 0-.73 2.73l.22.38a2 2 0 0 0 2.73.73l.15-.08a2 2 0 0 1 2 0l.43.25a2 2 0 0 1 1 1.73V20a2 2 0 0 0 2 2h.44a2 2 0 0 0 2-2v-.18a2 2 0 0 1 1-1.73l.43-.25a2 2 0 0 1 2 0l.15.08a2 2 0 0 0 2.73-.73l.22-.39a2 2 0 0 0-.73-2.73l-.15-.08a2 2 0 0 1-1-1.74v-.5a2 2 0 0 1 1-1.74l.15-.09a2 2 0 0 0 .73-2.73l-.22-.38a2 2 0 0 0-2.73-.73l-.15.08a2 2 0 0 1-2 0l-.43-.25a2 2 0 0 1-1-1.73V4a2 2 0 0 0-2-2z"/><circle cx="12" cy="12" r="3"/></svg>""",
    "layers": """<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m12.83 2.18a2 2 0 0 0-1.66 0L2.6 6.08a1 1 0 0 0 0 1.83l8.58 3.91a2 2 0 0 0 1.66 0l8.58-3.9a1 1 0 0 0 0-1.83Z"/><path d="m22 12.65-9.17 4.16a2 2 0 0 1-1.66 0L2 12.65"/><path d="m22 17.65-9.17 4.16a2 2 0 0 1-1.66 0L2 17.65"/></svg>""",
    "zap": """<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>""",
    "target": """<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/></svg>""",
    "info": """<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M12 16v-4"/><path d="M12 8h.01"/></svg>""",
    "check": """<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 6 9 17l-5-5"/></svg>""",
    "alert": """<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3Z"/><path d="M12 9v4"/><path d="M12 17h.01"/></svg>""",
    "loader": """<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="12" x2="12" y1="2" y2="6"/><line x1="12" x2="12" y1="18" y2="22"/><line x1="4.93" x2="7.76" y1="4.93" y2="7.76"/><line x1="16.24" x2="19.07" y1="16.24" y2="19.07"/><line x1="2" x2="6" y1="12" y2="12"/><line x1="18" x2="22" y1="12" y2="12"/><line x1="4.93" x2="7.76" y1="19.07" y2="16.24"/><line x1="16.24" x2="19.07" y1="7.76" y2="4.93"/></svg>""",
    "zoom-in": """<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"/><line x1="21" x2="16.65" y1="21" y2="16.65"/><line x1="11" x2="11" y1="8" y2="14"/><line x1="8" x2="14" y1="11" y2="11"/></svg>""",
    "filter": """<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="22 3 2 3 10 12.46 10 19 14 21 14 12.46 22 3"/></svg>""",
}


def render_loading(message: str = "Loading...", show_progress: bool = True) -> str:
    """Return HTML for a loading indicator."""
    progress_html = """
        <div class="loading-progress">
            <div class="loading-progress-bar"></div>
        </div>
    """ if show_progress else ""
    
    return f"""
    <div class="loading-overlay">
        <div class="loading-spinner"></div>
        <p class="loading-text">{message}</p>
        {progress_html}
    </div>
    """


def render_empty_state(message: str = "No data available", icon: str = "info") -> str:
    """Return HTML for an empty state."""
    return f"""
    <div class="empty-state">
        <div class="empty-state-icon" style="color: var(--text-muted);">
            {ICONS.get(icon, ICONS['info'])}
        </div>
        <p>{message}</p>
    </div>
    """


def render_badge(text: str, variant: str = "info") -> str:
    """Return HTML for a status badge."""
    icon = {
        "success": ICONS["check"],
        "warning": ICONS["alert"],
        "error": ICONS["alert"],
        "info": ICONS["info"],
    }.get(variant, ICONS["info"])
    
    return f"""
    <span class="badge badge-{variant}">
        {icon}
        {text}
    </span>
    """


def render_page_header(title: str, subtitle: str, icon_html: str = "") -> str:
    """Return HTML for a page header."""
    return f"""
    <div class="page-header">
        <div class="page-title">
            {icon_html}
            <h1>{title}</h1>
        </div>
        <p class="page-subtitle">{subtitle}</p>
    </div>
    """


def get_score_color(score: float) -> str:
    """Get gradient color based on similarity score."""
    if score >= 0.8:
        return "#10b981"  # Green
    elif score >= 0.6:
        return "#06b6d4"  # Cyan
    elif score >= 0.4:
        return "#6366f1"  # Indigo
    elif score >= 0.2:
        return "#8b5cf6"  # Purple
    else:
        return "#64748b"  # Gray
