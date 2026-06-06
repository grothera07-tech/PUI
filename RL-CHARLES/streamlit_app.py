import streamlit as st
from src.app_utils import model_ready
from src.ui_components import inject_global_styles, status_badge

st.set_page_config(
    page_title="Prediksi Penjualan UMKM",
    page_icon="📊",
    layout="wide",
)


def render_sidebar_brand() -> None:
    """Render premium branded sidebar with product narrative and status indicator."""
    ready = model_ready()
    badge_class, badge_text = status_badge(
        ready, 
        ready_text="Model & data ready",
        warning_text="Model / data not ready"
    )

    with st.sidebar:
        st.markdown(
            f"""
            <div class="sidebar-shell">
                <div class="sidebar-kicker">📊 Analytics Suite</div>
                <div class="sidebar-title">Sales Forecast Pro</div>
                <div class="sidebar-copy">
                    Enterprise-grade sales analytics platform. Analyze historical trends, 
                    simulate scenarios, and evaluate machine learning model performance 
                    in a unified workspace.
                </div>
                <div class="status-pill {badge_class}">{badge_text}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.divider()
        st.caption("**Navigation Guide**")
        st.caption("📈 Dashboard Data → Analyze sales trends and product performance")
        st.caption("🔮 Prediksi Penjualan → Build scenarios and predict outcomes")
        st.caption("🎯 Evaluasi Model → Review model quality and feature drivers")
        st.divider()
        st.markdown(
            """
            <div class="callout-box">
                <div class="callout-title">🚀 Workflow Tip</div>
                <div class="callout-copy">
                    Start from Data Dashboard to understand trends, then explore predictions 
                    with different scenarios, and finish with Model Evaluation for deep insight.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )


# Inject global design system used by all pages
inject_global_styles()
render_sidebar_brand()

pages = [
    st.Page("pages/1_Dashboard_Data.py", title="Dashboard Data"),
    st.Page("pages/2_Prediksi_Penjualan.py", title="Prediksi Penjualan"),
    st.Page("pages/3_Evaluasi_Model.py", title="Evaluasi Model"),
]

navigation = st.navigation(pages)
navigation.run()
