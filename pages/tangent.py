"""pages/tangent.py — เส้นสัมผัสและอนุพันธ์ (skeleton)

TODO: ใส่ logic กราฟจริง (plot_tangent) ให้สมบูรณ์
อ้างอิง blueprint: pages/riemann.py
"""

import streamlit as st

from utils.math_render import render_latex, render_steps
from utils.plotter import plot_tangent
from utils.riemann_solver import X
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

st.divider()
st.markdown("### ลองคำนวณ")

expr_input = st.text_input(
    "ฟังก์ชัน f(x)",
    value="x**2",
    placeholder="เช่น x**2, sin(x), x**3 - 2*x",
    key="tangent_expr",
)
a_val = st.slider("จุด a", min_value=-5.0, max_value=5.0, value=1.0, step=0.1, key="tangent_a")

if st.button("คำนวณ", type="primary", key="btn_tangent_calc"):
    if not expr_input.strip():
        st.error("กรุณาใส่ฟังก์ชันก่อน")
    else:
        res = compute_tangent(expr_input, a_val)
        if res["ok"]:
            st.markdown("### ผลลัพธ์")
            render_latex(res["latex"])
            st.divider()
            # TODO: เรียก plot_tangent(res["expr"], a_val) แล้ว st.pyplot(fig)
            render_steps(res["steps"])
        else:
            st.error(res["error"])
