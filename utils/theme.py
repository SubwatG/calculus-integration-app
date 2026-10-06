import streamlit as st


def inject_css() -> None:
    css = """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Fredoka:wght@400;500;600;700&family=Mali:ital,wght@0,400;0,500;0,600;0,700;1,400&family=Outfit:wght@400;500;600;700;800;900&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Material+Symbols+Rounded:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200');

    /* Global Typography & Pink Bauhaus Pop Canvas */
    html, body, [data-testid="stAppViewContainer"], .stApp {
        font-family: "Mali", "Outfit", -apple-system, BlinkMacSystemFont, sans-serif !important;
        background-color: #FFF0F5 !important;
        background-image: radial-gradient(#FBCFE8 1.5px, transparent 1.5px) !important;
        background-size: 22px 22px !important;
        color: #18181B !important;
    }

    /* Cheerful Rounded Headlines */
    h1, h2, h3, h4, h5, h6 {
        font-family: "Fredoka", "Mali", "Outfit", sans-serif !important;
        color: #18181B !important;
        font-weight: 700 !important;
        letter-spacing: -0.01em !important;
    }

    p, label, li, span:not([class*="material"]):not([data-testid*="Icon"]):not(.katex):not(.katex *) {
        font-family: "Mali", "Outfit", sans-serif !important;
        color: #18181B !important;
        font-weight: 500 !important;
    }

    /* Material Symbols / Icon Font Protection */
    [data-testid="stIconMaterial"],
    .material-symbols-rounded,
    .material-symbols-outlined,
    .material-icons,
    [data-testid="stExpanderToggleIcon"] span,
    [data-testid="stExpandSidebarButton"] span {
        font-family: "Material Symbols Rounded", "Material Icons" !important;
        font-weight: normal !important;
        font-style: normal !important;
        font-size: 20px !important;
        line-height: 1 !important;
        letter-spacing: normal !important;
        text-transform: none !important;
        display: inline-block !important;
        white-space: nowrap !important;
        word-wrap: normal !important;
        direction: ltr !important;
        -webkit-font-smoothing: antialiased !important;
    }

    /* Cute Bauhaus Sidebar Collapse / Expand Button */
    [data-testid="stExpandSidebarButton"],
    [data-testid="stSidebarCollapseButton"] {
        background-color: #FEF08A !important;
        border: 2.5px solid #18181B !important;
        border-radius: 12px !important;
        box-shadow: 3px 3px 0px #18181B !important;
        color: #18181B !important;
        transition: all 0.12s ease-out !important;
        padding: 6px 12px !important;
        display: inline-flex !important;
        align-items: center !important;
        justify-content: center !important;
        cursor: pointer !important;
    }

    [data-testid="stExpandSidebarButton"]:hover,
    [data-testid="stSidebarCollapseButton"]:hover {
        background-color: #FDE047 !important;
        transform: translate(-1px, -1px) !important;
        box-shadow: 4px 4px 0px #18181B !important;
    }

    [data-testid="stExpandSidebarButton"]:active,
    [data-testid="stSidebarCollapseButton"]:active {
        transform: translate(2px, 2px) !important;
        box-shadow: 1px 1px 0px #18181B !important;
    }

    [data-testid="stExpandSidebarButton"] span {
        font-size: 0 !important;
        line-height: 0 !important;
        display: inline-flex !important;
        align-items: center !important;
    }

    [data-testid="stExpandSidebarButton"] span::after {
        content: "✦ เมนู" !important;
        font-family: "Fredoka", "Mali", sans-serif !important;
        font-size: 13px !important;
        font-weight: 700 !important;
        color: #18181B !important;
        line-height: 1 !important;
    }

    [data-testid="stSidebarCollapseButton"] span {
        font-size: 0 !important;
        line-height: 0 !important;
        display: inline-flex !important;
        align-items: center !important;
    }

    [data-testid="stSidebarCollapseButton"] span::after {
        content: "◀ ย่อเมนู" !important;
        font-family: "Fredoka", "Mali", sans-serif !important;
        font-size: 13px !important;
        font-weight: 700 !important;
        color: #18181B !important;
        line-height: 1 !important;
    }

    /* Cute Expander Toggle Button */
    [data-testid="stExpanderToggleIcon"] {
        background-color: #BAE6FD !important;
        border: 1.5px solid #18181B !important;
        border-radius: 6px !important;
        box-shadow: 1.5px 1.5px 0px #18181B !important;
        padding: 3px 6px !important;
        display: inline-flex !important;
        align-items: center !important;
        justify-content: center !important;
    }

    [data-testid="stExpanderToggleIcon"] span {
        font-size: 0 !important;
        line-height: 0 !important;
    }

    [data-testid="stExpanderToggleIcon"] span::after {
        content: "▼" !important;
        font-size: 11px !important;
        font-weight: 900 !important;
        color: #18181B !important;
        line-height: 1 !important;
    }

    /* KaTeX Math Typography & Spacing (เว้นช่องไฟหน้าและหลังสมการที่ต่อจากภาษาไทย) */
    .katex {
        margin-left: 0.35em !important;
        margin-right: 0.35em !important;
        padding-left: 0.05em !important;
        padding-right: 0.05em !important;
        line-height: inherit !important;
    }

    .katex, .katex-display, .katex * {
        color: #18181B !important;
        font-weight: 600 !important;
    }

    /* Reset margins for display math blocks so they stay centered */
    .katex-display {
        margin-top: 0.85em !important;
        margin-bottom: 0.85em !important;
        overflow-x: auto !important;
        overflow-y: hidden !important;
    }

    .katex-display > .katex {
        margin-left: 0 !important;
        margin-right: 0 !important;
        padding-left: 0 !important;
        padding-right: 0 !important;
    }

    /* Main Container Padding */
    .block-container {
        padding-top: 2.5rem !important;
        padding-bottom: 3rem !important;
        max-width: 1060px !important;
    }

    /* Bauhaus Geometric Cards & Containers */
    [data-testid="stVerticalBlockBorderWrapper"] {
        background-color: #FFFFFF !important;
        border: 2.5px solid #18181B !important;
        border-radius: 14px !important;
        box-shadow: 4px 4px 0px #18181B !important;
        padding: 1.25rem !important;
    }

    /* Expanders with Bauhaus Shadow */
    [data-testid="stExpander"] {
        background-color: #FFFFFF !important;
        border: 2.5px solid #18181B !important;
        border-radius: 12px !important;
        box-shadow: 3px 3px 0px #18181B !important;
        margin-bottom: 0.75rem !important;
    }

    [data-testid="stExpander"] summary {
        font-family: "Fredoka", "Mali", sans-serif !important;
        font-weight: 600 !important;
        color: #18181B !important;
    }

    /* Primary Buttons (Coral-Rose Bauhaus Pop with Mechanical Press) */
    .stButton > button[kind="primary"],
    .stButton > button[data-testid="baseButton-primary"] {
        background-color: #FB7185 !important;
        color: #18181B !important;
        border-radius: 12px !important;
        border: 2.5px solid #18181B !important;
        font-family: "Fredoka", "Mali", sans-serif !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
        box-shadow: 3px 3px 0px #18181B !important;
        transition: all 0.12s ease-out !important;
    }

    .stButton > button[kind="primary"] *,
    .stButton > button[data-testid="baseButton-primary"] * {
        color: #18181B !important;
    }

    .stButton > button[kind="primary"]:hover,
    .stButton > button[data-testid="baseButton-primary"]:hover {
        background-color: #F43F5E !important;
        transform: translate(-1px, -1px) !important;
        box-shadow: 4px 4px 0px #18181B !important;
    }

    .stButton > button[kind="primary"]:active,
    .stButton > button[data-testid="baseButton-primary"]:active {
        transform: translate(2px, 2px) !important;
        box-shadow: 1px 1px 0px #18181B !important;
    }

    /* Secondary / Preset Buttons (White with Yellow Pop on Hover) */
    .stButton > button[kind="secondary"],
    .stButton > button[data-testid="baseButton-secondary"] {
        background-color: #FFFFFF !important;
        color: #18181B !important;
        border-radius: 12px !important;
        border: 2px solid #18181B !important;
        font-family: "Fredoka", "Mali", sans-serif !important;
        font-weight: 600 !important;
        box-shadow: 3px 3px 0px #18181B !important;
        transition: all 0.12s ease-out !important;
    }

    .stButton > button[kind="secondary"] *,
    .stButton > button[data-testid="baseButton-secondary"] * {
        color: #18181B !important;
    }

    .stButton > button[kind="secondary"]:hover,
    .stButton > button[data-testid="baseButton-secondary"]:hover {
        background-color: #FEF08A !important;
        transform: translate(-1px, -1px) !important;
        box-shadow: 4px 4px 0px #18181B !important;
        color: #18181B !important;
    }

    .stButton > button[kind="secondary"]:active,
    .stButton > button[data-testid="baseButton-secondary"]:active {
        transform: translate(2px, 2px) !important;
        box-shadow: 1px 1px 0px #18181B !important;
    }

    /* Inputs, Number Inputs, Sliders */
    input, textarea, select {
        color: #18181B !important;
        background-color: #FFFFFF !important;
        border: 2.5px solid #18181B !important;
        border-radius: 10px !important;
        box-shadow: 2px 2px 0px #18181B !important;
        font-family: "Mali", "Outfit", sans-serif !important;
        font-weight: 500 !important;
    }

    input:focus, textarea:focus, select:focus {
        border-color: #F43F5E !important;
        box-shadow: 3px 3px 0px #18181B !important;
        outline: none !important;
    }

    /* Metrics with Bauhaus Badge Look */
    [data-testid="stMetric"] {
        background-color: #FFFFFF !important;
        border: 2.5px solid #18181B !important;
        border-radius: 12px !important;
        box-shadow: 3px 3px 0px #18181B !important;
        padding: 12px 16px !important;
    }

    [data-testid="stMetricLabel"] p {
        font-family: "Fredoka", "Mali", sans-serif !important;
        font-weight: 600 !important;
        color: #4B5563 !important;
    }

    [data-testid="stMetricValue"] {
        font-family: "Outfit", "Fredoka", sans-serif !important;
        font-weight: 800 !important;
        color: #18181B !important;
    }

    /* Bauhaus Sidebar (Warm Peach/Pink Canvas) */
    [data-testid="stSidebar"] {
        background-color: #FFE4E6 !important;
        border-right: 3px solid #18181B !important;
    }

    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        font-family: "Fredoka", "Mali", sans-serif !important;
        color: #18181B !important;
    }

    [data-testid="stSidebar"] [data-testid="stSidebarNavItems"] a,
    [data-testid="stSidebar"] [data-testid="stSidebarNavItems"] button {
        border-radius: 10px !important;
        margin: 3px 0 !important;
        border: 1.5px solid transparent !important;
        font-family: "Mali", sans-serif !important;
        font-weight: 600 !important;
        color: #18181B !important;
        transition: all 0.12s ease !important;
    }

    [data-testid="stSidebarNavItems"] a:hover,
    [data-testid="stSidebarNavItems"] button:hover {
        background-color: #FED7AA !important;
        border: 1.5px solid #18181B !important;
        box-shadow: 2px 2px 0px #18181B !important;
    }

    [data-testid="stSidebarNavItems"] a[aria-current="page"],
    [data-testid="stSidebarNavItems"] button[aria-current="page"] {
        background-color: #FEF08A !important;
        color: #18181B !important;
        font-weight: 700 !important;
        border: 2px solid #18181B !important;
        box-shadow: 3px 3px 0px #18181B !important;
    }

    /* Bauhaus Color-Blocked Alerts */
    [data-testid="stAlert"] {
        border: 2.5px solid #18181B !important;
        border-radius: 12px !important;
        box-shadow: 3px 3px 0px #18181B !important;
        font-family: "Mali", sans-serif !important;
        font-weight: 500 !important;
        color: #18181B !important;
    }

    /* Radio buttons & Checkboxes */
    [data-testid="stRadio"] label,
    [data-testid="stCheckbox"] label {
        font-family: "Mali", sans-serif !important;
        font-weight: 600 !important;
        color: #18181B !important;
    }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)


def render_hero(title: str, subtitle: str) -> None:
    html = f"""
    <div style="
        background-color: #FFFFFF;
        border: 3px solid #18181B;
        border-radius: 16px;
        padding: 20px 24px;
        margin-bottom: 24px;
        box-shadow: 5px 5px 0px #18181B;
        position: relative;
    ">
        <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 12px;">
            <span style="display: inline-block; width: 13px; height: 13px; border-radius: 50%; background-color: #F43F5E; border: 1.5px solid #18181B;"></span>
            <span style="display: inline-block; width: 13px; height: 13px; background-color: #FBBF24; border: 1.5px solid #18181B;"></span>
            <span style="display: inline-block; width: 0; height: 0; border-left: 7px solid transparent; border-right: 7px solid transparent; border-bottom: 13px solid #38BDF8;"></span>
        </div>
        <h1 style="
            font-family: 'Fredoka', 'Mali', sans-serif;
            font-size: 26px;
            font-weight: 700;
            color: #18181B;
            margin: 0 0 6px 0;
            padding: 0;
            border: none;
            line-height: 1.25;
        ">{title}</h1>
        <p style="
            font-family: 'Mali', sans-serif;
            font-size: 15px;
            color: #4B5563;
            margin: 0;
            padding: 0;
            font-weight: 500;
        ">{subtitle}</p>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)
