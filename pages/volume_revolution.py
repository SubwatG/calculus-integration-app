"""pages/volume_revolution.py — ปริมาตรของทรงตัน (skeleton)

TODO: ใส่ logic กราฟจริง (plot_volume) ให้สมบูรณ์
อ้างอิง blueprint: pages/riemann.py
"""

import streamlit as st

from utils.math_render import render_latex, render_steps
from utils.plotter import plot_volume
from utils.riemann_solver import X
from utils.theme import render_hero
from utils.theory import THEORY_CONTENT
from utils.volume_solver import compute_volume

render_hero("ปริมาตรของทรงตัน", "คำนวณปริมาตรแบบ disk และ washer")

theory = THEORY_CONTENT["volume"]

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
    "ฟังก์ชันรัศมี R(x)",
    value="x",
    placeholder="เช่น x, sqrt(x), x**2",
    key="volume_expr",
)
col_a, col_b = st.columns(2)
with col_a:
    a_val = st.number_input("ขอบล่าง a", value=0.0, key="volume_a")
with col_b:
    b_val = st.number_input("ขอบบน b", value=2.0, key="volume_b")
method_label = st.selectbox(
    "วิธีคำนวณ",
    ["disk", "washer"],
    key="volume_method",
)

st.caption("TODO: ถ้าเลือก washer ให้เพิ่มช่องฟังก์ชันรัศมีใน r(x)")

if st.button("คำนวณ", type="primary", key="btn_volume_calc"):
    if not expr_input.strip():
        st.error("กรุณาใส่ฟังก์ชันก่อน")
    else:
        res = compute_volume(expr_input, a_val, b_val, method_label)
        if res["ok"]:
            st.markdown("### ผลลัพธ์")
            render_latex(res["latex"])
            st.divider()
            # TODO: เรียก plot_volume(res["expr"], a_val, b_val, method_label) แล้ว st.pyplot(fig)
            render_steps(res["steps"])
        else:
            st.error(res["error"])
