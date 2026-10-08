"""pages/tangent.py : บทเรียน interactive: เส้นสัมผัสและอนุพันธ์ (Tangent Line and Derivative)

โครงสร้างตาม blueprint: pages/riemann.py
"""

import streamlit as st

from utils.keypad import render_math_keypad
from utils.math_render import preview_math_expr, render_latex, render_steps, render_syntax_guide
from utils.plotter import plot_tangent
from utils.tangent_solver import compute_tangent
from utils.theme import render_hero
from utils.theory import THEORY_CONTENT

render_hero("เส้นสัมผัสและอนุพันธ์", "สำรวจความชันเส้นสัมผัสและอนุพันธ์แบบโต้ตอบ")

theory = THEORY_CONTENT["tangent"]

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
        st.markdown("**ความชันเส้นสัมผัสและอนุพันธ์ (Secant Line Limit to Tangent Slope)**")

    st.markdown(
        "ความชันของเส้นสัมผัส ณ จุด $x = a$ คือลิมิตของความชันเส้นตัด (Secant Line) เมื่อจุดทั้งสองเคลื่อนเข้าหากันจนเป็นจุดเดียว ($h \\to 0$):"
    )

    st.latex(r"m = f'(a) = \lim_{h \to 0} \frac{f(a+h) - f(a)}{h} \quad \implies \text{สมการเส้นสัมผัส: } y - f(a) = f'(a)(x - a)")

    st.info(
        """**👁️ จุดที่ควรสังเกตขณะทดลองด้านล่าง:**
- **ทิศทางความชัน ($f'(a)$):** เลื่อนจุด $a$ สังเกตหาก $f'(a) > 0$ เส้นชันขึ้น, $f'(a) < 0$ เส้นลาดลง, และ $f'(a) = 0$ เส้นสัมผัสเป็นแนวนอน (จุดวกกลับ/จุดวิกฤต)
- **การแนบชิดเฉพาะที่ (Local Linearity):** ใกล้จุดสัมผัส เส้นตรงจะแนบสนิทไปกับเส้นโค้ง ซึ่งเป็นรากฐานของการประมาณค่าเชิงเส้น"""
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
st.markdown("### ลองสำรวจเส้นสัมผัส")

def _set_tangent_preset(expr_val: str, a_val: float) -> None:
    st.session_state["tangent_expr"] = expr_val
    st.session_state["tangent_a"] = a_val

st.caption("ตัวอย่างโจทย์ยอดนิยม:")
col_pre1, col_pre2, col_pre3, col_pre4 = st.columns(4)
with col_pre1:
    st.button("x^2", key="btn_tan_1", use_container_width=True, on_click=_set_tangent_preset, args=("x^2", 1.0))
with col_pre2:
    st.button("x^3 - 3x", key="btn_tan_2", use_container_width=True, on_click=_set_tangent_preset, args=("x^3 - 3*x", 0.0))
with col_pre3:
    st.button("sin(x)", key="btn_tan_3", use_container_width=True, on_click=_set_tangent_preset, args=("sin(x)", 0.0))
with col_pre4:
    st.button("sqrt(x+5)", key="btn_tan_4", use_container_width=True, on_click=_set_tangent_preset, args=("sqrt(x+5)", -1.0))

col_f, col_a = st.columns([2, 1])
with col_f:
    expr_input = st.text_input(
        "ฟังก์ชัน f(x)",
        value=st.session_state.get("tangent_expr", "x^2"),
        placeholder="เช่น x^2, sin(x), x^3 - 3*x",
        key="tangent_expr",
    )
    preview_math_expr(expr_input)
    render_syntax_guide()

with col_a:
    a_val = st.slider(
        "จุดสัมผัส a",
        min_value=-5.0,
        max_value=5.0,
        value=float(st.session_state.get("tangent_a", 1.0)),
        step=0.1,
        key="tangent_a",
    )

render_math_keypad(target_key="tangent_expr", key_prefix="tan_kp", expanded=False)

if not expr_input.strip():
    st.info("กรุณาระบุฟังก์ชัน f(x) หรือคลิกเลือกตัวอย่างด้านบน")
else:
    res = compute_tangent(expr_input, a_val)
    if res["ok"]:
        st.markdown("### ผลลัพธ์สมการเส้นสัมผัส")
        col_m1, col_m2 = st.columns([1, 2])
        with col_m1:
            status = res.get("status")
            if status == "finite" and res["result"] is not None:
                m_str = f"{res['result']:.4f}"
            elif status == "vertical":
                m_str = "∞ (แนวดิ่ง)"
            elif status == "non_differentiable":
                m_str = "ไม่มีค่า (DNE)"
            else:
                m_val = res["result"]
                m_str = f"{m_val:.4f}" if m_val is not None else "-"
            st.metric(label="ความชันเส้นสัมผัส m = f'(a)", value=m_str)
        with col_m2:
            render_latex(res["latex"])

        st.divider()
        try:
            fig, _ = plot_tangent(
                res["expr"],
                a_val,
                slope=res.get("result"),
                status=res.get("status", "finite"),
            )
            st.pyplot(fig)
        except Exception:
            st.warning("ไม่สามารถวาดกราฟได้ ตรวจสอบฟังก์ชันอีกครั้ง")

        st.divider()
        render_steps(res["steps"])
    else:
        st.error(res["error"])

