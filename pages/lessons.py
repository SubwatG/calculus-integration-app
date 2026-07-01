import streamlit as st

from utils.content_loader import load_lesson


LESSONS = {
    "Integration Overview": "overview.md",
    "Basic Integration Rules": "basic_rules.md",
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
