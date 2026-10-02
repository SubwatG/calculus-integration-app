"""pages/volume_revolution.py — บทเรียน interactive: ปริมาตรของทรงตันที่เกิดจากการหมุน (Volume of Solids)

คำนวณปริมาตรแบบ Disk Method พร้อมพล็อตภาพตัดขวางและการหมุนรอบแกน
"""

import streamlit as st

from utils.math_render import preview_math_expr, render_latex, render_syntax_guide, render_steps
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
    st.markdown("**แนวทางการตัดสินใจ**")
    st.info(theory["decision_guide"])

st.divider()
st.markdown("### ลองคำนวณ")

st.markdown("**ตัวอย่างโจทย์ยอดนิยม:**")
p_cols = st.columns(3)
if p_cols[0].button("ทรงกรวย $R(x) = x$ บน $[0, 2]$", key="pre_vol_1"):
    st.session_state["volume_expr"] = "x"
    st.session_state["volume_a"] = 0.0
    st.session_state["volume_b"] = 2.0
    st.rerun()
if p_cols[1].button("พาราโบลอยด์ $R(x) = \\sqrt{x}$ บน $[0, 4]$", key="pre_vol_2"):
    st.session_state["volume_expr"] = "sqrt(x)"
    st.session_state["volume_a"] = 0.0
    st.session_state["volume_b"] = 4.0
    st.rerun()
if p_cols[2].button("ทรงระฆังคว่ำ $R(x) = 4 - x^2$ บน $[0, 2]$", key="pre_vol_3"):
    st.session_state["volume_expr"] = "4 - x**2"
    st.session_state["volume_a"] = 0.0
    st.session_state["volume_b"] = 2.0
    st.rerun()

expr_input = st.text_input(
    "ฟังก์ชันรัศมี R(x)",
    value="x",
    placeholder="เช่น x, sqrt(x), x**2",
    key="volume_expr",
)
preview_math_expr(expr_input, label="พรีวิว R(x)")
render_syntax_guide()

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

st.caption("[คำแนะนำ] ปัจจุบันรองรับการคำนวณแบบ Disk Method รอบแกน x (y = 0)")

if not expr_input.strip():
    st.info("กรุณาระบุฟังก์ชัน R(x) หรือคลิกเลือกตัวอย่างด้านบน")
else:
    res = compute_volume(expr_input, a_val, b_val, method_label)
    if res["ok"]:
        st.markdown("### ผลลัพธ์")
        render_latex(res["latex"])
        st.divider()

        st.markdown("### ภาพตัดขวางทรงตันและการหมุนรอบแกน")
        try:
            fig, ax = plot_volume(res["expr"], a_val, b_val, method_label)
            st.pyplot(fig)
        except Exception as e:
            st.warning(f"ไม่สามารถวาดกราฟได้: {e}")

        render_steps(res["steps"])
    else:
        st.error(res["error"])
