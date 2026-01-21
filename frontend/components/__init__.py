# Frontend components package
from .sidebar import render_sidebar
from .visualization import (
    plot_embeddings_scatter,
    plot_word_neighborhood,
    plot_comparison,
    create_similarity_bar_chart
)
from .similarity_panel import (
    render_similarity_results,
    render_comparison_results,
    render_word_chips
)
from .styles import (
    GLOBAL_STYLES,
    ICONS,
    render_loading,
    render_empty_state,
    render_badge,
    render_page_header,
    get_score_color
)
