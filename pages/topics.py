import streamlit as st

from utils.content_loader import list_lessons
from utils.theme import render_hero

render_hero("เลือกหัวข้อ", "เลือกหัวข้อหลักที่ต้องการเรียนหรือฝึก")

lessons = list_lessons()
title_to_file = {item["title"]: item["filename"] for item in lessons}
all_titles = list(title_to_file.keys())


def find_lesson(*keywords: str) -> str | None:
    """Return the first lesson title matching all given keywords."""
    for title in all_titles:
        if all(k.lower() in title.lower() for k in keywords):
            return title
    return None


topics = [
    "ค่าจำกัด (Limit)",
    "อนุพันธ์ (Derivative)",
    "ปริพันธ์ (Integral)",
    "พื้นที่ใต้กราฟ (Area)",
    "ปริมาตร (Volume)",
    "ลำดับอนุกรม (Series)",
    "สมการเชิงอนุพันธ์ (ODE)",
    "ฟังก์ชันหลายตัวแปร (Multivariable)",
]

# ใช้ title ตรงๆ (auto-discovery) ไม่ hardcode filename
topic_mapping = {
    "ค่าจำกัด (Limit)": [find_lesson("1.1", "ปฏิยานุพันธ์")],
    "อนุพันธ์ (Derivative)": [find_lesson("2.1", "การอินทิเกรตโดยการแทน")],
    "ปริพันธ์ (Integral)": [find_lesson("1.1", "ปฏิยานุพันธ์")],
    "พื้นที่ใต้กราฟ (Area)": [find_lesson("3.1", "พื้นที่ภายใต้เส้นโค้ง")],
    "ปริมาตร (Volume)": [find_lesson("3.2", "ปริมาตร")],
    "ลำดับอนุกรม (Series)": [],
    "สมการเชิงอนุพันธ์ (ODE)": [find_lesson("8.6")],
    "ฟังก์ชันหลายตัวแปร (Multivariable)": [find_lesson("6.1", "ฟังก์ชันหลายตัวแปร")],
}

if hasattr(st, "pills"):
    selected_topic = st.pills("เลือกหัวข้อ", topics, default="ปริพันธ์ (Integral)")
else:
    selected_topic = st.radio("เลือกหัวข้อ", topics, horizontal=True, index=2)

st.divider()

if selected_topic:
    mapped = [t for t in topic_mapping.get(selected_topic, []) if t is not None]
    if mapped:
        st.markdown(f"### เนื้อหาสำหรับหัวข้อ {selected_topic}")
        for title in mapped:
            st.markdown(f"- **{title}**")
            if st.button(f"เริ่มเรียน: {title}", key=f"btn_topic_{title}"):
                st.session_state["selected_lesson_key"] = title
                st.switch_page("pages/lessons.py")
    else:
        st.markdown("หัวข้อนี้ยังอยู่ในระหว่างจัดทำ")
