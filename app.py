import streamlit as st
from utils.theme import inject_css


st.set_page_config(
    page_title="MATH tutor",
    page_icon="∫",
    layout="wide",
)


def initialize_session_state() -> None:
    if "quiz_scores" not in st.session_state:
        st.session_state.quiz_scores = {}
    if "quiz_answers" not in st.session_state:
        st.session_state.quiz_answers = {}
    if "quiz_submitted" not in st.session_state:
        st.session_state.quiz_submitted = False


initialize_session_state()

home_page = st.Page("pages/home.py", title="หน้าหลัก")
lessons_page = st.Page("pages/lessons.py", title="บทเรียน")
topics_page = st.Page("pages/topics.py", title="เลือกหัวข้อ")
solver_page = st.Page("pages/solver.py", title="แก้โจทย์")
quiz_page = st.Page("pages/quiz.py", title="เกมทบทวน")
history_page = st.Page("pages/history.py", title="ประวัติที่ทำ")
help_page = st.Page("pages/help.py", title="ช่วยเหลือ")

pg = st.navigation(
    {
        "หน้าหลัก": [home_page],
        "เรียน": [lessons_page, topics_page],
        "ฝึก": [solver_page, quiz_page],
        "อื่น ๆ": [history_page, help_page],
    },
    position="sidebar",
)

inject_css()

pg.run()
