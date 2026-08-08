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
riemann_page = st.Page("pages/riemann.py", title="พื้นที่ใต้กราฟ (Riemann)")
tangent_page = st.Page("pages/tangent.py", title="เส้นสัมผัสและอนุพันธ์")
limit_page = st.Page("pages/limit_approach.py", title="ลิมิตเข้าใกล้จุด")
substitution_page = st.Page("pages/substitution.py", title="การอินทิเกรตโดยการแทน")
volume_page = st.Page("pages/volume_revolution.py", title="ปริมาตรของทรงตัน")
area_between_page = st.Page("pages/area_between.py", title="พื้นที่ระหว่างเส้นโค้ง")
improper_page = st.Page("pages/improper_integrals.py", title="อินทิกรัลไม่แท้")
solver_page = st.Page("pages/solver.py", title="แก้โจทย์")
quiz_page = st.Page("pages/quiz.py", title="เกมทบทวน")
history_page = st.Page("pages/history.py", title="ประวัติที่ทำ")
help_page = st.Page("pages/help.py", title="ช่วยเหลือ")

pg = st.navigation(
    {
        "หน้าหลัก": [home_page],
        "เรียน": [
            lessons_page,
            topics_page,
            riemann_page,
            tangent_page,
            limit_page,
            substitution_page,
            volume_page,
            area_between_page,
            improper_page,
        ],
        "ฝึก": [solver_page, quiz_page],
        "อื่น ๆ": [history_page, help_page],
    },
    position="sidebar",
)

inject_css()

pg.run()
