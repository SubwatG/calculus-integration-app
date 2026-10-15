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
        visibility: visible !important;
        opacity: 1 !important;
    }

    [data-testid="stSidebarCollapseButton"] button {
        visibility: visible !important;
        opacity: 1 !important;
    }

    /* Hide inner Material icons so they don't leak text or trigger duplicate ::after */
    [data-testid="stExpandSidebarButton"] [data-testid="stIconMaterial"],
    [data-testid="stSidebarCollapseButton"] [data-testid="stIconMaterial"] {
        display: none !important;
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

    [data-testid="stExpandSidebarButton"] > span,
    [data-testid="stSidebarCollapseButton"] button > span {
        font-size: 0 !important;
        line-height: 0 !important;
        display: inline-flex !important;
        align-items: center !important;
    }

    [data-testid="stExpandSidebarButton"] > span::after {
        content: "✦ เมนู" !important;
        font-family: "Fredoka", "Mali", sans-serif !important;
        font-size: 13px !important;
        font-weight: 700 !important;
        color: #18181B !important;
        line-height: 1 !important;
        white-space: nowrap !important;
    }

    [data-testid="stSidebarCollapseButton"] button > span::after {
        content: "◀ ย่อเมนู" !important;
        font-family: "Fredoka", "Mali", sans-serif !important;
        font-size: 13px !important;
        font-weight: 700 !important;
        color: #18181B !important;
        line-height: 1 !important;
        white-space: nowrap !important;
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

    /* KaTeX Math Typography & Headroom Protection (แก้ปัญหาสมการหัวขาดและขอบเขตบนไม่ชัดเจน) */
    .katex {
        margin-left: 0.25em !important;
        margin-right: 0.25em !important;
        padding-left: 0.05em !important;
        padding-right: 0.05em !important;
        line-height: normal !important;
        text-rendering: auto !important;
    }

    .katex, .katex-display {
        color: #18181B !important;
    }

    .katex .katex-html {
        color: #18181B !important;
        overflow: visible !important;
    }

    /* Streamlit LaTeX Block Container: ensure vertical overflow is never clipped */
    [data-testid="stLatex"],
    .stLatex {
        width: 100% !important;
        overflow-x: auto !important;
        overflow-y: visible !important;
        padding-top: 0.75rem !important;
        padding-bottom: 0.5rem !important;
    }

    /* Display Math Blocks: Generous headroom so upper limits (\\int_a^b), superscripts, and fractions are never cut off */
    .katex-display {
        margin-top: 1rem !important;
        margin-bottom: 1rem !important;
        padding-top: 1.25rem !important;
        padding-bottom: 0.75rem !important;
        padding-left: 0.5rem !important;
        padding-right: 0.5rem !important;
        overflow-x: auto !important;
        overflow-y: visible !important;
    }

    .katex-display > .katex {
        display: block !important;
        text-align: center !important;
        margin-left: 0 !important;
        margin-right: 0 !important;
        padding-top: 0.25rem !important;
        padding-bottom: 0.15rem !important;
        padding-left: 0 !important;
        padding-right: 0 !important;
        line-height: normal !important;
        overflow: visible !important;
    }

    /* Ensure KaTeX vertical layout components (limits, fractions, roots) have full headroom */
    .katex .vlist-t,
    .katex .vlist-r,
    .katex .vlist,
    .katex .msupsub,
    .katex .mop {
        overflow: visible !important;
    }

    /* Buttons containing math & text: ensure text wrapping and vertical clearance so labels never clip */
    .stButton button,
    [data-testid="stButton"] button,
    button[data-testid^="baseButton"] {
        min-height: 2.6rem !important;
        height: auto !important;
        padding: 0.4rem 0.5rem !important;
        display: inline-flex !important;
        align-items: center !important;
        justify-content: center !important;
        font-weight: 700 !important;
        white-space: normal !important;
        text-wrap: wrap !important;
        word-break: break-word !important;
        overflow-wrap: anywhere !important;
    }

    .stButton button .katex,
    [data-testid="stButton"] button .katex,
    button[data-testid^="baseButton"] .katex {
        line-height: normal !important;
        overflow: visible !important;
        vertical-align: middle !important;
        white-space: nowrap !important;
    }

    .stButton button div[data-testid="stMarkdownContainer"],
    [data-testid="stButton"] [data-testid="stMarkdownContainer"],
    button[data-testid^="baseButton"] [data-testid="stMarkdownContainer"] {
        text-align: center !important;
        white-space: normal !important;
        text-wrap: wrap !important;
        word-break: break-word !important;
        overflow-wrap: anywhere !important;
    }

    .stButton button div[data-testid="stMarkdownContainer"] p,
    .stButton button p,
    [data-testid="stButton"] [data-testid="stMarkdownContainer"] p,
    button[data-testid^="baseButton"] p {
        white-space: normal !important;
        text-wrap: wrap !important;
        word-break: break-word !important;
        overflow-wrap: anywhere !important;
        text-align: center !important;
        overflow: visible !important;
        line-height: 1.35 !important;
        margin: 0 !important;
        font-weight: 700 !important;
        font-size: 0.92rem !important;
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
        margin-bottom: 1.25rem !important;
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

    /* ==========================================================================
       Mobile Responsive Optimizations: Math Keypad, Quick Chips & Presets
       Prevents buttons from stretching to 100% full-screen width on mobile viewports
       ========================================================================== */

    /* 1. Math Keypad inside Expander:
          - Horizontal flex row
          - On mobile (<=768px): keys are fixed 48px wide and smoothly scrollable to the right!
          - On desktop (>768px): keys expand evenly to fill the expander
    */
    div[data-testid="stExpanderDetails"] div[data-testid="stHorizontalBlock"] {
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important;
        gap: 6px !important;
        width: 100% !important;
        margin-bottom: 6px !important;
        overflow-x: auto !important;
        -webkit-overflow-scrolling: touch !important;
        padding-bottom: 6px !important;
        touch-action: pan-x !important;
    }

    /* Desktop (>768px): Keypad expands evenly */
    @media (min-width: 769px) {
        div[data-testid="stExpanderDetails"] div[data-testid="stHorizontalBlock"] > div[data-testid="stColumn"] {
            flex: 1 1 0px !important;
            min-width: 0 !important;
            width: auto !important;
        }
    }

    /* Mobile (<=768px): Keypad rows 1 & 2 (8+ keys) scroll horizontally to the right */
    @media (max-width: 768px) {
        div[data-testid="stExpanderDetails"] div[data-testid="stHorizontalBlock"]:has(> div:nth-child(8)) > div[data-testid="stColumn"] {
            flex: 0 0 48px !important;
            min-width: 48px !important;
            max-width: 48px !important;
            width: 48px !important;
        }

        /* Keypad row 3 (4 keys: 1/x, |x|, ลบ, ล้าง) fills the width evenly */
        div[data-testid="stExpanderDetails"] div[data-testid="stHorizontalBlock"]:not(:has(> div:nth-child(8))) > div[data-testid="stColumn"] {
            flex: 1 1 calc(25% - 6px) !important;
            min-width: 54px !important;
        }
    }

    /* Keypad Scrollbar: clean, sleek and visible on touch devices */
    div[data-testid="stExpanderDetails"] div[data-testid="stHorizontalBlock"]::-webkit-scrollbar {
        height: 5px !important;
        display: block !important;
    }
    div[data-testid="stExpanderDetails"] div[data-testid="stHorizontalBlock"]::-webkit-scrollbar-track {
        background: #FBCFE8 !important;
        border-radius: 999px !important;
    }
    div[data-testid="stExpanderDetails"] div[data-testid="stHorizontalBlock"]::-webkit-scrollbar-thumb {
        background: #F43F5E !important;
        border-radius: 999px !important;
    }

    div[data-testid="stExpanderDetails"] div[data-testid="stHorizontalBlock"] .stButton button,
    div[data-testid="stExpanderDetails"] div[data-testid="stHorizontalBlock"] [data-testid="stButton"] button {
        min-height: 2.3rem !important;
        height: 2.3rem !important;
        padding: 0 4px !important;
        font-size: 0.9rem !important;
        font-weight: 700 !important;
        width: 100% !important;
        white-space: nowrap !important;
        text-align: center !important;
        border-radius: 8px !important;
        border: 1.5px solid #18181B !important;
        box-shadow: 1.5px 1.5px 0px #18181B !important;
    }

    div[data-testid="stExpanderDetails"] div[data-testid="stHorizontalBlock"] .stButton button p,
    div[data-testid="stExpanderDetails"] div[data-testid="stHorizontalBlock"] [data-testid="stButton"] button p {
        font-size: 0.9rem !important;
        line-height: 1 !important;
        white-space: nowrap !important;
    }

    /* 2. Quick Chips (จุดยอดนิยม / Nested Columns inside col_a):
          Always 4 compact columns (25% width each) on all screen sizes, never 100% full-screen!
    */
    div[data-testid="stColumn"] div[data-testid="stHorizontalBlock"] {
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important;
        gap: 4px !important;
        width: 100% !important;
        margin-bottom: 4px !important;
    }

    div[data-testid="stColumn"] div[data-testid="stHorizontalBlock"] > div[data-testid="stColumn"] {
        min-width: calc(25% - 4px) !important;
        max-width: calc(25% - 4px) !important;
        flex: 1 1 calc(25% - 4px) !important;
        width: calc(25% - 4px) !important;
    }

    div[data-testid="stColumn"] div[data-testid="stHorizontalBlock"] .stButton button,
    div[data-testid="stColumn"] div[data-testid="stHorizontalBlock"] [data-testid="stButton"] button {
        min-height: 2.1rem !important;
        height: 2.1rem !important;
        padding: 0 2px !important;
        font-size: 0.88rem !important;
        font-weight: 700 !important;
        width: 100% !important;
        white-space: nowrap !important;
        border-radius: 8px !important;
        border: 1.5px solid #18181B !important;
        box-shadow: 1.5px 1.5px 0px #18181B !important;
    }

    /* 3. Preset Example Buttons (ตัวอย่างโจทย์ยอดนิยม): 2-Column Responsive Grid on Mobile */
    @media (max-width: 768px) {
        div[data-testid="stHorizontalBlock"]:has(> div:nth-child(4)):not(:has(> div:nth-child(8))) {
            display: flex !important;
            flex-direction: row !important;
            flex-wrap: wrap !important;
            gap: 6px !important;
            width: 100% !important;
        }

        div[data-testid="stHorizontalBlock"]:has(> div:nth-child(4)):not(:has(> div:nth-child(8))) > div[data-testid="stColumn"] {
            flex: 1 1 calc(50% - 6px) !important;
            min-width: calc(50% - 6px) !important;
            max-width: calc(50% - 6px) !important;
            width: calc(50% - 6px) !important;
        }

        div[data-testid="stHorizontalBlock"]:has(> div:nth-child(4)):not(:has(> div:nth-child(8))) .stButton button {
            min-height: 2.2rem !important;
            height: auto !important;
            padding: 4px 6px !important;
            font-size: 0.82rem !important;
            line-height: 1.25 !important;
            border-radius: 8px !important;
            border: 1.5px solid #18181B !important;
            box-shadow: 2px 2px 0px #18181B !important;
        }

        /* จุดยอดนิยม (nested columns inside col_a): MUST STAY exactly 4 columns per row without wrapping! */
        div[data-testid="stColumn"] div[data-testid="stHorizontalBlock"]:has(> div:nth-child(4)):not(:has(> div:nth-child(8))) > div[data-testid="stColumn"],
        div[data-testid="stColumn"] div[data-testid="stHorizontalBlock"] > div[data-testid="stColumn"] {
            flex: 1 1 0px !important;
            min-width: 0 !important;
            max-width: none !important;
            width: auto !important;
        }

        div[data-testid="stColumn"] div[data-testid="stHorizontalBlock"] {
            display: flex !important;
            flex-direction: row !important;
            flex-wrap: nowrap !important;
            gap: 4px !important;
            width: 100% !important;
            margin-bottom: 4px !important;
        }
    }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)


def render_hero(title: str, subtitle: str) -> None:
    inject_css()
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
