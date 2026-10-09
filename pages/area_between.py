"""pages/area_between.py — บทเรียน interactive: พื้นที่ระหว่างเส้นโค้ง (Area Between Curves)

คำนวณพื้นที่ปิดล้อมระหว่างสองฟังก์ชัน f(x) และ g(x) พร้อมแรเงากราฟและแสดงขั้นตอนวิธีทำ
"""

import streamlit as st

from utils.area_solver import compute_area_between
from utils.math_render import preview_math_expr, render_latex, render_syntax_guide, render_steps
from utils.plotter import plot_area_between
from utils.theme import inject_css, render_hero
from utils.theory import THEORY_CONTENT

inject_css()
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

# ---------------------------------------------------------------------------
# Concept Anchor & What to Observe (มโนทัศน์หลักและจุดสังเกต)
# ---------------------------------------------------------------------------
with st.container(border=True):
    col_badge, col_concept = st.columns([1, 4])
    with col_badge:
        st.markdown(
            """<span style="
                background-color: #FEF08A;
                border: 1.5px solid #18181B;
                border-radius: 8px;
                padding: 4px 10px;
                font-family: 'Fredoka', 'Mali', sans-serif;
                font-size: 13px;
                font-weight: 700;
                color: #18181B;
                display: inline-block;
            ">🎯 มโนทัศน์หลัก</span>""",
            unsafe_allow_html=True,
        )
    with col_concept:
        st.markdown("**พื้นที่ระหว่างเส้นโค้งสองเส้น (Area Between Two Curves)**")

    st.markdown(
        "พื้นที่ระหว่างเส้นโค้งเกิดจากการอินทิเกรตผลต่างของความสูงแถบสี่เหลี่ยม: (เส้นโค้งบน ลบ เส้นโค้งล่าง) ตลอดช่วง $[a, b]$:"
    )

    st.latex(r"A = \int_a^b [f(x) - g(x)]\,dx \quad \left(\text{โดยที่ } f(x) \ge g(x) \text{ บนช่วง } [a, b]\right)")

    st.info(
        """**👁️ จุดที่ควรสังเกตขณะทดลองด้านล่าง:**
- **เส้นบน ลบ เส้นล่าง (Top minus Bottom):** ตรวจสอบให้มั่นใจว่า $f(x) \\ge g(x)$ ตลอดช่วง หากใส่สลับกัน ค่าพื้นที่ที่คำนวณได้จะติดลบ
- **จุดตัดของเส้นโค้ง ($f(x) = g(x)$):** ขอบเขต $a, b$ มักได้จากการแก้หาจุดตัด หากกราฟตัดกันสลับบน-ล่าง ต้องแยกอินทิเกรตทีละช่วง"""
    )

with st.expander("📖 รายละเอียดทฤษฎี ข้อควรระวัง และการประยุกต์ใช้เพิ่มเติม", expanded=False):
    col_t1, col_t2 = st.columns(2)
    with col_t1:
        st.markdown("**เงื่อนไขการใช้งาน**")
        for item in theory["conditions"]:
            st.markdown(f"- {item}")
        st.markdown("**สมบัติสำคัญ**")
        for item in theory["properties"]:
            st.markdown(f"- {item}")
    with col_t2:
        st.markdown("**ข้อควรระวัง**")
        st.warning(" / ".join(theory["cautions"]))
        st.markdown("**การประยุกต์ใช้**")
        for item in theory["applications"]:
            st.markdown(f"- {item}")

st.divider()
st.markdown("### ลองคำนวณ")

st.markdown("**ตัวอย่างโจทย์ยอดนิยม:**")

def _set_area_preset(f_val: str, g_val: str, a_val: float, b_val: float) -> None:
    st.session_state["area_f"] = f_val
    st.session_state["area_g"] = g_val
    st.session_state["area_a"] = a_val
    st.session_state["area_b"] = b_val

p_cols = st.columns(4)
with p_cols[0]:
    st.button("เส้นตรงกับพาราโบลา ($x$ และ $x^2$)", key="pre_area_1", use_container_width=True, wrap=True, on_click=_set_area_preset, args=("x", "x**2", 0.0, 1.0))
with p_cols[1]:
    st.button("พาราโบลาคว่ำ-หงาย ($2-x^2$ และ $x^2$)", key="pre_area_2", use_container_width=True, wrap=True, on_click=_set_area_preset, args=("2 - x**2", "x**2", -1.0, 1.0))
with p_cols[2]:
    st.button("คลื่นตรีโกณมิติ ($\cos(x)$ และ $x$)", key="pre_area_3", use_container_width=True, wrap=True, on_click=_set_area_preset, args=("cos(x)", "x", 0.0, 1.5))
with p_cols[3]:
    st.button("รากที่สาม ($x^{1/3}$ และ $x$)", key="pre_area_4", use_container_width=True, wrap=True, on_click=_set_area_preset, args=("x**(1/3)", "x", -1.0, 1.0))

col_f, col_g = st.columns(2)
with col_f:
    f_input = st.text_input(
        "เส้นโค้ง f(x)",
        value=st.session_state.get("area_f", "x"),
        placeholder="เช่น x, x**2, sin(x), x**(1/3)",
        key="area_f",
    )
    preview_math_expr(f_input, label="พรีวิว f(x)")
with col_g:
    g_input = st.text_input(
        "เส้นโค้ง g(x)",
        value=st.session_state.get("area_g", "x**2"),
        placeholder="เช่น x**2, x - 1, 0",
        key="area_g",
    )
    preview_math_expr(g_input, label="พรีวิว g(x)")

render_syntax_guide()

from utils.keypad import render_math_keypad
render_math_keypad(target_key="area_f", key_prefix="area_f_kp", title="แผงปุ่มลัดสัญลักษณ์คณิตศาสตร์ (พิมพ์ลงใน f(x))", expanded=False)

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
