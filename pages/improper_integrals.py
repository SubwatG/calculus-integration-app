"""pages/improper_integrals.py — บทเรียน interactive: ปริพันธ์ไม่ตรงแบบ (Improper Integrals)

สำรวจการลู่เข้าหรือลู่ออกของปริพันธ์บนช่วงอนันต์ พร้อมกราฟแรเงาและขั้นตอนการคำนวณลิมิต
"""

import streamlit as st

from utils.improper_solver import compute_improper
from utils.math_render import preview_math_expr, render_latex, render_syntax_guide, render_steps
from utils.plotter import plot_improper
from utils.riemann_solver import X
from utils.theme import render_hero
from utils.theory import THEORY_CONTENT

render_hero("ปริพันธ์ไม่ตรงแบบ", "สำรวจการลู่เข้าหรือลู่ออกของปริพันธ์บนช่วงอนันต์และจุดเอกฐาน")

theory = THEORY_CONTENT["improper"]

with st.expander(f"ทฤษฎี: {theory['title']}", expanded=False):
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
    st.markdown("**แนวทางการตัดสินใจ**")
    st.info(theory["decision_guide"])

st.divider()
st.markdown("### ลองคำนวณ")

st.markdown("**ตัวอย่างโจทย์ยอดนิยม:**")
p_cols = st.columns(3)
if p_cols[0].button("กำลังสอง $\\frac{1}{x^2}$ บน $[1, \\infty)$", key="pre_imp_1"):
    st.session_state["improper_expr"] = "1/x**2"
    st.session_state["improper_a"] = 1.0
    st.session_state["improper_upper_type"] = "อนันต์ (inf)"
    st.rerun()
if p_cols[1].button("ฮาร์มอนิก $\\frac{1}{x}$ บน $[1, \\infty)$", key="pre_imp_2"):
    st.session_state["improper_expr"] = "1/x"
    st.session_state["improper_a"] = 1.0
    st.session_state["improper_upper_type"] = "อนันต์ (inf)"
    st.rerun()
if p_cols[2].button("เอกซ์โพเนนเชียล $e^{-x}$ บน $[0, \\infty)$", key="pre_imp_3"):
    st.session_state["improper_expr"] = "exp(-x)"
    st.session_state["improper_a"] = 0.0
    st.session_state["improper_upper_type"] = "อนันต์ (inf)"
    st.rerun()

expr_input = st.text_input(
    "ฟังก์ชัน f(x)",
    value="1/x**2",
    placeholder="เช่น 1/x**2, 1/x, 1/sqrt(x)",
    key="improper_expr",
)
preview_math_expr(expr_input)
render_syntax_guide()

col_a, col_b = st.columns(2)
with col_a:
    a_val = st.number_input("ขอบล่าง a", value=1.0, key="improper_a")
with col_b:
    upper_type = st.selectbox("ขอบบน", ["อนันต์ (inf)", "จำนวนจำกัด"], key="improper_upper_type")
    b_val = None
    if upper_type.startswith("จำนวน"):
        b_val = st.number_input("ขอบบน b", value=2.0, key="improper_b")

st.caption("[คำแนะนำ] ปัจจุบันระบบรองรับการคำนวณอินทิกรัลบนช่วงอนันต์ [a, ∞) และช่วงจำกัด [a, b]")

if not expr_input.strip():
    st.info("กรุณาระบุฟังก์ชัน f(x) หรือคลิกเลือกตัวอย่างด้านบน")
else:
    res = compute_improper(expr_input, a_val, b_val)
    if res["ok"]:
        st.markdown("### ผลลัพธ์")
        render_latex(res["latex"])
        st.divider()

        st.markdown("### กราฟการลู่เข้าและพื้นที่ใต้กราฟ (Improper Integral Visualization)")
        try:
            fig, ax = plot_improper(res["expr"], a_val, b_val)
            st.pyplot(fig)
        except Exception as e:
            st.warning(f"ไม่สามารถวาดกราฟได้: {e}")

        render_steps(res["steps"])
    else:
        st.error(res["error"])
