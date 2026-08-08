"""pages/lessons.py — บทเรียน

แสดงเนื้อหาบทเรียนโดยรวมจาก utils/theory.py (THEORY_CONTENT)
ของแต่ละหัวข้อ interactive พร้อมปุ่มไปยังหน้า interactive ที่เกี่ยวข้อง

tab "เอกสารอ้างอิง" ยังเปิดเนื้อหา markdown ฉบับเต็มจาก data/lessons/ ได้
แต่ไม่ใช่การแสดงหลักอีกต่อไป
"""

import streamlit as st

from utils.content_loader import list_lessons, load_lesson
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

        st.markdown(f"## {theory['title']}")

        st.markdown("**เงื่อนไขการใช้งาน**")
        for item in theory["conditions"]:
            st.markdown(f"- {item}")

        st.markdown("**สูตรที่ใช้**")
        for item in theory["formulas"]:
            st.markdown(f"- {item}")

        st.markdown("**สมบัติ**")
        for item in theory["properties"]:
            st.markdown(f"- {item}")

        st.markdown("**ข้อควรระวัง**")
        st.warning(" / ".join(theory["cautions"]))

        st.markdown("**การประยุกต์ใช้**")
        for item in theory["applications"]:
            st.markdown(f"- {item}")

        st.markdown("**คำแนะนำการเลือกใช้**")
        st.markdown(theory["decision_guide"])

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
        ref_title = st.selectbox(
            "เลือกเอกสารอ้างอิง",
            list(ref_titles.keys()),
            key="selectbox_reference_doc",
        )
        content = load_lesson(ref_titles[ref_title])
        with st.expander("แสดงเนื้อหาฉบับเต็ม", expanded=True):
            st.markdown(content)
