"""
Visualization components using Plotly with progressive loading and rich animations.
"""
import plotly.express as px
import plotly.graph_objects as go
from typing import Dict, List, Optional, Tuple
import pandas as pd
import numpy as np

from frontend.components.styles import get_score_color


# Color palette for gradient visualization
COLOR_PALETTE = [
    "#6366f1",  # Indigo
    "#8b5cf6",  # Purple
    "#a855f7",  # Fuchsia
    "#d946ef",  # Pink
    "#ec4899",  # Rose
]


def create_base_layout(title: str, height: int = 600) -> dict:
    """Create base layout configuration for all charts."""
    return dict(
        title=dict(
            text=title,
            x=0.5,
            font=dict(size=16, color="#f8fafc", family="Inter, sans-serif")
        ),
        paper_bgcolor="#1e293b",
        plot_bgcolor="#0f172a",
        font=dict(family="Inter, sans-serif", color="#94a3b8"),
        height=height,
        margin=dict(l=60, r=40, t=60, b=60),
        xaxis=dict(
            gridcolor="#334155",
            zerolinecolor="#334155",
            title_font=dict(color="#94a3b8"),
            tickfont=dict(color="#64748b"),
        ),
        yaxis=dict(
            gridcolor="#334155",
            zerolinecolor="#334155",
            title_font=dict(color="#94a3b8"),
            tickfont=dict(color="#64748b"),
        ),
        hoverlabel=dict(
            bgcolor="#1e293b",
            font_size=12,
            font_family="Inter, sans-serif",
            bordercolor="#6366f1",
        ),
        dragmode="zoom",  # Enable zoom by default
        modebar=dict(
            bgcolor="rgba(0,0,0,0)",
            color="#64748b",
            activecolor="#6366f1",
        ),
    )


def plot_embeddings_scatter(
    data: Dict,
    highlight_words: Optional[List[str]] = None,
    title: Optional[str] = None,
    show_labels: bool = True,
    animate: bool = True
) -> go.Figure:
    """
    Create an interactive scatter plot of word embeddings with gradient colors.
    
    Args:
        data: API response with embedding points
        highlight_words: Optional list of words to highlight
        title: Optional custom title
        show_labels: Whether to show word labels
        animate: Whether to animate points on load
    
    Returns:
        Plotly figure
    """
    if not data or "points" not in data:
        fig = go.Figure()
        fig.update_layout(**create_base_layout("No Data"))
        fig.add_annotation(
            text="No data available. Check your connection to the backend.",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=14, color="#94a3b8")
        )
        return fig
    
    # Create DataFrame
    points = data["points"]
    df = pd.DataFrame(points)
    
    # Add highlight column
    if highlight_words:
        highlight_words_lower = [w.lower() for w in highlight_words]
        df["highlighted"] = df["word"].str.lower().isin(highlight_words_lower)
    else:
        df["highlighted"] = False
    
    # Normalize frequency for color and size
    if "frequency" in df.columns and df["frequency"].max() > 0:
        df["freq_norm"] = df["frequency"] / df["frequency"].max()
        df["marker_size"] = 6 + df["freq_norm"] * 14
    else:
        df["freq_norm"] = 0.5
        df["marker_size"] = 8
    
    # Create figure
    model_type = data.get("model_type", "Unknown").upper()
    method = data.get("reduction_method", "pca").upper()
    
    if title is None:
        title = f"<b>{model_type}</b> Embeddings ({method})"
    
    fig = go.Figure()
    
    # Non-highlighted points with gradient color based on frequency
    df_normal = df[~df["highlighted"]]
    if len(df_normal) > 0:
        fig.add_trace(go.Scatter(
            x=df_normal["x"],
            y=df_normal["y"],
            mode="markers+text" if show_labels else "markers",
            marker=dict(
                size=df_normal["marker_size"],
                color=df_normal["freq_norm"],
                colorscale=[
                    [0.0, "#64748b"],
                    [0.25, "#6366f1"],
                    [0.5, "#8b5cf6"],
                    [0.75, "#a855f7"],
                    [1.0, "#06b6d4"],
                ],
                showscale=True,
                colorbar=dict(
                    title=dict(text="Frequency", side="right", font=dict(color="#94a3b8")),
                    tickfont=dict(color="#94a3b8"),
                    bgcolor="rgba(0,0,0,0)",
                ),
                opacity=0.8,
                line=dict(width=1, color="rgba(255,255,255,0.2)")
            ),
            text=df_normal["word"] if show_labels else None,
            textposition="top center",
            textfont=dict(size=9, color="#94a3b8"),
            hovertemplate=(
                "<b style='color:#f8fafc;'>%{text}</b><br>"
                "<span style='color:#94a3b8;'>Position:</span> (%{x:.3f}, %{y:.3f})<br>"
                "<span style='color:#94a3b8;'>Frequency:</span> %{customdata}<br>"
                "<extra></extra>"
            ),
            customdata=df_normal.get("frequency", [0] * len(df_normal)),
            name="Words",
        ))
    
    # Highlighted points
    df_highlight = df[df["highlighted"]]
    if len(df_highlight) > 0:
        fig.add_trace(go.Scatter(
            x=df_highlight["x"],
            y=df_highlight["y"],
            mode="markers+text",
            marker=dict(
                size=16,
                color="#ef4444",
                symbol="star",
                line=dict(width=2, color="#fca5a5")
            ),
            text=df_highlight["word"],
            textposition="top center",
            textfont=dict(size=11, color="#ef4444", family="Inter, sans-serif"),
            hovertemplate=(
                "<b style='color:#ef4444;'>%{text}</b> ★<br>"
                "<span style='color:#94a3b8;'>Position:</span> (%{x:.3f}, %{y:.3f})<br>"
                "<extra></extra>"
            ),
            name="Highlighted",
        ))
    
    # Apply layout
    layout = create_base_layout(title)
    layout.update(
        xaxis_title="Component 1",
        yaxis_title="Component 2",
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(color="#94a3b8"),
            bgcolor="rgba(0,0,0,0)",
        ),
        hovermode="closest",
    )
    fig.update_layout(**layout)
    
    # Add annotations for controls
    fig.add_annotation(
        text="Scroll to zoom • Drag to pan • Double-click to reset",
        xref="paper", yref="paper",
        x=0.5, y=-0.12,
        showarrow=False,
        font=dict(size=10, color="#64748b"),
    )
    
    return fig


