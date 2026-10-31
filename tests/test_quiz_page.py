from pathlib import Path
from streamlit.testing.v1 import AppTest

PAGES_DIR = Path(__file__).resolve().parent.parent / "pages"
QUIZ_PAGE = str(PAGES_DIR / "quiz.py")


def test_quiz_page_initial_render():
    at = AppTest.from_file(QUIZ_PAGE)
    at.run(timeout=5)
    assert not at.exception
    assert at.session_state.quiz_q_index == 0
    assert at.session_state.quiz_score == 0


def test_quiz_reshuffle():
    at = AppTest.from_file(QUIZ_PAGE)
    at.run(timeout=5)
    assert not at.exception

    btn_reshuffle = at.button(key="btn_reshuffle_now")
    assert btn_reshuffle is not None
    btn_reshuffle.click().run(timeout=5)
    assert not at.exception
    assert at.session_state.quiz_round >= 1


def test_quiz_answer_and_hint_progression():
    at = AppTest.from_file(QUIZ_PAGE)
    at.run(timeout=5)
    assert not at.exception

    # Select topic radio
    topic_radio = at.radio(key="quiz_topic_selector_main")
    assert topic_radio is not None
    assert len(topic_radio.options) >= 1

    # Radio choice key for the question: radio_choice_{round}_{q_idx}_{attempt}
    r_key = f"radio_choice_{at.session_state.quiz_round}_{at.session_state.quiz_q_index}_{at.session_state.quiz_attempt_count}"
    choice_radio = at.radio(key=r_key)
    assert choice_radio is not None
    choice_radio.set_value(0).run(timeout=5)
    assert not at.exception

    # Submit button
    btn_submit = at.button(key=f"btn_submit_{at.session_state.quiz_q_index}")
    if btn_submit:
        btn_submit.click().run(timeout=5)
        assert not at.exception
