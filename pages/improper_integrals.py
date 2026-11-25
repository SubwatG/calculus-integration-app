"""pages/improper_integrals.py : บทเรียน interactive: ปริพันธ์ไม่ตรงแบบ (Improper Integrals)

สำรวจการลู่เข้าหรือลู่ออกของปริพันธ์บนช่วงอนันต์ พร้อมกราฟแรเงาและขั้นตอนการคำนวณลิมิต
"""

import streamlit as st

from utils.improper_solver import compute_improper
from utils.math_render import preview_math_expr, render_latex, render_syntax_guide, render_steps
from utils.plotter import plot_improper, plot_improper_plotly
from utils.riemann_solver import X
from utils.special_functions import describe_special_functions, numeric_approximation, special_functions_in
from utils.theme import inject_css, render_hero
from utils.theory import THEORY_CONTENT

inject_css()
render_hero("ปริพันธ์ไม่ตรงแบบ", "สำรวจการลู่เข้าหรือลู่ออกของปริพันธ์บนช่วงอนันต์และจุดที่ฟังก์ชันไม่ต่อเนื่อง")

# Responsive Table Styling Protection for Mobile
st.markdown(
    """
    <style>
    div[data-testid="stMarkdownContainer"]:has(table) {
        overflow-x: auto !important;
        -webkit-overflow-scrolling: touch !important;
        padding-bottom: 6px !important;
    }
    div[data-testid="stMarkdownContainer"] table {
        width: 100% !important;
        min-width: 520px !important;
        border-collapse: separate !important;
        border-spacing: 0 !important;
        border: 2px solid #18181B !important;
        border-radius: 12px !important;
        box-shadow: 3px 3px 0px #18181B !important;
        background-color: #FFFFFF !important;
        margin: 10px 0 16px 0 !important;
    }
    div[data-testid="stMarkdownContainer"] table th {
        background-color: #FEF08A !important;
        color: #18181B !important;
        font-weight: 700 !important;
        border-bottom: 2px solid #18181B !important;
        padding: 10px 14px !important;
        text-align: left !important;
    }
    div[data-testid="stMarkdownContainer"] table td {
        padding: 10px 14px !important;
        border-bottom: 1px solid #E4E4E7 !important;
        color: #18181B !important;
        vertical-align: middle !important;
    }
    div[data-testid="stMarkdownContainer"] table tr:last-child td {
        border-bottom: none !important;
    }
    div[data-testid="stMarkdownContainer"] table tr:hover {
        background-color: #FEF9C3 !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

theory = THEORY_CONTENT["improper"]

# ---------------------------------------------------------------------------
# Concept Anchor & What to Observe
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
            ">หลักการสำคัญ</span>""",
            unsafe_allow_html=True,
        )
    with col_concept:
        st.markdown("#### ปริพันธ์ไม่ตรงแบบและการลู่เข้า")

    st.latex(r"\int_a^\infty f(x)\,dx = \lim_{t \to \infty} \int_a^t f(x)\,dx \quad \left(\text{ถ้าลิมิตมีค่าจริง } \implies \text{ลู่เข้า}\right)")

    st.markdown(
        """
| ประเภทการพิจารณา | เงื่อนไขทางคณิตศาสตร์ | พฤติกรรมการลู่เข้า / ลู่ออก |
| :---: | :--- | :--- |
| ค่าของลิมิต | $\\lim_{t \\to \\infty} \\int_a^t f(x)\\,dx = L$ | มีค่าจริง = ลู่เข้า (Converges) / หาค่าไม่ได้ = ลู่ออก (Diverges) |
| การทดสอบด้วยปริพันธ์พี (p-Integral Test) | $\\int_1^\\infty \\frac{1}{x^p}\\,dx$ บนช่วง $[1, \\infty)$ | ลู่เข้าเมื่อ $p > 1$ และ ลู่ออกเมื่อ $p \\le 1$ |
        """
    )

st.divider()
st.markdown("### ลองคำนวณ")

def _set_improper_preset(expr_val: str, a_val: str, b_val: str) -> None:
    st.session_state["improper_expr"] = expr_val
    st.session_state["improper_a_str"] = a_val
    st.session_state["improper_b_str"] = b_val

st.markdown("**ตัวอย่างโจทย์:**")
p_cols = st.columns(4)
with p_cols[0]:
    st.button("$\\frac{1}{x^2}$ บน $[1, \\infty)$", key="pre_imp_1", use_container_width=True, on_click=_set_improper_preset, args=("1/x**2", "1", "inf"))
with p_cols[1]:
    st.button("$\\frac{1}{x}$ บน $[1, \\infty)$", key="pre_imp_2", use_container_width=True, on_click=_set_improper_preset, args=("1/x", "1", "inf"))
with p_cols[2]:
    st.button("$e^{-x}$ บน $[0, \\infty)$", key="pre_imp_3", use_container_width=True, on_click=_set_improper_preset, args=("exp(-x)", "0", "inf"))
with p_cols[3]:
    st.button("$\\frac{1}{1+x^2}$ บน $(-\\infty, \\infty)$", key="pre_imp_4", use_container_width=True, on_click=_set_improper_preset, args=("1/(1+x**2)", "-inf", "inf"))

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

st.caption("[คำแนะนำ] รองรับช่วงกึ่งอนันต์ [a, ∞), ช่วงสองฝั่ง (-∞, ∞), และช่วงจำกัด [a, b] ที่มีจุดที่ฟังก์ชันไม่ต่อเนื่องภายในช่วง")

if not expr_input.strip():
    st.info("กรุณาระบุฟังก์ชัน f(x) หรือคลิกเลือกตัวอย่างด้านบน")
else:
    res = compute_improper(expr_input, a_input, b_input)
    if res["ok"]:
        v_name = res.get("variable", "x")
        if v_name != "x":
            st.info(f"ตรวจพบตัวแปร **${v_name}$**: ระบบคำนวณและวาดกราฟเทียบกับตัวแปร ${v_name}$ อัตโนมัติ")

        st.markdown("### ผลลัพธ์")
        render_latex(res["latex"])
        special_names = special_functions_in(res.get("value_expr"))
        if special_names:
            st.info(describe_special_functions(special_names))
            approximation = numeric_approximation(res.get("value_expr"))
            if approximation is not None:
                st.caption(f"ค่าประมาณ: {approximation}")

        status = res.get("status")
        if status == "divergent":
            st.warning("ปริพันธ์นี้ลู่ออก ไม่ลู่เข้าสู่ค่าจำกัด")
        elif status == "unsupported":
            st.info("ยังไม่สามารถหาค่าปริพันธ์นี้ในรูปแบบปิดได้")

        st.divider()

        st.markdown("### กราฟการลู่เข้าและพื้นที่ใต้กราฟ")
        try:
            fig_plotly = plot_improper_plotly(res["expr"], a_input, b_input)
            st.plotly_chart(fig_plotly, use_container_width=True, config={"scrollZoom": True, "displayModeBar": True})
        except Exception as e:
            st.warning("แสดงผลกราฟ interactive ขัดข้อง กำลังสลับไปใช้กราฟสำรอง")
            try:
                fig, ax = plot_improper(res["expr"], a_input, b_input)
                st.pyplot(fig)
            except Exception as e2:
                st.warning(f"ไม่สามารถวาดกราฟได้: {e2}")

        render_steps(res["steps"])
    else:
        st.error(res["error"])
