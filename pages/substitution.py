"""pages/substitution.py : การอินทิเกรตโดยการแทนตัวแปร (Integration by Substitution)

ออกแบบเพื่อสร้างมโนทัศน์การตัดสินใจเลือกตัวแปร u และ du พร้อมระบบปลดล็อควิธีทำ (Active Scaffolding)
ครอบคลุมทั้งรูปแบบฟังก์ชันยกกำลัง ตัวส่วน ตรีโกณมิติ และการจัดรูปพีชคณิต
"""

import streamlit as st
import sympy as sp

from utils.keypad import render_math_keypad
from utils.math_render import format_inverse_trig, preview_math_expr, render_latex, render_steps, render_syntax_guide
from utils.substitution_solver import solve_substitution
from utils.theme import render_hero

render_hero(
    "การอินทิเกรตโดยการแทนตัวแปร (Integration by Substitution)",
    "สร้างมโนทัศน์การเลือกตัวแปร u และ du เพื่อลดทอนรูปอินทิกรัลให้เป็นรูปพื้นฐาน",
)

# =============================================================================
# 1. สรุปรูปแบบการสังเกตเลือกตัวแปร u
# =============================================================================
with st.expander("หลักการและ 4 รูปแบบสังเกตยอดนิยมในการเลือกตัวแปร u", expanded=True):
    st.markdown(
        """
        เป้าหมายของการเปลี่ยนตัวแปร คือการแปลงอินทิกรัลที่ซับซ้อนให้อยู่ในรูปพื้นฐาน $\\int f(u)\\,du$
        โดยมีหลักสำคัญคือ **ตัวแปร $x$ จะต้องถูกตัดทอนได้หมด**
        """
    )

    col_g1, col_g2 = st.columns(2)
    with col_g1:
        st.markdown("**1. ฟังก์ชันภายในวงเล็บยกกำลัง / ใต้กรณฑ์ (รูท):**")
        st.latex(r"\int [g(x)]^n \cdot g'(x) \, dx \implies \text{กำหนด } u = g(x)")
        st.caption("เมื่อ $u = g(x)$ จะได้ $du = g'(x)dx$ ซึ่งจะตัดกับ $g'(x)$ ในโจทย์พอดี")

        st.markdown("**2. ฟังก์ชันที่อยู่เป็นตัวส่วน (เศษส่วน):**")
        st.latex(r"\int \frac{g'(x)}{g(x)} \, dx \implies \text{กำหนด } u = g(x)")
        st.caption("เมื่อดิฟตัวส่วน $u = g(x)$ จะได้เศษ $g'(x)$ ซึ่งตัดทอนกันหมด กลายเป็นรูป $\\ln|u|$")

    with col_g2:
        st.markdown("**3. ฟังก์ชันในเลขชี้กำลังหรือฟังก์ชันตรีโกณมิติ:**")
        st.latex(r"\int f(g(x)) \cdot g'(x) \, dx \implies \text{กำหนด } u = g(x)")
        st.caption("เช่น $\\int e^{g(x)} g'(x) dx$ หรือ $\\int \\cos(g(x)) g'(x) dx$ กำหนด $u$ เป็นไส้ใน")

        st.markdown("**4. การปรับรูปพีชคณิตเสริม (Algebraic Adjustment):**")
        st.latex(r"\int x \sqrt{x+1} \, dx \implies \text{กำหนด } u = x+1 \implies x = u-1")
        st.caption("เมื่ออนุพันธ์ $du$ ตัดตัวแปรไม่หมด ให้จัดรูปตัวแปร $x$ ในรูปของ $u$ แล้วคูณกระจาย")

st.divider()

# =============================================================================
# 2. กรณีศึกษาฝึกตัดสินใจเลือกตัวแปร u (Active Scaffolding)
# =============================================================================
st.markdown("### กรณีศึกษาฝึกตัดสินใจเลือกตัวแปร $u$")

