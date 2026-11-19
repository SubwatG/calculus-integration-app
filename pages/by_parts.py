"""pages/by_parts.py : การอินทิเกรตทีละส่วน (Integration by Parts)

ออกแบบเพื่อสร้างมโนทัศน์การตัดสินใจเลือก u และ dv ตามกฎ LIATE
ครอบคลุมทั้งรูปแบบพหุนามคูณเอกซ์โพเนนเชียล ลอการิทึม การทำซ้ำหลายชั้น และการวนลูป
"""

import streamlit as st
import sympy as sp

from utils.by_parts_solver import solve_by_parts
from utils.keypad import render_math_keypad
from utils.math_render import format_inverse_trig, preview_math_expr, render_latex, render_steps, render_syntax_guide
from utils.theme import render_hero

render_hero(
    "การอินทิเกรตทีละส่วน (Integration by Parts)",
    "สร้างมโนทัศน์การเลือก u และ dv ตามกฎ LIATE พร้อมเทคนิคการอินทิเกรตแบบวนลูป",
)

# =============================================================================
# 1. สรุปหลักการทั่วไปในการเลือก u และ dv (กฎ LIATE)
# =============================================================================
with st.expander("หลักการและกลยุทธ์การเลือก u และ dv (กฎ LIATE)", expanded=True):
    st.markdown("สูตรหลักของการอินทิเกรตทีละส่วน (ย้อนกลับจากกฎการหาอนุพันธ์ของผลคูณ):")
    st.latex(r"\int u \, dv = uv - \int v \, du")

    st.markdown(
        """
        **หัวใจสำคัญในการตัดสินใจ:**
        1. **เลือก $u$:** ต้องเป็นฟังก์ชันที่ **หาอนุพันธ์แล้วได้รูปที่ง่ายขึ้นหรือดีกรีลดลง**
        2. **เลือก $dv$:** ต้องเป็นฟังก์ชันที่ **สามารถหาปริพันธ์กลับเป็น $v$ ได้ง่ายโดยรูปไม่ซับซ้อนขึ้น**
        """
    )

    st.markdown(
        """
        | ลำดับ | ตัวย่อ | ประเภทฟังก์ชัน | ตัวอย่างฟังก์ชัน | บทบาทที่เหมาะสม | เหตุผลทางคณิตศาสตร์ |
        | :---: | :---: | :--- | :--- | :---: | :--- |
        | **1** | **L** | **Logarithmic** | $\\ln x, \\log_2 x$ | ควรเลือกเป็น **$u$ เสมอ** | เพราะหาอนุพันธ์ง่าย ($1/x$) แต่หาอินทิกรัลตรง ๆ ยาก |
        | **2** | **I** | **Inverse Trig** | $\\arcsin x, \\arctan x$ | ควรเลือกเป็น **$u$ เสมอ** | ดิฟแล้วกลายเป็นฟังก์ชันพีชคณิต แต่ไม่มีสูตรอินทิเกรตตรง |
        | **3** | **A** | **Algebraic** | $x, x^2, 3x+1$ | ควรเลือกเป็น **$u$** (เมื่อคู่กับ T, E) | ดิฟแล้วดีกรีลดลง เช่น $x^2 \\to 2x \\to 2$ จนตัดทอนหมด |
        | **4** | **T** | **Trigonometric** | $\\sin x, \\cos x$ | มักเลือกเป็น **$dv$** | อินทิเกรตง่าย ไม่เพิ่มความซับซ้อน (สลับรูปวนไปมา) |
        | **5** | **E** | **Exponential** | $e^x, 2^x$ | มักเลือกเป็น **$dv$** | อินทิเกรตง่ายที่สุด เพราะ $\\int e^x dx = e^x$ รูปคงเดิมเสมอ |
        """
    )

st.divider()

# =============================================================================
# 2. กรณีศึกษาฝึกตัดสินใจ (Active Scaffolding)
# =============================================================================
st.markdown("### กรณีศึกษาฝึกตัดสินใจเลือก $u$ และ $dv$")

case_parts = st.selectbox(
    "เลือกกรณีศึกษาที่ต้องการเรียนรู้:",
    options=[
        "กรณีที่ 1: พหุนามคูณกับเอกซ์โพเนนเชียล (x e^x)",
        "กรณีที่ 2: ฟังก์ชันเดี่ยวที่หาอนุพันธ์ง่ายแต่อินทิเกรตยาก (ln x)",
        "กรณีที่ 3: พหุนามดีกรีสูงกว่า 1 ต้องทำซ้ำหลายชั้น (x² e^x)",
        "กรณีที่ 4: ฟังก์ชันวนลูปไม่รู้จบ (e^x cos x)",
    ],
    index=0,
)

