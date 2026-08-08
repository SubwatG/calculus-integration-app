"""pages/limit_approach.py — ลิมิตเข้าใกล้จุด (skeleton)

TODO: ใส่ logic กราฟจริง (plot_limit_near) ให้สมบูรณ์
อ้างอิง blueprint: pages/riemann.py
"""

import streamlit as st

from utils.limit_solver import compute_limit_near
from utils.math_render import render_latex, render_steps
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

expr_input = st.text_input(
    "ฟังก์ชัน f(x)",
    value="(x**2 - 4)/(x - 2)",
    placeholder="เช่น (x**2-4)/(x-2), sin(x)/x",
    key="limit_expr",
)
a_val = st.number_input("จุดที่ x เข้าใกล้ a", value=2.0, key="limit_a")

if st.button("คำนวณ", type="primary", key="btn_limit_calc"):
    if not expr_input.strip():
        st.error("กรุณาใส่ฟังก์ชันก่อน")
    else:
        res = compute_limit_near(expr_input, a_val)
        if res["ok"]:
            st.markdown("### ผลลัพธ์")
            render_latex(res["latex"])
            st.divider()
            # TODO: เรียก plot_limit_near(res["expr"], a_val) แล้ว st.pyplot(fig)
            render_steps(res["steps"])
        else:
            st.error(res["error"])
