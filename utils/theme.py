import streamlit as st


def inject_css() -> None:
    css = """
    <style>
    html, body, [data-testid="stAppViewContainer"], .stApp {
        font-family: "Chakra Petch", "Sarabun", "Tahoma", sans-serif;
        background-color: #ffffff;
        color: #1f2937;
    }

    [data-testid="stSidebar"] {
        background-color: #f9fafb;
        color: #1f2937;
        border-right: 1px solid #e5e7eb;
    }

    [data-testid="stSidebar"] * {
        color: #1f2937;
    }

    [data-testid="stSidebarNav"] a[aria-current="page"],
    [data-testid="stSidebarNav"] button[aria-current="page"] {
        background-color: #e5e7eb !important;
        box-shadow: none;
        font-weight: 600;
    }

    .block-container {
        padding-top: 4.5rem;
        padding-bottom: 3rem;
        max-width: 1080px;
    }

    .stButton > button[kind="primary"] *,
    .stButton > button[data-testid="baseButton-primary"] * {
        color: inherit !important;
    }

    .stButton > button[kind="primary"] {
        background-color: #111827;
        color: #ffffff !important;
        border-radius: 8px;
        border: none;
        font-weight: 600;
    }

    .stButton > button[kind="primary"]:hover {
        background-color: #374151;
        color: #ffffff !important;
    }

    .stButton > button[kind="secondary"] {
        border-radius: 8px;
        border: 1px solid #d1d5db;
        background-color: #ffffff;
        color: #1f2937;
    }

    .stButton > button[kind="secondary"]:hover {
        border-color: #9ca3af;
        background-color: #f9fafb;
        color: #111827;
    }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)


def render_hero(title: str, subtitle: str) -> None:
    html = f"""
    <div style="
        background-color: #ffffff;
        border: 1px solid #e5e7eb;
        border-radius: 12px;
        padding: 24px 28px;
        text-align: center;
        margin-bottom: 22px;
    ">
        <h1 style="font-size: 24px; font-weight: 700; color: #111827; margin: 0 0 6px 0; border: none; padding: 0;">{title}</h1>
        <p style="font-size: 14px; color: #6b7280; margin: 0; padding: 0;">{subtitle}</p>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)