case_sub = st.selectbox(
    "เลือกกรณีศึกษาที่ต้องการเรียนรู้:",
    options=[
        "กรณีที่ 1: ฟังก์ชันใต้กรณฑ์ยกกำลัง (2x √(x² + 1))",
        "กรณีที่ 2: ฟังก์ชันตัวส่วนและลอการิทึม ((ln x) / x)",
        "กรณีที่ 3: ฟังก์ชันตรีโกณมิติและเลขชี้กำลัง (cos(x) e^(sin x))",
        "กรณีที่ 4: การจัดรูปพีชคณิตเสริมเมื่อ x ไม่หมด (x √(x + 1))",
    ],
    index=0,
)

if "กรณีที่ 1" in case_sub:
    st.markdown("#### กรณีที่ 1: ฟังก์ชันใต้กรณฑ์ยกกำลัง")
    st.latex(r"\int 2x\sqrt{x^2+1} \, dx")

    u_choice = st.radio(
        "ท่านจะเลือกกำหนด u เป็นฟังก์ชันใด?",
        options=[
            "แนวทาง A (แนะนำ): ให้ u = x² + 1 (ฟังก์ชันใต้กรณฑ์)",
            "แนวทาง B: ให้ u = 2x (ฟังก์ชันสัมประสิทธิ์ด้านนอก)",
            "แนวทาง C: ให้ u = x (ตัวแปรเดิม)",
        ],
        index=None,
        key="radio_u_case1",
    )

    if u_choice is None:
        st.info("กรุณาคลิกเลือกแนวทางด้านบน")
    elif "แนวทาง A" in u_choice:
        st.success("**ถูกต้องตามหลักการ**")
        st.markdown(
            """
            * **ขั้นที่ 1: กำหนดตัวแปรและหาอนุพันธ์**
              $$u = x^2 + 1 \\implies \\frac{du}{dx} = 2x \\implies dx = \\frac{du}{2x}$$
            * **ขั้นที่ 2: นำกลับไปแทนค่าในโจทย์**
              $$\\int 2x\\sqrt{x^2+1} \\, dx = \\int 2x \\cdot \\sqrt{u} \\cdot \\frac{du}{2x}$$
            * **ขั้นที่ 3: สังเกตการตัดทอน**
              $2x$ ตัดทอนกันหมดจด! เหลือเพียง:
              $$\\int \\sqrt{u} \\, du = \\int u^{1/2} \\, du = \\frac{u^{3/2}}{3/2} + C = \\frac{2}{3}u^{3/2} + C$$
            * **ขั้นที่ 4: แทนค่า u กลับคืน**
              $$= \\frac{2}{3}(x^2+1)^{3/2} + C$$
            """
        )
    elif "แนวทาง B" in u_choice:
        st.error("**[ทางตัน] ตัวแปร x ตัดทอนไม่หมด**")
        st.markdown("หากเลือก $u = 2x$ จะได้ $du = 2dx$ โจทย์จะกลายเป็น $\\int u\\sqrt{(u/2)^2+1} \\frac{du}{2}$ ซึ่งพจน์ใต้กรณฑ์ยังคงติดตัวแปรและซับซ้อนเช่นเดิม")
    else:
        st.warning("**[ไม่มีความคืบหน้า]** การให้ $u = x$ เป็นเพียงการเปลี่ยนชื่อตัวอักษร ไม่ได้ช่วยลดทอนความซับซ้อนของฟังก์ชัน")

