"""pages/limit_approach.py : บทเรียน interactive: ลิมิตเข้าใกล้จุด (Limit at a Point)

โครงสร้างตาม blueprint: pages/riemann.py
"""

import numpy as np
import pandas as pd
import streamlit as st

from utils.keypad import render_math_keypad
from utils.limit_solver import compute_limit_near
from utils.math_render import preview_math_expr, render_latex, render_steps, render_syntax_guide
from utils.plotter import plot_limit_near
from utils.riemann_solver import X
from utils.theme import render_hero
from utils.theory import THEORY_CONTENT

render_hero("ลิมิตเข้าใกล้จุด", "สำรวจค่าลิมิตสองด้านและการลู่เข้าเมื่อ x เข้าใกล้จุด a")

theory = THEORY_CONTENT["limit"]

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
st.markdown("### ลองสำรวจการลู่เข้าของลิมิต")

def _set_target_point(val: str) -> None:
    st.session_state["limit_a_str"] = val


def _set_limit_preset(expr_val: str, a_val: str) -> None:
    st.session_state["limit_expr"] = expr_val
    st.session_state["limit_a_str"] = a_val


st.caption("ตัวอย่างโจทย์ยอดนิยม (ครอบคลุมรูปแบบไม่กำหนด, ตรีโกณมิติ, และลิมิตที่อนันต์):")
col_pre1, col_pre2, col_pre3, col_pre4, col_pre5, col_pre6 = st.columns(6)
with col_pre1:
    st.button(
        "(x^2 - 4)/(x - 2) → 2",
        key="btn_lim_1",
        use_container_width=True,
        on_click=_set_limit_preset,
        args=("(x**2 - 4)/(x - 2)", "2"),
    )
with col_pre2:
    st.button(
        "sin(x)/x → 0",
        key="btn_lim_2",
        use_container_width=True,
        on_click=_set_limit_preset,
        args=("sin(x)/x", "0"),
    )
with col_pre3:
    st.button(
        "tan(x) → π/2",
        key="btn_lim_3",
        use_container_width=True,
        on_click=_set_limit_preset,
        args=("tan(x)", "pi/2"),
    )
with col_pre4:
    st.button(
        "(1 + 1/x)^x → ∞",
        key="btn_lim_4",
        use_container_width=True,
        on_click=_set_limit_preset,
        args=("(1 + 1/x)**x", "inf"),
    )
with col_pre5:
    st.button(
        "(2x²+1)/(3x²-5) → ∞",
        key="btn_lim_5",
        use_container_width=True,
        on_click=_set_limit_preset,
        args=("(2*x**2 + 1)/(3*x**2 - 5)", "inf"),
    )
with col_pre6:
    st.button(
        "abs(x)/x → 0",
        key="btn_lim_6",
        use_container_width=True,
        on_click=_set_limit_preset,
        args=("abs(x)/x", "0"),
    )

