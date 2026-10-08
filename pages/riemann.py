"""
pages/riemann.py : บทเรียน interactive: พื้นที่ภายใต้เส้นโค้ง (Riemann Sum)

ตัวอย่างบทเรียน interactive สำหรับนักศึกษา project
โครงสร้างตาม blueprint จาก stat-distribution-solver:
  - Theory panel (ซ่อน/แสดงได้)
  - Widget ให้ผู้เรียนปรับค่า
  - Solver ทีละขั้น (LaTeX)
  - กราฟแสดงสี่เหลี่ยมรีมันน์
"""

import sympy as sp
import streamlit as st

from utils.math_render import preview_math_expr, render_latex, render_steps, render_syntax_guide
from utils.plotter import plot_riemann
from utils.riemann_solver import METHODS, X, compute_riemann
from utils.theme import render_hero
from utils.theory import THEORY_CONTENT

render_hero("พื้นที่ภายใต้เส้นโค้ง", "สำรวจแนวคิดผลรวมรีมันน์ (Riemann Sum) แบบโต้ตอบ")

theory = THEORY_CONTENT["riemann_sum"]

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
        st.markdown("**การประมาณพื้นที่ใต้กราฟสู่ค่าอินทิกรัลจริง (Riemann Sum to Definite Integral)**")

    st.markdown(
        "พื้นที่ใต้กราฟคำนวณจากผลรวมของพื้นที่แท่งสี่เหลี่ยมผืนผ้า $n$ แท่ง เมื่อซอยย่อยให้ละเอียดไม่สิ้นสุด ($n \\to \\infty$):"
    )

    st.latex(r"A = \lim_{n \to \infty} \sum_{i=1}^{n} f(x_i^*) \Delta x = \int_a^b f(x)\,dx \quad \left(\text{โดยที่ } \Delta x = \frac{b-a}{n}\right)")

    st.info(
        """**👁️ จุดที่ควรสังเกตขณะทดลองด้านล่าง:**
- **การลู่เข้า (Convergence):** ลองเลื่อนสไลเดอร์เพิ่ม $n$ สังเกตช่องว่างส่วนเกิน/ส่วนขาดจะเล็กลงจนผลรวมเข้าใกล้ค่าจริง
- **ทิศทางการประมาณ:** สำหรับฟังก์ชันเพิ่ม ($f' > 0$) ค่า $L_n$ จะประเมินต่ำกว่าจริง (Underestimate) ส่วน $R_n$ จะประเมินสูงกว่าจริง (Overestimate)"""
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

# ---------------------------------------------------------------------------
# Input widgets
# ---------------------------------------------------------------------------
st.markdown("### ลองเล่นกับผลรวมรีมันน์")

def _set_riemann_preset(expr_val: str) -> None:
    st.session_state["riemann_expr"] = expr_val

st.caption("ตัวอย่างโจทย์ยอดนิยม:")
col_pre1, col_pre2, col_pre3, col_pre4 = st.columns(4)
with col_pre1:
    st.button("x^2", key="btn_pre_1", use_container_width=True, on_click=_set_riemann_preset, args=("x^2",))
with col_pre2:
    st.button("x^3 - 2x", key="btn_pre_2", use_container_width=True, on_click=_set_riemann_preset, args=("x^3 - 2x",))
with col_pre3:
    st.button("sin(x)", key="btn_pre_3", use_container_width=True, on_click=_set_riemann_preset, args=("sin(x)",))
with col_pre4:
    st.button("1/(x+1)", key="btn_pre_4", use_container_width=True, on_click=_set_riemann_preset, args=("1/(x+1)",))

col_f, col_m = st.columns([2, 1])
with col_f:
    expr_input = st.text_input(
        "ฟังก์ชัน f(x)",
        value=st.session_state.get("riemann_expr", "x^2"),
        placeholder="เช่น x^2, sin(x), x^3 - 2x",
        key="riemann_expr",
    )
    preview_math_expr(expr_input)
    render_syntax_guide()
with col_m:
    method_label = st.selectbox(
        "วิธีคำนวณ",
        list(METHODS.keys()),
        format_func=lambda k: METHODS[k][0],
        key="riemann_method",
    )

from utils.keypad import render_math_keypad
render_math_keypad(target_key="riemann_expr", key_prefix="rie_kp", expanded=False)

col_a, col_b, col_n = st.columns(3)
with col_a:
    a_val = st.number_input("ขอบล่าง a", value=0.0, key="riemann_a")
with col_b:
    b_val = st.number_input("ขอบบน b", value=2.0, key="riemann_b")
with col_n:
    n_val = st.slider("จำนวนช่วง n", min_value=1, max_value=50, value=8, key="riemann_n")

# ---------------------------------------------------------------------------
# คำนวณและแสดงผลแบบโต้ตอบสด (Real-time Interactive Update)
# ---------------------------------------------------------------------------
if not expr_input.strip():
    st.info("กรุณาระบุฟังก์ชัน f(x) หรือคลิกเลือกตัวอย่างด้านบน")
else:
    res = compute_riemann(expr_input, a_val, b_val, n_val, method_label)

    if res["ok"]:
        st.markdown("### ผลลัพธ์การประมาณค่า")
        render_latex(res["latex"])
        st.divider()

        # กราฟ (ใช้ expr ที่ solver parse แล้ว กันปัญหา x undefined)
        try:
            expr = res["expr"]
            exact = sp.integrate(expr, (X, a_val, b_val))
            exact_val = float(exact)
            fig, _ = plot_riemann(expr, a_val, b_val, n_val, method_label, exact_val)
            st.pyplot(fig)
        except Exception:
            st.warning("ไม่สามารถวาดกราฟได้ ตรวจสอบฟังก์ชันอีกครั้ง")

        st.divider()
        render_steps(res["steps"])
    else:
        st.error(res["error"])
