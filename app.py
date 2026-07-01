import streamlit as st


st.set_page_config(
    page_title="Calculus Tutor: Integration",
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

home = st.Page("pages/home.py", title="Home")
lessons = st.Page("pages/lessons.py", title="Lessons")
quiz = st.Page("pages/quiz.py", title="Quiz")

pg = st.navigation(
    {
        "Main": [home],
        "Learn": [lessons],
        "Assess": [quiz],
    }
)

pg.run()
