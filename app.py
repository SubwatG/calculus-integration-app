import streamlit as st
from utils.theme import inject_css

st.set_page_config(
    page_title="Calculus Learning Sandbox",
    page_icon=":material/square_foot:",
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

# -----------------------------------------------------------------------------
# 1. ภาพรวมระบบ (Overview)
# -----------------------------------------------------------------------------
home_page = st.Page("pages/home.py", title="หน้าหลัก", icon=":material/home:")
lessons_page = st.Page("pages/lessons.py", title="ภาพรวมบทเรียนและทฤษฎี", icon=":material/menu_book:")

# -----------------------------------------------------------------------------
# 2. โมดูลการเรียนรู้ (ลำดับตามหลักสูตรแคลคูลัส)
# -----------------------------------------------------------------------------
limit_page = st.Page("pages/limit_approach.py", title="1. ลิมิตเข้าใกล้จุด", icon=":material/adjust:")
tangent_page = st.Page("pages/tangent.py", title="2. เส้นสัมผัสและอนุพันธ์", icon=":material/trending_up:")
riemann_page = st.Page("pages/riemann.py", title="3. ผลรวมรีมันน์ (พื้นที่ใต้กราฟ)", icon=":material/bar_chart:")
substitution_page = st.Page("pages/substitution.py", title="4. เทคนิคการอินทิเกรต (u-Sub & By Parts)", icon=":material/sync:")
area_between_page = st.Page("pages/area_between.py", title="5. พื้นที่ระหว่างเส้นโค้ง", icon=":material/area_chart:")
volume_page = st.Page("pages/volume_revolution.py", title="6. ปริมาตรของรูปทรงตัน", icon=":material/rotate_right:")
improper_page = st.Page("pages/improper_integrals.py", title="7. ปริพันธ์ไม่ตรงแบบ", icon=":material/all_inclusive:")

# -----------------------------------------------------------------------------
# 3. เครื่องมือและการประเมิน (Tools & Assessment)
# -----------------------------------------------------------------------------
solver_page = st.Page("pages/solver.py", title="เครื่องคิดเลขสัญลักษณ์ SymPy", icon=":material/calculate:")
quiz_page = st.Page("pages/quiz.py", title="แบบทดสอบมโนทัศน์ (มีคำใบ้)", icon=":material/lightbulb:")
survey_page = st.Page("pages/survey.py", title="แบบประเมินความพึงพอใจ (SUS)", icon=":material/rate_review:")

# -----------------------------------------------------------------------------
# 4. ข้อมูลระบบ (System Info)
# -----------------------------------------------------------------------------
history_page = st.Page("pages/history.py", title="ประวัติคะแนนในเซสชัน", icon=":material/history:")
help_page = st.Page("pages/help.py", title="คู่มือการใช้งานและโครงงาน", icon=":material/help:")
creators_page = st.Page("pages/creators.py", title="ประวัติคณะผู้จัดทำ", icon=":material/group:")

pg = st.navigation(
    {
        "ภาพรวมระบบ": [home_page, lessons_page],
        "โมดูลการเรียนรู้": [
            limit_page,
            tangent_page,
            riemann_page,
            substitution_page,
            area_between_page,
            volume_page,
            improper_page,
        ],
        "เครื่องมือและการประเมิน": [solver_page, quiz_page, survey_page],
        "ข้อมูลโครงงาน": [history_page, help_page, creators_page],
    },
    position="sidebar",
)

inject_css()

pg.run()
