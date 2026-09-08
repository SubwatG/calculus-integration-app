"""pages/substitution.py — เทคนิคการอินทิเกรต (การเปลี่ยนตัวแปรและการอินทิเกรตทีละส่วน)

ออกแบบเพื่อสร้างมโนทัศน์การตัดสินใจเลือกตัวแปร ไม่ใช่แค่การคำนวณสำเร็จรูป
"""

import streamlit as st

from utils.math_render import render_latex, render_steps
from utils.substitution_solver import solve_substitution
from utils.theme import render_hero
from utils.theory import THEORY_CONTENT

render_hero(
    "เทคนิคการอินทิเกรต",
    "ห้องทดลองมโนทัศน์การตัดสินใจ: การเปลี่ยนตัวแปร (u-Sub) และการอินทิเกรตทีละส่วน (By Parts)",
)

tab1, tab2, tab3 = st.tabs([
    "1. ฝึกเลือกตัวแปร u (u-Substitution)",
    "2. ฝึกเลือก u และ dv (Integration by Parts)",
    "3. คำนวณอัตโนมัติด้วย SymPy",
])

# ==========================================
# TAB 1: u-Substitution Scaffolding
# ==========================================
with tab1:
    st.markdown("### การตัดสินใจเลือกตัวแปร $u$ ในเทคนิคการเปลี่ยนตัวแปร")
    st.info(
        "💡 **หลักการสำคัญ:** การแทนค่าตัวแปรที่ดีต้องทำให้ตัวแปรเดิม $x$ หายไปทั้งหมด "
        "และทำให้นิพจน์ใหม่อยู่ในรูปที่อินทิเกรตต่อได้ง่ายทันที"
    )

    st.markdown("#### โจทย์ตัวอย่าง: $\\int 2x\\sqrt{x^2+1}\\,dx$")

    u_choice = st.radio(
        "หากท่านเป็นผู้แก้โจทย์ ท่านจะกำหนดให้ $u$ เท่ากับฟังก์ชันใด?",
        options=[
            "เลือก $u = x^2 + 1$",
            "เลือก $u = x$",
            "เลือก $u = 2x$",
            "เลือก $u = \\sin(x)$",
        ],
        index=0,
        key="radio_u_choice",
    )

    if u_choice == "เลือก $u = x^2 + 1$":
        st.success("🟢 **การตัดสินใจ: เหมาะสมที่สุด (Preferred Substitution)**")
        st.markdown(
            """
            * **อนุพันธ์ที่ได้:** $du = 2x\\,dx \\implies dx = \\frac{du}{2x}$
            * **การแทนค่าลงในโจทย์:**
              $$\\int 2x\\sqrt{x^2+1}\\,dx = \\int 2x \\cdot \\sqrt{u} \\cdot \\frac{du}{2x} = \\int \\sqrt{u}\\,du$$
            * **ผลการวิเคราะห์:** พจน์ $2x$ ตัดทอนกันหมดพอดี เหลือเพียง $\\int u^{1/2}\\,du$ ซึ่งอินทิเกรตได้โดยตรง:
              $$= \\frac{2}{3}u^{3/2} + C = \\frac{2}{3}(x^2+1)^{3/2} + C$$
            """
        )
    elif u_choice == "เลือก $u = x$":
        st.warning("🟡 **การตัดสินใจ: ถูกต้องตามกฎ แต่ไม่ช่วยให้ง่ายขึ้น (Valid but Inefficient)**")
        st.markdown(
            """
            * **อนุพันธ์ที่ได้:** $du = dx$
            * **การแทนค่าลงในโจทย์:**
              $$\\int 2x\\sqrt{x^2+1}\\,dx = \\int 2u\\sqrt{u^2+1}\\,du$$
            * **ผลการวิเคราะห์:** การให้ $u = x$ ไม่ได้ผิดกฎคณิตศาสตร์ แต่สมการใหม่มีโครงสร้างเหมือนเดิมทุกประการ ไม่เกิดประโยชน์ในการคำนวณ
            """
        )
    elif u_choice == "เลือก $u = 2x$":
        st.warning("🟡 **การตัดสินใจ: ถูกต้องตามกฎ แต่ทำให้ซับซ้อนขึ้น (Valid but Inefficient)**")
        st.markdown(
            """
            * **อนุพันธ์ที่ได้:** $du = 2\\,dx \\implies x = \\frac{u}{2}$
            * **การแทนค่าลงในโจทย์:**
              $$\\int 2x\\sqrt{x^2+1}\\,dx = \\int u\\sqrt{\\frac{u^2}{4}+1}\\,\\frac{du}{2}$$
            * **ผลการวิเคราะห์:** พจน์ใต้กรณฑ์กลายเป็นเศษส่วน ทำให้คำนวณยากกว่าโจทย์ตั้งต้น
            """
        )
    else:
        st.error("🔴 **การตัดสินใจ: ไม่ถูกต้องตามหลักการ (Invalid Substitution)**")
        st.markdown(
            """
            * **ผลการวิเคราะห์:** ฟังก์ชัน $\\sin(x)$ ไม่มีความเชื่อมโยงกับนิพจน์ใด ๆ ในโจทย์ตั้งต้น การเลือกนี้จะทำให้ตัวแปร $x$ ไม่สามารถตัดทอนได้
            """
        )

