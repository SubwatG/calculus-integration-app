"""pages/limit_approach.py : บทเรียน interactive: ลิมิตเข้าใกล้จุด (Limit at a Point)

โครงสร้างตาม blueprint: pages/riemann.py
"""

import numpy as np
import pandas as pd
import streamlit as st

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

st.caption("ตัวอย่างโจทย์ยอดนิยม (รูปแบบไม่กำหนด):")
col_pre1, col_pre2, col_pre3, col_pre4 = st.columns(4)
with col_pre1:
    if st.button("(x^2 - 4)/(x - 2)", key="btn_lim_1", use_container_width=True):
        st.session_state["limit_expr"] = "(x**2 - 4)/(x - 2)"
        st.session_state["limit_a"] = 2.0
        st.rerun()
with col_pre2:
    if st.button("sin(x)/x", key="btn_lim_2", use_container_width=True):
        st.session_state["limit_expr"] = "sin(x)/x"
        st.session_state["limit_a"] = 0.0
        st.rerun()
with col_pre3:
    if st.button("(sqrt(x) - 1)/(x - 1)", key="btn_lim_3", use_container_width=True):
        st.session_state["limit_expr"] = "(sqrt(x) - 1)/(x - 1)"
        st.session_state["limit_a"] = 1.0
        st.rerun()
with col_pre4:
    if st.button("(1 - cos(x))/x", key="btn_lim_4", use_container_width=True):
        st.session_state["limit_expr"] = "(1 - cos(x))/x"
        st.session_state["limit_a"] = 0.0
        st.rerun()

col_f, col_a, col_d = st.columns([2, 1, 1])
with col_f:
    expr_input = st.text_input(
        "ฟังก์ชัน f(x)",
        value="(x**2 - 4)/(x - 2)",
        placeholder="เช่น (x**2-4)/(x-2), sin(x)/x",
        key="limit_expr",
    )
    preview_math_expr(expr_input)
    render_syntax_guide()

with col_a:
    a_val = st.number_input(
        "จุดที่ x เข้าใกล้ a",
        value=2.0,
        step=0.5,
        format="%.2f",
        key="limit_a",
    )

with col_d:
    delta_val = st.slider(
        "ระยะเข้าใกล้ delta",
        min_value=0.01,
        max_value=2.0,
        value=0.4,
        step=0.01,
        key="limit_delta",
    )

if not expr_input.strip():
    st.info("กรุณาระบุฟังก์ชัน f(x) หรือคลิกเลือกตัวอย่างด้านบน")
else:
    res = compute_limit_near(expr_input, a_val)
    if res["ok"]:
        st.markdown("### ผลลัพธ์ลิมิต")
        col_m1, col_m2 = st.columns([1, 2])
        with col_m1:
            lim_val = res["result"]
            l_str = f"{lim_val:.4f}" if lim_val is not None else "หาค่าไม่ได้ / อนันต์"
            st.metric(label="ค่าลิมิตสองด้าน L", value=l_str)
        with col_m2:
            render_latex(res["latex"])

        st.divider()
        try:
            fig, _ = plot_limit_near(res["expr"], a_val, delta=delta_val)
            st.pyplot(fig)
        except Exception:
            st.warning("ไม่สามารถวาดกราฟได้ ตรวจสอบฟังก์ชันอีกครั้ง")

        # ตารางการแทนค่าเชิงตัวเลขเพื่อสร้างสัญชาตญาณ
        st.markdown("#### ตารางการเข้าใกล้เชิงตัวเลข (Numerical Inspection)")
        deltas = [delta_val, delta_val / 2, delta_val / 5, delta_val / 10, delta_val / 100]
        table_rows = []
        for d in deltas:
            xl = a_val - d
            xr = a_val + d
            try:
                yl = float(res["expr"].subs(X, xl))
                yl_str = f"{yl:.6f}"
            except Exception:
                yl_str = "N/A"
            try:
                yr = float(res["expr"].subs(X, xr))
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

