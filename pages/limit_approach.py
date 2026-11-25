"""pages/limit_approach.py : บทเรียน interactive: ลิมิตเข้าใกล้จุด (Limit at a Point)

โครงสร้างตาม blueprint: pages/riemann.py

ลำดับการนำเสนอ (ปรับใหม่):
  1) ทดลองสำรวจก่อน : ใส่ฟังก์ชัน/จุด a/ระยะ delta แล้วเห็นผลลัพธ์ กราฟ ตารางตัวเลข และวิธีทำทันที
  2) จึงตามด้วยทฤษฎีและแนวคิดแบบย่อ (รายละเอียดทั้งหมดอยู่ใน expander ที่ตั้งชื่อชัดเจน)
"""

import numpy as np
import streamlit as st
import sympy as sp

from utils.keypad import render_math_keypad
from utils.limit_solver import compute_limit_near
from utils.math_render import (
    preview_math_expr,
    render_latex,
    render_steps,
    render_syntax_guide,
)
from utils.plotter import plot_limit_near, plot_limit_plotly
from utils.riemann_solver import X
from utils.theme import render_hero
from utils.theory import THEORY_CONTENT

render_hero("ลิมิตเข้าใกล้จุด", "สำรวจค่าลิมิตสองด้านและการลู่เข้าเมื่อ x เข้าใกล้จุด a")

theory = THEORY_CONTENT["limit"]


def _set_target_point(val: str) -> None:
    st.session_state["limit_a_str"] = val


def _set_limit_preset(expr_val: str, a_val: str) -> None:
    st.session_state["limit_expr"] = expr_val
    st.session_state["limit_a_str"] = a_val


def _function_undefined_at_a(res: dict) -> bool:
    """True only when f(a) is provably undefined (nan/zoo); never guessed.

    Used to label a removable discontinuity (a hole); it is not used to infer the
    solving method.
    """
    expr = res.get("expr")
    a_sp = res.get("a_sp")
    var_name = res.get("variable", "x")
    if expr is None or a_sp is None or a_sp in (sp.oo, -sp.oo):
        return False
    try:
        value = expr.subs(sp.Symbol(var_name), a_sp)
        return bool(value.has(sp.nan, sp.zoo))
    except Exception:
        return False


def _one_sided_limit_str(value) -> str | None:
    """Short unicode label for a one-sided limit value, or None when unknown."""
    if value is None:
        return None
    if value == sp.oo:
        return "+∞"
    if value == -sp.oo:
        return "-∞"
    try:
        if getattr(value, "is_finite", None) is True and getattr(value, "is_real", None) is True:
            return f"{float(value):.4f}"
    except Exception:
        return None
    return None


