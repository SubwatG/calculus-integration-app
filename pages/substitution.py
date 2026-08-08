"""pages/substitution.py — การอินทิเกรตโดยการแทน (skeleton)

TODO: ใส่ logic กราฟจริง (plot_substitution) ถ้าจำเป็น
อ้างอิง blueprint: pages/riemann.py
"""

import streamlit as st

from utils.math_render import render_latex, render_steps
from utils.plotter import plot_substitution
from utils.substitution_solver import solve_substitution
from utils.theme import render_hero
from utils.theory import THEORY_CONTENT

render_hero("การอินทิเกรตโดยการแทน", "ฝึกตั้ง u หา du และแทนค่ากลับทีละขั้น")

theory = THEORY_CONTENT["substitution"]

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

expr_input = st.text_input(
    "อินทิกรัล f(g(x))·g'(x)",
    value="2*x*exp(x**2)",
    placeholder="เช่น 2*x*exp(x**2), 3*x**2*cos(x**3)",
    key="substitution_expr",
)

st.caption("TODO: เพิ่ม widget ที่จำเป็น (เช่น ตัวเลือกให้ผู้เรียนเดา u ก่อนเฉลย)")

if st.button("คำนวณ", type="primary", key="btn_substitution_calc"):
    if not expr_input.strip():
        st.error("กรุณาใส่นิพจน์ก่อน")
    else:
        res = solve_substitution(expr_input)
        if res["ok"]:
            st.markdown("### ผลลัพธ์")
            render_latex(res["latex"])
            st.divider()
            # TODO: เรียก plot_substitution(res["expr"]) แล้ว st.pyplot(fig)
            render_steps(res["steps"])
        else:
            st.error(res["error"])
