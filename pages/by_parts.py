"""pages/by_parts.py : การอินทิเกรตทีละส่วน (Integration by Parts)

ออกแบบเพื่อสร้างแนวคิดการตัดสินใจเลือก u และ dv ตามกฎ LIATE
ครอบคลุมทั้งรูปแบบพหุนามคูณเอกซ์โพเนนเชียล ลอการิทึม การทำซ้ำหลายชั้น และการวนลูป
"""

import streamlit as st
import sympy as sp

from utils.by_parts_solver import solve_by_parts
from utils.keypad import render_math_keypad
from utils.math_render import format_inverse_trig, preview_math_expr, render_latex, render_steps, render_syntax_guide
from utils.special_functions import describe_special_functions, special_functions_in
from utils.theme import render_hero

render_hero(
    "การอินทิเกรตทีละส่วน (Integration by Parts)",
    "หลักการเลือก u และ dv ตามกฎ LIATE พร้อมเทคนิคการอินทิเกรตแบบวนลูป",
)
# Custom Tactile Bauhaus styling & responsive table protection (matching Quiz UX)
st.markdown(
    r"""
    <style>
    /* Radio options styled as tactile Bauhaus cards (matching Quiz UX) */
    div[data-testid="stRadio"] div[role="radiogroup"]:not([aria-orientation="horizontal"]) {
        display: flex !important;
        flex-direction: column !important;
        gap: 10px !important;
        margin-top: 8px !important;
        margin-bottom: 14px !important;
    }
    div[data-testid="stRadio"] div[role="radiogroup"]:not([aria-orientation="horizontal"]) > label {
        background-color: #FFFFFF !important;
        border: 2px solid #18181B !important;
        border-radius: 12px !important;
        box-shadow: 3px 3px 0px #18181B !important;
        padding: 12px 16px !important;
        margin: 0 !important;
        cursor: pointer !important;
        transition: all 0.12s ease-out !important;
        width: 100% !important;
        display: flex !important;
        align-items: center !important;
    }
    div[data-testid="stRadio"] div[role="radiogroup"]:not([aria-orientation="horizontal"]) > label:hover {
        background-color: #FEF08A !important;
        transform: translate(-1.5px, -1.5px) !important;
        box-shadow: 4px 4px 0px #18181B !important;
    }
    div[data-testid="stRadio"] div[role="radiogroup"]:not([aria-orientation="horizontal"]) > label:has(input:checked) {
        background-color: #FEF9C3 !important;
        border: 2px solid #18181B !important;
        box-shadow: 3.5px 3.5px 0px #18181B !important;
    }
    div[data-testid="stRadio"] div[role="radiogroup"]:not([aria-orientation="horizontal"]) > label p {
        font-family: "Mali", "Outfit", sans-serif !important;
        font-size: 1rem !important;
        font-weight: 600 !important;
        line-height: 1.4 !important;
        margin: 0 !important;
        color: #18181B !important;
    }

    /* Responsive Table Styling: Prevent horizontal squishing on mobile */
    div[data-testid="stMarkdownContainer"]:has(table) {
        overflow-x: auto !important;
        -webkit-overflow-scrolling: touch !important;
        padding-bottom: 6px !important;
    }
    div[data-testid="stMarkdownContainer"] table {
        width: 100% !important;
        min-width: 520px !important;
        border-collapse: separate !important;
        border-spacing: 0 !important;
        border: 2px solid #18181B !important;
        border-radius: 12px !important;
        box-shadow: 3px 3px 0px #18181B !important;
        background-color: #FFFFFF !important;
        margin: 10px 0 16px 0 !important;
    }
    div[data-testid="stMarkdownContainer"] table th {
        background-color: #FEF08A !important;
        color: #18181B !important;
        font-weight: 700 !important;
        border-bottom: 2px solid #18181B !important;
        padding: 10px 14px !important;
        text-align: left !important;
    }
    div[data-testid="stMarkdownContainer"] table td {
        padding: 10px 14px !important;
        border-bottom: 1px solid #E4E4E7 !important;
        color: #18181B !important;
        vertical-align: middle !important;
    }
    div[data-testid="stMarkdownContainer"] table tr:last-child td {
        border-bottom: none !important;
    }
    div[data-testid="stMarkdownContainer"] table tr:hover {
        background-color: #FEF9C3 !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# =============================================================================
# 1. สรุปหลักการทั่วไปในการเลือก u และ dv (กฎ LIATE)
# =============================================================================
st.markdown("### ทฤษฎีและหลักการสำคัญ")
with st.container(border=True):
    col_badge, col_title = st.columns([1, 4])
    with col_badge:
        st.markdown(
            r"""<span style="
                background-color: #FEF08A;
                border: 1.5px solid #18181B;
                border-radius: 8px;
                padding: 4px 10px;
                font-family: 'Fredoka', 'Mali', sans-serif;
                font-size: 13px;
                font-weight: 700;
                color: #18181B;
                display: inline-block;
            ">By Parts</span>""",
            unsafe_allow_html=True,
        )
    with col_title:
        st.markdown("#### สูตรและหลักการเลือกตัวแปร $u$ และ $dv$")

    st.latex(r"\int u \, dv = uv - \int v \, du")

    st.markdown(
        r"""
| ลำดับ LIATE | ประเภทฟังก์ชัน | บทบาทที่แนะนำ | เหตุผลทางคณิตศาสตร์ |
| :---: | :--- | :---: | :--- |
| L, I | ลอการิทึม / ตรีโกณผกผัน | เลือกเป็น $u$ เสมอ | อินทิเกรตตรงยาก แต่ดิฟแล้วกลายเป็นพีชคณิต |
| A | พหุนาม / พีชคณิต $x^n$ | เลือกเป็น $u$ เมื่อคูณกับ $T$ หรือ $E$ | ดิฟแล้วดีกรีลดลงเรื่อย ๆ จนกลายเป็นค่าคงที่ |
| T, E | ตรีโกณมิติ / เลขชี้กำลัง | มักเลือกเป็น $dv$ | อินทิเกรตง่ายและวนกลับมารูปเดิม |
        """
    )

