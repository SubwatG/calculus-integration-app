"""pages/substitution.py — เทคนิคการอินทิเกรต (การเปลี่ยนตัวแปรและการอินทิเกรตทีละส่วน)

ออกแบบเพื่อสร้างมโนทัศน์การตัดสินใจเลือกตัวแปร พร้อมระบบปลดล็อควิธีทำ (Active Scaffolding)
"""

import streamlit as st

from utils.math_render import preview_math_expr, render_latex, render_steps, render_syntax_guide
from utils.substitution_solver import solve_substitution
from utils.theme import render_hero

render_hero(
    "เทคนิคการอินทิเกรต",
    "ห้องทดลองมโนทัศน์การตัดสินใจ: การเปลี่ยนตัวแปร (u-Sub) และการอินทิเกรตทีละส่วน (By Parts)",
)

tab1, tab2, tab3 = st.tabs([
    "1. เทคนิคการเปลี่ยนตัวแปร (u-Substitution)",
    "2. เทคนิคการอินทิเกรตทีละส่วน (Integration by Parts)",
    "3. เครื่องมือคำนวณอัตโนมัติ (SymPy CAS)",
])

# =============================================================================
# TAB 1: u-Substitution Scaffolding
# =============================================================================
with tab1:
    st.markdown("### 1.1 สรุปหลักการทั่วไปในการเลือกตัวแปร u")
    st.markdown(
        """
        เป้าหมายของการเปลี่ยนตัวแปร คือการแปลงอินทิกรัลที่ซับซ้อนให้อยู่ในรูปพื้นฐาน $\\int f(u)\\,du$
        โดยมีหลักสำคัญคือ **ตัวแปรเดิม $x$ จะต้องถูกตัดทอนให้หมดเกลี้ยง**

        **เกณฑ์การสังเกต 4 รูปแบบหลักในการกำหนด $u = g(x)$:**
        """
    )

    col_g1, col_g2 = st.columns(2)
    with col_g1:
        st.markdown("**1. ฟังก์ชันภายในวงเล็บยกกำลัง:**")
        st.latex(r"\int [g(x)]^n \cdot g'(x) \, dx \implies \text{กำหนด } u = g(x)")

        st.markdown("**2. ฟังก์ชันที่อยู่ใต้กรณฑ์ (รูท):**")
        st.latex(r"\int \sqrt{g(x)} \cdot g'(x) \, dx \implies \text{กำหนด } u = g(x)")

    with col_g2:
        st.markdown("**3. ฟังก์ชันที่อยู่เป็นตัวส่วน:**")
        st.latex(r"\int \frac{g'(x)}{g(x)} \, dx \implies \text{กำหนด } u = g(x)")

        st.markdown("**4. ฟังก์ชันบนเลขชี้กำลัง:**")
        st.latex(r"\int e^{g(x)} \cdot g'(x) \, dx \implies \text{กำหนด } u = g(x)")

    st.divider()

    st.markdown("### 1.2 ฝึกการตัดสินใจเลือกตัวแปร u (บังคับเลือกก่อนเปิดวิธีทำ)")
    st.markdown("#### โจทย์ทดสอบมโนทัศน์:")
    st.latex(r"\int 2x \sqrt{x^2 + 1} \, dx")

    u_choice = st.radio(
        "หากท่านเป็นผู้แก้โจทย์ ท่านจะกำหนดให้ u เท่ากับฟังก์ชันใด?",
        options=[
            "แนวทาง A: กำหนดให้ u = x^2 + 1",
            "แนวทาง B: กำหนดให้ u = x",
            "แนวทาง C: กำหนดให้ u = 2x",
            "แนวทาง D: กำหนดให้ u = sin(x)",
        ],
        index=None,
        key="radio_u_choice",
    )

    if u_choice is None:
        st.info("[การตัดสินใจ] กรุณาคลิกเลือกตัวแปร u ที่ท่านคิดว่าเหมาะสมด้านบน เพื่อให้ระบบวิเคราะห์และปลดล็อคขั้นตอนวิธีทำ")
    elif "แนวทาง A" in u_choice:
        st.success("**[ถูกต้องตามหลักการ] เหมาะสมที่สุด (Preferred Substitution)**")
        st.markdown("พจน์ $2x$ นอกกรณฑ์ตรงกับอนุพันธ์ของ $x^2+1$ พอดิบพอดี ทำให้ตัวแปร $x$ ถูกกำจัดหมด:")

        st.markdown("##### ขั้นตอนวิธีทำฉบับสมบูรณ์:")
        st.markdown("**ขั้นที่ 1: กำหนดตัวแปรและหาอนุพันธ์**")
        st.latex(r"u = x^2 + 1 \implies du = 2x \, dx \implies dx = \frac{du}{2x}")

        st.markdown("**ขั้นที่ 2: แทนค่า u และ dx ลงในโจทย์**")
        st.latex(r"\int 2x \sqrt{x^2 + 1} \, dx = \int 2x \cdot \sqrt{u} \cdot \left(\frac{du}{2x}\right)")
        st.latex(r"= \int \sqrt{u} \, du = \int u^{1/2} \, du")

        st.markdown("**ขั้นที่ 3: คำนวณปริพันธ์เทียบกับตัวแปร u**")
        st.latex(r"= \frac{u^{1/2 + 1}}{\frac{1}{2} + 1} + C = \frac{2}{3}u^{3/2} + C")

        st.markdown("**ขั้นที่ 4: แทนค่า u กลับคืนสู่ตัวแปร x**")
        st.latex(r"= \frac{2}{3}(x^2 + 1)^{3/2} + C")

        st.markdown("**ขั้นที่ 5: ตรวจสอบความถูกต้องด้วยอนุพันธ์ย้อนกลับ**")
        st.latex(r"\frac{d}{dx}\left[\frac{2}{3}(x^2 + 1)^{3/2} + C\right] = \frac{2}{3} \cdot \frac{3}{2}(x^2 + 1)^{1/2} \cdot (2x) = 2x\sqrt{x^2 + 1}")
    elif "แนวทาง B" in u_choice:
        st.warning("**[ถูกกฎคณิตศาสตร์ แต่ไม่ช่วยให้ง่ายขึ้น] (Valid but Inefficient)**")
        st.markdown("เมื่อแทน $u = x$ จะได้ $du = dx$ ส่งผลให้สมการกลายเป็น:")
        st.latex(r"\int 2u\sqrt{u^2+1}\,du")
        st.markdown("**ข้อสรุป:** โครงสร้างสมการเหมือนเดิมทุกประการ ไม่เกิดการลดทอนความซับซ้อน (ระบบจึงยังไม่แสดงวิธีทำสำเร็จรูป)")
    elif "แนวทาง C" in u_choice:
        st.warning("**[ทำให้รูปสมการซับซ้อนขึ้น] (Valid but Inefficient)**")
        st.markdown("เมื่อแทน $u = 2x \\implies x = u/2$ และ $dx = du/2$ จะได้:")
        st.latex(r"\int u\sqrt{\frac{u^2}{4}+1}\,\frac{du}{2}")
        st.markdown("**ข้อสรุป:** พจน์ใต้กรณฑ์กลายเป็นเศษส่วน ซึ่งยากกว่าโจทย์ตั้งต้น (กรุณาเลือกแนวทางใหม่)")
    else:
        st.error("**[ผิดหลักการ] (Invalid Substitution)**")
        st.markdown("ฟังก์ชัน $\\sin(x)$ ไม่มีความเชื่อมโยงใด ๆ กับนิพจน์ในโจทย์ การแทนค่านี้จะทำให้ตัวแปร $x$ ไม่สามารถตัดทอนได้")