if "กรณีที่ 1" in case_parts:
    st.markdown("#### กรณีที่ 1: พหุนามคูณกับเอกซ์โพเนนเชียล")
    st.latex(r"\int x e^x \, dx")
    st.caption("โจทย์ข้อนี้เกิดจากฟังก์ชันพีชคณิต (A: $x$) คูณกับเอกซ์โพเนนเชียล (E: $e^x$)")

    parts_choice = st.radio(
        "ตามกฎ LIATE ท่านควรเลือก u และ dv อย่างไร?",
        options=[
            "แนวทางที่ 1 (ถูกต้อง): ให้ u = x และ dv = e^x dx",
            "แนวทางที่ 2: ให้ u = e^x และ dv = x dx",
        ],
        index=None,
        key="radio_parts_case1",
    )

    if parts_choice is None:
        st.info("กรุณาคลิกเลือกแนวทางด้านบน")
    elif "แนวทางที่ 1" in parts_choice:
        st.success("**ถูกต้องตามหลักการ (A มาก่อน E ในกฎ LIATE)**")
        st.markdown(
            """
            * **ขั้นที่ 1: คำนวณส่วนประกอบ**
              * กำหนด $u = x \\implies du = dx$ (ดีกรีลดลงเหลือค่าคงที่)
              * กำหนด $dv = e^x dx \\implies v = \\int e^x dx = e^x$
            * **ขั้นที่ 2: แทนค่าลงในสูตร By Parts**
              $$\\int u \\, dv = uv - \\int v \\, du$$
              $$\\int x e^x \\, dx = x e^x - \\int e^x \\, dx$$
            * **ขั้นที่ 3: คำนวณอินทิกรัลส่วนที่เหลือ**
              $$= x e^x - e^x + C = e^x(x - 1) + C$$
            """
        )
    else:
        st.error("**[ข้อผิดพลาด] รูปสมการจะซับซ้อนขึ้น**")
        st.markdown(
            """
            หากให้ $u = e^x$ จะได้ $du = e^x dx$ แต่ $dv = x dx \\implies v = \\frac{x^2}{2}$
            เมื่อแทนในสูตรจะได้:
            $$\\int x e^x dx = \\frac{x^2 e^x}{2} - \\int \\frac{x^2 e^x}{2} dx$$
            สังเกตว่าพจน์อินทิกรัลใหม่กลายเป็น $x^2$ ซึ่ง **ดีกรีสูงขึ้นและยากกว่าเดิม**
            """
        )

elif "กรณีที่ 2" in case_parts:
    st.markdown("#### กรณีที่ 2: ฟังก์ชันเดี่ยวที่หาอนุพันธ์ง่ายแต่อินทิเกรตยาก")
    st.latex(r"\int \ln(x) \, dx")
    st.caption("ข้อสังเกต: แม้จะมีฟังก์ชันเดียว แต่สามารถมองเป็นผลคูณกับ 1 ได้เสมอ: $\\int \\ln(x) \\cdot 1 \\, dx$")

    parts_choice = st.radio(
        "ท่านจะแบ่งบทบาทอย่างไร?",
        options=[
            "แนวทางที่ 1: ให้ u = 1 และ dv = ln(x) dx",
            "แนวทางที่ 2 (ถูกต้อง): ให้ u = ln(x) และ dv = 1 dx",
        ],
        index=None,
        key="radio_parts_case2",
    )

    if parts_choice is None:
        st.info("กรุณาคลิกเลือกแนวทางด้านบน")
    elif "แนวทางที่ 2" in parts_choice:
        st.success("**ถูกต้อง (L มาเป็นอันดับแรกในกฎ LIATE)**")
        st.markdown(
            """
            * **ขั้นที่ 1: กำหนดส่วนประกอบ**
              * $u = \\ln(x) \\implies du = \\frac{1}{x} dx$ (เปลี่ยนลอการิทึมเป็นเศษส่วนพีชคณิต)
              * $dv = dx \\implies v = x$
            * **ขั้นที่ 2: แทนในสูตร By Parts**
              $$\\int \\ln(x) \\, dx = (\\ln x)(x) - \\int x \\cdot \\frac{1}{x} \\, dx$$
              $$= x \\ln(x) - \\int 1 \\, dx$$
            * **ขั้นที่ 3: สรุปผลลัพธ์**
              $$= x \\ln(x) - x + C = x(\\ln x - 1) + C \\quad (x > 0)$$
            """
        )
    else:
        st.error("**[ทางตัน] กลับไปสู่ปัญหาเดิม**")
        st.markdown("หากเลือก $dv = \\ln(x) dx$ ท่านจะต้องหา $v = \\int \\ln(x) dx$ ซึ่งก็คือโจทย์ตั้งต้นนั่นเอง")

