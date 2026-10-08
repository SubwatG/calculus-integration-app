"""pages/lessons.py — บทเรียน

แสดงเนื้อหาบทเรียนโดยรวมจาก utils/theory.py (THEORY_CONTENT)
ของแต่ละหัวข้อ interactive พร้อมปุ่มไปยังหน้า interactive ที่เกี่ยวข้อง

tab "เอกสารอ้างอิง" ยังเปิดเนื้อหา markdown ฉบับเต็มจาก data/lessons/ ได้
แต่ไม่ใช่การแสดงหลักอีกต่อไป
"""

import streamlit as st

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
# Tab 2: เอกสารอ้างอิงและตำราเรียน (ภาควิชาคณิตศาสตร์ มหาวิทยาลัยศิลปากร)
# ---------------------------------------------------------------------------
with tab_reference:
    st.markdown(
        """
        <div style="
            background-color: #FFFFFF;
            border: 2.5px solid #18181B;
            border-radius: 12px;
            padding: 18px 22px;
            margin-bottom: 20px;
            box-shadow: 3px 3px 0px #18181B;
        ">
            <h3 style="margin: 0 0 8px 0; font-family: 'Fredoka', 'Mali', sans-serif; font-size: 1.15rem; color: #18181B;">
                📚 แหล่งเรียนรู้อ้างอิงทางการ (Open Academic Resources)
            </h3>
            <p style="margin: 0; font-size: 0.95rem; color: #4B5563; line-height: 1.65;">
                เอกสารประกอบการเรียนรู้และชุดฝึกหัดฉบับเต็ม เผยแพร่เพื่อประโยชน์ทางการศึกษาโดย 
                <strong>ภาควิชาคณิตศาสตร์ คณะวิทยาศาสตร์ มหาวิทยาลัยศิลปากร</strong> 
                สามารถเข้าถึงคลังหนังสือและดาวน์โหลดเอกสารตำราฉบับสมบูรณ์ (PDF) ได้โดยตรง
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.link_button(
        "🌐 ไปยังคลังหนังสือ ภาควิชาคณิตศาสตร์ ม.ศิลปากร (math.sc.su.ac.th)",
        "https://math.sc.su.ac.th/หนังสือ/",
        type="primary",
        use_container_width=True,
    )

    st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)

    col_cal1, col_cal2 = st.columns(2)

    with col_cal1:
        st.markdown("### 📘 ไฟล์หนังสือเรียน แคลคูลัส I")
        cal1_links = [
            ("บทที่ 1 ลิมิตและความต่อเนื่อง", "https://math.sc.su.ac.th/wp-content/uploads/2025/10/cal1_ch1.pdf"),
            ("บทที่ 2 อนุพันธ์", "https://math.sc.su.ac.th/wp-content/uploads/2025/10/cal1_ch2.pdf"),
            ("บทที่ 3 การประยุกต์ของอนุพันธ์", "https://math.sc.su.ac.th/wp-content/uploads/2025/10/cal1_ch3.pdf"),
            ("บทที่ 4 กฎของโลปิตาล", "https://math.sc.su.ac.th/wp-content/uploads/2025/10/cal1_ch4.pdf"),
            ("บทที่ 5 ลำดับ อนุกรมและอนุกรมกำลัง", "https://math.sc.su.ac.th/wp-content/uploads/2025/10/cal1_ch5.pdf"),
            ("เฉลยแบบฝึกหัด แคลคูลัส I", "https://math.sc.su.ac.th/wp-content/uploads/2025/10/cal1_solutions.pdf"),
        ]
        for title, url in cal1_links:
            st.markdown(f"- [{title}]({url})")

    with col_cal2:
        st.markdown("### 📙 ไฟล์หนังสือเรียน แคลคูลัส II")
        cal2_links = [
            ("บทที่ 1 อินทิกรัล", "https://math.sc.su.ac.th/wp-content/uploads/2025/10/Calculus2-ch1-integrals.pdf"),
            ("บทที่ 2 เทคนิคการอินทิเกรต", "https://math.sc.su.ac.th/wp-content/uploads/2025/10/Calculus2-ch2-integration-techniques.pdf"),
            ("บทที่ 3 การประยุกต์ของอินทิกรัล", "https://math.sc.su.ac.th/wp-content/uploads/2025/10/Calculus2-ch3-applications-of-integrals.pdf"),
            ("บทที่ 4 อินทิกรัลไม่ตรงแบบ", "https://math.sc.su.ac.th/wp-content/uploads/2025/10/Calculus2-ch4-improper-integrals.pdf"),
            ("บทที่ 5 พื้นผิวในปริภูมิสามมิติ", "https://math.sc.su.ac.th/wp-content/uploads/2025/10/Calculus2-ch5-3d-surfaces.pdf"),
            ("บทที่ 6 ฟังก์ชันหลายตัวแปร", "https://math.sc.su.ac.th/wp-content/uploads/2025/10/Calculus2-ch6-multivariable-functions.pdf"),
            ("บทที่ 7 สมการอิงตัวแปรเสริมและพิกัดเชิงขั้ว", "https://math.sc.su.ac.th/wp-content/uploads/2025/10/Calculus2-ch7-parametric-equations.pdf"),
            ("บทที่ 8 สมการเชิงอนุพันธ์", "https://math.sc.su.ac.th/wp-content/uploads/2025/10/Calculus2-ch8-differential-equations.pdf"),
            ("เฉลยแบบฝึกหัด แคลคูลัส II", "https://math.sc.su.ac.th/wp-content/uploads/2025/10/Calculus2-solutions.pdf"),
        ]
        for title, url in cal2_links:
            st.markdown(f"- [{title}]({url})")

    with st.expander("📝 ชุดฝึกหัดเสริมเพิ่มเติม (คณิตศาสตร์ ม.ศิลปากร)"):
        exercise_links = [
            ("1-1 การพิสูจน์ลิมิตเป็นจริง", "https://math.sc.su.ac.th/wp-content/uploads/2025/10/1-1-.pdf"),
            ("1-2 การคำนวณค่าลิมิตทั่วไป", "https://math.sc.su.ac.th/wp-content/uploads/2025/10/1-2-.pdf"),
            ("1-3 ความต่อเนื่องของฟังก์ชัน", "https://math.sc.su.ac.th/wp-content/uploads/2025/10/1-3-.pdf"),
            ("2-1 การหาอนุพันธ์โดยนิยามและสูตรทั่วไป", "https://math.sc.su.ac.th/wp-content/uploads/2025/10/2-1-.pdf"),
            ("2-2 การหาอนุพันธ์โดยกฎลูกโซ่", "https://math.sc.su.ac.th/wp-content/uploads/2025/10/2-2-.pdf"),
            ("2-3 อนุพันธ์ของฟังก์ชันเชิงกำลังและฟังก์ชันลอการิทึม", "https://math.sc.su.ac.th/wp-content/uploads/2025/10/2-3-.pdf"),
            ("2-4 อนุพันธ์ของฟังก์ชันตรีโกณมิติและตรีโกณมิติผกผัน", "https://math.sc.su.ac.th/wp-content/uploads/2025/10/2-4-.pdf"),
            ("2-5 อนุพันธ์ของฟังก์ชันไฮเปอร์โบลิกและฟังก์ชันไฮเปอร์โบลิกผกผัน", "https://math.sc.su.ac.th/wp-content/uploads/2025/10/2-5-.pdf"),
            ("3 การหาค่าลิมิตรูปอินดิเทอร์มิเนต", "https://math.sc.su.ac.th/wp-content/uploads/2025/10/3.pdf"),
            ("4 เทคนิคการอินทิเกรต", "https://math.sc.su.ac.th/wp-content/uploads/2025/10/4.pdf"),
        ]
        for title, url in exercise_links:
            st.markdown(f"- [{title}]({url})")
