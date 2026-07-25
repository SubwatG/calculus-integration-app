import streamlit as st

from utils.content_loader import load_lesson


LESSONS = {
    "Integration Overview": "overview.md",
    "Basic Integration Rules": "basic_rules.md",
    # --- Silpakorn Calculus2 (OCR, cleaned) ---
    "บทที่ 1 บทนำ": "silpakorn-ch1-บทที่-1-บทนำ.md",
    "1.1 ปฏิยานุพันธ์และอินทิกรัลไม่จำกัดเขต": "silpakorn-ch1-antiderivative-indefinite.md",
    "แบบฝึกหัด 1.2": "silpakorn-ch1-แบบฝึกหัด-12.md",
    "แบบฝึกหัด 1.4": "silpakorn-ch1-แบบฝึกหัด-14.md",
    "บทที่ 2 บทนำ": "silpakorn-ch2-บทที่-2-บทนำ.md",
    "2.1 การอินทิเกรตโดยการแทน": "silpakorn-ch2-integration-by-substitution.md",
    "2.2 การอินทิเกรตโดยการแจงส่วน (Integration by Parts)": "silpakorn-ch2-integration-techniques-2-2.md",
    "2.3 การอินทิเกรตโดยการแจงเศษส่วนย่อย (Partial Fractions)": "silpakorn-ch2-integration-techniques-2-3.md",
    "แบบฝึกหัด 2.4": "silpakorn-ch2-แบบฝึกหัด-24.md",
    "2.5 อินทิกรัลที่ประกอบด้วยนิพจน์กำลังสอง": "silpakorn-ch2-integrals-with-quadratic.md",
    "บทที่ 3 บทนำ": "silpakorn-ch3-applications-of-integrals-บทที่-ch3-applications-of-integrals-บทนำ.md",
    "3.1 พื้นที่ภายใต้เส้นโค้ง": "silpakorn-ch3-area-under-curve.md",
    "3.2 ปริมาตรของของแข็ง (Volume of Solids)": "silpakorn-ch3-applications-of-integrals-3-2.md",
    "3.3 ความยาวของเส้นโค้ง (Arc Length)": "silpakorn-ch3-applications-of-integrals-3-3.md",
    "บทที่ 4 บทนำ": "silpakorn-ch4-บทที่-4-บทนำ.md",
    "4.1 อินทิกรัลจำกัดเขตของฟังก์ชันไม่ต่อเนื่องแบบมีขอบเขต": "silpakorn-ch4-improper-type1-discontinuous.md",
    "แบบฝึกหัด 4.1": "silpakorn-ch4-แบบฝึกหัด-41.md",
    "4.2.1 อินทิกรัลไม่ตรงแบบชนิดอินทิแกรนด์เป็นฟังก์ชันไม่มีขอบเขตบนช่วงจำกัด": "silpakorn-ch4-improper-type2-unbounded.md",
    "แบบฝึกหัด 4.2": "silpakorn-ch4-แบบฝึกหัด-42.md",
    # --- Silpakorn Calculus2 ch5-ch8 + solutions (OCR, cleaned) ---
    "บทที่ 5 บทนำ (พื้นผิวใน 3 มิติ)": "silpakorn-ch5-3d-surfaces-บทที่-ch5-3d-surfaces-บทนำ.md",
    "5.1 พื้นผิวในเอกภพสามมิติ": "silpakorn-ch5-3d-surfaces-5-1.md",
    "5.2 พื้นผิวจากสมการ": "silpakorn-ch5-3d-surfaces-5-2.md",
    "แบบฝึกหัด 5.2": "silpakorn-ch5-3d-surfaces-แบบฝึกหัด-52.md",
    "บทที่ 6 บทนำ (ฟังก์ชันหลายตัวแปร)": "silpakorn-ch6-multivariable-functions-บทที่-ch6-multivariable-functions-บทนำ.md",
    "6.1 ฟังก์ชันสองตัวแปร": "silpakorn-ch6-multivariable-functions-6-1.md",
    "6.2 ฟังก์ชันหลายตัวแปร": "silpakorn-ch6-multivariable-functions-6-2.md",
    "6.4 อินทิกรัลพื้นผิว": "silpakorn-ch6-multivariable-functions-6-4.md",
    "บทที่ 7 บทนำ (สมการออยกษ์)": "silpakorn-ch7-parametric-equations-บทที่-ch7-parametric-equations-บทนำ.md",
    "7.1 สมการพารามิเตอร์": "silpakorn-ch7-parametric-equations-7-1.md",
    "7.4 ปริพันธ์เส้น": "silpakorn-ch7-parametric-equations-7-4.md",
    "แบบฝึกหัด 7.3": "silpakorn-ch7-parametric-equations-แบบฝึกหัด-73.md",
    "แบบฝึกหัด 7.5": "silpakorn-ch7-parametric-equations-แบบฝึกหัด-75.md",
    "บทที่ 8 บทนำ (สมการเชิงอนุพันธ์)": "silpakorn-ch8-differential-equations-บทที่-ch8-differential-equations-บทนำ.md",
    "8.6 สมการเชิงอนุพันธ์": "silpakorn-ch8-differential-equations-8-6.md",
    "แบบฝึกหัด 8.5": "silpakorn-ch8-differential-equations-แบบฝึกหัด-85.md",
    "เฉลยแบบฝึกหัด (บทนำ)": "silpakorn-solutions-บทที่-solutions-บทนำ.md",
    "เฉลย 1.3": "silpakorn-solutions-แบบฝึกหัด-13.md",
    "เฉลย 3.2": "silpakorn-solutions-แบบฝึกหัด-32.md",
    "เฉลย 8.6": "silpakorn-solutions-8-6.md",
    "เฉลย 8.5": "silpakorn-solutions-แบบฝึกหัด-85.md",
    # --- Silpakorn Calculus1 ch1-ch5 + solutions (OCR, cleaned) ---
    "C1 บทที่ 1 บทนำ": "silpakorn-cal1-cal1_ch1-บทที่-cal1_ch1-บทนำ.md",
    "C1 แบบฝึกหัด 1.4": "silpakorn-cal1-cal1_ch1-แบบฝึกหัด-14.md",
    "C1 แบบฝึกหัด 1.5": "silpakorn-cal1-cal1_ch1-แบบฝึกหัด-15.md",
    "C1 บทที่ 2.1": "silpakorn-cal1-cal1_ch2-2-1.md",
    "C1 บทที่ 2 บทนำ": "silpakorn-cal1-cal1_ch2-บทที่-cal1_ch2-บทนำ.md",
    "C1 แบบฝึกหัด 2.3": "silpakorn-cal1-cal1_ch2-แบบฝึกหัด-23.md",
    "C1 แบบฝึกหัด 2.5": "silpakorn-cal1-cal1_ch2-แบบฝึกหัด-25.md",
    "C1 บทที่ 3.1": "silpakorn-cal1-cal1_ch3-3-1.md",
    "C1 บทที่ 3.6": "silpakorn-cal1-cal1_ch3-3-6.md",
    "C1 บทที่ 3 บทนำ": "silpakorn-cal1-cal1_ch3-บทที่-cal1_ch3-บทนำ.md",
    "C1 แบบฝึกหัด 3.5": "silpakorn-cal1-cal1_ch3-แบบฝึกหัด-35.md",
    "C1 บทที่ 3.6 (2)": "silpakorn-cal1-cal1_ch4-3-6.md",
    "C1 บทที่ 4.2": "silpakorn-cal1-cal1_ch4-4-2.md",
    "C1 บทที่ 4 บทนำ": "silpakorn-cal1-cal1_ch4-บทที่-cal1_ch4-บทนำ.md",
    "C1 แบบฝึกหัด 3.5 (2)": "silpakorn-cal1-cal1_ch4-แบบฝึกหัด-35.md",
    "C1 แบบฝึกหัด 4.2": "silpakorn-cal1-cal1_ch4-แบบฝึกหัด-42.md",
    "C1 บทที่ 5 บทนำ": "silpakorn-cal1-cal1_ch5-บทที่-cal1_ch5-บทนำ.md",
    "C1 แบบฝึกหัด 5.2": "silpakorn-cal1-cal1_ch5-แบบฝึกหัด-52.md",
    "C1 เฉลย บทนำ": "silpakorn-cal1-cal1_solutions-บทที่-cal1_solutions-บทนำ.md",
}


st.title("Integration Lessons")

st.markdown(
    """
## Learning objectives

เมื่อเรียนจากหน้านี้แล้ว ผู้เรียนควรสามารถ

1. อธิบายความหมายเบื้องต้นของอินทิเกรตได้
2. ใช้กฎพื้นฐานของอินทิเกรตกับฟังก์ชันง่าย ๆ ได้
3. ระบุข้อผิดพลาดที่พบบ่อย เช่น ลืม $+C$ หรือใช้ power rule ผิดกรณีได้
"""
)

selected_lesson = st.sidebar.radio(
    "Lesson",
    list(LESSONS.keys()),
    key="lesson_selector",
)

content = load_lesson(LESSONS[selected_lesson])
st.markdown(content)

st.divider()
st.subheader("สูตรสำคัญ")
st.latex(r"\int x^n\,dx = \frac{x^{n+1}}{n+1}+C,\quad n\ne -1")
st.latex(r"\int (f(x)+g(x))\,dx = \int f(x)\,dx+\int g(x)\,dx")