def _short_case_feedback(res: dict) -> tuple[str, str]:
    """Short per-case summary built only from fields the solver actually reports.

    Deliberately avoids inventing a method: a finite limit is not assumed to come
    from substitution/algebra (it may be an end-behaviour limit or a transcendental
    value); an "infinite" status is not assumed to come from a vanishing denominator;
    and a "dne" is not assumed to come from unequal one-sided values, because
    oscillation also yields "dne".

    Returns (level, text) where level is one of success/info/warning.
    """
    status = res.get("status")
    result = res.get("result")

    if status == "finite" and result is not None:
        if res.get("is_infinite"):
            return "success", (
                "**สรุป:** เมื่อตัวแปรมีขนาดใหญ่ขึ้นเรื่อย ๆ "
                f"ค่าฟังก์ชันลู่เข้าสู่ค่าคงที่ {result:.4f}"
            )
        if _function_undefined_at_a(res):
            return "success", (
                f"**สรุป:** ค่าลิมิตเท่ากับ {result:.4f} "
                "แม้ฟังก์ชันไม่นิยามที่จุด a "
                "ลิมิตจึงไม่ขึ้นกับค่าของฟังก์ชันที่จุดนั้น"
            )
        return "success", f"**สรุป:** ค่าลิมิตเท่ากับ {result:.4f}"

    if status == "infinite":
        if res.get("is_infinite"):
            return "warning", (
                "**สรุป:** เมื่อตัวแปรมีขนาดใหญ่ขึ้นเรื่อย ๆ "
                "ค่าฟังก์ชันลู่ออกอย่างไม่มีขอบเขต จึงไม่มีค่าลิมิตเป็นจำนวนจริง"
            )
        return "warning", (
            "**สรุป:** ค่าฟังก์ชันลู่ออกสู่อนันต์ทั้งสองฝั่งเมื่อเข้าใกล้จุด a "
            "(เส้นกำกับแนวดิ่ง) ลิมิตจึงไม่เป็นจำนวนจริง"
        )

    if status == "dne":
        if res.get("is_oscillating"):
            return "warning", (
                "**สรุป:** ค่าฟังก์ชันแกว่งกวัดไม่หยุดนิ่งเมื่อเข้าใกล้จุดนี้ "
                "จึงไม่ลู่เข้าหาค่าใดค่าหนึ่ง ลิมิตหาค่าไม่ได้"
            )
        left_s = _one_sided_limit_str(res.get("left_limit"))
        right_s = _one_sided_limit_str(res.get("right_limit"))
        if left_s is not None and right_s is not None:
            return "warning", (
                f"**สรุป:** ลิมิตทางซ้าย ({left_s}) "
                f"ไม่เท่ากับลิมิตทางขวา ({right_s}) ลิมิตสองด้านจึงหาค่าไม่ได้"
            )
        return "warning", "**สรุป:** ลิมิตสองด้านหาค่าไม่ได้"

    if status == "right_only":
        return "info", (
            "**สรุป:** ฟังก์ชันไม่นิยามทางซ้ายของจุดนี้ จึงพิจารณาเฉพาะลิมิตทางขวา"
        )
    if status == "left_only":
        return "info", (
            "**สรุป:** ฟังก์ชันไม่นิยามทางขวาของจุดนี้ จึงพิจารณาเฉพาะลิมิตทางซ้าย"
        )
    return "info", "**สรุป:** ระบบยังสรุปค่าไม่ได้ ต้องพิจารณาเพิ่มเติม"


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


# ---------------------------------------------------------------------------
# 1) Key theorems and principles (displayed openly)
# ---------------------------------------------------------------------------
st.divider()
st.markdown("### ทฤษฎีบทและหลักการสำคัญ")

with st.container(border=True):
    col_badge, col_title = st.columns([1, 4])
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
            ">ลำดับ 3 ขั้น</span>""",
            unsafe_allow_html=True,
        )
    with col_title:
        st.markdown("#### ลำดับการพิจารณาหาลิมิต 3 ขั้น")

    st.markdown(
        """
| ขั้นตอน | รูปแบบฟังก์ชัน | แนวทางการพิจารณาและคำนวณ |
| :---: | :--- | :--- |
| 1. ลองแทนค่าตรง | พหุนาม / ฟังก์ชันต่อเนื่อง ณ จุดนั้น | แทน $x = a$ ถ้าได้ค่าจริง $f(a) = L$ สรุปค่าลิมิตได้ทันที (เช่น พหุนาม, $\\sin x$, $\\cos x$ ซึ่งต่อเนื่องบน $\\mathbb{R}$) |
| 2. จัดรูปพีชคณิต | รูปแบบยังไม่กำหนด $\\frac{0}{0}$ | แยกตัวประกอบ, คูณสังยุค หรือใช้เอกลักษณ์ $\\lim_{x \\to 0} \\frac{\\sin x}{x} = 1$ |
| 3. แยกพิจารณาสองด้าน | ค่าสัมบูรณ์ / ตัวส่วนลู่เข้าศูนย์ | คำนวณลิมิตซ้าย ($x \\to a^-$) และลิมิตขวา ($x \\to a^+$) เพื่อดูเครื่องหมาย |
        """
    )
    st.latex(r"\lim_{x \to a} f(x) = L \iff \lim_{x \to a^-} f(x) = \lim_{x \to a^+} f(x) = L")

