"""pages/improper_integrals.py — บทเรียน interactive: ปริพันธ์ไม่ตรงแบบ (Improper Integrals)

สำรวจการลู่เข้าหรือลู่ออกของปริพันธ์บนช่วงอนันต์ พร้อมกราฟแรเงาและขั้นตอนการคำนวณลิมิต
"""

import streamlit as st

from utils.improper_solver import compute_improper
from utils.math_render import preview_math_expr, render_latex, render_syntax_guide, render_steps
from utils.plotter import plot_improper
from utils.riemann_solver import X
from utils.theme import inject_css, render_hero
from utils.theory import THEORY_CONTENT

inject_css()
render_hero("ปริพันธ์ไม่ตรงแบบ", "สำรวจการลู่เข้าหรือลู่ออกของปริพันธ์บนช่วงอนันต์และจุดเอกฐาน")

theory = THEORY_CONTENT["improper"]

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
        st.markdown("**ปริพันธ์ไม่ตรงแบบและการลู่เข้า (Improper Integrals & Limits)**")

    st.markdown(
        "การหาพื้นที่บนช่วงอนันต์หรือจุดที่ฟังก์ชันมีความไม่ต่อเนื่อง (จุดเอกฐาน) ต้องนิยามผ่านกระบวนการเทคลิมิตของ definite integral เสมอ:"
    )

    st.latex(r"\int_a^\infty f(x)\,dx = \lim_{t \to \infty} \int_a^t f(x)\,dx \quad \left(\text{ถ้าลิมิตมีค่าจริง } \implies \text{ลู่เข้า / Converges}\right)")

    st.info(
        """**👁️ จุดที่ควรสังเกตขณะทดลองด้านล่าง:**
- **การลู่เข้า vs ลู่ออก (Convergence vs Divergence):** สังเกตว่าเมื่อขอบเขตขยายสู่อนันต์ พื้นที่ใต้กราฟหยุดสะสมและคงที่ (ลู่เข้า) หรือโตขึ้นเรื่อย ๆ ไม่สิ้นสุด (ลู่ออก)
- **การทดสอบด้วยอันดับ ($p$-Integral Test):** บนช่วง $[1, \\infty)$ ฟังก์ชัน $\\frac{1}{x^p}$ จะลู่เข้าเมื่อ $p > 1$ และจะลู่ออกเมื่อ $p \\le 1$"""
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

def _set_improper_preset(expr_val: str, a_val: str, b_val: str) -> None:
    st.session_state["improper_expr"] = expr_val
    st.session_state["improper_a_str"] = a_val
    st.session_state["improper_b_str"] = b_val

st.markdown("**ตัวอย่างโจทย์ยอดนิยม:**")
p_cols = st.columns(4)
with p_cols[0]:
    st.button("กำลังสอง $\\frac{1}{x^2}$ บน $[1, \\infty)$", key="pre_imp_1", use_container_width=True, on_click=_set_improper_preset, args=("1/x**2", "1", "inf"))
with p_cols[1]:
    st.button("ฮาร์มอนิก $\\frac{1}{x}$ บน $[1, \\infty)$", key="pre_imp_2", use_container_width=True, on_click=_set_improper_preset, args=("1/x", "1", "inf"))
with p_cols[2]:
    st.button("เอกซ์โพเนนเชียล $e^{-x}$ บน $[0, \\infty)$", key="pre_imp_3", use_container_width=True, on_click=_set_improper_preset, args=("exp(-x)", "0", "inf"))
with p_cols[3]:
    st.button("สองฝั่งอนันต์ $\\frac{1}{1+x^2}$ บน $(-\\infty, \\infty)$", key="pre_imp_4", use_container_width=True, on_click=_set_improper_preset, args=("1/(1+x**2)", "-inf", "inf"))

expr_input = st.text_input(
    "ฟังก์ชัน f(x)",
    value=st.session_state.get("improper_expr", "1/x**2"),
    placeholder="เช่น 1/x**2, 1/x, 1/(1+x**2), exp(-x)",
    key="improper_expr",
)
preview_math_expr(expr_input)
render_syntax_guide()

from utils.keypad import render_math_keypad
render_math_keypad(target_key="improper_expr", key_prefix="imp_kp", expanded=False)

col_a, col_b = st.columns(2)
with col_a:
    a_input = st.text_input(
        "ขอบล่าง a (ใส่ตัวเลข, สัญลักษณ์ หรือ -inf)",
        value=st.session_state.get("improper_a_str", "1"),
        key="improper_a_str",
    )
with col_b:
    b_input = st.text_input(
        "ขอบบน b (ใส่ตัวเลข, สัญลักษณ์ หรือ inf)",
        value=st.session_state.get("improper_b_str", "inf"),
        key="improper_b_str",
    )

st.caption("[คำแนะนำ] รองรับช่วงกึ่งอนันต์ [a, ∞), ช่วงสองฝั่ง (-∞, ∞), และช่วงจำกัด [a, b] ที่มีจุดเอกฐานภายใน")

if not expr_input.strip():
    st.info("กรุณาระบุฟังก์ชัน f(x) หรือคลิกเลือกตัวอย่างด้านบน")
else:
    res = compute_improper(expr_input, a_input, b_input)
    if res["ok"]:
        st.markdown("### ผลลัพธ์")
        render_latex(res["latex"])

        status = res.get("status")
        if status == "divergent":
            st.warning("ปริพันธ์นี้ลู่ออก (Divergent) ไม่ลู่เข้าสู่ค่าจำกัด")
        elif status == "unsupported":
            st.info("ยังไม่สามารถหาค่าปริพันธ์นี้ในรูปแบบปิดได้")

        st.divider()

        st.markdown("### กราฟการลู่เข้าและพื้นที่ใต้กราฟ (Improper Integral Visualization)")
        try:
            fig, ax = plot_improper(res["expr"], a_input, b_input)
            st.pyplot(fig)
        except Exception as e:
            st.warning(f"ไม่สามารถวาดกราฟได้: {e}")

        render_steps(res["steps"])
    else:
        st.error(res["error"])
