"""pages/area_between.py — พื้นที่ระหว่างเส้นโค้ง (skeleton)

TODO: ใส่ logic กราฟจริง (plot_area_between) ให้สมบูรณ์
อ้างอิง blueprint: pages/riemann.py
"""

import streamlit as st

from utils.area_solver import compute_area_between
from utils.math_render import render_latex, render_steps
from utils.plotter import plot_area_between
from utils.theme import render_hero
from utils.theory import THEORY_CONTENT

render_hero("พื้นที่ระหว่างเส้นโค้ง", "คำนวณพื้นที่ระหว่างเส้นโค้งสองเส้น")

theory = THEORY_CONTENT["area_between"]

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

col_f, col_g = st.columns(2)
with col_f:
    f_input = st.text_input(
        "เส้นโค้งบน f(x)",
        value="x",
        placeholder="เช่น x, x**2, sin(x)",
        key="area_f",
    )
with col_g:
    g_input = st.text_input(
        "เส้นโค้งล่าง g(x)",
        value="x**2",
        placeholder="เช่น x**2, x - 1",
        key="area_g",
    )
col_a, col_b = st.columns(2)
with col_a:
    a_val = st.number_input("ขอบล่าง a", value=0.0, key="area_a")
with col_b:
    b_val = st.number_input("ขอบบน b", value=1.0, key="area_b")

if st.button("คำนวณ", type="primary", key="btn_area_calc"):
    if not f_input.strip() or not g_input.strip():
        st.error("กรุณาใส่ฟังก์ชันทั้งสองเส้นก่อน")
    else:
        res = compute_area_between(f_input, g_input, a_val, b_val)
        if res["ok"]:
            st.markdown("### ผลลัพธ์")
            render_latex(res["latex"])
            st.divider()
            # TODO: เรียก plot_area_between(f_expr, g_expr, a_val, b_val) แล้ว st.pyplot(fig)
            render_steps(res["steps"])
        else:
            st.error(res["error"])
