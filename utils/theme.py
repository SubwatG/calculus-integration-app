import streamlit as st


def inject_css() -> None:
    css = """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Chakra+Petch:wght@500;600;700&family=IBM+Plex+Sans+Thai+Looped:wght@300;400;500;600;700&family=Inter:wght@400;500;600;700&display=swap');

    /* Global Typography & Palette */
    html, body, [data-testid="stAppViewContainer"], .stApp {
        font-family: "IBM Plex Sans Thai Looped", "Inter", -apple-system, BlinkMacSystemFont, sans-serif !important;
        background-color: #FFFFFF !important;
        color: #0F172A !important;
    }

    h1, h2, h3, h4, h5, h6 {
        font-family: "Chakra Petch", "Inter", sans-serif !important;
        color: #0A2540 !important;
        font-weight: 700 !important;
    }

    p, span, label, li {
        color: #1E293B !important;
    }

    /* KaTeX Math Clarity */
    .katex, .katex-display, .katex * {
        color: #0F172A !important;
    }

    /* Container Spacing */
    .block-container {
        padding-top: 3.5rem !important;
        padding-bottom: 3rem !important;
        max-width: 1040px !important;
    }

    /* Cards & Containers */
    [data-testid="stVerticalBlockBorderWrapper"] {
        background-color: #FFFFFF !important;
        border: 1px solid #E2E8F0 !important;
        border-radius: 12px !important;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04) !important;
    }

    /* Primary Buttons */
    .stButton > button[kind="primary"],
    .stButton > button[data-testid="baseButton-primary"] {
        background-color: #1D4ED8 !important;
        color: #FFFFFF !important;
        border-radius: 8px !important;
        border: 1px solid #1E40AF !important;
        font-weight: 600 !important;
        box-shadow: 0 1px 2px rgba(0, 0, 0, 0.06) !important;
    }

    .stButton > button[kind="primary"] *,
    .stButton > button[data-testid="baseButton-primary"] * {
        color: #FFFFFF !important;
    }

    .stButton > button[kind="primary"]:hover,
    .stButton > button[data-testid="baseButton-primary"]:hover {
        background-color: #1E40AF !important;
        border-color: #1E3A8A !important;
        color: #FFFFFF !important;
    }

    /* Secondary Buttons */
    .stButton > button[kind="secondary"],
    .stButton > button[data-testid="baseButton-secondary"] {
        background-color: #F8FAFC !important;
        color: #1E293B !important;
        border-radius: 8px !important;
        border: 1px solid #CBD5E1 !important;
        font-weight: 500 !important;
        box-shadow: 0 1px 2px rgba(0, 0, 0, 0.03) !important;
    }

    .stButton > button[kind="secondary"] *,
    .stButton > button[data-testid="baseButton-secondary"] * {
        color: #1E293B !important;
    }

    .stButton > button[kind="secondary"]:hover,
    .stButton > button[data-testid="baseButton-secondary"]:hover {
        background-color: #F1F5F9 !important;
        border-color: #94A3B8 !important;
        color: #0F172A !important;
    }

    /* Inputs & Selectboxes */
    input, textarea, select {
        color: #0F172A !important;
        background-color: #FFFFFF !important;
        border-color: #CBD5E1 !important;
    }

    /* Sidebar Navigation */
    [data-testid="stSidebar"] {
        background-color: #F8FAFC !important;
        border-right: 1px solid #E2E8F0 !important;
    }

    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        color: #0A2540 !important;
    }

    [data-testid="stSidebar"] [data-testid="stSidebarNavItems"] a,
    [data-testid="stSidebar"] [data-testid="stSidebarNavItems"] button {
        border-radius: 6px !important;
        margin: 2px 0 !important;
    }

    [data-testid="stSidebarNavItems"] a[aria-current="page"],
    [data-testid="stSidebarNavItems"] button[aria-current="page"] {
        background-color: #EFF6FF !important;
        color: #1D4ED8 !important;
        font-weight: 600 !important;
        border-left: 3px solid #1D4ED8 !important;
    }

    /* Radio buttons & Checkboxes */
    [data-testid="stRadio"] label,
    [data-testid="stCheckbox"] label {
        color: #1E293B !important;
        font-size: 0.95rem !important;
    }

    /* Alert callouts */
    [data-testid="stAlert"] {
        border-radius: 8px !important;
        font-size: 0.92rem !important;
    }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)


def render_hero(title: str, subtitle: str) -> None:
    html = f"""
    <div style="
        background: linear-gradient(135deg, #F8FAFC 0%, #EFF6FF 100%);
        border: 1px solid #DBEAFE;
        border-left: 5px solid #1D4ED8;
        border-radius: 12px;
        padding: 20px 24px;
        margin-bottom: 22px;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
    ">
        <h1 style="font-family: 'Chakra Petch', sans-serif; font-size: 23px; font-weight: 700; color: #0A2540; margin: 0 0 6px 0; padding: 0; border: none;">{title}</h1>
        <p style="font-family: 'IBM Plex Sans Thai Looped', sans-serif; font-size: 14.5px; color: #475569; margin: 0; padding: 0;">{subtitle}</p>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)