elif "กรณีที่ 2" in case_sub:
    st.markdown("#### กรณีที่ 2: ฟังก์ชันตัวส่วนและลอการิทึม")
    st.latex(r"\int \frac{\ln x}{x} \, dx")

    u_choice = st.radio(
        "ท่านจะเลือกกำหนด u เป็นฟังก์ชันใด?",
        options=[
            "แนวทาง A: ให้ u = x (ตัวส่วน)",
            "แนวทาง B (แนะนำ): ให้ u = ln(x) (ตัวเศษ)",
            "แนวทาง C: ให้ u = 1/x",
        ],
        index=None,
        key="radio_u_case2",
    )

    if u_choice is None:
        st.info("กรุณาคลิกเลือกแนวทางด้านบน")
    elif "แนวทาง B" in u_choice:
        st.success("**ถูกต้องตามหลักการ (สังเกตเห็นอนุพันธ์ร่วม)**")
        st.markdown(
            """
            * **ขั้นที่ 1: คำนวณอนุพันธ์**
              $$u = \\ln x \\implies \\frac{du}{dx} = \\frac{1}{x} \\implies dx = x\\,du$$
            * **ขั้นที่ 2: แทนค่าในโจทย์**
              $$\\int \\frac{\\ln x}{x} \\, dx = \\int \\frac{u}{x} \\cdot (x\\,du)$$
            * **ขั้นที่ 3: ตัดทอนตัวแปร**
              $x$ ตัดกับ $x$ หมดเกลี้ยง เหลือเพียง:
              $$\\int u \\, du = \\frac{u^2}{2} + C$$
            * **ขั้นที่ 4: แทนค่า u กลับคืน**
              $$= \\frac{(\\ln x)^2}{2} + C \\quad (x > 0)$$
            """
        )
    elif "แนวทาง A" in u_choice:
        st.error("**[ไม่มีความคืบหน้า]** ได้เพียง $\\int \\frac{\\ln u}{u} du$ ซึ่งเหมือนโจทย์เดิม")
    else:
        st.error("**[ทางตัน]** หากเลือก $u = 1/x$ จะได้ $du = -\\frac{1}{x^2} dx$ จะยิ่งทำให้มีดีกรีของ $x$ บวมขึ้น")

elif "กรณีที่ 3" in case_sub:
    st.markdown("#### กรณีที่ 3: ฟังก์ชันตรีโกณมิติและเลขชี้กำลัง")
    st.latex(r"\int \cos(x) e^{\sin(x)} \, dx")

    u_choice = st.radio(
        "ท่านจะเลือกกำหนด u เป็นฟังก์ชันใด?",
        options=[
            "แนวทาง A (แนะนำ): ให้ u = sin(x) (ไส้ในของเลขชี้กำลัง)",
            "แนวทาง B: ให้ u = cos(x)",
            "แนวทาง C: ให้ u = e^(sin x)",
        ],
        index=None,
        key="radio_u_case3",
    )

    if u_choice is None:
        st.info("กรุณาคลิกเลือกแนวทางด้านบน")
    elif "แนวทาง A" in u_choice:
        st.success("**ถูกต้องตามหลักการ**")
        st.markdown(
            """
            * **ขั้นที่ 1: กำหนดตัวแปร**
              $$u = \\sin(x) \\implies du = \\cos(x)dx \\implies dx = \\frac{du}{\\cos(x)}$$
            * **ขั้นที่ 2: แทนค่าและตัดทอน**
              $$\\int \\cos(x) e^u \\cdot \\frac{du}{\\cos(x)} = \\int e^u \\, du = e^u + C$$
            * **ขั้นที่ 3: แทนค่า u กลับคืน**
              $$= e^{\\sin(x)} + C$$
            """
        )
    elif "แนวทาง C" in u_choice:
        st.info("**[ทำได้เช่นกัน]** หากให้ $u = e^{\\sin x} \\implies du = e^{\\sin x}\\cos(x)dx$ จะได้ $\\int 1 du = u + C = e^{\\sin x} + C$ ซึ่งรวดเร็วเช่นกัน")
    else:
        st.error("**[ข้อผิดพลาดทางเครื่องหมายและรูปสมการ]** หากให้ $u = \\cos(x)$ จะได้ $du = -\\sin(x)dx$ ซึ่งไม่สามารถตัดกับ $\\sin(x)$ ที่ติดอยู่บนเลขชี้กำลังได้")

