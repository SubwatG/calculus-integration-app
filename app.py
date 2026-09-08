import streamlit as st
from utils.theme import inject_css

st.set_page_config(
    page_title="Calculus Learning Sandbox",
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

# -----------------------------------------------------------------------------
# 1. ภาพรวมระบบ (Overview)
# -----------------------------------------------------------------------------
home_page = st.Page("pages/home.py", title="หน้าหลัก", icon="🏠")
lessons_page = st.Page("pages/lessons.py", title="ภาพรวมบทเรียนและทฤษฎี", icon="📖")

# -----------------------------------------------------------------------------
# 2. โมดูลการเรียนรู้ (6 หัวข้อหลักตามโครงร่างโครงงาน)
# -----------------------------------------------------------------------------
tangent_page = st.Page("pages/tangent.py", title="1. เส้นสัมผัสและอนุพันธ์", icon="📈")
limit_page = st.Page("pages/limit_approach.py", title="2. ลิมิตเข้าใกล้จุด", icon="🎯")
riemann_page = st.Page("pages/riemann.py", title="3. ผลรวมรีมันน์ (พื้นที่ใต้กราฟ)", icon="📊")
substitution_page = st.Page("pages/substitution.py", title="4. เทคนิคการอินทิเกรต (u-Sub & By Parts)", icon="🧩")
area_between_page = st.Page("pages/area_between.py", title="5. พื้นที่ระหว่างเส้นโค้ง", icon="📐")
improper_page = st.Page("pages/improper_integrals.py", title="6. ปริพันธ์ไม่ตรงแบบ", icon="♾️")

# -----------------------------------------------------------------------------
# 3. เครื่องมือและการประเมิน (Tools & Assessment)
# -----------------------------------------------------------------------------
solver_page = st.Page("pages/solver.py", title="เครื่องคิดเลขสัญลักษณ์ SymPy", icon="⚙️")
quiz_page = st.Page("pages/quiz.py", title="แบบทดสอบมโนทัศน์ (มีคำใบ้)", icon="📝")

# -----------------------------------------------------------------------------
# 4. ข้อมูลระบบ (System Info)
# -----------------------------------------------------------------------------
history_page = st.Page("pages/history.py", title="ประวัติคะแนนในเซสชัน", icon="🏆")
help_page = st.Page("pages/help.py", title="คู่มือการใช้งานและโครงงาน", icon="ℹ️")

pg = st.navigation(
    {
        "ภาพรวม": [home_page, lessons_page],
        "โมดูลการเรียนรู้ (6 หัวข้อหลัก)": [
            tangent_page,
            limit_page,
            riemann_page,
            substitution_page,
            area_between_page,
            improper_page,
        ],
        "เครื่องมือและการประเมิน": [solver_page, quiz_page],
        "ข้อมูลระบบ": [history_page, help_page],
    },
    position="sidebar",
)

inject_css()

pg.run()