elif "กรณีที่ 3" in case_parts:
    st.markdown("#### กรณีที่ 3: พหุนามดีกรีสูงกว่า 1 (ทำซ้ำหลายชั้น)")
    st.latex(r"\int x^2 e^x \, dx")
    st.caption("ข้อสังเกต: เมื่อพหุนามมีดีกรี $n$ จะต้องทำ By Parts ซ้ำ $n$ ครั้งจนกว่าพจน์พหุนามจะถูกดิฟจนกลายเป็นค่าคงที่")

    parts_choice = st.radio(
        "ขั้นตอนการลดรูปควรเป็นอย่างไร?",
        options=[
            "แนวทาง A (ถูกต้อง): ทำรอบที่ 1 ลดเหลือ x e^x แล้วทำรอบที่ 2 ลดเหลือค่าคงที่",
            "แนวทาง B: สลับ u และ dv ในรอบที่ 2 เพื่อความรวดเร็ว",
        ],
        index=None,
        key="radio_parts_case3",
    )

    if parts_choice is None:
        st.info("กรุณาคลิกเลือกแนวทางด้านบน")
    elif "แนวทาง A" in parts_choice:
        st.success("**ถูกต้อง: กฎการลดทอนดีกรีแบบต่อเนื่อง**")
        st.markdown(
            """
            * **รอบที่ 1:** ให้ $u = x^2 \\implies du = 2x dx$, $dv = e^x dx \\implies v = e^x$
              $$\\int x^2 e^x dx = x^2 e^x - 2\\int x e^x dx$$
            * **รอบที่ 2:** ทำ By Parts ต่อที่ก้อน $\\int x e^x dx$ โดยให้ $u = x \\implies du = dx$, $dv = e^x dx \\implies v = e^x$
              $$\\int x e^x dx = x e^x - e^x$$
            * **ประกอบผลลัพธ์:**
              $$\\int x^2 e^x dx = x^2 e^x - 2(x e^x - e^x) + C = e^x(x^2 - 2x + 2) + C$$
            """
        )
    else:
        st.error("**[ข้อผิดพลาด] อย่าสลับบทบาทกลับไปมา**")
        st.markdown("การสลับบทบาทในรอบถัดไปจะทำให้พจน์ตัดทอนกันหมดกลายเป็น $0 = 0$")

else:
    st.markdown("#### กรณีที่ 4: ฟังก์ชันวนลูปไม่รู้จบ (Cyclic Integration)")
    st.latex(r"I = \int e^x \cos(x) \, dx")
    st.caption("ข้อสังเกต: ทั้ง $e^x$ และ $\\cos(x)$ เป็นฟังก์ชันที่หาอนุพันธ์หรือปริพันธ์แล้ววนกลับมา จึงใช้วิธีอินทิเกรตทีละส่วน 2 ครั้ง แล้วแก้สมการเชิงพีชคณิต")

    parts_choice = st.radio(
        "ท่านจะเริ่มต้นกำหนด u และ dv รอบแรกอย่างไร?",
        options=[
            "แนวทางที่ 1: กำหนด u = cos(x) และ dv = e^x dx (แล้วทำรอบสองให้สอดคล้องกัน)",
            "แนวทางที่ 2: กำหนด u = e^x และ dv = cos(x) dx (แล้วทำรอบสองให้สอดคล้องกัน)",
            "แนวทางที่ 3: รอบแรกเลือก u = cos(x) แต่รอบสองสลับกลับมาเลือก u = e^x",
        ],
        index=None,
        key="radio_parts_case4",
    )

    if parts_choice is None:
        st.info("กรุณาเลือกแนวทางด้านบน")
    elif "แนวทางที่ 3" in parts_choice:
        st.error("**ข้อควรระวัง: การสลับตัวแปรกลับไปมา**")
        st.markdown("หากรอบแรกกำหนดฟังก์ชันหนึ่งเป็น $u$ แต่รอบที่สองสลับกลับมา ผลลัพธ์จะหักล้างกันกลายเป็น $I = I$ หรือ $0 = 0$ ทำให้ไม่ก้าวหน้าในการหาคำตอบ")
    else:
        st.success("**ถูกต้อง: การอินทิเกรตทีละส่วนแบบวนลูป**")
        st.markdown("ทั้งแนวทางที่ 1 และ 2 สามารถแก้ได้สำเร็จ โดยมีขั้นตอนการทำ 2 รอบดังนี้:")

        st.markdown("##### ขั้นตอนวิธีทำ (โดยวิธี u = e^x, dv = cos(x) dx):")
        st.markdown("**รอบที่ 1:**")
        st.latex(r"u = e^x \implies du = e^x \, dx, \quad dv = \cos(x) \, dx \implies v = \sin(x)")
        st.latex(r"I = e^x \sin(x) - \int e^x \sin(x) \, dx")

        st.markdown(r"**รอบที่ 2 (ทำ By Parts ซ้ำกับก้อน $\int e^x \sin x dx$ โดยคงบทบาทเดิม):**")
        st.latex(r"u = e^x \implies du = e^x \, dx, \quad dv = \sin(x) \, dx \implies v = -\cos(x)")
        st.latex(r"\int e^x \sin(x) \, dx = -e^x \cos(x) - \int (-e^x \cos x) \, dx = -e^x \cos(x) + I")

        st.markdown("**นำผลรอบที่ 2 แทนกลับเข้าไปในสมการแรก:**")
        st.latex(r"I = e^x \sin(x) - \left[ -e^x \cos(x) + I \right] = e^x \sin(x) + e^x \cos(x) - I")

        st.markdown("**ย้ายข้างสมการทางพีชคณิต (บวก I ทั้งสองข้าง):**")
        st.latex(r"2I = e^x(\sin x + \cos x) \implies I = \frac{e^x}{2}(\sin x + \cos x) + C")