else:
    st.markdown("#### กรณีที่ 4: การจัดรูปพีชคณิตเสริมเมื่อ x ไม่หมด")
    st.latex(r"\int x\sqrt{x+1} \, dx")
    st.caption("ข้อสังเกต: เมื่อให้ $u = x+1$ จะได้ $du = dx$ ซึ่งไม่สามารถตัด $x$ ด้านหน้าทิ้งได้ จึงต้องแก้สมการกลับ: $x = u - 1$")

    u_choice = st.radio(
        "ท่านจะแก้ปัญหาตัวแปร x ด้านหน้าที่เหลืออยู่อย่างไร?",
        options=[
            "แนวทาง A (ถูกต้อง): แทน x = u - 1 แล้วคูณกระจายเข้าไปในวงเล็บ",
            "แนวทาง B: ดึง x ออกนอกอินทิกรัลเลยเพราะเป็นตัวคูณ",
            "แนวทาง C: ถือว่าทำไม่ได้ด้วย u-Substitution ต้องเปลี่ยนไปใช้วิธีอื่นทันที",
            "แนวทาง D: ให้ u = √(x+1)",
        ],
        index=None,
        key="radio_u_case4",
    )

    if u_choice is None:
        st.info("กรุณาคลิกเลือกแนวทางด้านบน")
    elif "แนวทาง B" in u_choice:
        st.error("**[ข้อห้ามร้ายแรงทางแคลคูลัส!]** ห้ามดึงตัวแปรที่กำลังอินทิเกรต ($x$) ออกนอกเครื่องหมาย $\\int$ เด็ดขาด ดึงได้เฉพาะค่าคงที่เท่านั้น")
    elif "แนวทาง A" in u_choice:
        st.success("**ถูกต้อง: นี่คือเทคนิคการปรับรูปพีชคณิตเสริม**")
        st.markdown(
            """
            * **ขั้นที่ 1: สลับรูปตัวแปร**
              $$u = x + 1 \\implies x = u - 1 \\quad \\text{และ} \\quad dx = du$$
            * **ขั้นที่ 2: แทนค่าลงในอินทิกรัล**
              $$\\int x\\sqrt{x+1}\\,dx = \\int (u - 1)\\sqrt{u}\\,du = \\int (u - 1)u^{1/2}\\,du$$
            * **ขั้นที่ 3: คูณกระจายเลขชี้กำลัง**
              $$= \\int (u^{3/2} - u^{1/2})\\,du = \\frac{u^{5/2}}{5/2} - \\frac{u^{3/2}}{3/2} + C = \\frac{2}{5}u^{5/2} - \\frac{2}{3}u^{3/2} + C$$
            * **ขั้นที่ 4: แทนค่า u กลับคืน**
              $$= \\frac{2}{5}(x+1)^{5/2} - \\frac{2}{3}(x+1)^{3/2} + C$$
            """
        )
    elif "แนวทาง D" in u_choice:
        st.info("**[ทำได้เช่นกัน]** หากให้ $u = \\sqrt{x+1} \\implies u^2 = x+1 \\implies x = u^2-1$ และ $dx = 2u du$ จะได้ $\\int (u^2-1)(u)(2u du) = \\int 2(u^4 - u^2) du$ ซึ่งได้คำตอบเดียวกัน")
    else:
        st.warning("**[ไม่ถูกต้อง]** การแทนค่านี้สามารถแก้ได้โดยการจัดรูปพีชคณิตเสริม")

st.divider()

# =============================================================================
# 3. เครื่องคิดเลขคำนวณการเปลี่ยนตัวแปรด้วย SymPy
# =============================================================================
st.markdown("### คำนวณนิพจน์ด้วย SymPy")
st.caption("ระบบจะคำนวณปฏิยานุพันธ์ ตรวจจับตัวแปร $u$ ที่เหมาะสม และแสดงขั้นตอนอย่างละเอียด")

def _set_sub_preset(val: str) -> None:
    st.session_state["substitution_expr"] = val