col_f, col_a, col_d = st.columns([2.2, 1.4, 1.0])
with col_f:
    expr_input = st.text_input(
        "ฟังก์ชัน f(x)",
        value=st.session_state.get("limit_expr", "(x**2 - 4)/(x - 2)"),
        placeholder="เช่น (x**2-4)/(x-2), sin(x)/x, tan(x), (1+1/x)**x",
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

with col_d:
    s_a_clean = str(a_input).strip().lower().replace(" ", "")
    is_inf_target = s_a_clean in ("inf", "+inf", "-inf", "oo", "+oo", "-oo")
    if is_inf_target:
        st.info("โหมดลิมิตที่อนันต์ (x → ±∞) ไม่ต้องกำหนดระยะ delta")
        delta_val = 0.5
    else:
        delta_val = st.slider(
            "ระยะเข้าใกล้ delta",
            min_value=0.01,
            max_value=2.0,
            value=0.4,
            step=0.01,
            key="limit_delta",
        )

# Math Keypad Reusable Component
render_math_keypad(target_key="limit_expr", key_prefix="lim_kp", expanded=False)

if not expr_input.strip():
    st.info("กรุณาระบุฟังก์ชัน f(x) หรือคลิกเลือกตัวอย่างด้านบน")
else:
    res = compute_limit_near(expr_input, a_input)
    if res["ok"]:
        st.markdown("### ผลลัพธ์ลิมิต")
        col_m1, col_m2 = st.columns([1, 2])
        with col_m1:
            status = res.get("status")
            if status == "finite" and res["result"] is not None:
                l_str = f"{res['result']:.4f}"
            elif status == "infinite":
                l_str = "∞ (อนันต์)"
            elif status == "dne":
                l_str = "ไม่มีลิมิต (DNE)"
            elif status == "unsupported":
                l_str = "ยังตัดสินไม่ได้"
            else:
                lim_val = res["result"]
                l_str = f"{lim_val:.4f}" if lim_val is not None else "หาค่าไม่ได้"
            st.metric(label="ค่าลิมิต L", value=l_str)
        with col_m2:
            render_latex(res["latex"])

        st.divider()
        try:
            fig, _ = plot_limit_near(res["expr"], a_input, delta=delta_val)
            st.pyplot(fig)
        except Exception:
            st.warning("ไม่สามารถวาดกราฟได้ ตรวจสอบฟังก์ชันอีกครั้ง")

        is_infinite = res.get("is_infinite", False)

        if is_infinite:
            # กล่องอธิบายมโนทัศน์สำหรับลิมิตที่อนันต์
            st.markdown("#### มโนทัศน์พื้นฐาน: ลิมิตที่อนันต์และเส้นกำกับแนวนอนคืออะไร?")
            st.info(
                """
                * **พฤติกรรมระยะไกล (End Behavior):** ลิมิตที่อนันต์ ($x \\to \\infty$ หรือ $x \\to -\\infty$) ไม่ได้มีลิมิตซ้าย-ขวา แต่เป็นการศึกษาพฤติกรรมเมื่อค่า $x$ ขยายตัวอย่างมหาศาลบนแกนนอน
                * **เส้นกำกับแนวนอน (Horizontal Asymptote):** หากเมื่อ $x \\to \\infty$ ค่าฟังก์ชันลู่เข้าสู่ค่าคงที่ $L$ เส้นตรง $y = L$ จะทำหน้าที่เป็นเส้นกำกับแนวนอนที่กราฟวิ่งเข้าแนบชิด
                """
            )

            # ตารางการแทนค่าเชิงตัวเลขขนาดใหญ่
            st.markdown("#### ตารางการเข้าใกล้เชิงตัวเลขเมื่อ x ขยายสู่ขนาดใหญ่ (Numerical Inspection)")
            st.caption("สังเกตพฤติกรรมตัวเลข: เมื่อค่า x เพิ่มขึ้นสู่ขนาดใหญ่ ให้สังเกตว่าค่า f(x) วิ่งลู่เข้าหาค่าคงที่ใด")
            is_pos = (s_a_clean in ("inf", "+inf", "oo", "+oo"))
            test_xs = [5.0, 10.0, 50.0, 100.0, 500.0, 1000.0] if is_pos else [-5.0, -10.0, -50.0, -100.0, -500.0, -1000.0]
            table_rows = []
            target_L = res.get("result")
            for tx in test_xs:
                try:
                    y_val = float(res["expr"].subs(X, tx).evalf())
                    y_str = f"{y_val:.6f}"
                    diff_str = f"{abs(y_val - target_L):.6f}" if target_L is not None else "-"
                except Exception:
                    y_str = "N/A"
                    diff_str = "-"
                table_rows.append({
                    "ค่าตัวแปร x": f"{tx:g}",
                    "ค่าฟังก์ชัน f(x)": y_str,
                    "ผลต่างจากค่าลิมิต |f(x) - L|": diff_str,
                })
            st.dataframe(pd.DataFrame(table_rows), use_container_width=True, hide_index=True)

        else:
            # กล่องอธิบายมโนทัศน์: ความหมายของการเข้าใกล้ทางซ้ายและขวา (กรณีจุดจำกัด)
            st.markdown("#### มโนทัศน์พื้นฐาน: ลิมิตซ้ายและลิมิตขวาคืออะไร?")
            try:
                a_num_val = float(res.get("a_sp", 0).evalf())
            except Exception:
                a_num_val = 0.0

            col_c_left, col_c_right = st.columns(2)
            with col_c_left:
                st.info(
                    f"""
                    **ลิมิตทางซ้าย ($x \\to a^-$)**
                    * **ทิศทาง:** ก้าวเท้ามาจากฝั่งซ้ายของเส้นจำนวน
                    * **เงื่อนไข:** ค่า $x$ น้อยกว่า $a$ เสมอ ($x < a$) เช่น ขยับจาก {a_num_val - 0.2:.2f} $\\to$ {a_num_val - 0.05:.2f} $\\to$ {a_num_val - 0.001:.3f}
                    * **เป้าหมาย:** สังเกตว่าเมื่อ $x$ วิ่งเฉียดเข้าใกล้ $a$ ความสูงของกราฟ $f(x)$ ลู่เข้าหาเลขใด
                    """
                )
            with col_c_right:
                st.info(
                    f"""
                    **ลิมิตทางขวา ($x \\to a^+$)**
                    * **ทิศทาง:** ก้าวเท้ามาจากฝั่งขวาของเส้นจำนวน
                    * **เงื่อนไข:** ค่า $x$ มากกว่า $a$ เสมอ ($x > a$) เช่น ขยับจาก {a_num_val + 0.2:.2f} $\\to$ {a_num_val + 0.05:.2f} $\\to$ {a_num_val + 0.001:.3f}
                    * **เป้าหมาย:** สังเกตว่าเมื่อ $x$ วิ่งเฉียดเข้าใกล้ $a$ ความสูงของกราฟ $f(x)$ ลู่เข้าหาเลขใด
                    """
                )

            st.markdown(
                """
                > **หัวใจสำคัญของการมีลิมิต (Two-Sided Limit):**  
                > ลิมิตไม่ได้ถามว่า *"ที่จุด $x = a$ ฟังก์ชันมีค่าเท่าไหร่"* (ตรงจุดนั้นอาจเป็นรูโหว่หรือหาค่าไม่ได้ เช่น $\\frac{0}{0}$)  
                > แต่ลิมิตกำลังถามว่า *"เมื่อเดินเข้าใกล้จุด $a$ จากสองฝั่ง กราฟกำลังจะไปเจอกันที่ความสูงเท่าไหร่"*  
                > **ถ้าสองฝั่งเดินมาชนกันที่ความสูงเดียวกัน ($L^- = L^+$)** $\\implies$ **มีลิมิตสองด้าน**  
                > **ถ้าสองฝั่งแยกทางกันหรือไปคนละทิศ ($L^- \\neq L^+$)** $\\implies$ **ไม่มีลิมิตสองด้าน (DNE)**
                """
            )

            # ตารางการแทนค่าเชิงตัวเลขเพื่อสร้างสัญชาตญาณ
            st.markdown("#### ตารางการเข้าใกล้เชิงตัวเลข (Numerical Inspection)")
            st.caption("สังเกตพฤติกรรมตัวเลข: เมื่อระยะห่าง d ลดลงเรื่อย ๆ ($x$ ขยับเข้าใกล้จุด $a$ มากขึ้น) ให้สังเกตว่าค่า f(x) ฝั่งซ้าย และ f(x) ฝั่งขวา กำลังบีบเข้าหาตัวเลขใด")
            deltas = [delta_val, delta_val / 2, delta_val / 5, delta_val / 10, delta_val / 100]
            table_rows = []
            for d in deltas:
                xl = a_num_val - d
                xr = a_num_val + d
                try:
                    yl = float(res["expr"].subs(X, xl).evalf())
                    yl_str = f"{yl:.6f}"
                except Exception:
                    yl_str = "N/A"
                try:
                    yr = float(res["expr"].subs(X, xr).evalf())
                    yr_str = f"{yr:.6f}"
                except Exception:
                    yr_str = "N/A"
                table_rows.append({
                    "ระยะห่าง d": f"{d:.4f}",
                    "ฝั่งซ้าย x = a - d": f"{xl:.4f}",
                    "ค่า f(x) ซ้าย": yl_str,
                    "ฝั่งขวา x = a + d": f"{xr:.4f}",
                    "ค่า f(x) ขวา": yr_str,
                })
            st.dataframe(pd.DataFrame(table_rows), use_container_width=True, hide_index=True)

        st.divider()
        render_steps(res["steps"])
    else:
        st.error(res["error"])

