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

from utils.math_render import render_latex, render_steps
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

col_f, col_m = st.columns([2, 1])
with col_f:
    expr_input = st.text_input(
        "ฟังก์ชัน f(x)",
        value="x**2",
        placeholder="เช่น x**2, sin(x), x**3 - 2*x",
        key="riemann_expr",
    )
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
# คำนวณ + แสดงผล
# ---------------------------------------------------------------------------
if st.button("คำนวณ", type="primary", key="btn_riemann_calc"):
    if not expr_input.strip():
        st.error("กรุณาใส่ฟังก์ชันก่อน")
    else:
        res = compute_riemann(expr_input, a_val, b_val, n_val, method_label)

        if res["ok"]:
            st.markdown("### ผลลัพธ์")
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
