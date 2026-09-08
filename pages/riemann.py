"""
pages/riemann.py : บทเรียน interactive: พื้นที่ภายใต้เส้นโค้ง (Riemann Sum)

ตัวอย่างบทเรียน interactive สำหรับนักศึกษา project
โครงสร้างตาม blueprint จาก stat-distribution-solver:
  - Theory panel (ซ่อน/แสดงได้)
  - Widget ให้ผู้เรียนปรับค่า
  - Solver ทีละขั้น (LaTeX)
  - กราฟแสดงสี่เหลี่ยมรีมันน์
"""

import sympy as sp
import streamlit as st

from utils.math_render import preview_math_expr, render_latex, render_steps, render_syntax_guide
from utils.plotter import plot_riemann
from utils.riemann_solver import METHODS, X, compute_riemann
from utils.theme import render_hero
from utils.theory import THEORY_CONTENT

render_hero("พื้นที่ภายใต้เส้นโค้ง", "สำรวจแนวคิดผลรวมรีมันน์ (Riemann Sum) แบบโต้ตอบ")

theory = THEORY_CONTENT["riemann_sum"]

# ---------------------------------------------------------------------------
# Theory panel (ซ่อน/แสดงได้)
# ---------------------------------------------------------------------------
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

# ---------------------------------------------------------------------------
# Input widgets
# ---------------------------------------------------------------------------
st.markdown("### ลองเล่นกับผลรวมรีมันน์")

st.caption("ตัวอย่างโจทย์ยอดนิยม:")
col_pre1, col_pre2, col_pre3, col_pre4 = st.columns(4)
with col_pre1:
    if st.button("x^2", key="btn_pre_1", use_container_width=True):
        st.session_state["riemann_expr"] = "x^2"
        st.rerun()
with col_pre2:
    if st.button("x^3 - 2x", key="btn_pre_2", use_container_width=True):
        st.session_state["riemann_expr"] = "x^3 - 2x"
        st.rerun()
with col_pre3:
    if st.button("sin(x)", key="btn_pre_3", use_container_width=True):
        st.session_state["riemann_expr"] = "sin(x)"
        st.rerun()
with col_pre4:
    if st.button("1/(x+1)", key="btn_pre_4", use_container_width=True):
        st.session_state["riemann_expr"] = "1/(x+1)"
        st.rerun()

col_f, col_m = st.columns([2, 1])
with col_f:
    expr_input = st.text_input(
        "ฟังก์ชัน f(x)",
        value="x^2",
        placeholder="เช่น x^2, sin(x), x^3 - 2x",
        key="riemann_expr",
    )
    preview_math_expr(expr_input)
    render_syntax_guide()
with col_m:
    method_label = st.selectbox(
        "วิธีคำนวณ",
        list(METHODS.keys()),
        format_func=lambda k: METHODS[k][0],
        key="riemann_method",
    )

col_a, col_b, col_n = st.columns(3)
with col_a:
    a_val = st.number_input("ขอบล่าง a", value=0.0, key="riemann_a")
with col_b:
    b_val = st.number_input("ขอบบน b", value=2.0, key="riemann_b")
with col_n:
    n_val = st.slider("จำนวนช่วง n", min_value=1, max_value=50, value=8, key="riemann_n")

# ---------------------------------------------------------------------------
# คำนวณและแสดงผลแบบโต้ตอบสด (Real-time Interactive Update)
# ---------------------------------------------------------------------------
if not expr_input.strip():
    st.info("กรุณาระบุฟังก์ชัน f(x) หรือคลิกเลือกตัวอย่างด้านบน")
else:
    res = compute_riemann(expr_input, a_val, b_val, n_val, method_label)

    if res["ok"]:
        st.markdown("### ผลลัพธ์การประมาณค่า")
        render_latex(res["latex"])
        st.divider()

        # กราฟ (ใช้ expr ที่ solver parse แล้ว กันปัญหา x undefined)
        try:
            expr = res["expr"]
            exact = sp.integrate(expr, (X, a_val, b_val))
            exact_val = float(exact)
            fig, _ = plot_riemann(expr, a_val, b_val, n_val, method_label, exact_val)
            st.pyplot(fig)
        except Exception:
            st.warning("ไม่สามารถวาดกราฟได้ ตรวจสอบฟังก์ชันอีกครั้ง")

        st.divider()
        render_steps(res["steps"])
    else:
        st.error(res["error"])
