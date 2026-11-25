"""pages/by_parts.py : การอินทิเกรตทีละส่วน (Integration by Parts)

ออกแบบเพื่อสร้างแนวคิดการตัดสินใจเลือก u และ dv ตามกฎ LIATE
ครอบคลุมทั้งรูปแบบพหุนามคูณเอกซ์โพเนนเชียล ลอการิทึม การทำซ้ำหลายชั้น และการวนลูป
"""

import streamlit as st
import sympy as sp

from utils.decision_cases import BY_PARTS_CASES, render_decision_case
from utils.by_parts_solver import solve_by_parts
from utils.keypad import render_math_keypad
from utils.math_render import format_inverse_trig, preview_math_expr, render_latex, render_steps, render_syntax_guide
from utils.special_functions import describe_special_functions, special_functions_in
from utils.theme import render_hero

render_hero(
    "การอินทิเกรตทีละส่วน (Integration by Parts)",
    "หลักการเลือก u และ dv ตามกฎ LIATE พร้อมเทคนิคการอินทิเกรตแบบวนลูป",
)
# Custom Tactile Bauhaus styling & responsive table protection (matching Quiz UX)
st.markdown(
    r"""
    <style>
    /* Radio options styled as tactile Bauhaus cards (matching Quiz UX) */
    div[data-testid="stRadio"] div[role="radiogroup"]:not([aria-orientation="horizontal"]) {
        display: flex !important;
        flex-direction: column !important;
        gap: 10px !important;
        margin-top: 8px !important;
        margin-bottom: 14px !important;
    }
    div[data-testid="stRadio"] div[role="radiogroup"]:not([aria-orientation="horizontal"]) > label {
        background-color: #FFFFFF !important;
        border: 2px solid #18181B !important;
        border-radius: 12px !important;
        box-shadow: 3px 3px 0px #18181B !important;
        padding: 12px 16px !important;
        margin: 0 !important;
        cursor: pointer !important;
        transition: all 0.12s ease-out !important;
        width: 100% !important;
        display: flex !important;
        align-items: center !important;
    }
    div[data-testid="stRadio"] div[role="radiogroup"]:not([aria-orientation="horizontal"]) > label:hover {
        background-color: #FEF08A !important;
        transform: translate(-1.5px, -1.5px) !important;
        box-shadow: 4px 4px 0px #18181B !important;
    }
    div[data-testid="stRadio"] div[role="radiogroup"]:not([aria-orientation="horizontal"]) > label:has(input:checked) {
        background-color: #FEF9C3 !important;
        border: 2px solid #18181B !important;
        box-shadow: 3.5px 3.5px 0px #18181B !important;
    }
    div[data-testid="stRadio"] div[role="radiogroup"]:not([aria-orientation="horizontal"]) > label p {
        font-family: "Mali", "Outfit", sans-serif !important;
        font-size: 1rem !important;
        font-weight: 600 !important;
        line-height: 1.4 !important;
        margin: 0 !important;
        color: #18181B !important;
    }

    /* Responsive Table Styling: Prevent horizontal squishing on mobile */
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


# =============================================================================
# 1. สรุปหลักการทั่วไปในการเลือก u และ dv (กฎ LIATE)
# =============================================================================
st.markdown("### ทฤษฎีและหลักการสำคัญ")
with st.container(border=True):
    col_badge, col_title = st.columns([1, 4])
    with col_badge:
        st.markdown(
            r"""<span style="
                background-color: #FEF08A;
                border: 1.5px solid #18181B;
                border-radius: 8px;
                padding: 4px 10px;
                font-family: 'Fredoka', 'Mali', sans-serif;
                font-size: 13px;
                font-weight: 700;
                color: #18181B;
                display: inline-block;
            ">By Parts</span>""",
            unsafe_allow_html=True,
        )
    with col_title:
        st.markdown("#### สูตรและหลักการเลือกตัวแปร $u$ และ $dv$")

    st.latex(r"\int u \, dv = uv - \int v \, du")

    st.markdown(
        r"""
| ลำดับ LIATE | ประเภทฟังก์ชัน | บทบาทที่แนะนำ | เหตุผลทางคณิตศาสตร์ |
| :---: | :--- | :---: | :--- |
| L, I | ลอการิทึม / ตรีโกณผกผัน | เลือกเป็น $u$ เสมอ | หาปริพันธ์ตรงยาก แต่หาอนุพันธ์แล้วกลายเป็นพีชคณิต |
| A | พหุนาม / พีชคณิต $x^n$ | เลือกเป็น $u$ เมื่อคูณกับ $T$ หรือ $E$ | หาอนุพันธ์แล้วดีกรีลดลงเรื่อย ๆ จนกลายเป็นค่าคงที่ |
| T, E | ตรีโกณมิติ / เลขชี้กำลัง | มักเลือกเป็น $dv$ | อินทิเกรตง่ายและวนกลับมารูปเดิม |
        """
    )

