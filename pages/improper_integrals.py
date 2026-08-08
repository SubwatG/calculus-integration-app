"""pages/improper_integrals.py — อินทิกรัลไม่แท้ (skeleton)

TODO: ใส่ logic กราฟจริง (plot_improper) ให้สมบูรณ์
อ้างอิง blueprint: pages/riemann.py
"""

import streamlit as st

from utils.improper_solver import compute_improper
from utils.math_render import render_latex, render_steps
from utils.plotter import plot_improper
from utils.riemann_solver import X
from utils.theme import render_hero
from utils.theory import THEORY_CONTENT

render_hero("อินทิกรัลไม่แท้", "ตรวจสอบการลู่เข้าของอินทิกรัลไม่แท้")

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

st.divider()
st.markdown("### ลองคำนวณ")

expr_input = st.text_input(
    "ฟังก์ชัน f(x)",
    value="1/x**2",
    placeholder="เช่น 1/x**2, 1/x, 1/sqrt(x)",
    key="improper_expr",
)
col_a, col_b = st.columns(2)
with col_a:
    a_val = st.number_input("ขอบล่าง a", value=1.0, key="improper_a")
with col_b:
    upper_type = st.selectbox("ขอบบน", ["อนันต์ (inf)", "จำนวนจำกัด"], key="improper_upper_type")
    b_val = None
    if upper_type.startswith("จำนวน"):
        b_val = st.number_input("ขอบบน b", value=2.0, key="improper_b")

st.caption("TODO: เพิ่มกรณีฟังก์ชันไม่ต่อเนื่องภายในช่วง (แยกอินทิกรัล)")

if st.button("คำนวณ", type="primary", key="btn_improper_calc"):
    if not expr_input.strip():
        st.error("กรุณาใส่ฟังก์ชันก่อน")
    else:
        res = compute_improper(expr_input, a_val, b_val)
        if res["ok"]:
            st.markdown("### ผลลัพธ์")
            render_latex(res["latex"])
            st.divider()
            # TODO: เรียก plot_improper(res["expr"], a_val, b_val) แล้ว st.pyplot(fig)
            render_steps(res["steps"])
        else:
            st.error(res["error"])