# =============================================================================
# TAB 2: Integration by Parts Scaffolding
# =============================================================================
with tab2:
    st.markdown("### 2.1 สรุปหลักการทั่วไปในการเลือก u และ dv")
    st.markdown("สูตรหลักของการอินทิเกรตทีละส่วน (มาจากกฎการหาอนุพันธ์ของผลคูณ):")
    st.latex(r"\int u \, dv = uv - \int v \, du")

    st.markdown(
        """
        **หัวใจสำคัญในการตัดสินใจ:**
        1. **เลือก $u$:** ต้องเป็นฟังก์ชันที่ **หาอนุพันธ์แล้วได้รูปที่ง่ายขึ้นหรือดีกรีลดลง**
        2. **เลือก $dv$:** ต้องเป็นฟังก์ชันที่ **สามารถหาปริพันธ์กลับเป็น $v$ ได้ง่ายโดยรูปไม่บวมขึ้น**

        **ตารางจัดลำดับความสำคัญตามกฎ LIATE (จากควรเลือกเป็น $u$ มากที่สุด $\\to$ ควรเลือกเป็น $dv$ มากที่สุด):**
        """
    )

    st.markdown(
        """
        | ลำดับ | ตัวย่อ | ประเภทฟังก์ชัน | ตัวอย่างฟังก์ชัน | บทบาทที่เหมาะสม | เหตุผลทางคณิตศาสตร์ |
        |:---:|:---:|:---|:---|:---:|:---|
        | 1 | **L** | Logarithmic | $\\ln x, \\log_a x$ | **ควรเป็น $u$ เสมอ** | หาอนุพันธ์ง่าย ($1/x$) แต่หาปริพันธ์ตรง ๆ ยาก |
        | 2 | **I** | Inverse Trigonometric | $\\arcsin x, \\arctan x$ | **ควรเป็น $u$ เสมอ** | หาอนุพันธ์แล้วเป็นฟังก์ชันพีชคณิต แต่หาปริพันธ์ตรง ๆ ยาก |
        | 3 | **A** | Algebraic | $x, x^2, 3x+5$ | **มักกำหนดเป็น $u$** | เมื่อดิฟแล้วดีกรีของ $x$ จะลดลงเรื่อย ๆ จนหมดไป |
        | 4 | **T** | Trigonometric | $\\sin x, \\cos x$ | **มักกำหนดเป็น $dv$** | อินทิเกรตแล้ววนลูปสลับกัน ดีกรีไม่เพิ่มขึ้น |
        | 5 | **E** | Exponential | $e^x, 2^x$ | **ควรเป็น $dv$ เสมอ** | อินทิเกรตง่ายที่สุด $e^x$ ได้รูปเดิม ไม่เพิ่มภาระ |
        """
    )

    st.divider()

    st.markdown("### 2.2 ฝึกการตัดสินใจเลือก u และ dv (บังคับเลือกก่อนเปิดวิธีทำ)")
    st.markdown("#### โจทย์ทดสอบมโนทัศน์:")
    st.latex(r"\int x e^x \, dx")

    parts_choice = st.radio(
        "ท่านจะกำหนดการจับคู่ u และ dv อย่างไรเพื่อให้แก้โจทย์ได้สำเร็จ?",
        options=[
            "แนวทางที่ 1: กำหนด u = x (พีชคณิต) และ dv = e^x dx (เอกซ์โพเนนเชียล)",
            "แนวทางที่ 2: กำหนด u = e^x (เอกซ์โพเนนเชียล) และ dv = x dx (พีชคณิต)",
            "แนวทางที่ 3: กำหนด u = x e^x และ dv = dx",
        ],
        index=None,
        key="radio_parts_choice",
    )

    if parts_choice is None:
        st.info("[การตัดสินใจ] กรุณาคลิกเลือกการจับคู่ u และ dv ด้านบน เพื่อให้ระบบวิเคราะห์และปลดล็อคขั้นตอนวิธีทำ")
    elif "แนวทางที่ 1" in parts_choice:
        st.success("**[ถูกต้องตามหลักการ] ความซับซ้อนลดทอนลงสำเร็จ (Complexity Reduced)**")
        st.markdown("การเลือก $u = x$ ทำให้อนุพันธ์มีดีกรีลดลงจาก 1 เหลือ 0 ปลดล็อคขั้นตอนวิธีทำสมบูรณ์:")

        st.markdown("##### ขั้นตอนวิธีทำฉบับสมบูรณ์:")
        st.markdown("**ขั้นที่ 1: หาอนุพันธ์ของ u และหาปริพันธ์ของ dv**")
        st.latex(r"u = x \implies du = \frac{d}{dx}[x] \, dx = dx")
        st.latex(r"dv = e^x \, dx \implies v = \int e^x \, dx = e^x")

        st.markdown("**ขั้นที่ 2: แทนค่าลงในสูตรอินทิเกรตทีละส่วน**")
        st.latex(r"\int u \, dv = uv - \int v \, du")
        st.latex(r"\int x e^x \, dx = (x)(e^x) - \int (e^x)(dx)")

        st.markdown("**ขั้นที่ 3: คำนวณปริพันธ์ในพจน์ที่เหลือและสรุปคำตอบ**")
        st.latex(r"= x e^x - e^x + C = (x - 1)e^x + C")

        st.markdown("**ขั้นที่ 4: ตรวจสอบความถูกต้องด้วยอนุพันธ์ย้อนกลับ**")
        st.latex(r"\frac{d}{dx}\left[(x - 1)e^x + C\right] = (1)e^x + (x - 1)e^x = x e^x")
        st.markdown("ผลลัพธ์ตรงกับโจทย์ตั้งต้น 100%")
    elif "แนวทางที่ 2" in parts_choice:
        st.warning("**[กับดักความซับซ้อน] Complexity Increased Warning!**")
        st.markdown("หากเลือกสลับตำแหน่ง จะเกิดผลลัพธ์ดังนี้:")
        st.latex(r"u = e^x \implies du = e^x \, dx")
        st.latex(r"dv = x \, dx \implies v = \int x \, dx = \frac{x^2}{2}")
        st.latex(r"\int x e^x \, dx = \left(\frac{x^2}{2}\right)e^x - \int \frac{x^2}{2} e^x \, dx")
        st.markdown(
            """
            **ข้อวิเคราะห์:** พจน์ปริพันธ์ใหม่คือ $\\int \\frac{x^2}{2} e^x \\, dx$ ซึ่งมีดีกรีของ $x$ **เพิ่มขึ้นจาก 1 เป็น 2**
            ทำให้โจทย์ซับซ้อนและยากกว่าโจทย์ตั้งต้น และหากทำต่อไปจะวนลูปดีกรีสูงขึ้นเรื่อย ๆ
            *(ระบบจึงไม่แสดงวิธีทำจนจบ เพื่อให้ผู้เรียนสังเกตเห็นกับดักนี้และเลือกแนวทางใหม่)*
            """
        )
    else:
        st.error("**[ไม่เกิดประโยชน์] ความซับซ้อนเพิ่มขึ้นอย่างรวดเร็ว**")
        st.markdown("เมื่อให้ $u = x e^x$ จะได้ $du = (e^x + x e^x)dx$ และ $v = x$ ส่งผลให้:")
        st.latex(r"\int x e^x \, dx = x^2 e^x - \int (x e^x + x^2 e^x) \, dx")
        st.markdown("พจน์ใหม่มีพจน์กำลังสองเพิ่มขึ้นมา ทำให้ไม่สามารถหาคำตอบได้")

# =============================================================================
# TAB 3: Free SymPy Solver
# =============================================================================
with tab3:
    st.markdown("### คำนวณนิพจน์อิสระด้วย SymPy CAS")
    expr_input = st.text_input(
        "ใส่นิพจน์อินทิกรัลที่ต้องการคำนวณ",
        value="2x*e^(x^2)",
        placeholder="เช่น 2x*e^(x^2), 3x^2*cos(x^3)",
        key="substitution_expr",
    )
    preview_math_expr(expr_input)
    render_syntax_guide()

    if st.button("คำนวณ", type="primary", key="btn_substitution_calc"):
        if not expr_input.strip():
            st.error("กรุณาใส่นิพจน์ก่อน")
        else:
            res = solve_substitution(expr_input)
            if res["ok"]:
                st.markdown("#### ผลลัพธ์การคำนวณ")
                render_latex(res["latex"])
                st.divider()
                st.markdown("#### ขั้นตอนการพิจารณา")
                render_steps(res["steps"])
            else:
                st.error(res["error"])