with st.expander("อ่านหลักการตัดสินใจและเทคนิคการอินทิเกรตทีละส่วน", expanded=False):
    st.markdown(
        r"""
- **หลักการเลือก $u$:** ฟังก์ชันที่ **หาอนุพันธ์แล้วได้รูปที่ง่ายขึ้นหรือดีกรีลดลง**
- **หลักการเลือก $dv$:** ฟังก์ชันที่ **หาปริพันธ์กลับเป็น $v$ ได้ง่ายโดยรูปไม่ซับซ้อนขึ้น**
- **ลำดับความสำคัญตามกฎ LIATE (เลือกเป็น $u$ จากซ้ายไปขวา):** $L$ (Log), $I$ (Inv Trig), $A$ (Algebra), $T$ (Trig), $E$ (Exp)
- **เทคนิคการวนซ้ำ:** กรณีฟังก์ชันตรีโกณมิติกับเอกซ์โพเนนเชียล เช่น $\int e^x \sin x\,dx$ หรือ $\int 2^x \cos x\,dx$ หลังทำ By Parts สองรอบจะได้รูปเดิม ให้ย้ายข้างสมการทางพีชคณิตเพื่อหาคำตอบ
        """
    )

st.divider()

# =============================================================================
# 2. กรณีศึกษาฝึกตัดสินใจ (Active Scaffolding)
# =============================================================================
st.markdown("### กรณีศึกษาฝึกตัดสินใจเลือก $u$ และ $dv$ (LIATE Decision Challenge)")

case_options = [c["selector_title"] for c in BY_PARTS_CASES]
case_parts = st.selectbox(
    "เลือกกรณีศึกษาที่ต้องการเรียนรู้:",
    options=case_options,
    index=0,
)
selected_case = next(c for c in BY_PARTS_CASES if c["selector_title"] == case_parts)
render_decision_case(selected_case)


st.divider()

# =============================================================================
# 3. เครื่องคิดเลข By Parts ด้วย SymPy
# =============================================================================
st.markdown("### คำนวณโจทย์การอินทิเกรตทีละส่วนด้วย SymPy")

def _set_byparts_preset(val: str) -> None:
    st.session_state["byparts_expr"] = val

st.markdown("**ตัวอย่างโจทย์:**")
bp_cols = st.columns(4)
with bp_cols[0]:
    st.button("x e^x", key="pre_bp_1", use_container_width=True, on_click=_set_byparts_preset, args=("x*exp(x)",))
with bp_cols[1]:
    st.button("x ln(x)", key="pre_bp_2", use_container_width=True, on_click=_set_byparts_preset, args=("x*ln(x)",))
with bp_cols[2]:
    st.button("x² sin(x)", key="pre_bp_3", use_container_width=True, on_click=_set_byparts_preset, args=("x^2*sin(x)",))
with bp_cols[3]:
    st.button("e^x cos(x)", key="pre_bp_4", use_container_width=True, on_click=_set_byparts_preset, args=("exp(x)*cos(x)",))

bp_cols2 = st.columns(4)
with bp_cols2[0]:
    st.button("ln(x)", key="pre_bp_5", use_container_width=True, on_click=_set_byparts_preset, args=("ln(x)",))
with bp_cols2[1]:
    st.button("x cos(x)", key="pre_bp_6", use_container_width=True, on_click=_set_byparts_preset, args=("x*cos(x)",))
with bp_cols2[2]:
    st.button("arctan(x)", key="pre_bp_7", use_container_width=True, on_click=_set_byparts_preset, args=("atan(x)",))
with bp_cols2[3]:
    st.button("2^x cos(x)", key="pre_bp_8", use_container_width=True, on_click=_set_byparts_preset, args=("2^x*cos(x)",))

expr_input = st.text_input(
    "ใส่นิพจน์อินทิกรัลที่ต้องการคำนวณ",
    value=st.session_state.get("byparts_expr", "x*exp(x)"),
    placeholder="เช่น x*exp(x), x*ln(x), exp(x)*cos(x)",
    key="byparts_expr",
)
preview_math_expr(expr_input)
render_syntax_guide()

render_math_keypad(target_key="byparts_expr", key_prefix="byparts_kp", expanded=False)

btn_calc = st.button("คำนวณผลลัพธ์", type="primary", key="btn_byparts_calc")
if expr_input.strip() or btn_calc:
    if not expr_input.strip():
        st.error("กรุณาใส่นิพจน์ก่อน")
    else:
        res = solve_by_parts(expr_input)
        if res["ok"]:
            v_name = res.get("variable", "x")
            if v_name != "x":
                st.info(f"ตรวจพบตัวแปร **${v_name}$**: ระบบคำนวณและอินทิเกรตเทียบกับ $d{v_name}$ อัตโนมัติ")

            st.markdown("#### ผลลัพธ์การคำนวณ")
            render_latex(res["latex"])

            special_names = special_functions_in(res.get("result"))
            if special_names:
                st.info(describe_special_functions(special_names))
            elif res.get("status") == "better_suited_for_substitution":
                st.warning(res.get("warning", "โจทย์ข้อนี้เหมาะสมกับการใช้การแทนตัวแปร u มากกว่าการอินทิเกรตทีละส่วน"))
            elif res.get("status") == "non_elementary":
                st.warning("ฟังก์ชันนี้ไม่มีปฏิยานุพันธ์ในรูปฟังก์ชันมูลฐาน")
            elif res.get("parts_info"):
                p = res["parts_info"]
                u_lat = format_inverse_trig(sp.latex(p["u"]))
                dv_lat = format_inverse_trig(sp.latex(p["dv"]))
                st.info(f"การอินทิเกรตทีละส่วน (By Parts): กำหนด $u = {u_lat}$ และ $dv = {dv_lat} \\, d{v_name}$")

            st.divider()
            render_steps(res["steps"])
        else:
            st.error(res["error"])
