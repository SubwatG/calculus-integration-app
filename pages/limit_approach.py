"""pages/limit_approach.py — ลิมิตเข้าใกล้จุด (skeleton)

TODO: ใส่ logic กราฟจริง (plot_limit_near) ให้สมบูรณ์
อ้างอิง blueprint: pages/riemann.py
"""

import streamlit as st

from utils.limit_solver import compute_limit_near
from utils.math_render import preview_math_expr, render_latex, render_syntax_guide, render_steps
from utils.plotter import plot_limit_near
from utils.riemann_solver import X
from utils.theme import render_hero
from utils.theory import THEORY_CONTENT

render_hero("ลิมิตเข้าใกล้จุด", "สำรวจค่าลิมิตเมื่อ x เข้าใกล้จุด a")

theory = THEORY_CONTENT["limit"]

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

st.divider()
st.markdown("### ลองคำนวณ")

st.markdown("**ตัวอย่างโจทย์คลาสสิก:**")
p_cols = st.columns(3)
if p_cols[0].button("มีรูโหว่ $\\frac{x^2-4}{x-2}$ ที่ $a=2$", key="pre_lim_1"):
    st.session_state["limit_expr"] = "(x**2 - 4)/(x - 2)"
    st.session_state["limit_a"] = 2.0
    st.rerun()
if p_cols[1].button("ตรีโกณมิติ $\\frac{\\sin(x)}{x}$ ที่ $a=0$", key="pre_lim_2"):
    st.session_state["limit_expr"] = "sin(x)/x"
    st.session_state["limit_a"] = 0.0
    st.rerun()
if p_cols[2].button("ส่วนกลับ $\\frac{1}{x}$ ที่ $a=0$", key="pre_lim_3"):
    st.session_state["limit_expr"] = "1/x"
    st.session_state["limit_a"] = 0.0
    st.rerun()

expr_input = st.text_input(
    "ฟังก์ชัน f(x)",
    value="(x**2 - 4)/(x - 2)",
    placeholder="เช่น (x**2-4)/(x-2), sin(x)/x",
    key="limit_expr",
)
preview_math_expr(expr_input)
render_syntax_guide()

a_val = st.number_input("จุดที่ x เข้าใกล้ a", value=2.0, key="limit_a")

if not expr_input.strip():
    st.info("กรุณาระบุฟังก์ชัน f(x) หรือคลิกเลือกตัวอย่างด้านบน")
else:
    res = compute_limit_near(expr_input, a_val)
    if res["ok"]:
        st.markdown("### ผลลัพธ์")
        render_latex(res["latex"])
        st.divider()

        st.markdown("### กราฟการเข้าใกล้ลิมิต (Limit Approach Visualization)")
        try:
            fig, ax = plot_limit_near(res["expr"], a_val)
            st.pyplot(fig)
        except Exception as e:
            st.warning(f"ไม่สามารถวาดกราฟได้: {e}")

        render_steps(res["steps"])
    else:
        st.error(res["error"])