with st.expander("อ่านรายละเอียดทฤษฎี ข้อสังเกต และหัวใจสำคัญของการมีลิมิตสองด้าน", expanded=False):
    st.markdown(
        """
1. **ลองแทนค่าตรงก่อน:** แทน $x = a$ ใน $f(x)$ ถ้าได้ค่าจริง $f(a) = L$ สรุป $\\lim_{x \\to a} f(x) = L$ ทันที (ใช้ได้กับพหุนามและฟังก์ชันต่อเนื่อง ณ จุดนั้น)
2. **ถ้าแทนค่าแล้วติดรูปแบบยังไม่กำหนด $\\frac{0}{0}$:** ยังสรุปค่าไม่ได้ ต้องจัดรูปพีชคณิตก่อนแล้วแทนค่าใหม่ (ไม่ได้หมายความว่าค่าฟังก์ชันหาค่าไม่ได้เสมอไป) เช่น แยกตัวประกอบแล้วตัดทอน คูณสังยุค หรือใช้ $\\lim_{x \\to 0} \\frac{\\sin x}{x} = 1$
3. **เมื่อพฤติกรรมสองฝั่งของจุด a ทำงานต่างกัน:** จึงค่อยแยกพิจารณาลิมิตซ้าย ($x \\to a^-$) และขวา ($x \\to a^+$) เช่น กรณีค่าสัมบูรณ์ ฟังก์ชันแบ่งช่วง หรือกรณีตัวส่วนลู่เข้าศูนย์ (รูป $\\frac{c}{0}$ เมื่อ $c \\neq 0$) เพื่อดูเครื่องหมาย
        """
    )
    st.markdown("#### หัวใจสำคัญของการมีลิมิตสองด้าน")
    st.markdown(
        """
- **นิยามการมีลิมิต:** $\\lim_{x \\to a} f(x) = L$ มีค่าได้ ก็ต่อเมื่อ ลิมิตซ้ายเท่ากับลิมิตขวา
- **พฤติกรรมรอบจุด ไม่ใช่ที่จุด:** ลิมิตพิจารณาค่าที่ฟังก์ชัน **วิ่งเข้าหา** เมื่อ $x$ เข้าใกล้ $a$ ไม่ได้ขึ้นกับว่าที่จุด $x = a$ ฟังก์ชันมีค่าหรือไม่ (ตรงจุดนั้นฟังก์ชันอาจไม่นิยาม แต่ลิมิตอาจหาค่าได้)
- **ลิมิตที่อนันต์ ($x \\to \\pm\\infty$):** ศึกษาแนวโน้มเมื่อ $x$ เพิ่มขึ้นไม่สิ้นสุด หากลู่เข้าหาค่าคงที่ $L$ เส้นตรง $y = L$ จะเป็นเส้นกำกับแนวนอน
        """
    )

# ---------------------------------------------------------------------------
# 2) Interactive exploration
# ---------------------------------------------------------------------------
st.markdown("### ลองสำรวจการลู่เข้าของลิมิต")
st.caption("ตัวอย่างโจทย์")
col_pre1, col_pre2, col_pre3, col_pre4, col_pre5, col_pre6 = st.columns(6)
with col_pre1:
    st.button(
        "3x + 1 (x -> 2)",
        key="btn_lim_1",
        use_container_width=True,
        on_click=_set_limit_preset,
        args=("3*x + 1", "2"),
    )
with col_pre2:
    st.button(
        "(x² - 4)/(x - 2) (x -> 2)",
        key="btn_lim_2",
        use_container_width=True,
        on_click=_set_limit_preset,
        args=("(x**2 - 4)/(x - 2)", "2"),
    )
with col_pre3:
    st.button(
        "sin(x)/x (x -> 0)",
        key="btn_lim_3",
        use_container_width=True,
        on_click=_set_limit_preset,
        args=("sin(x)/x", "0"),
    )
with col_pre4:
    st.button(
        "1/x (x -> 0)",
        key="btn_lim_4",
        use_container_width=True,
        on_click=_set_limit_preset,
        args=("1/x", "0"),
    )
with col_pre5:
    st.button(
        "|x|/x (x -> 0)",
        key="btn_lim_5",
        use_container_width=True,
        on_click=_set_limit_preset,
        args=("abs(x)/x", "0"),
    )
with col_pre6:
    st.button(
        "(2x² + 1)/(3x² - 5) (x -> ∞)",
        key="btn_lim_6",
        use_container_width=True,
        on_click=_set_limit_preset,
        args=("(2*x**2 + 1)/(3*x**2 - 5)", "inf"),
    )

