"""pages/tangent.py : บทเรียน interactive: เส้นสัมผัสและอนุพันธ์ (Tangent Line and Derivative)

โครงสร้างตาม blueprint: pages/riemann.py

ลำดับการนำเสนอ (ปรับใหม่):
  1) ทดลองสำรวจก่อน - ใส่ฟังก์ชัน จุดสัมผัส a แล้วเห็นความชัน สมการเส้นสัมผัส กราฟ
     และวิธีทำทันที
  2) จึงตามด้วยมโนทัศน์หลักและทฤษฎีแบบย่อ (รายละเอียดทั้งหมดอยู่ใน expander ที่ตั้งชื่อชัดเจน)

หมายเหตุขอบเขต: หน้านี้ยังไม่มีตัวควบคุม h และยังไม่มีการวาดเส้นตัด (secant) การแสดง
เส้นตัดที่เลื่อนเข้าหาเส้นสัมผัสตามค่า h เป็นงานพัฒนาต่อในอนาคต ไม่ได้อยู่ในรอบนี้
"""

import streamlit as st

from utils.keypad import render_math_keypad
from utils.math_render import (
    format_math_spacing,
    preview_math_expr,
    render_latex,
    render_steps,
    render_syntax_guide,
)
from utils.plotter import plot_tangent
from utils.tangent_solver import compute_tangent
from utils.theme import render_hero
from utils.theory import THEORY_CONTENT

render_hero("เส้นสัมผัสและอนุพันธ์", "สำรวจความชันเส้นสัมผัสและอนุพันธ์แบบโต้ตอบ")

theory = THEORY_CONTENT["tangent"]


def _set_tangent_preset(expr_val: str, a_val: float) -> None:
    st.session_state["tangent_expr"] = expr_val
    st.session_state["tangent_a"] = a_val


def _short_case_feedback(res: dict) -> tuple[str, str]:
    """Short per-case summary built only from fields the solver actually reports.

    The solver returns the exact derivative f'(a) computed with sympy.diff. This helper
    only describes the reported case; it never replaces the exact derivative with a
    finite difference and never claims the difference quotient is defined at h = 0.

    Returns (level, text) where level is one of success/info/warning.
    """
    status = res.get("status")
    result = res.get("result")

    if status == "finite" and result is not None:
        value = float(result)
        if value == 0:
            return "info", (
                "**สรุปสั้น:** ความชันที่จุด a เท่ากับ 0 เส้นสัมผัสเป็นแนวนอน "
                "(จุดนิ่ง / stationary point) โดยจุดนิ่งไม่จำเป็นต้องเป็นจุดวกกลับ "
                "หรือจุดสูงสุด/ต่ำสุดเสมอไป"
            )
        if value > 0:
            return "success", (
                f"**สรุปสั้น:** ความชันที่จุด a เท่ากับ {value:.4f} เป็นค่าบวก "
                "กราฟกำลังเพิ่มขึ้น (increasing) ที่จุดนี้ เส้นสัมผัสจึงชันขึ้นจากซ้ายไปขวา"
            )
        return "success", (
            f"**สรุปสั้น:** ความชันที่จุด a เท่ากับ {value:.4f} เป็นค่าลบ "
            "กราฟกำลังลดลง (decreasing) ที่จุดนี้ เส้นสัมผัสจึงลาดลงจากซ้ายไปขวา"
        )

    if status == "vertical":
        return "warning", (
            "**สรุปสั้น:** เส้นสัมผัสเป็นแนวดิ่ง (vertical tangent) "
            "ความชันไม่มีค่าจำกัดเป็นจำนวนจริง ณ จุดนี้"
        )
    if status == "non_differentiable":
        return "warning", (
            "**สรุปสั้น:** ระบบรายงานว่าฟังก์ชันหาอนุพันธ์ไม่ได้ที่จุดนี้ "
            "จึงไม่มีเส้นสัมผัสที่มีความชันเป็นจำนวนจริงจำกัด "
            "เปิดวิธีทำเพื่อดูพฤติกรรมของอัตราส่วนผลต่างจากแต่ละด้าน"
        )
    if status == "undefined_point":
        return "warning", (
            "**สรุปสั้น:** ฟังก์ชันไม่นิยามที่จุด a (หรือไม่อยู่ในโดเมนจำนวนจริง) "
            "จึงไม่มีเส้นสัมผัส ณ จุดนี้"
        )
    if status == "unsupported":
        return "info", "**สรุปสั้น:** ระบบยังระบุเส้นสัมผัสได้ไม่แน่ชัด"
    return "warning", "**สรุปสั้น:** ระบบยังคำนวณเส้นสัมผัสไม่ได้ โปรดดูรายละเอียดข้อผิดพลาดที่แสดง"


