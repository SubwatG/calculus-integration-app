"""pages/lessons.py — บทเรียน

แสดงเนื้อหาบทเรียนโดยรวมจาก utils/theory.py (THEORY_CONTENT)
ของแต่ละหัวข้อ interactive พร้อมปุ่มไปยังหน้า interactive ที่เกี่ยวข้อง

tab "เอกสารอ้างอิง" ยังเปิดเนื้อหา markdown ฉบับเต็มจาก data/lessons/ ได้
แต่ไม่ใช่การแสดงหลักอีกต่อไป
"""

import re

import streamlit as st

from utils.content_loader import list_lessons, load_lesson
from utils.math_render import format_math_spacing
from utils.theme import render_hero
from utils.theory import THEORY_CONTENT

render_hero("บทเรียน", "เนื้อหาบทเรียนเรียงตามหัวข้อ")

# ---------------------------------------------------------------------------
# Mapping: key ใน THEORY_CONTENT -> หน้า interactive ที่เกี่ยวข้อง
# ---------------------------------------------------------------------------
INTERACTIVE_PAGES = {
    "riemann_sum": "pages/riemann.py",
    "tangent": "pages/tangent.py",
    "limit": "pages/limit_approach.py",
    "substitution": "pages/substitution.py",
    "volume": "pages/volume_revolution.py",
    "area_between": "pages/area_between.py",
    "improper": "pages/improper_integrals.py",
}

# key ที่ยังไม่มีหน้า interactive (เผื่อเพิ่มในอนาคต)
ALL_THEORY_KEYS = list(THEORY_CONTENT.keys())

tab_interactive, tab_reference = st.tabs(
    ["บทเรียน interactive", "เอกสารอ้างอิง (ฉบับเต็ม)"]
)

# ---------------------------------------------------------------------------
# Tab 1: บทเรียน interactive (จาก theory.py)
# ---------------------------------------------------------------------------
with tab_interactive:
    interactive_keys = [k for k in ALL_THEORY_KEYS if k in INTERACTIVE_PAGES]
    if not interactive_keys:
        st.warning("ยังไม่มีบทเรียน interactive")
    else:
        lesson_titles = {
            k: THEORY_CONTENT[k]["title"]
            for k in interactive_keys
        }
        selected_key = st.selectbox(
            "เลือกบทเรียน",
            interactive_keys,
            format_func=lambda k: lesson_titles[k],
            key="selectbox_interactive_lesson",
        )

        theory = THEORY_CONTENT[selected_key]

        st.markdown(f"## {format_math_spacing(theory['title'])}")

        st.markdown("**เงื่อนไขการใช้งาน**")
        for item in theory["conditions"]:
            st.markdown(f"- {format_math_spacing(item)}")

        st.markdown("**สูตรที่ใช้**")
        for item in theory["formulas"]:
            st.markdown(f"- {format_math_spacing(item)}")

        st.markdown("**สมบัติ**")
        for item in theory["properties"]:
            st.markdown(f"- {format_math_spacing(item)}")

        st.markdown("**ข้อควรระวัง**")
        st.warning(" / ".join(format_math_spacing(c) for c in theory["cautions"]))

        st.markdown("**การประยุกต์ใช้**")
        for item in theory["applications"]:
            st.markdown(f"- {format_math_spacing(item)}")

        st.markdown("**คำแนะนำการเลือกใช้**")
        st.markdown(format_math_spacing(theory["decision_guide"]))

        st.divider()
        target = INTERACTIVE_PAGES[selected_key]
        if st.button("ไปลองเล่นแบบ interactive", type="primary", key="btn_go_interactive"):
            st.switch_page(target)

# ---------------------------------------------------------------------------
# Tab 2: เอกสารอ้างอิง (markdown ฉบับเต็มจาก data/lessons/)
# ---------------------------------------------------------------------------
with tab_reference:
    st.caption("เนื้อหาอ้างอิงฉบับเต็มจาก data/lessons/ (เอกสารต้นทาง ไม่ใช่บทเรียนหลัก)")

    lessons = list_lessons()
    if not lessons:
        st.warning("ไม่พบเอกสารอ้างอิงใน data/lessons/")
    else:
        ref_titles = {item["title"]: item["filename"] for item in lessons}
        
        col_ref1, col_ref2 = st.columns([3, 2])
        with col_ref1:
            ref_title = st.selectbox(
                "เลือกเอกสารอ้างอิง",
                list(ref_titles.keys()),
                key="selectbox_reference_doc",
            )
        with col_ref2:
            font_size_label = st.radio(
                "ขนาดตัวอักษรเอกสาร",
                ["กะทัดรัด (15px)", "ปกติ (17px)", "ใหญ่สบายตา (19px)"],
                index=1,
                horizontal=True,
                key="ref_font_size_choice",
            )

        size_map = {
            "กะทัดรัด (15px)": "15px",
            "ปกติ (17px)": "17px",
            "ใหญ่สบายตา (19px)": "19px",
        }
        chosen_size = size_map.get(font_size_label, "17px")

        raw_content = load_lesson(ref_titles[ref_title])
        # ตัด YAML frontmatter ออกเพื่อไม่ให้แสดง metadata บั๊คด้านบน
        clean_content = re.sub(r"^---\s*\n.*?\n---\s*\n", "", raw_content, flags=re.DOTALL)

        # สไตล์ปรับขนาดตัวอักษรให้อ่านสบายตา และปรับหัวข้อให้ได้สัดส่วนพอดี
        st.markdown(
            f"""
            <style>
            [data-testid="stExpanderDetails"] {{
                font-size: {chosen_size} !important;
            }}
            [data-testid="stExpanderDetails"] p,
            [data-testid="stExpanderDetails"] li,
            [data-testid="stExpanderDetails"] span:not(.katex):not(.katex *) {{
                font-size: {chosen_size} !important;
                line-height: 1.85 !important;
            }}
            [data-testid="stExpanderDetails"] h1 {{
                font-size: 1.55em !important;
                margin-top: 1rem !important;
                margin-bottom: 0.6rem !important;
            }}
            [data-testid="stExpanderDetails"] h2 {{
                font-size: 1.3em !important;
                margin-top: 0.85rem !important;
                margin-bottom: 0.5rem !important;
            }}
            [data-testid="stExpanderDetails"] h3 {{
                font-size: 1.15em !important;
                margin-top: 0.75rem !important;
                margin-bottom: 0.4rem !important;
            }}
            [data-testid="stExpanderDetails"] .katex {{
                font-size: 1.05em !important;
            }}
            [data-testid="stExpanderDetails"] blockquote {{
                background: #FDF2F8 !important;
                border-left: 4px solid #FB7185 !important;
                border-radius: 6px !important;
                padding: 0.6rem 1rem !important;
                margin: 0.75rem 0 !important;
                font-size: 0.9em !important;
                color: #4B5563 !important;
            }}
            </style>
            """,
            unsafe_allow_html=True,
        )

        with st.expander("แสดงเนื้อหาฉบับเต็ม", expanded=True):
            st.markdown(clean_content)