st.markdown("**ตัวอย่างโจทย์ยอดนิยม (คลิกเพื่อโหลดสูตร):**")
p_cols1 = st.columns(4)
with p_cols1[0]:
    st.button("2x √(x² + 1)", key="pre_sub_1", use_container_width=True, on_click=_set_sub_preset, args=("2x*sqrt(x^2+1)",))
with p_cols1[1]:
    st.button("(ln x) / x", key="pre_sub_2", use_container_width=True, on_click=_set_sub_preset, args=("ln(x)/x",))
with p_cols1[2]:
    st.button("cos(x) e^(sin x)", key="pre_sub_3", use_container_width=True, on_click=_set_sub_preset, args=("cos(x)*exp(sin(x))",))
with p_cols1[3]:
    st.button("x √(x + 1)", key="pre_sub_4", use_container_width=True, on_click=_set_sub_preset, args=("x*sqrt(x+1)",))

p_cols2 = st.columns(3)
with p_cols2[0]:
    st.button("2x / (x² + 1)", key="pre_sub_5", use_container_width=True, on_click=_set_sub_preset, args=("2x/(x^2+1)",))
with p_cols2[1]:
    st.button("3x² (x³ + 5)⁴", key="pre_sub_6", use_container_width=True, on_click=_set_sub_preset, args=("3x^2*(x^3+5)^4",))
with p_cols2[2]:
    st.button("e^(-x²) (ไม่เป็นฟังก์ชันมูลฐาน)", key="pre_sub_7", use_container_width=True, on_click=_set_sub_preset, args=("exp(-x^2)",))

expr_input = st.text_input(
    "ใส่นิพจน์อินทิกรัลที่ต้องการคำนวณ",
    value=st.session_state.get("substitution_expr", "2x*sqrt(x^2+1)"),
    placeholder="เช่น 2x*sqrt(x^2+1), ln(x)/x, 3x^2*(x^3+1)^4",
    key="substitution_expr",
)
preview_math_expr(expr_input)
render_syntax_guide()

render_math_keypad(target_key="substitution_expr", key_prefix="sub_kp", expanded=False)

if st.button("คำนวณผลลัพธ์", type="primary", key="btn_substitution_calc"):
    if not expr_input.strip():
        st.error("กรุณาใส่นิพจน์ก่อน")
    else:
        res = solve_substitution(expr_input)
        if res["ok"]:
            v_name = res.get("variable", "x")
            if v_name != "x":
                st.info(f"ตรวจพบตัวแปร **${v_name}$**: ระบบคำนวณและอินทิเกรตเทียบกับ $d{v_name}$ อัตโนมัติ")

            st.markdown("#### ผลลัพธ์การคำนวณ")
            render_latex(res["latex"])

            if res.get("status") == "non_elementary":
                st.warning("ข้อสังเกตเชิงมโนทัศน์: ฟังก์ชันนี้ไม่มีปฏิยานุพันธ์ในรูปฟังก์ชันมูลฐาน (Non-Elementary Function) คำตอบที่ได้อยู่ในรูปฟังก์ชันพิเศษระดับสูง เช่น erf, Si, li")
            elif res.get("method") == "by_parts" and res.get("parts_info"):
                p = res["parts_info"]
                u_lat = format_inverse_trig(sp.latex(p["u"]))
                dv_lat = format_inverse_trig(sp.latex(p["dv"]))
                st.info(f"การอินทิเกรตทีละส่วน (By Parts): กำหนด $u = {u_lat}$ และ $dv = {dv_lat} \\, d{v_name}$")
            elif res.get("u_candidate") is not None:
                u_c = format_inverse_trig(sp.latex(res["u_candidate"]))
                du_c = format_inverse_trig(sp.latex(res["du_candidate"]))
                st.info(f"คำแนะนำเทคนิคการเปลี่ยนตัวแปร: สามารถกำหนดให้ $u = {u_c}$ ซึ่งจะได้ $du = {du_c} \\, d{v_name}$")

            st.divider()
            st.markdown("#### ขั้นตอนการพิจารณา")
            render_steps(res["steps"])
        else:
            st.error(res["error"])
