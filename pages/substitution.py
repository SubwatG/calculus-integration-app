"""pages/substitution.py — เทคนิคการอินทิเกรต (การเปลี่ยนตัวแปรและการอินทิเกรตทีละส่วน)

ออกแบบเพื่อสร้างมโนทัศน์การตัดสินใจเลือกตัวแปร พร้อมระบบปลดล็อควิธีทำ (Active Scaffolding)
ครอบคลุมทั้งรูปแบบฟังก์ชันยกกำลัง ตัวส่วน ตรีโกณมิติ ลอการิทึม และการวนลูป
"""

import streamlit as st
import sympy as sp

from utils.keypad import render_math_keypad
from utils.math_render import preview_math_expr, render_latex, render_steps, render_syntax_guide
from utils.substitution_solver import solve_substitution
from utils.theme import render_hero

render_hero(
    "เทคนิคการอินทิเกรต",
    "ห้องทดลองมโนทัศน์การตัดสินใจ: การเปลี่ยนตัวแปร (u-Sub) และการอินทิเกรตทีละส่วน (By Parts)",
)

# =============================================================================
# กล่องเข็มทิศการตัดสินใจ (Decision Compass)
# =============================================================================
with st.expander("เข็มทิศการตัดสินใจ: ควรเลือกใช้ u-Substitution หรือ By Parts เมื่อไหร่?", expanded=True):
    col_dec1, col_dec2 = st.columns(2)
    with col_dec1:
        st.markdown("#### 1. การเปลี่ยนตัวแปร (u-Substitution)")
        st.markdown(
            """
            * **ทฤษฎีเบื้องหลัง:** เป็นการย้อนกลับของ **กฎลูกโซ่ (Chain Rule)**
            * **จุดสังเกตหลัก:** 
              1. มี **ฟังก์ชันก้อนใน $g(x)$** และ **อนุพันธ์ $g'(x)$** คูณร่วมอยู่ด้วยกันในโจทย์
              2. เมื่อกำหนด $u = g(x)$ แล้ว ตัวแปรเดิม $x$ จะต้องถูก **ตัดทอนให้หมดเกลี้ยง 100%**
            * **ตัวอย่างโจทย์ที่เหมาะสม:**
              * $\\int 2x\\sqrt{x^2+1}\\,dx$ (มี $2x$ เป็นอนุพันธ์ของ $x^2+1$)
              * $\\int \\frac{\\ln x}{x}\\,dx$ (มี $\\frac{1}{x}$ เป็นอนุพันธ์ของ $\\ln x$)
              * $\\int \\cos(x)e^{\\sin(x)}\\,dx$ (มี $\\cos x$ เป็นอนุพันธ์ของ $\\sin x$)
            """
        )
    with col_dec2:
        st.markdown("#### 2. การอินทิเกรตทีละส่วน (Integration by Parts)")
        st.markdown(
            """
            * **ทฤษฎีเบื้องหลัง:** เป็นการย้อนกลับของ **กฎผลคูณ (Product Rule)**
            * **จุดสังเกตหลัก:**
              1. เป็นผลคูณของ **สองฟังก์ชันต่างตระกูล** (ตามกฎ LIATE) ที่ดิฟตัวหนึ่งแล้วไม่สามารถตัดอีกตัวได้
              2. ฟังก์ชันที่มี $x$ คูณกับ $e^x, \\sin x, \\cos x$ (ดิฟ $x$ เพื่อลดดีกรี)
              3. ฟังก์ชันเดี่ยวที่ **หาอนุพันธ์ง่าย แต่หาปริพันธ์ตรง ๆ ยาก** เช่น $\\ln x, \\arcsin x$ (กำหนด $dv = dx$)
            * **สูตรแกนหลัก:**
              $$\\int u \\, dv = uv - \\int v \\, du$$
            """
        )

st.divider()

tab1, tab2, tab3 = st.tabs([
    "1. เทคนิคการเปลี่ยนตัวแปร (u-Substitution)",
    "2. เทคนิคการอินทิเกรตทีละส่วน (Integration by Parts)",
    "3. เครื่องคิดเลขและเครื่องมือคำนวณ (SymPy CAS)",
])