with st.expander("อ่านหลักการตัดสินใจและเทคนิคการอินทิเกรตทีละส่วน", expanded=False):
    st.markdown(
        r"""
- **หลักการเลือก $u$:** ฟังก์ชันที่ **หาอนุพันธ์แล้วได้รูปที่ง่ายขึ้นหรือดีกรีลดลง**
- **หลักการเลือก $dv$:** ฟังก์ชันที่ **หาปริพันธ์กลับเป็น $v$ ได้ง่ายโดยรูปไม่ซับซ้อนขึ้น**
- **ลำดับความสำคัญตามกฎ LIATE (เลือกเป็น $u$ จากซ้ายไปขวา):** $L$ (Log), $I$ (Inv Trig), $A$ (Algebra), $T$ (Trig), $E$ (Exp)
- **เทคนิคการวนซ้ำ:** กรณีฟังก์ชันตรีโกณมิติกับเอกซ์โพเนนเชียล เช่น $\int e^x \sin x\,dx$ หรือ $\int 2^x \cos x\,dx$ หลังทำ By Parts สองรอบจะได้รูปเดิม ให้ย้ายข้างสมการทางพีชคณิตเพื่อหาคำตอบ
        """
    )

st.divider()

# =============================================================================
# 2. กรณีศึกษาฝึกตัดสินใจ (Active Scaffolding)
# =============================================================================
st.markdown("### กรณีศึกษาฝึกตัดสินใจเลือก $u$ และ $dv$ (LIATE Decision Challenge)")