# ---------------------------------------------------------------------------
# 1) ทดลองสำรวจก่อน (Experiment First)
# ---------------------------------------------------------------------------
st.markdown("### ลองสำรวจเส้นสัมผัส")
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
    st.caption("จุดสัมผัส a เลื่อนแล้วกราฟและความชันด้านล่างอัปเดตทันที")
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
    v_name = res.get("variable", "x")

    if res["ok"]:
        if v_name != "x":
            st.info(
                f"ตรวจพบตัวแปร **${v_name}$** "
                f"ระบบคำนวณและวาดกราฟเทียบกับตัวแปร ${v_name}$ อัตโนมัติ"
            )

        st.markdown("### ผลลัพธ์สมการเส้นสัมผัส")
        col_m1, col_m2 = st.columns([1, 2])
        with col_m1:
            status = res.get("status")
            if status == "finite" and res["result"] is not None:
                m_str = f"{res['result']:.4f}"
            elif status == "vertical":
                m_str = "∞ (แนวดิ่ง)"
            elif status == "non_differentiable":
                m_str = "ไม่มีค่า (หาอนุพันธ์ไม่ได้)"
            else:
                m_val = res["result"]
                m_str = f"{m_val:.4f}" if m_val is not None else "-"
            st.metric(label="ความชันเส้นสัมผัส m = f'(a)", value=m_str)
        with col_m2:
            render_latex(res["latex"])

        # ข้อความสรุปสั้นต่อกรณี (พร้อมค่าความชัน) ชิดกับผลลัพธ์
        feedback_kind, feedback_text = _short_case_feedback(res)
        if feedback_kind == "success":
            st.success(feedback_text)
        elif feedback_kind == "warning":
            st.warning(feedback_text)
        else:
            st.info(feedback_text)

        # กราฟวางติดกับตัวควบคุมด้านบน เพื่อให้เห็นผลทันทีหลังเลื่อนจุด a
        try:
            fig, _ = plot_tangent(
                res["expr"],
                a_val,
                slope=res.get("result"),
                status=res.get("status", "finite"),
            )
            st.pyplot(fig)
        except Exception as e:
            st.warning(f"ไม่สามารถวาดกราฟได้: {e}")

        # วิธีทำฉบับเต็มอยู่ใน expander ที่ตั้งชื่อชัดเจน
        with st.expander("วิธีทำทีละขั้นตอนฉบับเต็ม (Full Worked Solution)", expanded=False):
            render_steps(res["steps"])
    else:
        st.error(res["error"])
        feedback_kind, feedback_text = _short_case_feedback(res)
        if feedback_kind == "warning":
            st.warning(feedback_text)
        else:
            st.info(feedback_text)

# ---------------------------------------------------------------------------
# 2) มโนทัศน์หลักและทฤษฎี (หลังการทดลอง)
# ---------------------------------------------------------------------------
st.divider()
st.markdown("### มโนทัศน์หลักและทฤษฎี")

with st.expander("มโนทัศน์หลัก: ความชันเส้นสัมผัสมาจากลิมิตของเส้นตัดอย่างไร?", expanded=False):
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
            ">มโนทัศน์หลัก</span>""",
            unsafe_allow_html=True,
        )
    with col_concept:
        st.markdown("**ความชันเส้นสัมผัสและอนุพันธ์ (Secant Line Limit to Tangent Slope)**")

    st.markdown(
        "ความชันของเส้นสัมผัส ณ จุด $x = a$ คือลิมิตของความชันเส้นตัด (Secant Line) "
        "เมื่อจุดทั้งสองเคลื่อนเข้าหากันโดยที่ $h \\neq 0$ และให้ $h \\to 0$ "
        "(ไม่ใช่การแทนค่า $h = 0$ ซึ่งจะทำให้ตัวส่วนเป็นศูนย์และนิพจน์ไม่นิยาม):"
    )

    st.latex(r"m = f'(a) = \lim_{h \to 0} \frac{f(a+h) - f(a)}{h} \quad \implies \text{สมการเส้นสัมผัส: } y - f(a) = f'(a)(x - a)")

    st.info(
        """**จุดที่ควรสังเกตขณะทดลองด้านบน:**
- **ทิศทางความชัน ($f'(a)$):** เลื่อนจุด $a$ สังเกตหาก $f'(a) > 0$ เส้นชันขึ้น, $f'(a) < 0$ เส้นลาดลง, และ $f'(a) = 0$ เส้นสัมผัสเป็นแนวนอน (จุดนิ่ง / stationary point) โดยจุดนิ่งไม่จำเป็นต้องเป็นจุดวกกลับหรือจุดสูงสุด/ต่ำสุดเสมอไป เช่น $f(x) = x^3$ ที่ $x = 0$
- **การแนบชิดเฉพาะที่ (Local Linearity):** ใกล้จุดสัมผัส เส้นตรงจะแนบสนิทไปกับเส้นโค้ง ซึ่งเป็นรากฐานของการประมาณค่าเชิงเส้น"""
    )

with st.expander("รายละเอียดทฤษฎี ข้อควรระวัง และการประยุกต์ใช้เพิ่มเติม", expanded=False):
    col_t1, col_t2 = st.columns(2)
    with col_t1:
        st.markdown("**เงื่อนไขการใช้งาน**")
        for item in theory["conditions"]:
            st.markdown(f"- {format_math_spacing(item)}")
        st.markdown("**สมบัติสำคัญ**")
        for item in theory["properties"]:
            st.markdown(f"- {format_math_spacing(item)}")
    with col_t2:
        st.markdown("**ข้อควรระวัง**")
        with st.container(border=True):
            for caution in theory["cautions"]:
                st.markdown(f"- {format_math_spacing(caution)}")
        st.markdown("**การประยุกต์ใช้**")
        for item in theory["applications"]:
            st.markdown(f"- {format_math_spacing(item)}")
