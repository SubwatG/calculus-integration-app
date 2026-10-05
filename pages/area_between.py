"""pages/area_between.py — บทเรียน interactive: พื้นที่ระหว่างเส้นโค้ง (Area Between Curves)

คำนวณพื้นที่ปิดล้อมระหว่างสองฟังก์ชัน f(x) และ g(x) พร้อมแรเงากราฟและแสดงขั้นตอนวิธีทำ
"""

import streamlit as st

from utils.area_solver import compute_area_between
from utils.math_render import preview_math_expr, render_latex, render_syntax_guide, render_steps
from utils.plotter import plot_area_between
from utils.theme import render_hero
from utils.theory import THEORY_CONTENT

render_hero("พื้นที่ระหว่างเส้นโค้ง", "คำนวณพื้นที่ระหว่างเส้นโค้งสองเส้น")

if "area_f" not in st.session_state:
    st.session_state["area_f"] = "x"
if "area_g" not in st.session_state:
    st.session_state["area_g"] = "x**2"
if "area_a" not in st.session_state:
    st.session_state["area_a"] = 0.0
if "area_b" not in st.session_state:
    st.session_state["area_b"] = 1.0

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
    st.markdown("**แนวทางการตัดสินใจ**")
    st.info(theory["decision_guide"])

st.divider()
st.markdown("### ลองคำนวณ")

st.markdown("**ตัวอย่างโจทย์ยอดนิยม:**")
p_cols = st.columns(4)
if p_cols[0].button("เส้นตรงกับพาราโบลา ($x$ และ $x^2$)", key="pre_area_1"):
    st.session_state["area_f"] = "x"
    st.session_state["area_g"] = "x**2"
    st.session_state["area_a"] = 0.0
    st.session_state["area_b"] = 1.0
    st.rerun()
if p_cols[1].button("พาราโบลาคว่ำ-หงาย ($2-x^2$ และ $x^2$)", key="pre_area_2"):
    st.session_state["area_f"] = "2 - x**2"
    st.session_state["area_g"] = "x**2"
    st.session_state["area_a"] = -1.0
    st.session_state["area_b"] = 1.0
    st.rerun()
if p_cols[2].button("คลื่นตรีโกณมิติ ($\\cos(x)$ และ $x$)", key="pre_area_3"):
    st.session_state["area_f"] = "cos(x)"
    st.session_state["area_g"] = "x"
    st.session_state["area_a"] = 0.0
    st.session_state["area_b"] = 1.5
    st.rerun()
if p_cols[3].button("รากที่สาม ($x^{1/3}$ และ $x$)", key="pre_area_4"):
    st.session_state["area_f"] = "x**(1/3)"
    st.session_state["area_g"] = "x"
    st.session_state["area_a"] = -1.0
    st.session_state["area_b"] = 1.0
    st.rerun()

col_f, col_g = st.columns(2)
with col_f:
    f_input = st.text_input(
        "เส้นโค้ง f(x)",
        placeholder="เช่น x, x**2, sin(x), x**(1/3)",
        key="area_f",
    )
    preview_math_expr(f_input, label="พรีวิว f(x)")
with col_g:
    g_input = st.text_input(
        "เส้นโค้ง g(x)",
        placeholder="เช่น x**2, x - 1, 0",
        key="area_g",
    )
    preview_math_expr(g_input, label="พรีวิว g(x)")

render_syntax_guide()

col_a, col_b = st.columns(2)
with col_a:
    a_val = st.number_input("ขอบล่าง a", key="area_a")
with col_b:
    b_val = st.number_input("ขอบบน b", key="area_b")

if not f_input.strip() or not g_input.strip():
    st.info("กรุณาระบุฟังก์ชัน f(x) และ g(x) หรือคลิกเลือกตัวอย่างด้านบน")
else:
    res = compute_area_between(f_input, g_input, a_val, b_val)
    if res["ok"]:
        st.markdown("### ผลลัพธ์")
        render_latex(res["latex"])
        st.divider()

        st.markdown("### กราฟพื้นที่ระหว่างเส้นโค้ง")
        try:
            fig, ax = plot_area_between(res["f_expr"], res["g_expr"], a_val, b_val)
            st.pyplot(fig)
        except Exception as e:
            st.warning(f"ไม่สามารถวาดกราฟได้: {e}")

        render_steps(res["steps"])
    else:
        st.error(res["error"])
