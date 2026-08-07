import streamlit as st

from utils.content_loader import list_lessons, load_lesson
from utils.theme import render_hero

render_hero("บทเรียน", "เนื้อหาบทเรียนเรียงตามลำดับ")

with st.expander("คำอธิบายรายวิชา", expanded=False):
    st.markdown("ประมวลเนื้อหาบทเรียนแคลคูลัสและการประยุกต์ พร้อมตัวอย่างขั้นตอนคำนวณและแบบฝึกหัด")

lessons = list_lessons()
if not lessons:
    st.warning("ไม่พบบทเรียนใน data/lessons/")
    st.stop()

lesson_titles = [item["title"] for item in lessons]
title_to_file = {item["title"]: item["filename"] for item in lessons}

default_index = 0
if "selected_lesson_key" in st.session_state and st.session_state["selected_lesson_key"] in title_to_file:
    default_index = lesson_titles.index(st.session_state["selected_lesson_key"])

selected_lesson = st.selectbox(
    "เลือกบทเรียน",
    lesson_titles,
    index=default_index,
    key="selectbox_lesson",
)

content = load_lesson(title_to_file[selected_lesson])
st.markdown(content)

st.divider()
st.subheader("สูตรสำคัญ")
st.latex(r"\int x^n\,dx = \frac{x^{n+1}}{n+1}+C,\quad n\ne -1")
st.latex(r"\int (f(x)+g(x))\,dx = \int f(x)\,dx+\int g(x)\,dx")