col_f, col_a = st.columns([2.4, 1.6])
with col_f:
    expr_input = st.text_input(
        "ฟังก์ชัน f(x)",
        value=st.session_state.get("limit_expr", "(x**2 - 4)/(x - 2)"),
        placeholder="เช่น 3*x+1, (x**2-4)/(x-2), sin(x)/x, 1/x, abs(x)/x",
        key="limit_expr",
    )
    preview_math_expr(expr_input)
    render_syntax_guide()

with col_a:
    a_input = st.text_input(
        "จุดที่ x เข้าใกล้ a",
        value=st.session_state.get("limit_a_str", "2"),
        placeholder="เช่น 2, 0, pi/2, e, inf, -inf",
        key="limit_a_str",
    )
    st.caption("จุดยอดนิยม:")
    r1_cols = st.columns(4)
    row1 = [("0", "0"), ("1", "1"), ("2", "2"), ("π", "pi")]
    for idx, (p_lbl, p_val) in enumerate(row1):
        with r1_cols[idx]:
            st.button(
                p_lbl,
                key=f"chip_a1_{idx}",
                use_container_width=True,
                on_click=_set_target_point,
                args=(p_val,),
            )

    r2_cols = st.columns(4)
    row2 = [("π/2", "pi/2"), ("e", "e"), ("∞", "inf"), ("-∞", "-inf")]
    for idx, (p_lbl, p_val) in enumerate(row2):
        with r2_cols[idx]:
            st.button(
                p_lbl,
                key=f"chip_a2_{idx}",
                use_container_width=True,
                on_click=_set_target_point,
                args=(p_val,),
            )

s_a_clean = str(a_input).strip().lower().replace(" ", "")
is_inf_target = s_a_clean in ("inf", "+inf", "-inf", "oo", "+oo", "-oo")

delta_val = 0.4

# Math Keypad Reusable Component
render_math_keypad(target_key="limit_expr", key_prefix="lim_kp", expanded=False)

if not expr_input.strip():
    st.info("กรุณาระบุฟังก์ชัน f(x) หรือคลิกเลือกตัวอย่างด้านบน")
else:
    res = compute_limit_near(expr_input, a_input)
    if res["ok"]:
        v_name = res.get("variable", "x")
        var_sym = sp.Symbol(v_name)

        st.markdown("### ผลลัพธ์ลิมิต")
        col_m1, col_m2 = st.columns([1, 2])
        with col_m1:
            status = res.get("status")
            if status == "finite" and res["result"] is not None:
                l_str = f"{res['result']:.4f}"
            elif status == "infinite":
                l_str = "∞ (อนันต์)"
            elif status == "dne":
                l_str = "ลิมิตหาค่าไม่ได้"
            elif status == "unsupported":
                l_str = "ยังตัดสินไม่ได้"
            else:
                lim_val = res["result"]
                l_str = f"{lim_val:.4f}" if lim_val is not None else "หาค่าไม่ได้"
            st.metric(label="ค่าลิมิต L", value=l_str)
        with col_m2:
            render_latex(res["latex"])

        # Concise summary per case (with limit value) placed near result
        feedback_kind, feedback_text = _short_case_feedback(res)
        if feedback_kind == "success":
            st.success(feedback_text)
        elif feedback_kind == "warning":
            st.warning(feedback_text)
        else:
            st.info(feedback_text)

        # Plot placed next to delta control for immediate feedback
        st.markdown("### กราฟการเข้าใกล้ลิมิต")
        try:
            fig_plotly = plot_limit_plotly(res["expr"], a_input, delta=delta_val)
            st.plotly_chart(fig_plotly, use_container_width=True, config={"scrollZoom": True, "displayModeBar": True})
        except Exception as e:
            st.warning("แสดงผลกราฟ interactive ขัดข้อง กำลังสลับไปใช้กราฟสำรอง")
            try:
                fig, _ = plot_limit_near(res["expr"], a_input, delta=delta_val)
                st.pyplot(fig)
            except Exception as e2:
                st.warning(f"ไม่สามารถวาดกราฟได้: {e2}")

        # -------------------------------------------------------------
        # Worked solution: display steps immediately without collapsing
        # -------------------------------------------------------------
        render_steps(res["steps"])
    else:
        st.error(res["error"])