def plot_word_neighborhood(
    data: Dict,
    title: Optional[str] = None,
    animate_connections: bool = True
) -> go.Figure:
    """
    Create a visualization of a word and its neighbors with animated connections.
    
    Args:
        data: API response with neighborhood data
        title: Optional custom title
        animate_connections: Whether to animate connection lines
    
    Returns:
        Plotly figure
    """
    if not data or "points" not in data:
        fig = go.Figure()
        fig.update_layout(**create_base_layout("No Data", height=500))
        fig.add_annotation(
            text="Word not found in vocabulary",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=14, color="#f59e0b")
        )
        return fig
    
    points = data["points"]
    query_word = data.get("query_word", "word")
    
    if title is None:
        title = f"Neighborhood of <b>{query_word}</b>"
    
    # Create DataFrame
    df = pd.DataFrame(points)
    
    # Separate query word and neighbors
    df_query = df[df.get("is_query", False) == True]
    df_neighbors = df[df.get("is_query", False) == False]
    
    fig = go.Figure()
    
    # Draw connection lines from query to neighbors
    if len(df_query) > 0 and len(df_neighbors) > 0:
        query_x = df_query["x"].values[0]
        query_y = df_query["y"].values[0]
        
        for _, row in df_neighbors.iterrows():
            similarity = row.get("similarity", 0.5)
            color = get_score_color(similarity)
            opacity = max(0.3, similarity)
            
            fig.add_trace(go.Scatter(
                x=[query_x, row["x"]],
                y=[query_y, row["y"]],
                mode="lines",
                line=dict(color=color, width=1 + similarity * 2),
                opacity=opacity,
                hoverinfo="skip",
                showlegend=False
            ))
    
    # Neighbor points with gradient based on similarity
    if len(df_neighbors) > 0:
        similarities = df_neighbors.get("similarity", pd.Series([0.5] * len(df_neighbors)))
        sizes = 8 + similarities * 12
        
        fig.add_trace(go.Scatter(
            x=df_neighbors["x"],
            y=df_neighbors["y"],
            mode="markers+text",
            marker=dict(
                size=sizes,
                color=similarities,
                colorscale=[
                    [0.0, "#64748b"],
                    [0.3, "#6366f1"],
                    [0.6, "#8b5cf6"],
                    [0.8, "#06b6d4"],
                    [1.0, "#10b981"],
                ],
                showscale=True,
                colorbar=dict(
                    title=dict(text="Similarity", side="right", font=dict(color="#94a3b8")),
                    tickfont=dict(color="#94a3b8"),
                ),
                line=dict(width=1, color="rgba(255,255,255,0.3)")
            ),
            text=df_neighbors["word"],
            textposition="top center",
            textfont=dict(size=10, color="#f8fafc"),
            hovertemplate=(
                "<b>%{text}</b><br>"
                "Similarity: %{marker.color:.4f}<br>"
                "<extra></extra>"
            ),
            name="Neighbors"
        ))
    
    # Query word point (center/focus)
    if len(df_query) > 0:
        fig.add_trace(go.Scatter(
            x=df_query["x"],
            y=df_query["y"],
            mode="markers+text",
            marker=dict(
                size=24,
                color="#ef4444",
                symbol="star",
                line=dict(width=2, color="#fca5a5")
            ),
            text=df_query["word"],
            textposition="top center",
            textfont=dict(size=12, color="#ef4444", family="Inter, sans-serif"),
            hovertemplate="<b>%{text}</b> (Query)<extra></extra>",
            name="Query"
        ))
    
    # Apply layout
    layout = create_base_layout(title, height=500)
    layout.update(
        xaxis_title="Component 1",
        yaxis_title="Component 2",
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(color="#94a3b8"),
        ),
    )
    fig.update_layout(**layout)
    
    return fig


