"""pages/tangent.py : บทเรียน interactive: เส้นสัมผัสและอนุพันธ์ (Tangent Line and Derivative)

โครงสร้างตาม blueprint: pages/riemann.py
"""

import streamlit as st

from utils.math_render import preview_math_expr, render_latex, render_steps, render_syntax_guide
from utils.plotter import plot_tangent
from utils.tangent_solver import compute_tangent
from utils.theme import render_hero
from utils.theory import THEORY_CONTENT

render_hero("เส้นสัมผัสและอนุพันธ์", "สำรวจความชันเส้นสัมผัสและอนุพันธ์แบบโต้ตอบ")

theory = THEORY_CONTENT["tangent"]

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
st.markdown("### ลองสำรวจเส้นสัมผัสและอนุพันธ์")

st.caption("ตัวอย่างโจทย์ยอดนิยม:")
col_pre1, col_pre2, col_pre3, col_pre4 = st.columns(4)
with col_pre1:
    if st.button("x^2", key="btn_tan_1", use_container_width=True):
        st.session_state["tangent_expr"] = "x^2"
        st.session_state["tangent_a"] = 1.0
        st.rerun()
with col_pre2:
    if st.button("x^3 - 3x", key="btn_tan_2", use_container_width=True):
        st.session_state["tangent_expr"] = "x^3 - 3*x"
        st.session_state["tangent_a"] = 0.0
        st.rerun()
with col_pre3:
    if st.button("sin(x)", key="btn_tan_3", use_container_width=True):
        st.session_state["tangent_expr"] = "sin(x)"
        st.session_state["tangent_a"] = 0.0
        st.rerun()
with col_pre4:
    if st.button("sqrt(x+5)", key="btn_tan_4", use_container_width=True):
        st.session_state["tangent_expr"] = "sqrt(x+5)"
        st.session_state["tangent_a"] = -1.0
        st.rerun()

col_f, col_a = st.columns([2, 1])
with col_f:
    expr_input = st.text_input(
        "ฟังก์ชัน f(x)",
        value="x^2",
        placeholder="เช่น x^2, sin(x), x^3 - 3*x",
        key="tangent_expr",
    )
    preview_math_expr(expr_input)
    render_syntax_guide()

with col_a:
    a_val = st.slider(
        "จุดสัมผัส a",
        min_value=-5.0,
        max_value=5.0,
        value=1.0,
        step=0.1,
        key="tangent_a",
    )

if not expr_input.strip():
    st.info("กรุณาระบุฟังก์ชัน f(x) หรือคลิกเลือกตัวอย่างด้านบน")
else:
    res = compute_tangent(expr_input, a_val)
    if res["ok"]:
        st.markdown("### ผลลัพธ์สมการเส้นสัมผัส")
        col_m1, col_m2 = st.columns([1, 2])
        with col_m1:
            m_val = res["result"]
            m_str = f"{m_val:.4f}" if m_val is not None else "-"
            st.metric(label="ความชันเส้นสัมผัส m = f'(a)", value=m_str)
        with col_m2:
            render_latex(res["latex"])

        st.divider()
        try:
            fig, _ = plot_tangent(res["expr"], a_val)
            st.pyplot(fig)
        except Exception:
            st.warning("ไม่สามารถวาดกราฟได้ ตรวจสอบฟังก์ชันอีกครั้ง")

        st.divider()
        render_steps(res["steps"])
    else:
        st.error(res["error"])

