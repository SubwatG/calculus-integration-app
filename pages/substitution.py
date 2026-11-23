"""pages/substitution.py : การอินทิเกรตโดยการแทนตัวแปร (Integration by Substitution)

ออกแบบเพื่อสร้างแนวคิดการตัดสินใจเลือกตัวแปร u และ du พร้อมระบบปลดล็อควิธีทำ (Active Scaffolding)
ครอบคลุมทั้งรูปแบบฟังก์ชันยกกำลัง ตัวส่วน ตรีโกณมิติ และการจัดรูปพีชคณิต
"""

import streamlit as st
import sympy as sp

from utils.keypad import render_math_keypad
from utils.math_render import format_inverse_trig, preview_math_expr, render_latex, render_steps, render_syntax_guide
from utils.special_functions import describe_special_functions, special_functions_in
from utils.substitution_solver import (
    get_suggested_u_candidates,
    solve_substitution,
    verify_user_u_substitution,
)
from utils.theme import render_hero

render_hero(
    "การอินทิเกรตโดยการแทนตัวแปร (Integration by Substitution)",
    "หลักการและขั้นตอนการเลือกตัวแปร u และ du เพื่อลดรูปอินทิกรัลให้อยู่ในรูปพื้นฐาน",
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
# 1. สรุปรูปแบบการสังเกตเลือกตัวแปร u
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
            ">การแทนตัวแปร u</span>""",
            unsafe_allow_html=True,
        )
    with col_title:
        st.markdown("#### รูปแบบการสังเกตเลือกตัวแปร $u$")

    st.markdown(
        r"""
| รูปแบบฟังก์ชันในโจทย์ | รูปแบบทั่วไป | การกำหนดตัวแปร $u$ |
| :--- | :--- | :--- |
| **ในวงเล็บยกกำลัง / ใต้กรณฑ์** | $\int [g(x)]^n g'(x)\,dx$ | กำหนด $u = g(x)$ (ดิฟแล้วตัดกับ $g'(x)$ พอดี) |
| **ตัวส่วนของเศษส่วน** | $\int \frac{g'(x)}{g(x)}\,dx$ | กำหนด $u = g(x)$ (ดิฟแล้วตัดเศษ ได้รูป $\ln|u|$) |
| **เลขชี้กำลังหรือตรีโกณมิติ** | $\int f(g(x)) g'(x)\,dx$ | กำหนด $u = g(x)$ เป็นไส้ในของฟังก์ชัน |
| **การจัดรูปพีชคณิตเสริม** | $\int x \sqrt{x+1}\,dx$ | กำหนด $u = x+1$ แล้วจัดรูป $x = u-1$ แทนกลับ |
        """
    )

with st.expander("อ่านเป้าหมายและหลักการเปลี่ยนตัวแปร u เพิ่มเติม", expanded=False):
    st.markdown(
        r"""
- **เป้าหมายหลัก:** แปลงอินทิกรัลให้อยู่ในรูปพื้นฐาน $\int f(u)\,du$ โดยมีหลักสำคัญคือ **ตัวแปร $x$ จะต้องถูกตัดทอนได้หมด**
- **วิธีตรวจสอบ:** เมื่อดิฟ $u$ ได้ $du = g'(x)\,dx$ แล้วแทน $dx = \frac{du}{g'(x)}$ ตัวแปร $x$ ทั้งหมดต้องตัดทอนกันหายไป เหลือเฉพาะตัวแปร $u$
- **หากตัวแปร $x$ ไม่หมด:** ให้พิจารณาว่าสามารถจัดรูป $x$ ในเทอมของ $u$ มาแทนค่าเพิ่มได้หรือไม่ หากไม่ได้ อาจต้องใช้วิธีอื่น เช่น อินทิเกรตทีละส่วน (By Parts)
        """
    )

st.divider()

# =============================================================================
# 2. กรณีศึกษาฝึกตัดสินใจเลือกตัวแปร u (Active Scaffolding)
# =============================================================================
st.markdown("### กรณีศึกษาฝึกตัดสินใจเลือกตัวแปร $u$ (Decision Challenge)")