def plot_comparison(
    data1: Dict,
    data2: Dict,
    label1: str = "Model 1",
    label2: str = "Model 2"
) -> Tuple[go.Figure, go.Figure]:
    """
    Create side-by-side comparison plots.
    
    Returns:
        Tuple of two Plotly figures
    """
    fig1 = plot_embeddings_scatter(data1, title=f"<b>{label1}</b>", show_labels=False)
    fig2 = plot_embeddings_scatter(data2, title=f"<b>{label2}</b>", show_labels=False)
    
    # Make them smaller for side-by-side
    fig1.update_layout(height=450, showlegend=False)
    fig2.update_layout(height=450, showlegend=False)
    
    # Remove colorbar for comparison view
    fig1.update_traces(marker=dict(showscale=False), selector=dict(name="Words"))
    fig2.update_traces(marker=dict(showscale=False), selector=dict(name="Words"))
    
    return fig1, fig2


def create_similarity_bar_chart(similar_words: List[Dict], query_word: str) -> go.Figure:
    """
    Create a horizontal bar chart for similarity scores.
    
    Args:
        similar_words: List of {word, similarity} dicts
        query_word: The query word
    
    Returns:
        Plotly figure
    """
    if not similar_words:
        fig = go.Figure()
        fig.update_layout(**create_base_layout("No Results", height=300))
        return fig
    
    words = [w["word"] for w in similar_words]
    scores = [w["similarity"] for w in similar_words]
    colors = [get_score_color(s) for s in scores]
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=scores,
        y=words,
        orientation='h',
        marker=dict(
            color=colors,
            line=dict(width=0),
            cornerradius=4,
        ),
        text=[f"{s:.3f}" for s in scores],
        textposition='outside',
        textfont=dict(color="#f8fafc", size=11),
        hovertemplate="<b>%{y}</b><br>Similarity: %{x:.4f}<extra></extra>",
    ))
    
    layout = create_base_layout(f"Similar to <b>{query_word}</b>", height=max(250, len(words) * 35))
    layout.update(
        xaxis_title="Cosine Similarity",
        yaxis=dict(
            autorange="reversed",
            tickfont=dict(color="#f8fafc", size=12),
        ),
        xaxis=dict(
            range=[0, 1.1],
            dtick=0.2,
        ),
        bargap=0.4,
    )
    fig.update_layout(**layout)
    
    return fig