case_parts = st.selectbox(
    "เลือกกรณีศึกษาที่ต้องการเรียนรู้:",
    options=[
        "กรณีที่ 1: พหุนามคูณกับเอกซ์โพเนนเชียล (x e^x)",
        "กรณีที่ 2: ฟังก์ชันเดี่ยวที่หาอนุพันธ์ง่ายแต่อินทิเกรตยาก (ln x)",
        "กรณีที่ 3: พหุนามดีกรีสูงกว่า 1 ต้องทำซ้ำหลายชั้น (x² e^x)",
        "กรณีที่ 4: ฟังก์ชันวนลูปไม่รู้จบ (e^x cos x)",
        "กรณีที่ 5: พีชคณิตคูณกับฟังก์ชันตรีโกณมิติ (x sin x)",
        "กรณีที่ 6: พีชคณิตคูณกับลอการิทึม (x ln x)",
    ],
    index=0,
)

if "กรณีที่ 1" in case_parts:
    with st.container(border=True):
        st.markdown(
            r"""
            <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 8px;">
                <span style="background-color: #FEF08A; border: 1.5px solid #18181B; border-radius: 6px; padding: 2px 10px; font-size: 13px; font-weight: 700; box-shadow: 1.5px 1.5px 0px #18181B;">กรณีศึกษาที่ 1 / 6</span>
                <span style="font-size: 13px; font-weight: 700; color: #4B5563;">พหุนามคูณกับเอกซ์โพเนนเชียล</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.latex(r"\int x e^x \, dx")
        st.markdown("โจทย์ข้อนี้เกิดจากฟังก์ชันพีชคณิต ($A$: $x$) คูณกับเอกซ์โพเนนเชียล ($E$: $e^x$)")
        st.markdown("**ตามกฎ LIATE ท่านควรเลือก $u$ และ $dv$ อย่างไร?**")

        parts_choice = st.radio(
            "ตามกฎ LIATE ท่านควรเลือก u และ dv อย่างไร?",
            options=[
                "แนวทางที่ 1: ให้ u = x และ dv = e^x dx",
                "แนวทางที่ 2: ให้ u = e^x และ dv = x dx",
            ],
            index=None,
            key="radio_parts_case1",
            label_visibility="collapsed",
        )

        p_choice = parts_choice or ""
        if not p_choice:
            st.info("โปรดเลือกแนวทางด้านบนเพื่อตรวจสอบความเข้าใจและรับผลป้อนกลับ")
        elif "แนวทางที่ 1" in p_choice:
            st.success("**ถูกต้องตามหลักการ (A มาก่อน E ในกฎ LIATE):** ดิฟ $u = x$ ดีกรีลดลงเหลือ $1$ ส่วน $e^x$ อินทิเกรตง่ายและคงรูปเดิม")
            st.markdown("##### ผลลัพธ์สุดท้าย")
            st.latex(r"\int x e^x \, dx = e^x(x - 1) + C")
            with st.container(border=True):
                st.markdown("**วิธีทำทีละขั้นตอนอย่างละเอียด:**")
                st.markdown(
                    r"""
                    1. **คำนวณส่วนประกอบ:**
                       * กำหนด $u = x \implies du = dx$ (ดีกรีลดลงเหลือค่าคงที่)
                       * กำหนด $dv = e^x dx \implies v = \int e^x dx = e^x$
                    2. **แทนค่าลงในสูตร By Parts:**
                       $$\int u \, dv = uv - \int v \, du$$
                       $$\int x e^x \, dx = x e^x - \int e^x \, dx$$
                    3. **คำนวณอินทิกรัลส่วนที่เหลือ:**
                       $$= x e^x - e^x + C = e^x(x - 1) + C$$
                    """
                )
        else:
            st.error(r"**รูปสมการจะซับซ้อนขึ้น:** หากเลือก $dv = x dx$ จะได้ $v = \frac{x^2}{2}$ ทำให้อินทิกรัลใหม่กลายเป็น $x^2 e^x$ ซึ่งดีกรีสูงขึ้นและยากกว่าเดิม")

elif "กรณีที่ 2" in case_parts:
    with st.container(border=True):
        st.markdown(
            r"""
            <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 8px;">
                <span style="background-color: #FEF08A; border: 1.5px solid #18181B; border-radius: 6px; padding: 2px 10px; font-size: 13px; font-weight: 700; box-shadow: 1.5px 1.5px 0px #18181B;">กรณีศึกษาที่ 2 / 6</span>
                <span style="font-size: 13px; font-weight: 700; color: #4B5563;">ฟังก์ชันเดี่ยว (ln x)</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.latex(r"\int \ln(x) \, dx")
        st.markdown(r"**ตามกฎ LIATE ท่านควรแบ่งบทบาท $u$ และ $dv$ อย่างไรสำหรับ $\int \ln(x) \cdot 1 \, dx$?**")

        parts_choice = st.radio(
            "ท่านจะแบ่งบทบาทอย่างไร?",
            options=[
                "แนวทางที่ 1: ให้ u = 1 และ dv = ln(x) dx",
                "แนวทางที่ 2: ให้ u = ln(x) และ dv = 1 dx",
            ],
            index=None,
            key="radio_parts_case2",
            label_visibility="collapsed",
        )

        p_choice = parts_choice or ""
        if not p_choice:
            st.info("โปรดเลือกแนวทางด้านบนเพื่อตรวจสอบความเข้าใจและรับผลป้อนกลับ")
        elif "แนวทางที่ 2" in p_choice:
            st.success(r"**ถูกต้องตามหลักการ (L มาเป็นอันดับแรกในกฎ LIATE):** $\ln(x)$ อินทิเกรตตรงยาก แต่ดิฟได้ $\frac{1}{x}$ พีชคณิต ซึ่งตัดทอนกับ $v = x$ ได้ลงตัว")
            st.markdown("##### ผลลัพธ์สุดท้าย")
            st.latex(r"\int \ln(x) \, dx = x(\ln x - 1) + C")
            with st.container(border=True):
                st.markdown("**วิธีทำทีละขั้นตอนอย่างละเอียด:**")
                st.markdown(
                    r"""
                    1. **กำหนดส่วนประกอบ:**
                       * $u = \ln(x) \implies du = \frac{1}{x} dx$ (เปลี่ยนลอการิทึมเป็นเศษส่วนพีชคณิต)
                       * $dv = dx \implies v = x$
                    2. **แทนในสูตร By Parts:**
                       $$\int \ln(x) \, dx = (\ln x)(x) - \int x \cdot \frac{1}{x} \, dx = x \ln(x) - \int 1 \, dx$$
                    3. **สรุปผลลัพธ์:**
                       $$= x \ln(x) - x + C = x(\ln x - 1) + C \quad (x > 0)$$
                    """
                )
        else:
            st.error(r"**ทางตัน:** หากเลือก $dv = \ln(x) dx$ ท่านจะต้องหา $v = \int \ln(x) dx$ ซึ่งก็คือโจทย์ตั้งต้นนั่นเอง")

elif "กรณีที่ 3" in case_parts:
    with st.container(border=True):
        st.markdown(
            r"""
            <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 8px;">
                <span style="background-color: #FEF08A; border: 1.5px solid #18181B; border-radius: 6px; padding: 2px 10px; font-size: 13px; font-weight: 700; box-shadow: 1.5px 1.5px 0px #18181B;">กรณีศึกษาที่ 3 / 6</span>
                <span style="font-size: 13px; font-weight: 700; color: #4B5563;">พหุนามดีกรีสูงกว่า 1</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.latex(r"\int x^2 e^x \, dx")
        st.markdown("**ขั้นตอนการลดรูปพหุนามควรเป็นอย่างไร?**")

        parts_choice = st.radio(
            "ขั้นตอนการลดรูปควรเป็นอย่างไร?",
            options=[
                "แนวทาง A: ทำรอบที่ 1 ลดเหลือ x e^x แล้วทำรอบที่ 2 ลดเหลือค่าคงที่",
                "แนวทาง B: สลับ u และ dv ในรอบที่ 2 เพื่อความรวดเร็ว",
            ],
            index=None,
            key="radio_parts_case3",
            label_visibility="collapsed",
        )

        p_choice = parts_choice or ""
        if not p_choice:
            st.info("โปรดเลือกแนวทางด้านบนเพื่อตรวจสอบความเข้าใจและรับผลป้อนกลับ")
        elif "แนวทาง A" in p_choice:
            st.success(r"**ถูกต้องตามหลักการ (ลดทอนดีกรีแบบต่อเนื่อง):** พหุนามดีกรี 2 ต้องทำ 2 รอบ ($x^2 \to 2x \to 2$) จนกระทั่งเหลืออินทิกรัลพื้นฐาน")
            st.markdown("##### ผลลัพธ์สุดท้าย")
            st.latex(r"\int x^2 e^x \, dx = e^x(x^2 - 2x + 2) + C")
            with st.container(border=True):
                st.markdown("**วิธีทำทีละขั้นตอนอย่างละเอียด:**")
                st.markdown(
                    r"""
                    1. **รอบที่ 1:** ให้ $u = x^2 \implies du = 2x dx$, $dv = e^x dx \implies v = e^x$
                       $$\int x^2 e^x dx = x^2 e^x - 2\int x e^x dx$$
                    2. **รอบที่ 2 (ทำซ้ำกับก้อน $\int x e^x dx$):** ให้ $u = x \implies du = dx$, $dv = e^x dx \implies v = e^x$
                       $$\int x e^x dx = x e^x - e^x$$
                    3. **ประกอบผลลัพธ์:**
                       $$\int x^2 e^x dx = x^2 e^x - 2(x e^x - e^x) + C = e^x(x^2 - 2x + 2) + C$$
                    """
                )
        else:
            st.error("**ข้อควรระวัง:** การสลับบทบาท $u$ และ $dv$ ในรอบถัดไปจะทำให้พจน์ตัดทอนกันหมดกลายเป็น $0 = 0$")

elif "กรณีที่ 4" in case_parts:
    with st.container(border=True):
        st.markdown(
            r"""
            <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 8px;">
                <span style="background-color: #FEF08A; border: 1.5px solid #18181B; border-radius: 6px; padding: 2px 10px; font-size: 13px; font-weight: 700; box-shadow: 1.5px 1.5px 0px #18181B;">กรณีศึกษาที่ 4 / 6</span>
                <span style="font-size: 13px; font-weight: 700; color: #4B5563;">ฟังก์ชันวนลูปไม่รู้จบ (Cyclic Integration)</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.latex(r"I = \int e^x \cos(x) \, dx")
        st.markdown("**ท่านจะเริ่มต้นกำหนด $u$ และ $dv$ รอบแรกอย่างไร?**")

        parts_choice = st.radio(
            "ท่านจะเริ่มต้นกำหนด u และ dv รอบแรกอย่างไร?",
            options=[
                "แนวทางที่ 1: กำหนด u = cos(x) และ dv = e^x dx (แล้วทำรอบสองให้สอดคล้องกัน)",
                "แนวทางที่ 2: กำหนด u = e^x และ dv = cos(x) dx (แล้วทำรอบสองให้สอดคล้องกัน)",
                "แนวทางที่ 3: รอบแรกเลือก u = cos(x) แต่รอบสองสลับกลับมาเลือก u = e^x",
            ],
            index=None,
            key="radio_parts_case4",
            label_visibility="collapsed",
        )

        p_choice = parts_choice or ""
        if not p_choice:
            st.info("โปรดเลือกแนวทางด้านบนเพื่อตรวจสอบความเข้าใจและรับผลป้อนกลับ")
        elif "แนวทางที่ 3" in p_choice:
            st.error("**ข้อควรระวัง:** หากรอบแรกกำหนดฟังก์ชันหนึ่งเป็น $u$ แต่รอบที่สองสลับกลับมา ผลลัพธ์จะหักล้างกันกลายเป็น $I = I$ หรือ $0 = 0$")
        else:
            st.success(r"**ถูกต้องตามหลักการ (Cyclic By Parts):** ทั้ง $e^x$ และ $\cos(x)$ วนกลับมารูปเดิม ทำ By Parts 2 รอบแล้วย้ายข้างสมการทางพีชคณิตเพื่อหาคำตอบ")
            st.markdown("##### ผลลัพธ์สุดท้าย")
            st.latex(r"\int e^x \cos(x) \, dx = \frac{e^x(\sin x + \cos x)}{2} + C")
            with st.container(border=True):
                st.markdown("**วิธีทำทีละขั้นตอนอย่างละเอียด:**")
                st.markdown(
                    r"""
                    1. **รอบที่ 1 ($u = e^x, dv = \cos(x) dx$):**
                       $$u = e^x \implies du = e^x dx, \quad dv = \cos(x) dx \implies v = \sin(x)$$
                       $$I = e^x \sin(x) - \int e^x \sin(x) \, dx$$
                    2. **รอบที่ 2 (ทำ By Parts ซ้ำกับ $\int e^x \sin x dx$ โดยคงบทบาทเดิม):**
                       $$u = e^x \implies du = e^x dx, \quad dv = \sin(x) dx \implies v = -\cos(x)$$
                       $$\int e^x \sin(x) \, dx = -e^x \cos(x) - \int (-e^x \cos x) \, dx = -e^x \cos(x) + I$$
                    3. **นำผลรอบที่ 2 แทนกลับในสมการแรกแล้วย้ายข้าง:**
                       $$I = e^x \sin(x) - \left[ -e^x \cos(x) + I \right] = e^x \sin(x) + e^x \cos(x) - I$$
                       $$2I = e^x(\sin x + \cos x) \implies I = \frac{e^x}{2}(\sin x + \cos x) + C$$
                    """
                )

elif "กรณีที่ 5" in case_parts:
    with st.container(border=True):
        st.markdown(
            r"""
            <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 8px;">
                <span style="background-color: #FEF08A; border: 1.5px solid #18181B; border-radius: 6px; padding: 2px 10px; font-size: 13px; font-weight: 700; box-shadow: 1.5px 1.5px 0px #18181B;">กรณีศึกษาที่ 5 / 6</span>
                <span style="font-size: 13px; font-weight: 700; color: #4B5563;">พีชคณิตคูณกับตรีโกณมิติ</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.latex(r"\int x \sin(x) \, dx")
        st.markdown("**ตามกฎ LIATE ท่านควรเลือก $u$ และ $dv$ อย่างไร?**")

        parts_choice = st.radio(
            "ท่านจะเลือกกำหนด u และ dv อย่างไร?",
            options=[
                "แนวทางที่ 1: ให้ u = x และ dv = sin(x) dx",
                "แนวทางที่ 2: ให้ u = sin(x) และ dv = x dx",
            ],
            index=None,
            key="radio_parts_case5",
            label_visibility="collapsed",
        )

        p_choice = parts_choice or ""
        if not p_choice:
            st.info("โปรดเลือกแนวทางด้านบนเพื่อตรวจสอบความเข้าใจและรับผลป้อนกลับ")
        elif "แนวทางที่ 1" in p_choice:
            st.success(r"**ถูกต้องตามกฎ LIATE (A มาก่อน T):** เลือก $u = x$ ทำให้ดิฟได้ $du = dx$ ดีกรีลดลง ส่วน $\sin(x)$ อินทิเกรตได้ $-\cos(x)$")
            st.markdown("##### ผลลัพธ์สุดท้าย")
            st.latex(r"\int x \sin(x) \, dx = -x\cos(x) + \sin(x) + C")
            with st.container(border=True):
                st.markdown("**วิธีทำทีละขั้นตอนอย่างละเอียด:**")
                st.markdown(
                    r"""
                    1. **กำหนดตัวแปรและหาอนุพันธ์/ปฏิยานุพันธ์:**
                       * $u = x \implies du = dx$
                       * $dv = \sin(x)dx \implies v = -\cos(x)$
                    2. **แทนค่าในสูตร By Parts:**
                       $$\int x\sin(x)\,dx = (x)(-\cos x) - \int (-\cos x)\,dx = -x\cos(x) + \int \cos(x)\,dx$$
                    3. **คำนวณผลลัพธ์สุดท้าย:**
                       $$= -x\cos(x) + \sin(x) + C$$
                    """
                )
        else:
            st.error(r"**รูปสมการจะซับซ้อนขึ้น:** หากเลือก $dv = x dx$ จะได้ $v = \frac{x^2}{2}$ ทำให้อินทิกรัลใหม่กลายเป็น $x^2 \cos(x)$ ซึ่งดีกรีสูงขึ้น")

else:
    with st.container(border=True):
        st.markdown(
            r"""
            <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 8px;">
                <span style="background-color: #FEF08A; border: 1.5px solid #18181B; border-radius: 6px; padding: 2px 10px; font-size: 13px; font-weight: 700; box-shadow: 1.5px 1.5px 0px #18181B;">กรณีศึกษาที่ 6 / 6</span>
                <span style="font-size: 13px; font-weight: 700; color: #4B5563;">พีชคณิตคูณกับลอการิทึม</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.latex(r"\int x \ln(x) \, dx")
        st.markdown("**ตามกฎ LIATE ท่านควรเลือก $u$ เป็นฟังก์ชันใด?**")

        parts_choice = st.radio(
            "ตามกฎ LIATE ท่านควรเลือก u เป็นฟังก์ชันใด?",
            options=[
                "แนวทางที่ 1: ให้ u = ln(x) และ dv = x dx",
                "แนวทางที่ 2: ให้ u = x และ dv = ln(x) dx",
            ],
            index=None,
            key="radio_parts_case6",
            label_visibility="collapsed",
        )

        p_choice = parts_choice or ""
        if not p_choice:
            st.info("โปรดเลือกแนวทางด้านบนเพื่อตรวจสอบความเข้าใจและรับผลป้อนกลับ")
        elif "แนวทางที่ 1" in p_choice:
            st.success(r"**ถูกต้องตามกฎ LIATE (L มาก่อน A เสมอ):** แม้ $x$ จะเป็นพหุนาม แต่ $\ln(x)$ อินทิเกรตยาก จึงต้องเลือกเป็น $u$ เพื่อดิฟให้เป็นพีชคณิต $\frac{1}{x}$")
            st.markdown("##### ผลลัพธ์สุดท้าย")
            st.latex(r"\int x \ln(x) \, dx = \frac{x^2}{4}(2\ln x - 1) + C")
            with st.container(border=True):
                st.markdown("**วิธีทำทีละขั้นตอนอย่างละเอียด:**")
                st.markdown(
                    r"""
                    1. **กำหนดตัวแปรและหาอนุพันธ์:**
                       * $u = \ln(x) \implies du = \frac{1}{x}dx$
                       * $dv = x dx \implies v = \frac{x^2}{2}$
                    2. **แทนค่าลงในสูตร By Parts:**
                       $$\int x\ln(x)\,dx = (\ln x)\left(\frac{x^2}{2}\right) - \int \frac{x^2}{2} \cdot \frac{1}{x}\,dx = \frac{x^2\ln x}{2} - \frac{1}{2}\int x\,dx$$
                    3. **คำนวณผลลัพธ์สุดท้าย:**
                       $$= \frac{x^2\ln x}{2} - \frac{x^2}{4} + C = \frac{x^2}{4}(2\ln x - 1) + C$$
                    """
                )
        else:
            st.error(r"**ทางตัน:** หากเลือก $dv = \ln(x)dx$ จะต้องหาปริพันธ์ของ $\ln(x)$ ซึ่งต้องใช้ By Parts ซ้ำซ้อนและผิดหลัก LIATE")


st.divider()

# =============================================================================
# 3. เครื่องคิดเลข By Parts ด้วย SymPy
# =============================================================================
st.markdown("### คำนวณโจทย์การอินทิเกรตทีละส่วนด้วย SymPy")

def _set_byparts_preset(val: str) -> None:
    st.session_state["byparts_expr"] = val

st.markdown("**ตัวอย่างโจทย์:**")
bp_cols = st.columns(4)
with bp_cols[0]:
    st.button("x e^x", key="pre_bp_1", use_container_width=True, on_click=_set_byparts_preset, args=("x*exp(x)",))
with bp_cols[1]:
    st.button("x ln(x)", key="pre_bp_2", use_container_width=True, on_click=_set_byparts_preset, args=("x*ln(x)",))
with bp_cols[2]:
    st.button("x² sin(x)", key="pre_bp_3", use_container_width=True, on_click=_set_byparts_preset, args=("x^2*sin(x)",))
with bp_cols[3]:
    st.button("e^x cos(x)", key="pre_bp_4", use_container_width=True, on_click=_set_byparts_preset, args=("exp(x)*cos(x)",))

bp_cols2 = st.columns(4)
with bp_cols2[0]:
    st.button("ln(x)", key="pre_bp_5", use_container_width=True, on_click=_set_byparts_preset, args=("ln(x)",))
with bp_cols2[1]:
    st.button("x cos(x)", key="pre_bp_6", use_container_width=True, on_click=_set_byparts_preset, args=("x*cos(x)",))
with bp_cols2[2]:
    st.button("arctan(x)", key="pre_bp_7", use_container_width=True, on_click=_set_byparts_preset, args=("atan(x)",))
with bp_cols2[3]:
    st.button("2^x cos(x)", key="pre_bp_8", use_container_width=True, on_click=_set_byparts_preset, args=("2^x*cos(x)",))

expr_input = st.text_input(
    "ใส่นิพจน์อินทิกรัลที่ต้องการคำนวณ",
    value=st.session_state.get("byparts_expr", "x*exp(x)"),
    placeholder="เช่น x*exp(x), x*ln(x), exp(x)*cos(x)",
    key="byparts_expr",
)
preview_math_expr(expr_input)
render_syntax_guide()

render_math_keypad(target_key="byparts_expr", key_prefix="byparts_kp", expanded=False)

btn_calc = st.button("คำนวณผลลัพธ์", type="primary", key="btn_byparts_calc")
if expr_input.strip() or btn_calc:
    if not expr_input.strip():
        st.error("กรุณาใส่นิพจน์ก่อน")
    else:
        res = solve_by_parts(expr_input)
        if res["ok"]:
            v_name = res.get("variable", "x")
            if v_name != "x":
                st.info(f"ตรวจพบตัวแปร **${v_name}$**: ระบบคำนวณและอินทิเกรตเทียบกับ $d{v_name}$ อัตโนมัติ")

            st.markdown("#### ผลลัพธ์การคำนวณ")
            render_latex(res["latex"])

            special_names = special_functions_in(res.get("result"))
            if special_names:
                st.info(describe_special_functions(special_names))
            elif res.get("status") == "better_suited_for_substitution":
                st.warning(res.get("warning", "โจทย์ข้อนี้เหมาะสมกับการใช้การแทนตัวแปร u มากกว่าการอินทิเกรตทีละส่วน"))
            elif res.get("status") == "non_elementary":
                st.warning("ฟังก์ชันนี้ไม่มีปฏิยานุพันธ์ในรูปฟังก์ชันมูลฐาน")
            elif res.get("parts_info"):
                p = res["parts_info"]
                u_lat = format_inverse_trig(sp.latex(p["u"]))
                dv_lat = format_inverse_trig(sp.latex(p["dv"]))
                st.info(f"การอินทิเกรตทีละส่วน (By Parts): กำหนด $u = {u_lat}$ และ $dv = {dv_lat} \\, d{v_name}$")

            st.divider()
            render_steps(res["steps"])
        else:
            st.error(res["error"])
