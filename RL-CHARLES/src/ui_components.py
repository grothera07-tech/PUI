"""
Shared UI components and theme utilities for premium enterprise dashboard.
Eliminates duplication and ensures consistent design language across all pages.
"""

import streamlit as st
from typing import Optional, Dict, Any


# Color palette
COLORS = {
    "primary": "#1E87EC",
    "primary_dark": "#146bc0",
    "primary_soft": "#eef6ff",
    "accent": "#AF1B09",
    "accent_soft": "#fff1ef",
    "text": "#111827",
    "muted": "#6B7280",
    "bg": "#F4F7FB",
    "bg_soft": "#FAFBFD",
    "card": "#FFFFFF",
    "border": "#E5E7EB",
    "success": "#16A34A",
    "warning": "#D97706",
    "danger": "#DC2626",
}

SHADOWS = {
    "sm": "0 8px 24px rgba(15, 23, 42, 0.05)",
    "md": "0 18px 38px rgba(15, 23, 42, 0.08)",
}

RADIUS = {
    "xl": "28px",
    "lg": "22px",
    "md": "18px",
    "sm": "14px",
}


def inject_global_styles() -> None:
    """Inject comprehensive global CSS theme used by all pages."""
    st.markdown(
        f"""
        <style>
            :root {{
                --primary: {COLORS['primary']};
                --primary-dark: {COLORS['primary_dark']};
                --primary-soft: {COLORS['primary_soft']};
                --accent: {COLORS['accent']};
                --accent-soft: {COLORS['accent_soft']};
                --text: {COLORS['text']};
                --muted: {COLORS['muted']};
                --bg: {COLORS['bg']};
                --bg-soft: {COLORS['bg_soft']};
                --card: {COLORS['card']};
                --border: {COLORS['border']};
                --success: {COLORS['success']};
                --warning: {COLORS['warning']};
                --danger: {COLORS['danger']};
                --shadow-sm: {SHADOWS['sm']};
                --shadow-md: {SHADOWS['md']};
                --radius-xl: {RADIUS['xl']};
                --radius-lg: {RADIUS['lg']};
                --radius-md: {RADIUS['md']};
                --radius-sm: {RADIUS['sm']};
            }}

            .stApp {{
                background: linear-gradient(180deg, #F8FBFF 0%, var(--bg) 28%, #F3F6FA 100%);
                color: var(--text);
            }}

            .block-container {{
                max-width: 1450px;
                padding-top: 1.6rem;
                padding-bottom: 2.5rem;
            }}

            h1, h2, h3, h4, h5 {{
                color: var(--text);
                letter-spacing: -0.02em;
            }}

            p, span, label, .stMarkdown, .stCaption {{
                color: var(--text);
            }}

            [data-testid="stSidebar"] {{
                background: linear-gradient(180deg, #f8fbff 0%, #ffffff 100%);
                border-right: 1px solid rgba(229, 231, 235, 0.9);
            }}

            [data-testid="stSidebarNav"] {{
                padding-top: 0.2rem;
            }}

            [data-testid="stSidebarNav"] a {{
                border-radius: 16px;
                margin-bottom: 0.25rem;
                padding-top: 0.35rem;
                padding-bottom: 0.35rem;
            }}

            [data-testid="stSidebarNav"] a:hover {{
                background: rgba(30, 135, 236, 0.08);
            }}

            /* Hero Surface */
            .hero-surface {{
                background: linear-gradient(135deg, #ffffff 0%, #f7fbff 70%, rgba(30,135,236,0.08) 100%);
                border: 1px solid rgba(229, 231, 235, 0.92);
                border-radius: var(--radius-xl);
                padding: 1.4rem 1.5rem;
                box-shadow: var(--shadow-md);
                margin-bottom: 1.25rem;
            }}

            .hero-kicker {{
                color: var(--primary);
                font-size: 0.82rem;
                font-weight: 800;
                text-transform: uppercase;
                letter-spacing: 0.08em;
                margin-bottom: 0.35rem;
            }}

            .hero-title {{
                font-size: 2.15rem;
                line-height: 1.1;
                font-weight: 850;
                color: var(--text);
                margin-bottom: 0.4rem;
            }}

            .hero-copy {{
                color: var(--muted);
                font-size: 0.98rem;
                line-height: 1.7;
                max-width: 760px;
            }}

            /* Section Header */
            .section-intro {{
                margin: 0.35rem 0 0.85rem;
            }}

            .section-kicker {{
                color: var(--primary);
                font-size: 0.78rem;
                font-weight: 800;
                letter-spacing: 0.08em;
                text-transform: uppercase;
                margin-bottom: 0.2rem;
            }}

            .section-title {{
                color: var(--text);
                font-size: 1.2rem;
                font-weight: 800;
                margin-bottom: 0.12rem;
            }}

            .section-copy {{
                color: var(--muted);
                font-size: 0.93rem;
                line-height: 1.65;
            }}

            /* Metric Card */
            div[data-testid="stVerticalBlockBorderWrapper"] {{
                background: var(--card);
                border: 1px solid rgba(229, 231, 235, 0.95);
                border-radius: var(--radius-lg);
                box-shadow: var(--shadow-sm);
            }}

            .metric-tile {{
                background: linear-gradient(180deg, #ffffff 0%, #fbfdff 100%);
                border: 1px solid rgba(229, 231, 235, 0.95);
                border-radius: var(--radius-lg);
                padding: 1rem 1.1rem;
                box-shadow: var(--shadow-sm);
                min-height: 144px;
                position: relative;
                overflow: hidden;
            }}

            .metric-tile::after {{
                content: "";
                position: absolute;
                top: 0;
                left: 0;
                width: 100%;
                height: 4px;
                background: linear-gradient(90deg, var(--primary), #6db6ff);
            }}

            .metric-label {{
                color: var(--muted);
                font-size: 0.8rem;
                font-weight: 800;
                letter-spacing: 0.08em;
                text-transform: uppercase;
                margin-bottom: 0.7rem;
            }}

            .metric-value {{
                color: var(--text);
                font-size: 1.8rem;
                font-weight: 850;
                line-height: 1.15;
                margin-bottom: 0.28rem;
                word-break: break-word;
                overflow-wrap: break-word;
            }}

            .metric-note {{
                color: var(--muted);
                font-size: 0.9rem;
                line-height: 1.55;
            }}

            /* Status Badges */
            .status-pill {{
                display: inline-flex;
                align-items: center;
                gap: 0.35rem;
                padding: 0.42rem 0.75rem;
                border-radius: 999px;
                font-size: 0.78rem;
                font-weight: 800;
                border: 1px solid transparent;
            }}

            .status-ready {{
                background: rgba(22, 163, 74, 0.12);
                color: var(--success);
                border-color: rgba(22, 163, 74, 0.16);
            }}

            .status-warn {{
                background: rgba(217, 119, 6, 0.12);
                color: var(--warning);
                border-color: rgba(217, 119, 6, 0.18);
            }}

            /* Mini Stats */
            .mini-stat {{
                display: inline-flex;
                align-items: center;
                padding: 0.38rem 0.7rem;
                border-radius: 999px;
                font-size: 0.79rem;
                font-weight: 800;
                color: var(--text);
                border: 1px solid rgba(229,231,235,0.95);
                background: #ffffff;
                margin-right: 0.4rem;
                margin-bottom: 0.4rem;
            }}

            /* Result Panel */
            .result-panel {{
                background: linear-gradient(135deg, rgba(30,135,236,0.12), #ffffff 62%, rgba(175,27,9,0.06) 100%);
                border: 1px solid rgba(30,135,236,0.16);
                border-radius: var(--radius-xl);
                padding: 1.2rem 1.25rem;
                box-shadow: var(--shadow-md);
            }}

            .result-kicker {{
                color: var(--primary);
                font-size: 0.82rem;
                text-transform: uppercase;
                letter-spacing: 0.08em;
                font-weight: 800;
                margin-bottom: 0.45rem;
            }}

            .result-number {{
                color: var(--text);
                font-size: 2.5rem;
                font-weight: 850;
                line-height: 1.05;
                margin-bottom: 0.5rem;
                word-break: break-word;
                overflow-wrap: break-word;
            }}

            .result-copy {{
                color: var(--muted);
                font-size: 0.95rem;
                line-height: 1.65;
            }}

            /* Callout Box */
            .callout-box {{
                background: #ffffff;
                border: 1px solid rgba(229,231,235,0.95);
                border-left: 4px solid var(--primary);
                border-radius: var(--radius-md);
                padding: 0.9rem 1rem;
                box-shadow: var(--shadow-sm);
            }}

            .callout-title {{
                color: var(--text);
                font-size: 0.84rem;
                font-weight: 800;
                text-transform: uppercase;
                letter-spacing: 0.08em;
                margin-bottom: 0.2rem;
            }}

            .callout-copy {{
                color: var(--muted);
                font-size: 0.93rem;
                line-height: 1.65;
            }}

            /* Buttons */
            .stButton > button,
            .stDownloadButton > button {{
                background: linear-gradient(135deg, var(--primary), var(--primary-dark));
                color: #ffffff;
                border-radius: 14px;
                border: none;
                font-weight: 800;
                padding: 0.72rem 1rem;
                box-shadow: 0 10px 28px rgba(30, 135, 236, 0.24);
            }}

            .stButton > button:hover,
            .stDownloadButton > button:hover {{
                filter: brightness(1.03);
            }}

            /* Form inputs */
            .stTextInput input,
            .stNumberInput input,
            .stDateInput input,
            .stTextArea textarea,
            div[data-baseweb="select"] > div {{
                border-radius: 14px !important;
                border: 1px solid rgba(229,231,235,0.95) !important;
                background: #ffffff !important;
            }}

            /* Data display */
            .stDataFrame,
            [data-testid="stTable"] {{
                background: #ffffff;
                border: 1px solid rgba(229,231,235,0.95);
                border-radius: var(--radius-lg);
                overflow: hidden;
                box-shadow: var(--shadow-sm);
            }}

            [data-testid="stAlert"] {{
                border-radius: 16px;
                border: 1px solid rgba(229,231,235,0.95);
            }}

            /* Sidebar branding */
            .sidebar-shell {{
                background: linear-gradient(180deg, rgba(30,135,236,0.10), rgba(255,255,255,0.98));
                border: 1px solid rgba(30,135,236,0.14);
                border-radius: var(--radius-xl);
                padding: 1.1rem 1rem 1rem;
                box-shadow: var(--shadow-md);
                margin-bottom: 0.9rem;
            }}

            .sidebar-kicker {{
                color: var(--primary);
                font-size: 0.78rem;
                font-weight: 800;
                text-transform: uppercase;
                letter-spacing: 0.08em;
                margin-bottom: 0.3rem;
            }}

            .sidebar-title {{
                color: var(--text);
                font-size: 1.18rem;
                font-weight: 800;
                line-height: 1.25;
                margin-bottom: 0.3rem;
            }}

            .sidebar-copy {{
                color: var(--muted);
                font-size: 0.92rem;
                line-height: 1.65;
                margin-bottom: 0.9rem;
            }}

            /* Responsive */
            @media (max-width: 900px) {{
                .hero-title {{
                    font-size: 1.7rem;
                }}

                .result-number,
                .metric-value {{
                    font-size: 1.75rem;
                }}
            }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def hero_section(
    kicker: str, title: str, copy: str = "", badge_class: str = "status-ready", badge_text: str = ""
) -> None:
    """Render a hero banner section with title, description, and optional status badge."""
    badge_html = f'<div style="margin-top:0.95rem;"><span class="status-pill {badge_class}">{badge_text}</span></div>' if badge_text else ""
    st.markdown(
        f"""
        <div class="hero-surface">
            <div class="hero-kicker">{kicker}</div>
            <div class="hero-title">{title}</div>
            <div class="hero-copy">{copy}</div>
            {badge_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def section_header(kicker: str, title: str, copy: str = "") -> None:
    """Render a section header with kicker, title, and optional description."""
    st.markdown(
        f"""
        <div class="section-intro">
            <div class="section-kicker">{kicker}</div>
            <div class="section-title">{title}</div>
            {'<div class="section-copy">' + copy + '</div>' if copy else ''}
        </div>
        """,
        unsafe_allow_html=True,
    )


def metric_tile(label: str, value: str, note: str = "") -> None:
    """Render a KPI metric card with label, value, and optional note."""
    note_html = f'<div class="metric-note">{note}</div>' if note else ""
    st.markdown(
        f"""
        <div class="metric-tile">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
            {note_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def status_badge(is_ready: bool, ready_text: str = "Ready", warning_text: str = "Not ready") -> tuple[str, str]:
    """Return badge class and text based on ready status."""
    if is_ready:
        return "status-ready", ready_text
    return "status-warn", warning_text


def render_status_pills(pills: list[str]) -> str:
    """Render a list of mini stat pills as HTML."""
    return "".join([f'<span class="mini-stat">{pill}</span>' for pill in pills])


def get_plotly_theme() -> Dict[str, Any]:
    """Return a standardized Plotly theme configuration for consistent charts across all pages."""
    return {
        "layout": {
            "height": 390,
            "margin": dict(l=10, r=10, t=10, b=10),
            "paper_bgcolor": "white",
            "plot_bgcolor": "white",
            "hovermode": "x unified",
            "font": dict(family="sans-serif", size=12, color=COLORS["text"]),
        },
        "yaxis": {
            "gridcolor": "rgba(229,231,235,0.85)",
            "tickprefix": "Rp ",
        },
    }


def format_currency_label(value: float) -> str:
    """Format a numeric value as Indonesian Rupiah for display."""
    if value >= 1_000_000:
        return f"Rp {value/1_000_000:.1f}M"
    elif value >= 1_000:
        return f"Rp {value/1_000:.0f}K"
    return f"Rp {value:.0f}"
