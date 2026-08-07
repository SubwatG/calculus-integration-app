import streamlit as st


def inject_css() -> None:
    css = """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Chakra+Petch:wght@400;500;600;700&display=swap');

    html, body, [data-testid="stAppViewContainer"], .stApp {
        font-family: "Chakra Petch", "Sarabun", "Tahoma", sans-serif;
        background-color: #eaf1ff;
        color: #232a4d;
    }

    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #b9bce8, #d3d5f5);
        color: #232a4d;
    }

    [data-testid="stSidebar"] * {
        color: #232a4d;
    }

    [data-testid="stSidebarNav"] a[aria-current="page"],
    [data-testid="stSidebarNav"] button[aria-current="page"] {
        background-color: rgba(255, 255, 255, 0.62) !important;
        box-shadow: 0 2px 8px rgba(45, 58, 138, 0.12);
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
        background-color: #3d4bc5;
        color: #ffffff !important;
        border-radius: 999px;
        border: none;
        font-weight: 600;
    }

    .stButton > button[kind="primary"]:hover {
        background-color: #2f3aa8;
        color: #ffffff !important;
    }

    .stButton > button[kind="secondary"] {
        border-radius: 10px;
        border: 1.5px solid #d6dff5;
        background-color: #ffffff;
        color: #232a4d;
    }

    .stButton > button[kind="secondary"]:hover {
        border-color: #3d4bc5;
        background-color: #e4e9ff;
        color: #2f3aa8;
    }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)


def render_hero(title: str, subtitle: str) -> None:
    html = f"""
    <div style="
        background: linear-gradient(180deg, #cfdcff, #dde8ff);
        border: 1.5px solid #b9cbfa;
        border-radius: 16px;
        padding: 24px 28px;
        text-align: center;
        margin-bottom: 22px;
    ">
        <h1 style="font-size: 24px; font-weight: 700; color: #2f3aa8; margin: 0 0 6px 0; border: none; padding: 0;">{title}</h1>
        <p style="font-size: 14px; color: #5a6289; margin: 0; padding: 0;">{subtitle}</p>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)