# =============================================================================
# TAB 1: u-Substitution Scaffolding
# =============================================================================
with tab1:
    st.markdown("### 1.1 สรุป 4 รูปแบบสังเกตยอดนิยมในการเลือกตัวแปร u")
    st.markdown(
        """
        เป้าหมายของการเปลี่ยนตัวแปร คือการแปลงอินทิกรัลที่ซับซ้อนให้อยู่ในรูปพื้นฐาน $\\int f(u)\\,du$
        โดยมีหลักสำคัญคือ **ตัวแปรเดิม $x$ จะต้องถูกตัดทอนให้หมดเกลี้ยง**
        """
    )

    col_g1, col_g2 = st.columns(2)
    with col_g1:
        st.markdown("**1. ฟังก์ชันภายในวงเล็บยกกำลัง / ใต้กรณฑ์ (รูท):**")
        st.latex(r"\int [g(x)]^n \cdot g'(x) \, dx \implies \text{กำหนด } u = g(x)")
        st.caption("เมื่อ $u = g(x)$ จะได้ $du = g'(x)dx$ ซึ่งจะตัดกับ $g'(x)$ ในโจทย์พอดี")

        st.markdown("**2. ฟังก์ชันที่อยู่เป็นตัวส่วน (เศษส่วน):**")
        st.latex(r"\int \frac{g'(x)}{g(x)} \, dx \implies \text{กำหนด } u = g(x)")
        st.caption("ผลลัพธ์จะกลายเป็น $\\int \\frac{1}{u}du = \\ln|u| + C$")

    with col_g2:
        st.markdown("**3. ฟังก์ชันบนเลขชี้กำลัง:**")
        st.latex(r"\int e^{g(x)} \cdot g'(x) \, dx \implies \text{กำหนด } u = g(x)")
        st.caption("ผลลัพธ์จะกลายเป็น $\\int e^u du = e^u + C$")

        st.markdown("**4. ฟังก์ชันภายในฟังก์ชันตรีโกณมิติ:**")
        st.latex(r"\int \cos(g(x)) \cdot g'(x) \, dx \implies \text{กำหนด } u = g(x)")
        st.caption("ผลลัพธ์จะกลายเป็น $\\int \\cos(u) du = \\sin(u) + C$")

    st.divider()

    st.markdown("### 1.2 ห้องทดลองฝึกการตัดสินใจเลือกตัวแปร u (Active Scaffolding)")
    st.caption("เลือกโจทย์ตัวอย่างด้านล่าง แล้วลองตัดสินใจเลือกตัวแปร $u$ เพื่อวิเคราะห์ความถูกต้องและปลดล็อคขั้นตอนวิธีทำ")

    u_cases = {
        "โจทย์ที่ 1: ฟังก์ชันใต้กรณฑ์/ยกกำลัง — ∫ 2x √(x² + 1) dx": "case1",
        "โจทย์ที่ 2: ฟังก์ชันเศษส่วนและลอการิทึม — ∫ (ln x) / x dx": "case2",
        "โจทย์ที่ 3: ฟังก์ชันเลขชี้กำลังและตรีโกณ — ∫ cos(x) e^(sin x) dx": "case3",
        "โจทย์ที่ 4: พีชคณิตเหลือเศษ (Linear Adjustment) — ∫ x √(x + 1) dx": "case4",
    }

    selected_u_label = st.selectbox(
        "เลือกโจทย์ทดสอบมโนทัศน์:",
        list(u_cases.keys()),
        key="select_u_case",
    )
    selected_u_case = u_cases[selected_u_label]

    # -------------------------------------------------------------
    # CASE 1: 2x * sqrt(x^2 + 1)
    # -------------------------------------------------------------
    if selected_u_case == "case1":
        st.latex(r"\int 2x \sqrt{x^2 + 1} \, dx")
        u_choice = st.radio(
            "หากท่านเป็นผู้แก้โจทย์ ท่านจะกำหนดให้ u เท่ากับฟังก์ชันใด?",
            options=[
                "แนวทาง A: กำหนดให้ u = x^2 + 1 (ฟังก์ชันภายในเครื่องหมายกรณฑ์)",
                "แนวทาง B: กำหนดให้ u = x (ตัวแปรธรรมดา)",
                "แนวทาง C: กำหนดให้ u = 2x (ตัวคูณด้านหน้า)",
                "แนวทาง D: กำหนดให้ u = sin(x) (ฟังก์ชันตรีโกณ)",
            ],
            index=None,
            key="radio_u_case1",
        )

        if u_choice is None:
            st.info("[การตัดสินใจ] กรุณาคลิกเลือกตัวแปร u ที่ท่านคิดว่าเหมาะสมด้านบน เพื่อให้ระบบวิเคราะห์และปลดล็อคขั้นตอนวิธีทำ")
        elif "แนวทาง A" in u_choice:
            st.success("**[ถูกต้องตามหลักการ] เหมาะสมที่สุด (Preferred Substitution)**")
            st.markdown("พจน์ $2x$ นอกกรณฑ์ตรงกับอนุพันธ์ของ $x^2+1$ พอดิบพอดี ทำให้ตัวแปร $x$ ถูกกำจัดหมดเกลี้ยง:")

            st.markdown("##### ขั้นตอนวิธีทำฉบับสมบูรณ์:")
            st.markdown("**ขั้นที่ 1: กำหนดตัวแปรและหาอนุพันธ์**")
            st.latex(r"u = x^2 + 1 \implies du = 2x \, dx \implies dx = \frac{du}{2x}")

            st.markdown("**ขั้นที่ 2: แทนค่า u และ dx ลงในโจทย์**")
            st.latex(r"\int 2x \sqrt{x^2 + 1} \, dx = \int 2x \cdot \sqrt{u} \cdot \left(\frac{du}{2x}\right) = \int \sqrt{u} \, du = \int u^{1/2} \, du")

            st.markdown("**ขั้นที่ 3: คำนวณปริพันธ์เทียบกับตัวแปร u**")
            st.latex(r"= \frac{u^{1/2 + 1}}{\frac{1}{2} + 1} + C = \frac{2}{3}u^{3/2} + C")

            st.markdown("**ขั้นที่ 4: แทนค่า u กลับคืนสู่ตัวแปร x**")
            st.latex(r"= \frac{2}{3}(x^2 + 1)^{3/2} + C")

            st.markdown("**ขั้นที่ 5: ตรวจสอบความถูกต้องด้วยอนุพันธ์ย้อนกลับ (Verification Check)**")
            st.latex(r"\frac{d}{dx}\left[\frac{2}{3}(x^2 + 1)^{3/2} + C\right] = \frac{2}{3} \cdot \frac{3}{2}(x^2 + 1)^{1/2} \cdot (2x) = 2x\sqrt{x^2 + 1}")
        elif "แนวทาง B" in u_choice:
            st.warning("**[ถูกกฎคณิตศาสตร์ แต่ไม่ช่วยให้ง่ายขึ้น] (Valid but Inefficient)**")
            st.markdown("เมื่อแทน $u = x$ จะได้ $du = dx$ ส่งผลให้สมการกลายเป็น $\\int 2u\\sqrt{u^2+1}\\,du$ ซึ่งโครงสร้างสมการเหมือนเดิมทุกประการ ไม่เกิดการลดทอนความซับซ้อน")
        elif "แนวทาง C" in u_choice:
            st.warning("**[ทำให้รูปสมการซับซ้อนขึ้น] (Valid but Inefficient)**")
            st.markdown("เมื่อแทน $u = 2x \\implies x = u/2$ จะได้ $\\int u\\sqrt{\\frac{u^2}{4}+1}\\,\\frac{du}{2}$ พจน์ใต้กรณฑ์กลายเป็นเศษส่วน ซึ่งยากกว่าโจทย์ตั้งต้น")
        else:
            st.error("**[ผิดหลักการ] (Invalid Substitution)**")
            st.markdown("ฟังก์ชัน $\\sin(x)$ ไม่มีความเชื่อมโยงใด ๆ กับนิพจน์ในโจทย์ การแทนค่านี้จะทำให้ตัวแปร $x$ ไม่สามารถตัดทอนได้")

    # -------------------------------------------------------------
    # CASE 2: ln(x) / x
    # -------------------------------------------------------------
    elif selected_u_case == "case2":
        st.latex(r"\int \frac{\ln(x)}{x} \, dx")
        u_choice = st.radio(
            "หากท่านเป็นผู้แก้โจทย์ ท่านจะกำหนดให้ u เท่ากับฟังก์ชันใด?",
            options=[
                "แนวทาง A: กำหนดให้ u = x (ตัวส่วน)",
                "แนวทาง B: กำหนดให้ u = ln(x) (ฟังก์ชันลอการิทึม)",
                "แนวทาง C: กำหนดให้ u = 1/x (ส่วนกลับของ x)",
                "แนวทาง D: กำหนดให้ u = x ln(x) (ผลคูณ)",
            ],
            index=None,
            key="radio_u_case2",
        )

        if u_choice is None:
            st.info("[การตัดสินใจ] กรุณาคลิกเลือกตัวแปร u ด้านบนเพื่อตรวจคำตอบ")
        elif "แนวทาง B" in u_choice:
            st.success("**[ถูกต้องตามหลักการ] เหมาะสมที่สุด (Preferred Substitution)**")
            st.markdown("เนื่องจาก $\\frac{d}{dx}[\\ln x] = \\frac{1}{x}$ ซึ่งตรงกับตัวส่วนในโจทย์ $\\frac{1}{x}dx$ พอดิบพอดี:")

            st.markdown("##### ขั้นตอนวิธีทำฉบับสมบูรณ์:")
            st.markdown("**ขั้นที่ 1: กำหนดตัวแปรและหาอนุพันธ์**")
            st.latex(r"u = \ln(x) \implies du = \frac{1}{x} \, dx \implies dx = x \, du")

            st.markdown("**ขั้นที่ 2: แทนค่า u และ dx ลงในโจทย์**")
            st.latex(r"\int \frac{\ln(x)}{x} \, dx = \int \frac{u}{x} \cdot (x \, du) = \int u \, du")

            st.markdown("**ขั้นที่ 3: คำนวณปริพันธ์เทียบกับ u**")
            st.latex(r"= \frac{u^2}{2} + C")

            st.markdown("**ขั้นที่ 4: แทนค่า u กลับคืนสู่ตัวแปร x**")
            st.latex(r"= \frac{(\ln x)^2}{2} + C")

            st.markdown("**ขั้นที่ 5: ตรวจสอบความถูกต้องด้วยอนุพันธ์ย้อนกลับ**")
            st.latex(r"\frac{d}{dx}\left[\frac{(\ln x)^2}{2} + C\right] = \frac{1}{2} \cdot 2(\ln x) \cdot \frac{1}{x} = \frac{\ln x}{x}")
        elif "แนวทาง A" in u_choice:
            st.warning("**[ไม่ช่วยให้ง่ายขึ้น]** การแทน $u = x$ ทำให้ได้ $\\int \\frac{\\ln u}{u} du$ ซึ่งเหมือนโจทย์เดิมทุกประการ")
        elif "แนวทาง C" in u_choice:
            st.warning("**[กับดักความซับซ้อน]** เมื่อให้ $u = 1/x = x^{-1}$ จะได้ $du = -x^{-2}dx$ ส่งผลให้ตัวแปร $x$ มีดีกรีติดลบเพิ่มขึ้นและไม่สามารถตัดทอน $\\ln x$ ได้")
        else:
            st.error("**[ผิดหลักการ]** การเลือก $u = x \\ln x$ จะได้ $du = (\\ln x + 1)dx$ ซึ่งทำให้รูปสมการซับซ้อนขึ้นอย่างมาก")

    # -------------------------------------------------------------
    # CASE 3: cos(x) * exp(sin(x))
    # -------------------------------------------------------------
    elif selected_u_case == "case3":
        st.latex(r"\int \cos(x) e^{\sin(x)} \, dx")
        u_choice = st.radio(
            "หากท่านเป็นผู้แก้โจทย์ ท่านจะกำหนดให้ u เท่ากับฟังก์ชันใด?",
            options=[
                "แนวทาง A: กำหนดให้ u = cos(x) (ฟังก์ชันตัวคูณด้านหน้า)",
                "แนวทาง B: กำหนดให้ u = e^(sin x) (ฟังก์ชันเอกซ์โพเนนเชียลทั้งก้อน)",
                "แนวทาง C: กำหนดให้ u = sin(x) (ฟังก์ชันบนเลขชี้กำลัง)",
                "แนวทาง D: กำหนดให้ u = x",
            ],
            index=None,
            key="radio_u_case3",
        )

        if u_choice is None:
            st.info("[การตัดสินใจ] กรุณาคลิกเลือกตัวแปร u ด้านบนเพื่อตรวจคำตอบ")
        elif "แนวทาง C" in u_choice:
            st.success("**[ถูกต้องตามหลักการ] เหมาะสมที่สุด (Preferred Substitution)**")
            st.markdown("เนื่องจากอนุพันธ์ของเลขชี้กำลัง $\\frac{d}{dx}[\\sin x] = \\cos x$ ซึ่งตรงกับตัวคูณด้านหน้าพอดี:")

            st.markdown("##### ขั้นตอนวิธีทำฉบับสมบูรณ์:")
            st.markdown("**ขั้นที่ 1: กำหนดตัวแปรและหาอนุพันธ์**")
            st.latex(r"u = \sin(x) \implies du = \cos(x) \, dx \implies dx = \frac{du}{\cos(x)}")

            st.markdown("**ขั้นที่ 2: แทนค่าลงในโจทย์**")
            st.latex(r"\int \cos(x) e^{\sin(x)} \, dx = \int \cos(x) \cdot e^u \cdot \frac{du}{\cos(x)} = \int e^u \, du")

            st.markdown("**ขั้นที่ 3: คำนวณปริพันธ์และแทนค่ากลับ**")
            st.latex(r"= e^u + C = e^{\sin(x)} + C")

            st.markdown("**ขั้นที่ 4: ตรวจสอบความถูกต้องด้วยอนุพันธ์ย้อนกลับ**")
            st.latex(r"\frac{d}{dx}\left[e^{\sin(x)} + C\right] = e^{\sin(x)} \cdot \frac{d}{dx}[\sin(x)] = \cos(x) e^{\sin(x)}")
        elif "แนวทาง A" in u_choice:
            st.warning("**[ตัดทอนไม่หมด]** อนุพันธ์ของ $\\cos x$ คือ $-\\sin x$ ซึ่งไม่สามารถไปตัดกับ $\\sin x$ ที่อยู่บนเลขชี้กำลัง $e^{\\sin x}$ ได้")
        elif "แนวทาง B" in u_choice:
            st.info("**[ทำได้เช่นกันแต่วิธี C ตรงไปตรงมากว่า]** หากให้ $u = e^{\\sin x}$ จะได้ $du = \\cos(x)e^{\\sin x}dx \\implies \\int 1 du = u + C = e^{\\sin x} + C$")
        else:
            st.warning("**[ไม่ช่วยให้ง่ายขึ้น]** การแทน $u = x$ ไม่ได้ช่วยลดทอนความซับซ้อน")

    # -------------------------------------------------------------
    # CASE 4: x * sqrt(x + 1)
    # -------------------------------------------------------------
    else:
        st.latex(r"\int x \sqrt{x + 1} \, dx")
        st.caption("ข้อสังเกต: ข้อนี้อนุพันธ์ของ $x+1$ คือ $1$ ซึ่งไม่ได้ตัด $x$ ด้านหน้าให้หมดไปโดยตรง แต่เราสามารถแก้สมการหา $x$ ในรูปของ $u$ ได้!")
        u_choice = st.radio(
            "หากท่านเป็นผู้แก้โจทย์ ท่านจะกำหนดให้ u เท่ากับฟังก์ชันใด?",
            options=[
                "แนวทาง A: กำหนดให้ u = x",
                "แนวทาง B: กำหนดให้ u = x^2",
                "แนวทาง C: กำหนดให้ u = √(x + 1)",
                "แนวทาง D: กำหนดให้ u = x + 1 แล้วจัดรูปย้อนกลับ x = u - 1 (Linear Adjustment)",
            ],
            index=None,
            key="radio_u_case4",
        )

        if u_choice is None:
            st.info("[การตัดสินใจ] กรุณาคลิกเลือกตัวแปร u ด้านบนเพื่อตรวจคำตอบ")
        elif "แนวทาง D" in u_choice:
            st.success("**[ถูกต้องตามหลักการขั้นสูง] เทคนิคตัวแปรเหลือเศษ (Algebraic Adjustment)**")
            st.markdown("การจัดรูปย้อนกลับ $x = u - 1$ ช่วยเปลี่ยนการคูณนอกกรณฑ์ ให้กลายเป็นการกระจายกำลังพหุนามที่อินทิเกรตได้ง่าย:")

            st.markdown("##### ขั้นตอนวิธีทำฉบับสมบูรณ์:")
            st.markdown("**ขั้นที่ 1: กำหนดตัวแปรและจัดรูป x ในเทอมของ u**")
            st.latex(r"u = x + 1 \implies x = u - 1 \quad \text{และ} \quad du = dx")

            st.markdown("**ขั้นที่ 2: แทนค่าลงในโจทย์**")
            st.latex(r"\int x \sqrt{x + 1} \, dx = \int (u - 1) \cdot \sqrt{u} \, du = \int (u - 1) u^{1/2} \, du")
            st.latex(r"= \int \left( u^{3/2} - u^{1/2} \right) \, du")

            st.markdown("**ขั้นที่ 3: คำนวณปริพันธ์เทียบกับตัวแปร u**")
            st.latex(r"= \frac{u^{5/2}}{\frac{5}{2}} - \frac{u^{3/2}}{\frac{3}{2}} + C = \frac{2}{5}u^{5/2} - \frac{2}{3}u^{3/2} + C")

            st.markdown("**ขั้นที่ 4: แทนค่า u กลับคืนสู่ตัวแปร x**")
            st.latex(r"= \frac{2}{5}(x + 1)^{5/2} - \frac{2}{3}(x + 1)^{3/2} + C")

            st.markdown("**ขั้นที่ 5: ตรวจสอบความถูกต้องด้วยอนุพันธ์ย้อนกลับ**")
            st.latex(r"\frac{d}{dx}\left[\frac{2}{5}(x+1)^{5/2} - \frac{2}{3}(x+1)^{3/2}\right] = (x+1)^{3/2} - (x+1)^{1/2} = (x+1-1)\sqrt{x+1} = x\sqrt{x+1}")
        elif "แนวทาง D" in u_choice:
            st.info("**[ทำได้เช่นกันแต่วุ่นวายกว่า]** หากให้ $u = \\sqrt{x+1} \\implies u^2 = x+1 \\implies x = u^2-1$ และ $dx = 2u du$ จะได้ $\\int (u^2-1)(u)(2u du) = \\int 2(u^4 - u^2) du$ ซึ่งได้คำตอบเดียวกัน")
        else:
            st.warning("**[ไม่สามารถแก้ได้]** การแทนค่านี้ไม่ช่วยกำจัดความซับซ้อนของพจน์ใต้กรณฑ์")