case_sub = st.selectbox(
    "เลือกกรณีศึกษาที่ต้องการเรียนรู้:",
    options=[
        "กรณีที่ 1: ฟังก์ชันใต้กรณฑ์ยกกำลัง (2x √(x² + 1))",
        "กรณีที่ 2: ฟังก์ชันตัวส่วนและลอการิทึม ((ln x) / x)",
        "กรณีที่ 3: ฟังก์ชันตรีโกณมิติและเลขชี้กำลัง (cos(x) e^(sin x))",
        "กรณีที่ 4: การจัดรูปพีชคณิตเสริมเมื่อ x ไม่หมด (x √(x + 1))",
        "กรณีที่ 5: ฟังก์ชันเศษส่วนและอนุพันธ์ของตัวส่วน (2x / (x² + 1))",
        "กรณีที่ 6: พหุนามยกกำลังและอนุพันธ์ภายใน (3x² (x³ + 5)⁴)",
    ],
    index=0,
)

if "กรณีที่ 1" in case_sub:
    with st.container(border=True):
        st.markdown(
            r"""
            <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 8px;">
                <span style="background-color: #FEF08A; border: 1.5px solid #18181B; border-radius: 6px; padding: 2px 10px; font-size: 13px; font-weight: 700; box-shadow: 1.5px 1.5px 0px #18181B;">กรณีศึกษาที่ 1 / 6</span>
                <span style="font-size: 13px; font-weight: 700; color: #4B5563;">ฟังก์ชันใต้กรณฑ์ยกกำลัง</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.latex(r"\int 2x\sqrt{x^2+1} \, dx")
        st.markdown("**ท่านจะเลือกกำหนดตัวแปร $u$ เป็นฟังก์ชันใด?**")

        u_choice = st.radio(
            "ท่านจะเลือกกำหนด u เป็นฟังก์ชันใด?",
            options=[
                "แนวทาง A: ให้ u = x² + 1 (ฟังก์ชันใต้กรณฑ์)",
                "แนวทาง B: ให้ u = 2x (ฟังก์ชันสัมประสิทธิ์ด้านนอก)",
                "แนวทาง C: ให้ u = x (ตัวแปรเดิม)",
            ],
            index=None,
            key="radio_u_case1",
            label_visibility="collapsed",
        )

        parts_choice = u_choice or ""
        if not parts_choice:
            st.info("โปรดเลือกแนวทางด้านบนเพื่อตรวจสอบความเข้าใจและรับผลป้อนกลับ")
        elif "แนวทาง A" in parts_choice:
            st.success(r"**ถูกต้องตามหลักการ:** เมื่อเลือก $u = x^2 + 1$ จะได้ $du = 2x\,dx$ ซึ่งพจน์ $2x$ จะตัดทอนกับตัวคูณด้านหน้าหมดพอดี")
            st.markdown("##### ผลลัพธ์สุดท้าย")
            st.latex(r"\int 2x\sqrt{x^2+1} \, dx = \frac{2}{3}(x^2+1)^{3/2} + C")
            with st.container(border=True):
                st.markdown("**วิธีทำทีละขั้นตอนอย่างละเอียด:**")
                st.markdown(
                    r"""
                    1. **กำหนดตัวแปรและหาอนุพันธ์:**
                       $$u = x^2 + 1 \implies \frac{du}{dx} = 2x \implies dx = \frac{du}{2x}$$
                    2. **แทนค่าในโจทย์:**
                       $$\int 2x\sqrt{x^2+1} \, dx = \int 2x \cdot \sqrt{u} \cdot \frac{du}{2x}$$
                    3. **ตัดทอนตัวแปรเดิม:**
                       $$\int \sqrt{u} \, du = \int u^{1/2} \, du = \frac{2}{3}u^{3/2} + C$$
                    4. **แทนค่า $u$ กลับคืน:**
                       $$= \frac{2}{3}(x^2+1)^{3/2} + C$$
                    """
                )
        elif "แนวทาง B" in parts_choice:
            st.error(r"**ยังไม่เหมาะสม:** หากเลือก $u = 2x$ จะได้ $du = 2dx$ ใต้กรณฑ์จะกลายเป็น $\sqrt{(u/2)^2+1}$ ซึ่งยังคงติดตัวแปร $u$ ซับซ้อนและตัดทอนไม่ได้")
        else:
            st.warning("**ไม่มีการเปลี่ยนแปลง:** การให้ $u = x$ เป็นเพียงการเปลี่ยนชื่อตัวแปร ไม่ได้ช่วยลดความซับซ้อนของโจทย์")

elif "กรณีที่ 2" in case_sub:
    with st.container(border=True):
        st.markdown(
            r"""
            <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 8px;">
                <span style="background-color: #FEF08A; border: 1.5px solid #18181B; border-radius: 6px; padding: 2px 10px; font-size: 13px; font-weight: 700; box-shadow: 1.5px 1.5px 0px #18181B;">กรณีศึกษาที่ 2 / 6</span>
                <span style="font-size: 13px; font-weight: 700; color: #4B5563;">ฟังก์ชันตัวส่วนและลอการิทึม</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.latex(r"\int \frac{\ln x}{x} \, dx")
        st.markdown("**ท่านจะเลือกกำหนดตัวแปร $u$ เป็นฟังก์ชันใด?**")

        u_choice = st.radio(
            "ท่านจะเลือกกำหนด u เป็นฟังก์ชันใด?",
            options=[
                "แนวทาง A: ให้ u = x (ตัวส่วน)",
                "แนวทาง B: ให้ u = ln(x) (ตัวเศษ)",
                "แนวทาง C: ให้ u = 1/x",
            ],
            index=None,
            key="radio_u_case2",
            label_visibility="collapsed",
        )

        parts_choice = u_choice or ""
        if not parts_choice:
            st.info("โปรดเลือกแนวทางด้านบนเพื่อตรวจสอบความเข้าใจและรับผลป้อนกลับ")
        elif "แนวทาง B" in parts_choice:
            st.success(r"**ถูกต้องตามหลักการ:** อนุพันธ์ของ $\ln(x)$ คือ $\frac{1}{x}$ ซึ่งจะตัดกับตัวส่วน $x$ หายไปหมดพอดี")
            st.markdown("##### ผลลัพธ์สุดท้าย")
            st.latex(r"\int \frac{\ln x}{x} \, dx = \frac{(\ln x)^2}{2} + C")
            with st.container(border=True):
                st.markdown("**วิธีทำทีละขั้นตอนอย่างละเอียด:**")
                st.markdown(
                    r"""
                    1. **กำหนดตัวแปรและหาอนุพันธ์:**
                       $$u = \ln x \implies \frac{du}{dx} = \frac{1}{x} \implies dx = x\,du$$
                    2. **แทนค่าในโจทย์:**
                       $$\int \frac{\ln x}{x} \, dx = \int \frac{u}{x} \cdot (x\,du)$$
                    3. **ตัดทอนตัวแปรเดิม:**
                       $$\int u \, du = \frac{u^2}{2} + C$$
                    4. **แทนค่า $u$ กลับคืน:**
                       $$= \frac{(\ln x)^2}{2} + C \quad (x > 0)$$
                    """
                )
        elif "แนวทาง A" in parts_choice:
            st.warning(r"**ไม่มีการเปลี่ยนแปลง:** ได้เพียง $\int \frac{\ln u}{u}\,du$ ซึ่งเหมือนโจทย์เดิม")
        else:
            st.error(r"**รูปจะซับซ้อนขึ้น:** หากเลือก $u = 1/x$ จะได้ $du = -\frac{1}{x^2}\,dx$ ซึ่งทำให้ดีกรีตัวส่วนเพิ่มขึ้นเป็น $x^2$")

elif "กรณีที่ 3" in case_sub:
    with st.container(border=True):
        st.markdown(
            r"""
            <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 8px;">
                <span style="background-color: #FEF08A; border: 1.5px solid #18181B; border-radius: 6px; padding: 2px 10px; font-size: 13px; font-weight: 700; box-shadow: 1.5px 1.5px 0px #18181B;">กรณีศึกษาที่ 3 / 6</span>
                <span style="font-size: 13px; font-weight: 700; color: #4B5563;">ฟังก์ชันตรีโกณมิติและเลขชี้กำลัง</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.latex(r"\int \cos(x) e^{\sin(x)} \, dx")
        st.markdown("**ท่านจะเลือกกำหนดตัวแปร $u$ เป็นฟังก์ชันใด?**")

        u_choice = st.radio(
            "ท่านจะเลือกกำหนด u เป็นฟังก์ชันใด?",
            options=[
                "แนวทาง A: ให้ u = sin(x) (ไส้ในของเลขชี้กำลัง)",
                "แนวทาง B: ให้ u = cos(x) (สัมประสิทธิ์ด้านหน้า)",
                "แนวทาง C: ให้ u = e^(sin x)",
            ],
            index=None,
            key="radio_u_case3",
            label_visibility="collapsed",
        )

        parts_choice = u_choice or ""
        if not parts_choice:
            st.info("โปรดเลือกแนวทางด้านบนเพื่อตรวจสอบความเข้าใจและรับผลป้อนกลับ")
        elif "แนวทาง A" in parts_choice:
            st.success(r"**ถูกต้องตามหลักการ:** ดิฟ $u = \sin(x)$ ได้ $du = \cos(x)\,dx$ ซึ่งตัดกับ $\cos(x)$ ด้านหน้าหมดพอดี")
            st.markdown("##### ผลลัพธ์สุดท้าย")
            st.latex(r"\int \cos(x) e^{\sin(x)} \, dx = e^{\sin(x)} + C")
            with st.container(border=True):
                st.markdown("**วิธีทำทีละขั้นตอนอย่างละเอียด:**")
                st.markdown(
                    r"""
                    1. **กำหนดตัวแปรและหาอนุพันธ์:**
                       $$u = \sin(x) \implies du = \cos(x)\,dx \implies dx = \frac{du}{\cos(x)}$$
                    2. **แทนค่าและตัดทอน:**
                       $$\int \cos(x) e^u \cdot \frac{du}{\cos(x)} = \int e^u \, du = e^u + C$$
                    3. **แทนค่า $u$ กลับคืน:**
                       $$= e^{\sin(x)} + C$$
                    """
                )
        elif "แนวทาง C" in parts_choice:
            st.info(r"**ทำได้เช่นกัน:** หากให้ $u = e^{\sin x} \implies du = e^{\sin x}\cos(x)dx$ จะได้ $\int 1\,du = u + C = e^{\sin x} + C$")
        else:
            st.error(r"**ยังไม่เหมาะสม:** ดิฟ $\cos(x)$ ได้ $-\sin(x)$ ซึ่งไม่สามารถตัดกับ $\sin(x)$ ที่ติดอยู่บนเลขชี้กำลังได้")

elif "กรณีที่ 4" in case_sub:
    with st.container(border=True):
        st.markdown(
            r"""
            <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 8px;">
                <span style="background-color: #FEF08A; border: 1.5px solid #18181B; border-radius: 6px; padding: 2px 10px; font-size: 13px; font-weight: 700; box-shadow: 1.5px 1.5px 0px #18181B;">กรณีศึกษาที่ 4 / 6</span>
                <span style="font-size: 13px; font-weight: 700; color: #4B5563;">การจัดรูปพีชคณิตเสริมเมื่อ x ไม่หมด</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.latex(r"\int x\sqrt{x+1} \, dx")
        st.markdown("**ท่านจะแก้ปัญหาตัวแปร $x$ ด้านหน้าที่เหลืออยู่อย่างไร?**")

        u_choice = st.radio(
            "ท่านจะแก้ปัญหาตัวแปร x ด้านหน้าที่เหลืออยู่อย่างไร?",
            options=[
                "แนวทาง A: แทน x = u - 1 แล้วคูณกระจายเข้าไปในวงเล็บ",
                "แนวทาง B: ดึง x ออกนอกอินทิกรัลเลยเพราะเป็นตัวคูณ",
                "แนวทาง C: ถือว่าทำไม่ได้ด้วย u-Substitution ต้องเปลี่ยนไปใช้วิธีอื่นทันที",
                "แนวทาง D: ให้ u = √(x+1)",
            ],
            index=None,
            key="radio_u_case4",
            label_visibility="collapsed",
        )

        parts_choice = u_choice or ""
        if not parts_choice:
            st.info("โปรดเลือกแนวทางด้านบนเพื่อตรวจสอบความเข้าใจและรับผลป้อนกลับ")
        elif "แนวทาง B" in parts_choice:
            st.error(r"**ข้อควรระวัง:** ห้ามดึงตัวแปรที่กำลังอินทิเกรต ($x$) ออกนอกเครื่องหมาย $\int$ ดึงได้เฉพาะค่าคงที่เท่านั้น")
        elif "แนวทาง A" in parts_choice:
            st.success("**ถูกต้องตามหลักการ:** จัดรูป $x = u - 1$ แล้วคูณกระจาย $(u - 1)u^{1/2} = u^{3/2} - u^{1/2}$ ทำให้หาอินทิกรัลทีละพจน์ได้")
            st.markdown("##### ผลลัพธ์สุดท้าย")
            st.latex(r"\int x\sqrt{x+1} \, dx = \frac{2}{5}(x+1)^{5/2} - \frac{2}{3}(x+1)^{3/2} + C")
            with st.container(border=True):
                st.markdown("**วิธีทำทีละขั้นตอนอย่างละเอียด:**")
                st.markdown(
                    r"""
                    1. **สลับรูปตัวแปร:**
                       $$u = x + 1 \implies x = u - 1 \quad \text{และ} \quad dx = du$$
                    2. **แทนค่าลงในอินทิกรัล:**
                       $$\int x\sqrt{x+1}\,dx = \int (u - 1)\sqrt{u}\,du = \int (u - 1)u^{1/2}\,du$$
                    3. **คูณกระจายและอินทิเกรตทีละพจน์:**
                       $$= \int (u^{3/2} - u^{1/2})\,du = \frac{2}{5}u^{5/2} - \frac{2}{3}u^{3/2} + C$$
                    4. **แทนค่า $u$ กลับคืน:**
                       $$= \frac{2}{5}(x+1)^{5/2} - \frac{2}{3}(x+1)^{3/2} + C$$
                    """
                )
        elif "แนวทาง D" in parts_choice:
            st.info(r"**ทำได้เช่นกัน:** หากให้ $u = \sqrt{x+1} \implies u^2 = x+1$ จัดรูปเป็น $\int 2(u^4 - u^2)\,du$ ซึ่งได้ผลลัพธ์เดียวกัน")
        else:
            st.warning("**สามารถแก้ได้:** การแทนค่านี้สามารถแก้ได้สำเร็จโดยใช้เทคนิคการจัดรูปพีชคณิตเสริม")

elif "กรณีที่ 5" in case_sub:
    with st.container(border=True):
        st.markdown(
            r"""
            <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 8px;">
                <span style="background-color: #FEF08A; border: 1.5px solid #18181B; border-radius: 6px; padding: 2px 10px; font-size: 13px; font-weight: 700; box-shadow: 1.5px 1.5px 0px #18181B;">กรณีศึกษาที่ 5 / 6</span>
                <span style="font-size: 13px; font-weight: 700; color: #4B5563;">ฟังก์ชันเศษส่วนและอนุพันธ์ของตัวส่วน</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.latex(r"\int \frac{2x}{x^2+1} \, dx")
        st.markdown("**ท่านจะเลือกกำหนดตัวแปร $u$ เป็นฟังก์ชันใด?**")

        u_choice = st.radio(
            "ท่านจะเลือกกำหนด u เป็นฟังก์ชันใด?",
            options=[
                "แนวทาง A: ให้ u = x² + 1 (ตัวส่วนทั้งก้อน)",
                "แนวทาง B: ให้ u = 2x (ตัวเศษ)",
                "แนวทาง C: ให้ u = x",
            ],
            index=None,
            key="radio_u_case5",
            label_visibility="collapsed",
        )

        parts_choice = u_choice or ""
        if not parts_choice:
            st.info("โปรดเลือกแนวทางด้านบนเพื่อตรวจสอบความเข้าใจและรับผลป้อนกลับ")
        elif "แนวทาง A" in parts_choice:
            st.success(r"**ถูกต้องตามหลักการ:** ตัวเศษ $2x$ คืออนุพันธ์ของตัวส่วนพอดี ได้รูปพื้นฐาน $\int \frac{1}{u}\,du = \ln|u| + C$")
            st.markdown("##### ผลลัพธ์สุดท้าย")
            st.latex(r"\int \frac{2x}{x^2+1} \, dx = \ln(x^2+1) + C")
            with st.container(border=True):
                st.markdown("**วิธีทำทีละขั้นตอนอย่างละเอียด:**")
                st.markdown(
                    r"""
                    1. **กำหนดตัวแปรและหาอนุพันธ์:**
                       $$u = x^2 + 1 \implies du = 2x\,dx \implies dx = \frac{du}{2x}$$
                    2. **แทนค่าลงในอินทิกรัลและตัดทอน:**
                       $$\int \frac{2x}{x^2+1}\,dx = \int \frac{2x}{u} \cdot \frac{du}{2x} = \int \frac{1}{u}\,du$$
                    3. **คำนวณปริพันธ์พื้นฐาน:**
                       $$= \ln|u| + C = \ln(x^2+1) + C \quad (\text{เนื่องจาก } x^2+1 > 0 \text{ เสมอ})$$
                    """
                )
        elif "แนวทาง B" in parts_choice:
            st.error("**ยังไม่เหมาะสม:** หากให้ $u = 2x$ จะได้ตัวส่วนเป็น $(u/2)^2+1$ ซึ่งยังคงเป็นเศษส่วนพีชคณิตและไม่ช่วยให้ง่ายขึ้น")
        else:
            st.warning("**ไม่มีการเปลี่ยนแปลง:** การให้ $u = x$ ไม่ได้ช่วยลดความซับซ้อนของฟังก์ชัน")

else:
    with st.container(border=True):
        st.markdown(
            r"""
            <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 8px;">
                <span style="background-color: #FEF08A; border: 1.5px solid #18181B; border-radius: 6px; padding: 2px 10px; font-size: 13px; font-weight: 700; box-shadow: 1.5px 1.5px 0px #18181B;">กรณีศึกษาที่ 6 / 6</span>
                <span style="font-size: 13px; font-weight: 700; color: #4B5563;">พหุนามยกกำลังและอนุพันธ์ภายใน</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.latex(r"\int 3x^2 (x^3+5)^4 \, dx")
        st.markdown("**ท่านจะเลือกกำหนดตัวแปร $u$ เป็นฟังก์ชันใด?**")

        u_choice = st.radio(
            "ท่านจะเลือกกำหนด u เป็นฟังก์ชันใด?",
            options=[
                "แนวทาง A: ให้ u = x³ + 5 (ฟังก์ชันฐานในวงเล็บยกกำลัง)",
                "แนวทาง B: ให้ u = 3x² (สัมประสิทธิ์ด้านหน้า)",
                "แนวทาง C: ให้ u = (x³ + 5)⁴",
            ],
            index=None,
            key="radio_u_case6",
            label_visibility="collapsed",
        )

        parts_choice = u_choice or ""
        if not parts_choice:
            st.info("โปรดเลือกแนวทางด้านบนเพื่อตรวจสอบความเข้าใจและรับผลป้อนกลับ")
        elif "แนวทาง A" in parts_choice:
            st.success(r"**ถูกต้องตามหลักการ:** ดิฟฐาน $u = x^3 + 5$ ได้ $du = 3x^2\,dx$ ตัดกับ $3x^2$ ด้านหน้าหมด เหลือเพียง $\int u^4\,du$")
            st.markdown("##### ผลลัพธ์สุดท้าย")
            st.latex(r"\int 3x^2 (x^3+5)^4 \, dx = \frac{(x^3+5)^5}{5} + C")
            with st.container(border=True):
                st.markdown("**วิธีทำทีละขั้นตอนอย่างละเอียด:**")
                st.markdown(
                    r"""
                    1. **กำหนดตัวแปรและหาอนุพันธ์:**
                       $$u = x^3 + 5 \implies du = 3x^2\,dx \implies dx = \frac{du}{3x^2}$$
                    2. **แทนค่าและตัดทอน:**
                       $$\int 3x^2(x^3+5)^4\,dx = \int 3x^2 \cdot u^4 \cdot \frac{du}{3x^2} = \int u^4\,du$$
                    3. **คำนวณปริพันธ์และแทนค่ากลับ:**
                       $$= \frac{u^5}{5} + C = \frac{(x^3+5)^5}{5} + C$$
                    """
                )
        elif "แนวทาง C" in parts_choice:
            st.error("**รูปจะซับซ้อนขึ้น:** การเลือกยกกำลัง 4 จะทำให้เกิดพจน์อนุพันธ์ลูกโซ่ซับซ้อนย้อนกลับไปหาร")
        else:
            st.error("**ยังไม่เหมาะสม:** ดิฟ $3x^2$ ได้ $6x$ ซึ่งไม่สามารถตัดทอนพจน์ $(x^3+5)^4$ ได้")


st.divider()

# =============================================================================
# 3. เครื่องคิดเลขคำนวณและทดลองเลือกตัวแปร u
# =============================================================================
st.markdown("### คำนวณและทดลองเลือกตัวแปร u")

def _set_sub_preset(val: str) -> None:
    st.session_state["substitution_expr"] = val

st.markdown("**ตัวอย่างโจทย์:**")
p_cols1 = st.columns(4)
with p_cols1[0]:
    st.button("2x √(x² + 1)", key="pre_sub_1", use_container_width=True, on_click=_set_sub_preset, args=("2x*sqrt(x^2+1)",))
with p_cols1[1]:
    st.button("(ln x) / x", key="pre_sub_2", use_container_width=True, on_click=_set_sub_preset, args=("ln(x)/x",))
with p_cols1[2]:
    st.button("cos(x) e^(sin x)", key="pre_sub_3", use_container_width=True, on_click=_set_sub_preset, args=("cos(x)*exp(sin(x))",))
with p_cols1[3]:
    st.button("x √(x + 1)", key="pre_sub_4", use_container_width=True, on_click=_set_sub_preset, args=("x*sqrt(x+1)",))

p_cols2 = st.columns(3)
with p_cols2[0]:
    st.button("2x / (x² + 1)", key="pre_sub_5", use_container_width=True, on_click=_set_sub_preset, args=("2x/(x^2+1)",))
with p_cols2[1]:
    st.button("3x² (x³ + 5)⁴", key="pre_sub_6", use_container_width=True, on_click=_set_sub_preset, args=("3x^2*(x^3+5)^4",))
with p_cols2[2]:
    st.button("x e^x (เหมาะกับ By Parts)", key="pre_sub_7", use_container_width=True, on_click=_set_sub_preset, args=("x*exp(x)",))

expr_input = st.text_input(
    "ใส่นิพจน์อินทิกรัลที่ต้องการคำนวณ",
    value=st.session_state.get("substitution_expr", "2x*sqrt(x^2+1)"),
    placeholder="เช่น 2x*sqrt(x^2+1), ln(x)/x, x*sqrt(x+1)",
    key="substitution_expr",
)
preview_math_expr(expr_input)
render_syntax_guide()
render_math_keypad(target_key="substitution_expr", key_prefix="sub_kp", expanded=False)

tab_user, tab_auto = st.tabs(["ทดลองกำหนดตัวแปร u ด้วยตนเอง", "ระบบเฉลยวิธีทำโดยอัตโนมัติ"])

with tab_user:
    st.markdown("#### ทดลองกำหนดตัวแปร u ด้วยตนเอง")

    candidates = get_suggested_u_candidates(expr_input)
    if st.session_state.get("_prev_sub_expr") != expr_input:
        st.session_state["_prev_sub_expr"] = expr_input
        if candidates:
            st.session_state["user_u_input"] = candidates[0]
        else:
            st.session_state["user_u_input"] = ""

    if candidates:
        st.markdown("**ตัวเลือกตัวแปร u ที่น่าสนใจในโจทย์นี้:**")
        cand_cols = st.columns(min(len(candidates), 5))
        for idx, cand_str in enumerate(candidates[:5]):
            with cand_cols[idx]:
                if st.button(
                    f"u = {cand_str}",
                    key=f"btn_cand_u_{idx}",
                    use_container_width=True,
                ):
                    st.session_state["user_u_input"] = cand_str
    else:
        st.info("โจทย์ข้อนี้เป็นรูปฟังก์ชันพื้นฐานของแคลคูลัส สามารถหาปริพันธ์ได้โดยตรงตามสูตรมาตรฐานโดยไม่ต้องใช้การแทนตัวแปร u (ท่านสามารถดูวิธีทำได้ที่แท็บ 'ระบบเฉลยวิธีทำโดยอัตโนมัติ')")

    if "user_u_input" not in st.session_state:
        st.session_state["user_u_input"] = candidates[0] if candidates else ""

    u_input_val = st.text_input(
        "ระบุฟังก์ชัน u(x) ที่ท่านเลือก:",
        placeholder="เช่น x^2 + 1, ln(x), cos(x)" if candidates else "โจทย์นี้เป็นสูตรพื้นฐาน ไม่จำเป็นต้องแทนตัวแปร u",
        key="user_u_input",
    )

    if st.button("ตรวจสอบการเลือกตัวแปร u", type="primary", key="btn_check_u"):
        if not expr_input.strip() or not u_input_val.strip():
            st.error("กรุณาระบุทั้งโจทย์อินทิกรัลและฟังก์ชัน u")
        else:
            ver_res = verify_user_u_substitution(expr_input, u_input_val)
            st.divider()

            if ver_res["status"] == "direct":
                st.success(f"**{ver_res['status_th']}** : {ver_res['message']}")
                st.markdown("##### ผลลัพธ์สุดท้าย")
                render_latex(ver_res["latex"])
                render_steps(ver_res["steps"], title="วิธีทำทีละขั้นตอน")

            elif ver_res["status"] == "algebraic_adjustment":
                st.info(f"**{ver_res['status_th']}** : {ver_res['message']}")
                st.markdown("##### ผลลัพธ์สุดท้าย")
                render_latex(ver_res["latex"])
                render_steps(ver_res["steps"], title="วิธีทำทีละขั้นตอน (พร้อมการจัดรูปพีชคณิต)")

            elif ver_res["status"] == "incompatible":
                st.error(f"**{ver_res['status_th']}** : {ver_res['message']}")
                render_steps(ver_res["steps"], title="รายละเอียดว่าเหตุใดการเลือกนี้จึงไม่สามารถแก้ได้")

            elif ver_res["status"] == "trivial":
                st.warning(f"**{ver_res['status_th']}** : {ver_res['message']}")
                render_steps(ver_res["steps"], title="คำอธิบาย")

            elif ver_res["status"] == "unsuitable_for_substitution":
                st.warning(f"**{ver_res['status_th']}** : {ver_res['message']}")
                render_steps(ver_res["steps"], title="คำแนะนำแนวทางที่เหมาะสม")
            else:
                st.error(ver_res.get("message", "เกิดข้อผิดพลาดในการคำนวณ"))

with tab_auto:
    st.markdown("#### ระบบวิเคราะห์และเฉลยวิธีทำโดยอัตโนมัติ")
    st.caption("ระบบจะค้นหาตัวแปร u ที่เหมาะสมที่สุด หรือแนะนำเทคนิคที่ตรงกับโจทย์")

    btn_calc = st.button("คำนวณและแสดงวิธีทำ", type="primary", key="btn_substitution_calc")
    if expr_input.strip() or btn_calc:
        if not expr_input.strip():
            st.error("กรุณาใส่นิพจน์ก่อน")
        else:
            res = solve_substitution(expr_input)
            if res["ok"]:
                v_name = res.get("variable", "x")
                if v_name != "x":
                    st.info(f"ตรวจพบตัวแปร **${v_name}$**: ระบบคำนวณเทียบกับ $d{v_name}$ อัตโนมัติ")

                st.markdown("##### ผลลัพธ์การคำนวณ")
                render_latex(res["latex"])

                special_names = special_functions_in(res.get("result"))
                if special_names:
                    st.info(describe_special_functions(special_names))
                elif res.get("status") == "non_elementary":
                    st.warning("ฟังก์ชันนี้ไม่มีปฏิยานุพันธ์ในรูปฟังก์ชันมูลฐาน")
                elif res.get("method") == "by_parts":
                    st.warning("ข้อสังเกต: โจทย์ข้อนี้ไม่สามารถแก้ด้วยการแทนตัวแปร u ได้ แนะนำให้ใช้วิธีการอินทิเกรตทีละส่วน (Integration by Parts)")
                elif res.get("u_candidate") is not None:
                    u_c = format_inverse_trig(sp.latex(res["u_candidate"]))
                    du_c = format_inverse_trig(sp.latex(res["du_candidate"]))
                    st.info(f"แนะนำตัวแปรที่เหมาะสม: กำหนดให้ $u = {u_c}$ ซึ่งจะได้ $du = {du_c} \\, d{v_name}$")

                st.divider()
                render_steps(res["steps"])
            else:
                st.error(res["error"])
