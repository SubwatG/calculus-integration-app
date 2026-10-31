from pathlib import Path
from streamlit.testing.v1 import AppTest

PAGES_DIR = Path(__file__).resolve().parent.parent / "pages"
SUB_PAGE = str(PAGES_DIR / "substitution.py")


def test_substitution_page_initial_render():
    at = AppTest.from_file(SUB_PAGE)
    at.run(timeout=5)
    assert not at.exception
    assert len(at.title) >= 1 or len(at.markdown) >= 1


def test_substitution_preset_click_and_compute():
    at = AppTest.from_file(SUB_PAGE)
    at.run(timeout=5)
    assert not at.exception

    # Click first preset button
    btn_preset = at.button(key="pre_sub_1")
    assert btn_preset is not None
    btn_preset.click().run(timeout=5)
    assert not at.exception
    assert at.session_state.substitution_expr == "2x*sqrt(x^2+1)"

    # Click calculate button
    btn_calc = at.button(key="btn_substitution_calc")
    assert btn_calc is not None
    btn_calc.click().run(timeout=5)
    assert not at.exception


def test_substitution_decision_gate_radio():
    at = AppTest.from_file(SUB_PAGE)
    at.run(timeout=5)
    assert not at.exception

    # Interact with radio for case 1 u-choice if present
    if at.radio(key="radio_u_case1"):
        r = at.radio(key="radio_u_case1")
        # Change selection to correct choice
        r.set_value(r.options[0]).run(timeout=5)
        assert not at.exception