# =============================================================================
# TAB 2: Integration by Parts Scaffolding
# =============================================================================
with tab2:
    st.markdown("### 2.1 สรุปหลักการทั่วไปในการเลือก u และ dv (กฎ LIATE)")
    st.markdown("สูตรหลักของการอินทิเกรตทีละส่วน (มาจากกฎการหาอนุพันธ์ของผลคูณ):")
    st.latex(r"\int u \, dv = uv - \int v \, du")

    st.markdown(
        """
        **หัวใจสำคัญในการตัดสินใจ:**
        1. **เลือก $u$:** ต้องเป็นฟังก์ชันที่ **หาอนุพันธ์แล้วได้รูปที่ง่ายขึ้นหรือดีกรีลดลง**
        2. **เลือก $dv$:** ต้องเป็นฟังก์ชันที่ **สามารถหาปริพันธ์กลับเป็น $v$ ได้ง่ายโดยรูปไม่บวมขึ้น**
        """
    )

    st.markdown(
        """
        | ลำดับ | ตัวย่อ | ประเภทฟังก์ชัน | ตัวอย่างฟังก์ชัน | บทบาทที่เหมาะสม | เหตุผลทางคณิตศาสตร์ |
        |:---:|:---:|:---|:---|:---:|:---|
        | 1 | **L** | Logarithmic | $\\ln x, \\log_a x$ | **ควรเป็น $u$ เสมอ** | หาอนุพันธ์ง่าย ($1/x$) แต่หาปริพันธ์ตรง ๆ ยาก |
        | 2 | **I** | Inverse Trigonometric | $\\arcsin x, \\arctan x$ | **ควรเป็น $u$ เสมอ** | หาอนุพันธ์แล้วเป็นฟังก์ชันพีชคณิต แต่หาปริพันธ์ตรง ๆ ยาก |
        | 3 | **A** | Algebraic | $x, x^2, 3x+5$ | **มักกำหนดเป็น $u$** | เมื่อดิฟแล้วดีกรีของ $x$ จะลดลงเรื่อย ๆ จนหมดไป |
        | 4 | **T** | Trigonometric | $\\sin x, \\cos x$ | **มักกำหนดเป็น $dv$** | อินทิเกรตแล้ววนลูปสลับกัน ดีกรีไม่เพิ่มขึ้น |
        | 5 | **E** | Exponential | $e^x, 2^x$ | **ควรเป็น $dv$ เสมอ** | อินทิเกรตง่ายที่สุด $e^x$ ได้รูปเดิม ไม่เพิ่มภาระ |
        """
    )

    st.divider()

    st.markdown("### 2.2 ห้องทดลองฝึกการตัดสินใจเลือก u และ dv (Active Scaffolding)")
    st.caption("เลือกโจทย์ตัวอย่างด้านล่าง แล้วลองตัดสินใจจับคู่ $u$ และ $dv$ เพื่อวิเคราะห์ความถูกต้องและปลดล็อคขั้นตอนวิธีทำ")

    parts_cases = {
        "โจทย์ที่ 1: พีชคณิต × เอกซ์โพเนนเชียล — ∫ x e^(2x) dx": "parts1",
        "โจทย์ที่ 2: พีชคณิต × ตรีโกณมิติ — ∫ x sin(x) dx": "parts2",
        "โจทย์ที่ 3: ลอการิทึมเดี่ยว (ซ่อน dv = dx) — ∫ ln(x) dx": "parts3",
        "โจทย์ที่ 4: วนลูปกลับมาที่เดิม (Cyclic Integration) — ∫ e^x cos(x) dx": "parts4",
    }

    selected_p_label = st.selectbox(
        "เลือกโจทย์ทดสอบมโนทัศน์ By Parts:",
        list(parts_cases.keys()),
        key="select_p_case",
    )
    selected_p_case = parts_cases[selected_p_label]

    # -------------------------------------------------------------
    # PARTS CASE 1: x * exp(2x)
    # -------------------------------------------------------------
    if selected_p_case == "parts1":
        st.latex(r"\int x e^{2x} \, dx")
        parts_choice = st.radio(
            "ท่านจะกำหนดการจับคู่ u และ dv อย่างไรเพื่อให้แก้โจทย์ได้สำเร็จ?",
            options=[
                "แนวทางที่ 1: กำหนด u = x (พีชคณิต) และ dv = e^(2x) dx (เอกซ์โพเนนเชียล)",
                "แนวทางที่ 2: กำหนด u = e^(2x) (เอกซ์โพเนนเชียล) และ dv = x dx (พีชคณิต)",
                "แนวทางที่ 3: กำหนด u = x e^(2x) และ dv = dx",
            ],
            index=None,
            key="radio_parts_case1",
        )

        if parts_choice is None:
            st.info("[การตัดสินใจ] กรุณาคลิกเลือกการจับคู่ u และ dv ด้านบน เพื่อดูผลวิเคราะห์และขั้นตอนวิธีทำ")
        elif "แนวทางที่ 1" in parts_choice:
            st.success("**[ถูกต้องตามหลักการ LIATE] ดีกรีของพีชคณิตลดลงสำเร็จ (Optimal)**")
            st.markdown("การเลือก $u = x$ ทำให้เมื่อหาอนุพันธ์ $du = dx$ ดีกรีลดลงเหลือ 0 ในขณะที่ $e^{2x}$ อินทิเกรตง่าย:")

            st.markdown("##### ขั้นตอนวิธีทำฉบับสมบูรณ์:")
            st.markdown("**ขั้นที่ 1: กำหนดตัวแปร หา du และ v**")
            st.latex(r"u = x \implies du = dx")
            st.latex(r"dv = e^{2x} \, dx \implies v = \int e^{2x} \, dx = \frac{1}{2}e^{2x}")

            st.markdown("**ขั้นที่ 2: แทนค่าลงในสูตรอินทิเกรตทีละส่วน**")
            st.latex(r"\int u \, dv = uv - \int v \, du")
            st.latex(r"\int x e^{2x} \, dx = (x)\left(\frac{1}{2}e^{2x}\right) - \int \left(\frac{1}{2}e^{2x}\right) \, dx")

            st.markdown("**ขั้นที่ 3: คำนวณปริพันธ์ที่เหลือและจัดรูปคำตอบ**")
            st.latex(r"= \frac{1}{2}x e^{2x} - \frac{1}{4}e^{2x} + C = \frac{1}{4}(2x - 1)e^{2x} + C")

            st.markdown("**ขั้นที่ 4: ตรวจสอบความถูกต้องด้วยอนุพันธ์ย้อนกลับ**")
            st.latex(r"\frac{d}{dx}\left[\frac{1}{2}x e^{2x} - \frac{1}{4}e^{2x} + C\right] = \left(\frac{1}{2}e^{2x} + x e^{2x}\right) - \frac{1}{2}e^{2x} = x e^{2x}")
        elif "แนวทางที่ 2" in parts_choice:
            st.warning("**[กับดักความซับซ้อน] Complexity Increased Warning!**")
            st.markdown("หากเลือกสลับตำแหน่ง จะได้ $v = \\frac{x^2}{2}$ ส่งผลให้พจน์ใหม่กลายเป็น:")
            st.latex(r"\int x e^{2x} \, dx = \frac{x^2}{2}e^{2x} - \int x^2 e^{2x} \, dx")
            st.markdown("ดีกรีของ $x$ **เพิ่มขึ้นจาก 1 เป็น 2** ทำให้สมการยากกว่าโจทย์ตั้งต้น และวนลูปบวมขึ้นเรื่อย ๆ")
        else:
            st.error("**[ไม่เกิดประโยชน์]** พจน์ใหม่จะมี $x^2$ เพิ่มขึ้นมาและซับซ้อนยิ่งขึ้น")

    # -------------------------------------------------------------
    # PARTS CASE 2: x * sin(x)
    # -------------------------------------------------------------
    elif selected_p_case == "parts2":
        st.latex(r"\int x \sin(x) \, dx")
        parts_choice = st.radio(
            "ท่านจะกำหนดการจับคู่ u และ dv อย่างไร?",
            options=[
                "แนวทางที่ 1: กำหนด u = x (พีชคณิต) และ dv = sin(x) dx (ตรีโกณมิติ)",
                "แนวทางที่ 2: กำหนด u = sin(x) (ตรีโกณมิติ) และ dv = x dx (พีชคณิต)",
                "แนวทางที่ 3: กำหนด u = 1 และ dv = x sin(x) dx",
            ],
            index=None,
            key="radio_parts_case2",
        )

        if parts_choice is None:
            st.info("[การตัดสินใจ] กรุณาคลิกเลือกการจับคู่ u และ dv ด้านบน")
        elif "แนวทางที่ 1" in parts_choice:
            st.success("**[ถูกต้องตามหลักการ LIATE] เหมาะสมที่สุด**")
            st.markdown("ตามกฎ LIATE พีชคณิต (A) ต้องมาก่อนตรีโกณมิติ (T) ดังนั้น $u = x$ และ $dv = \\sin(x)dx$:")

            st.markdown("##### ขั้นตอนวิธีทำฉบับสมบูรณ์:")
            st.markdown("**ขั้นที่ 1: กำหนดตัวแปร หา du และ v**")
            st.latex(r"u = x \implies du = dx")
            st.latex(r"dv = \sin(x) \, dx \implies v = \int \sin(x) \, dx = -\cos(x)")

            st.markdown("**ขั้นที่ 2: แทนค่าลงในสูตรอินทิเกรตทีละส่วน**")
            st.latex(r"\int x \sin(x) \, dx = (x)(-\cos x) - \int (-\cos x) \, dx")
            st.latex(r"= -x \cos(x) + \int \cos(x) \, dx")

            st.markdown("**ขั้นที่ 3: คำนวณปริพันธ์ที่เหลือและสรุปคำตอบ**")
            st.latex(r"= -x \cos(x) + \sin(x) + C")

            st.markdown("**ขั้นที่ 4: ตรวจสอบความถูกต้องด้วยอนุพันธ์ย้อนกลับ**")
            st.latex(r"\frac{d}{dx}[-x \cos(x) + \sin(x) + C] = (-\cos x + x \sin x) + \cos x = x \sin(x)")
        elif "แนวทางที่ 2" in parts_choice:
            st.warning("**[กับดักความซับซ้อน]** จะได้ $v = \\frac{x^2}{2}$ ส่งผลให้เกิด $\\int \\frac{x^2}{2}\\cos(x)dx$ ซึ่งดีกรีของ $x$ สูงขึ้น ยากกว่าเดิม")
        else:
            st.error("**[วนกลับมาที่เดิม]** การให้ $dv = x\\sin(x)dx$ จำเป็นต้องอินทิเกรต $x\\sin(x)$ ซึ่งก็คือโจทย์ตั้งต้นนั่นเอง")

    # -------------------------------------------------------------
    # PARTS CASE 3: ln(x)
    # -------------------------------------------------------------
    elif selected_p_case == "parts3":
        st.latex(r"\int \ln(x) \, dx")
        st.caption("ข้อสังเกต: ดูเหมือนว่ามีฟังก์ชันเดียว แต่จริง ๆ แล้วเราสามารถมองเป็น $\\int (\\ln x) \\cdot 1 \\, dx$ ได้!")
        parts_choice = st.radio(
            "ท่านจะกำหนดการจับคู่ u และ dv อย่างไรเพื่อแก้โจทย์อินทิกรัลของ ln(x)?",
            options=[
                "แนวทางที่ 1: กำหนด u = ln(x) (ลอการิทึม) และ dv = dx (ฟังก์ชันคงที่ 1)",
                "แนวทางที่ 2: กำหนด u = 1 และ dv = ln(x) dx",
                "แนวทางที่ 3: กำหนด u = x และ dv = (ln x / x) dx",
            ],
            index=None,
            key="radio_parts_case3",
        )

        if parts_choice is None:
            st.info("[การตัดสินใจ] กรุณาคลิกเลือกการจับคู่ u และ dv ด้านบน")
        elif "แนวทางที่ 1" in parts_choice:
            st.success("**[เทคนิคระดับตำนาน] การซ่อน dv = dx ปลดล็อคฟังก์ชันลอการิทึมสำเร็จ!**")
            st.markdown("เนื่องจากเราไม่ทราบสูตรอินทิเกรตของ $\\ln x$ ตรง ๆ แต่เรา **หาอนุพันธ์ของ $\\ln x$ ได้ง่ายมาก** คือ $\\frac{1}{x}$:")

            st.markdown("##### ขั้นตอนวิธีทำฉบับสมบูรณ์:")
            st.markdown("**ขั้นที่ 1: กำหนดตัวแปร หา du และ v**")
            st.latex(r"u = \ln(x) \implies du = \frac{1}{x} \, dx")
            st.latex(r"dv = dx \implies v = \int 1 \, dx = x")

            st.markdown("**ขั้นที่ 2: แทนค่าลงในสูตรอินทิเกรตทีละส่วน**")
            st.latex(r"\int \ln(x) \, dx = uv - \int v \, du = (\ln x)(x) - \int (x)\left(\frac{1}{x} \, dx\right)")
            st.latex(r"= x \ln(x) - \int 1 \, dx")

            st.markdown("**ขั้นที่ 3: คำนวณปริพันธ์ที่เหลือและสรุปคำตอบ**")
            st.latex(r"= x \ln(x) - x + C = x(\ln x - 1) + C")

            st.markdown("**ขั้นที่ 4: ตรวจสอบความถูกต้องด้วยอนุพันธ์ย้อนกลับ**")
            st.latex(r"\frac{d}{dx}[x \ln(x) - x + C] = \left(1 \cdot \ln x + x \cdot \frac{1}{x}\right) - 1 = \ln x + 1 - 1 = \ln(x)")
        elif "แนวทางที่ 2" in parts_choice:
            st.error("**[วนกลับมาที่เดิม]** หากเลือก $dv = \\ln(x)dx$ เราก็ยังไม่รู้วิธีหา $v = \\int \\ln(x)dx$ อยู่ดี ซึ่งเป็นปัญหาเดิมของโจทย์")
        else:
            st.warning("**[ซับซ้อนเกินจำเป็น]** แนวทางที่ 1 เรียบง่ายและตรงไปตรงมากว่ามาก")

    # -------------------------------------------------------------
    # PARTS CASE 4: e^x * cos(x) (Cyclic)
    # -------------------------------------------------------------
    else:
        st.latex(r"I = \int e^x \cos(x) \, dx")
        st.caption("ข้อสังเกต: ทั้ง $e^x$ และ $\\cos(x)$ ต่างก็เป็นฟังก์ชันที่ดิฟหรืออินทิเกรตแล้ววนลูปไม่รู้จบ จึงต้องทำ By Parts 2 ครั้งแล้วย้ายข้างสมการพีชคณิต!")
        parts_choice = st.radio(
            "ท่านจะเริ่มต้นกำหนด u และ dv รอบแรกอย่างไร?",
            options=[
                "แนวทางที่ 1: กำหนด u = cos(x) และ dv = e^x dx (แล้วทำรอบสองให้สอดคล้องกัน)",
                "แนวทางที่ 2: กำหนด u = e^x และ dv = cos(x) dx (แล้วทำรอบสองให้สอดคล้องกัน)",
                "แนวทางที่ 3: รอบแรกเลือก u = cos(x) แต่รอบสองสลับกลับมาเลือก u = e^x",
            ],
            index=None,
            key="radio_parts_case4",
        )

        if parts_choice is None:
            st.info("[การตัดสินใจ] กรุณาคลิกเลือกแนวทางด้านบน")
        elif "แนวทางที่ 3" in parts_choice:
            st.error("**[กับดักการสลับตัวแปรไปมา] 0 = 0 Trap!**")
            st.markdown("หากรอบแรกเลือกฟังก์ชันหนึ่งเป็น $u$ แต่รอบสองกลับลำเลือกสลับกัน ผลลัพธ์จะตัดทอนกันหมดกลายเป็น $I = I$ หรือ $0 = 0$ ซึ่งไม่สามารถหาคำตอบได้!")
        else:
            st.success("**[ถูกต้องตามหลักการอินทิเกรตแบบวนลูป (Cyclic Integration)]**")
            st.markdown("ทั้งแนวทางที่ 1 และ 2 สามารถแก้ได้สำเร็จ โดยมีขั้นตอนการทำ 2 รอบดังนี้:")

            st.markdown("##### ขั้นตอนวิธีทำฉบับสมบูรณ์ (โดยวิธี u = e^x, dv = cos(x) dx):")
            st.markdown("**รอบที่ 1:**")
            st.latex(r"u = e^x \implies du = e^x \, dx, \quad dv = \cos(x) \, dx \implies v = \sin(x)")
            st.latex(r"I = e^x \sin(x) - \int e^x \sin(x) \, dx")

            st.markdown("**รอบที่ 2 (ทำ By Parts ซ้ำกับก้อน $\int e^x \sin x dx$ โดยคงบทบาทเดิม):**")
            st.latex(r"u = e^x \implies du = e^x \, dx, \quad dv = \sin(x) \, dx \implies v = -\cos(x)")
            st.latex(r"\int e^x \sin(x) \, dx = -e^x \cos(x) - \int (-e^x \cos x) \, dx = -e^x \cos(x) + I")

            st.markdown("**นำผลรอบที่ 2 แทนกลับเข้าไปในสมการแรก:**")
            st.latex(r"I = e^x \sin(x) - \left[ -e^x \cos(x) + I \right] = e^x \sin(x) + e^x \cos(x) - I")

            st.markdown("**ย้ายข้างสมการทางพีชคณิต (บวก I ทั้งสองข้าง):**")
            st.latex(r"2I = e^x(\sin x + \cos x) \implies I = \frac{e^x}{2}(\sin x + \cos x) + C")