st.divider()

# =============================================================================
# 3. เครื่องคิดเลข By Parts ด้วย SymPy
# =============================================================================
st.markdown("### คำนวณโจทย์การอินทิเกรตทีละส่วนด้วย SymPy")
st.caption("ระบบจะจัดคู่ตัวแปร $u$ และ $dv$ ให้โดยอัตโนมัติตามกฎ LIATE พร้อมแสดงขั้นตอนอย่างละเอียด")

def _set_byparts_preset(val: str) -> None:
    st.session_state["byparts_expr"] = val

st.markdown("**ตัวอย่างโจทย์ยอดนิยม (คลิกเพื่อโหลดสูตร):**")
bp_cols = st.columns(4)
with bp_cols[0]:
    st.button("x e^x", key="pre_bp_1", use_container_width=True, on_click=_set_byparts_preset, args=("x*exp(x)",))
with bp_cols[1]:
    st.button("x ln(x)", key="pre_bp_2", use_container_width=True, on_click=_set_byparts_preset, args=("x*ln(x)",))
with bp_cols[2]:
    st.button("x² sin(x)", key="pre_bp_3", use_container_width=True, on_click=_set_byparts_preset, args=("x^2*sin(x)",))
with bp_cols[3]:
    st.button("e^x cos(x)", key="pre_bp_4", use_container_width=True, on_click=_set_byparts_preset, args=("exp(x)*cos(x)",))

bp_cols2 = st.columns(3)
with bp_cols2[0]:
    st.button("ln(x)", key="pre_bp_5", use_container_width=True, on_click=_set_byparts_preset, args=("ln(x)",))
with bp_cols2[1]:
    st.button("x cos(x)", key="pre_bp_6", use_container_width=True, on_click=_set_byparts_preset, args=("x*cos(x)",))
with bp_cols2[2]:
    st.button("arctan(x)", key="pre_bp_7", use_container_width=True, on_click=_set_byparts_preset, args=("atan(x)",))

expr_input = st.text_input(
    "ใส่นิพจน์อินทิกรัลที่ต้องการคำนวณ",
    value=st.session_state.get("byparts_expr", "x*exp(x)"),
    placeholder="เช่น x*exp(x), x*ln(x), exp(x)*cos(x)",
    key="byparts_expr",
)
preview_math_expr(expr_input)
render_syntax_guide()

render_math_keypad(target_key="byparts_expr", key_prefix="byparts_kp", expanded=False)

if st.button("คำนวณผลลัพธ์", type="primary", key="btn_byparts_calc"):
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

            if res.get("status") == "better_suited_for_substitution":
                st.warning(res.get("warning", "โจทย์ข้อนี้เหมาะสมกับการใช้การแทนตัวแปร u มากกว่าการอินทิเกรตทีละส่วน"))
            elif res.get("parts_info"):
                p = res["parts_info"]
                u_lat = format_inverse_trig(sp.latex(p["u"]))
                dv_lat = format_inverse_trig(sp.latex(p["dv"]))
                st.info(f"การอินทิเกรตทีละส่วน (By Parts): กำหนด $u = {u_lat}$ และ $dv = {dv_lat} \\, d{v_name}$")

            st.divider()
            st.markdown("#### ขั้นตอนการพิจารณา")
            render_steps(res["steps"])
        else:
            st.error(res["error"])