# ==========================================
# TAB 2: Integration by Parts Scaffolding
# ==========================================
with tab2:
    st.markdown("### การตัดสินใจเลือก $u$ และ $dv$ ในเทคนิคการอินทิเกรตทีละส่วน")
    st.latex(r"\int u \, dv = uv - \int v \, du")

    st.markdown(
        """
        หลักการลำดับความสำคัญตามกฎ **LIATE Rule** ในการเลือก $u$:
        1. **L** - Logarithmic functions (เช่น $\\ln x$)
        2. **I** - Inverse Trigonometric functions (เช่น $\\arcsin x$)
        3. **A** - Algebraic functions (เช่น $x, x^2$)
        4. **T** - Trigonometric functions (เช่น $\\sin x, \\cos x$)
        5. **E** - Exponential functions (เช่น $e^x$)
        """
    )

    st.divider()
    st.markdown("#### โจทย์ทดสอบมโนทัศน์: $\\int x e^x \\, dx$")

    parts_choice = st.radio(
        "ท่านจะจับคู่ $u$ และ $dv$ อย่างไร?",
        options=[
            "แนวทางที่ 1: ให้ u = x (พีชคณิต) และ dv = e^x dx (เอกซ์โพเนนเชียล)",
            "แนวทางที่ 2: ให้ u = e^x (เอกซ์โพเนนเชียล) และ dv = x dx (พีชคณิต)",
        ],
        index=0,
        key="radio_parts_choice",
    )

    if "แนวทางที่ 1" in parts_choice:
        st.success("🟢 **สถานะ: ถูกต้องตามกฎ LIATE (Complexity Reduced)**")
        st.markdown(
            """
            * **ขั้นตอนการอนุพันธ์และการหาปริพันธ์:**
              * $u = x \\implies du = dx$ (ดีกรีของ $x$ ลดลงจาก 1 เหลือ 0)
              * $dv = e^x dx \\implies v = e^x$
            * **แทนค่าลงในสูตร:**
              $$\\int x e^x \\, dx = x e^x - \\int e^x \\, dx$$
            * **ผลลัพธ์สุดท้าย:**
              $$= x e^x - e^x + C = (x - 1)e^x + C$$
            * **ข้อสรุป:** พจน์ปริพันธ์ใหม่ $\\int e^x dx$ มีความง่ายกว่าโจทย์เดิม ทำให้ได้คำตอบทันที
            """
        )
    else:
        st.warning("🟠 **สถานะ: กับดักความซับซ้อน (Complexity Increased Warning)**")
        st.markdown(
            """
            * **ขั้นตอนการอนุพันธ์และการหาปริพันธ์:**
              * $u = e^x \\implies du = e^x dx$
              * $dv = x dx \\implies v = \\frac{x^2}{2}$ (ดีกรีของ $x$ เพิ่มขึ้นจาก 1 เป็น 2)
            * **แทนค่าลงในสูตร:**
              $$\\int x e^x \\, dx = \\frac{x^2}{2}e^x - \\int \\frac{x^2}{2}e^x \\, dx$$
            * **ผลการวิเคราะห์:** พจน์ใหม่ $\\int \\frac{x^2}{2}e^x \\, dx$ มีความซับซ้อน **มากกว่าโจทย์ตั้งต้น** (ดีกรีสูงขึ้น) หากทำต่อไปจะวนลูปเป็นกำลัง 3, 4 ไม่สิ้นสุด
            """
        )

# ==========================================
# TAB 3: Free SymPy Solver
# ==========================================
with tab3:
    st.markdown("### คำนวณนิพจน์อิสระด้วย SymPy CAS")
    expr_input = st.text_input(
        "ใส่นิพจน์อินทิกรัลที่ต้องการคำนวณ",
        value="2*x*exp(x**2)",
        placeholder="เช่น 2*x*exp(x**2), 3*x**2*cos(x**3)",
        key="substitution_expr",
    )

    if st.button("คำนวณ", type="primary", key="btn_substitution_calc"):
        if not expr_input.strip():
            st.error("กรุณาใส่นิพจน์ก่อน")
        else:
            res = solve_substitution(expr_input)
            if res["ok"]:
                st.markdown("#### ผลลัพธ์การคำนวณ")
                render_latex(res["latex"])
                st.divider()
                st.markdown("#### ขั้นตอนการพิจารณา")
                render_steps(res["steps"])
            else:
                st.error(res["error"])