# =============================================================================
# TAB 3: Free SymPy Solver
# =============================================================================
with tab3:
    st.markdown("### คำนวณนิพจน์อิสระด้วย SymPy CAS")
    st.caption("ระบบจะคำนวณปฏิยานุพันธ์ ตรวจจับตัวแปร $u$ ที่เหมาะสม และแจ้งเตือนหากเป็นฟังก์ชันพิเศษที่ไม่เป็นมูลฐาน")

    def _set_sub_preset(val: str) -> None:
        st.session_state["substitution_expr"] = val

    st.markdown("**ตัวอย่างโจทย์ยอดนิยม (คลิกเพื่อโหลดสูตร):**")
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
        st.button("x e^(2x) (By Parts)", key="pre_sub_5", use_container_width=True, on_click=_set_sub_preset, args=("x*exp(2x)",))
    with p_cols2[1]:
        st.button("ln(x) (By Parts)", key="pre_sub_6", use_container_width=True, on_click=_set_sub_preset, args=("ln(x)",))
    with p_cols2[2]:
        st.button("e^(-x²) (Non-elementary)", key="pre_sub_7", use_container_width=True, on_click=_set_sub_preset, args=("exp(-x^2)",))

    expr_input = st.text_input(
        "ใส่นิพจน์อินทิกรัลที่ต้องการคำนวณ",
        value=st.session_state.get("substitution_expr", "2x*sqrt(x^2+1)"),
        placeholder="เช่น 2x*sqrt(x^2+1), ln(x)/x, x*exp(2x)",
        key="substitution_expr",
    )
    preview_math_expr(expr_input)
    render_syntax_guide()

    render_math_keypad(target_key="substitution_expr", key_prefix="sub_kp", expanded=False)

    if st.button("คำนวณผลลัพธ์", type="primary", key="btn_substitution_calc"):
        if not expr_input.strip():
            st.error("กรุณาใส่นิพจน์ก่อน")
        else:
            res = solve_substitution(expr_input)
            if res["ok"]:
                v_name = res.get("variable", "x")
                if v_name != "x":
                    st.info(f"✨ ตรวจพบตัวแปร **${v_name}$** — ระบบคำนวณและอินทิเกรตเทียบกับ $d{v_name}$ อัตโนมัติ")

                st.markdown("#### ผลลัพธ์การคำนวณ")
                render_latex(res["latex"])

                if res.get("status") == "non_elementary":
                    st.warning("ข้อสังเกตเชิงมโนทัศน์: ฟังก์ชันนี้ไม่มีปฏิยานุพันธ์ในรูปฟังก์ชันมูลฐาน (Non-Elementary Function) คำตอบที่ได้อยู่ในรูปฟังก์ชันพิเศษระดับสูง เช่น erf, Si, li")
                elif res.get("u_candidate") is not None:
                    u_c = res["u_candidate"]
                    du_c = res["du_candidate"]
                    st.info(f"💡 คำแนะนำเทคนิคการเปลี่ยนตัวแปร: สามารถกำหนดให้ $u = {sp.latex(u_c)}$ ซึ่งจะได้ $du = {sp.latex(du_c)} \\, d{v_name}$")

                st.divider()
                st.markdown("#### ขั้นตอนการพิจารณา")
                render_steps(res["steps"])
            else:
                st.error(res["error"])
