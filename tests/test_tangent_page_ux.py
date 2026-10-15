"""UX regression tests for pages/tangent.py (tangent page only).

Scope: the tangent page experiment-first/disclosure pilot plus the tangent-specific
truthfulness defects reproduced on the live baseline (page sha256 4b4e0c09...):

  T1  long theory sat above the interactive experiment (controls, result, graph pushed
      down); the concept anchor and full theory must move into named collapsed expanders.
  T2  emoji leaked into user-visible labels/strings (badge, "จุดที่ควรสังเกต", theory
      expander, cautions, variable note).
  T3  wording implied the difference quotient is evaluated at ``h = 0``
      ("จุดทั้งสองเคลื่อนเข้าหากันจนเป็นจุดเดียว").
  T4  ``f'(a) = 0`` was labelled "(จุดวกกลับ/จุดวิกฤต)". A stationary point is not
      necessarily a turning point (``x^3`` at ``0``).
  T5  the full worked solution was rendered open instead of a collapsed expander.

The page must keep its existing controls/state keys and the exact solver/plotter APIs.
Tests assert behaviour through the page (AppTest) and through the public solver dict;
they do not assert on private helpers. This pilot deliberately adds NO secant plot and
NO ``h`` control (see test_no_new_secant_or_h_control_added).
"""

import re
from pathlib import Path

import pytest
from streamlit.testing.v1 import AppTest

from utils.tangent_solver import compute_tangent

PAGE = str(Path(__file__).resolve().parent.parent / "pages" / "tangent.py")
PAGE_SRC = Path(PAGE).read_text(encoding="utf-8")

BARE_LATEX_CMD = re.compile(r"\\[a-zA-Z]{2,}")
INLINE_OR_DISPLAY_MATH = re.compile(r"\$[^$]*\$")
# Emoji / pictograph blocks only (arrows such as U+2192 are covered separately).
EMOJI = re.compile("[\U0001F300-\U0001FAFF\u2600-\u26FF\u2700-\u27BF\u2B00-\u2BFF\uFE0F]")
EM_DASH = "\u2014"
RIGHT_ARROW = "\u2192"

# Expander names the refactor must expose (content preserved, not deleted)
NAMED_EXPANDERS = {
    "มโนทัศน์หลัก: ความชันเส้นสัมผัสมาจากลิมิตของเส้นตัดอย่างไร?",
    "รายละเอียดทฤษฎี ข้อควรระวัง และการประยุกต์ใช้เพิ่มเติม",
    "วิธีทำทีละขั้นตอนฉบับเต็ม (Full Worked Solution)",
}


def _render(expr: str, a: float) -> AppTest:
    at = AppTest.from_file(PAGE, default_timeout=120)
    at.run()
    assert not at.exception, at.exception
    at.text_input(key="tangent_expr").set_value(expr)
    at.slider(key="tangent_a").set_value(a)
    at.run()
    assert not at.exception, at.exception
    return at


def _visible_texts(at: AppTest) -> list:
    """All user-visible markdown/message strings on the rendered page."""
    out = [m.value for m in at.markdown]
    out += [m.value for m in at.caption]
    out += [e.value for e in at.info]
    out += [e.value for e in at.success]
    out += [e.value for e in at.warning]
    out += [e.value for e in at.error]
    return out


def _feedback(at: AppTest) -> str:
    """The single short per-case feedback string, identified by its 'สรุปสั้น' marker."""
    found = [v for v in _visible_texts(at) if "สรุปสั้น" in v]
    assert len(found) == 1, found
    return found[0]


def _raw_latex_leaks(at: AppTest) -> list:
    """Bare LaTeX commands rendered as plain text (outside $...$)."""
    leaks = []
    for text in _visible_texts(at):
        if not text or "<div" in text or "<span" in text or "<style" in text:
            continue
        residue = INLINE_OR_DISPLAY_MATH.sub("", text)
        found = BARE_LATEX_CMD.findall(residue)
        if found:
            leaks.append((sorted(set(found)), text[:160]))
    return leaks


# ---------------------------------------------------------------------------
# T1 / T5 — experiment first, instructional content behind named expanders
# ---------------------------------------------------------------------------
class TestPageLayout:
    def test_experiment_section_precedes_theory_section(self):
        at = _render("x^2", 1.0)
        md = [m.value for m in at.markdown]
        idx_experiment = next(i for i, v in enumerate(md) if "ลองสำรวจเส้นสัมผัส" in v)
        idx_theory = next(i for i, v in enumerate(md) if "มโนทัศน์หลักและทฤษฎี" in v)
        assert idx_experiment < idx_theory

    def test_result_metric_appears_before_theory(self):
        at = _render("x^2", 1.0)
        md = [m.value for m in at.markdown]
        idx_result = next(i for i, v in enumerate(md) if v.startswith("### ผลลัพธ์สมการเส้นสัมผัส"))
        idx_theory = next(i for i, v in enumerate(md) if "มโนทัศน์หลักและทฤษฎี" in v)
        assert idx_result < idx_theory

    def test_graph_is_rendered_next_to_the_controls(self):
        at = _render("x^2", 1.0)
        assert any(s.key == "tangent_a" for s in at.slider)
        assert len(at.get("image")) >= 1, "tangent graph (st.pyplot) was not rendered"
        # source order: tangent-point control, then the plot call, then the theory divider
        i_ctrl = PAGE_SRC.index("จุดสัมผัส a เลื่อนแล้วกราฟ")
        i_plot = PAGE_SRC.index("st.pyplot(fig)")
        i_theory = PAGE_SRC.index("### มโนทัศน์หลักและทฤษฎี")
        assert i_ctrl < i_plot < i_theory

    def test_named_expanders_present(self):
        at = _render("x^2", 1.0)
        labels = {e.label for e in at.expander}
        assert NAMED_EXPANDERS.issubset(labels)

    def test_concept_anchor_is_a_named_expander_not_open_container(self):
        at = _render("x^2", 1.0)
        labels = {e.label for e in at.expander}
        assert "มโนทัศน์หลัก: ความชันเส้นสัมผัสมาจากลิมิตของเส้นตัดอย่างไร?" in labels
        # The badge + concept block must sit inside that expander, i.e. after the
        # experiment header in source order (no fully open top-of-page container).
        i_experiment = PAGE_SRC.index("### ลองสำรวจเส้นสัมผัส")
        i_badge = PAGE_SRC.index("มโนทัศน์หลัก</span>")
        assert i_badge > i_experiment
        assert "with st.container(border=True):\n    col_badge" not in PAGE_SRC
        # Content preserved inside the expander.
        assert "จุดที่ควรสังเกต" in " ".join(_visible_texts(at))

    def test_full_worked_solution_is_collapsed_in_named_expander(self):
        at = _render("x^2", 1.0)
        assert "วิธีทำทีละขั้นตอนฉบับเต็ม (Full Worked Solution)" in {e.label for e in at.expander}
        assert 'st.expander("วิธีทำทีละขั้นตอนฉบับเต็ม (Full Worked Solution)", expanded=False):' in PAGE_SRC
        i_expander = PAGE_SRC.index("วิธีทำทีละขั้นตอนฉบับเต็ม (Full Worked Solution)")
        i_render_steps = PAGE_SRC.index("render_steps(res")
        assert i_expander < i_render_steps
        assert PAGE_SRC.count("render_steps(res") == 1  # single call site

    def test_parsed_equation_preview_retained(self):
        at = _render("x^2", 1.0)
        assert any("สมการที่ระบบเข้าใจ" in c.value for c in at.caption)

    def test_no_emoji_arrows_or_em_dash_in_page(self):
        assert not EMOJI.search(PAGE_SRC), EMOJI.findall(PAGE_SRC)
        assert EM_DASH not in PAGE_SRC
        assert RIGHT_ARROW not in PAGE_SRC
        page_labels = re.findall(r'st\.expander\(\s*"([^"]+)"', PAGE_SRC)
        assert page_labels
        assert [lb for lb in page_labels if EMOJI.search(lb)] == []
        fb = _feedback(_render("x^2", 1.0))
        assert not EMOJI.search(fb), fb

    def test_controls_and_state_keys_preserved(self):
        assert 'key="tangent_expr"' in PAGE_SRC
        assert 'key="tangent_a"' in PAGE_SRC
        for k in ("btn_tan_1", "btn_tan_2", "btn_tan_3", "btn_tan_4"):
            assert f'"{k}"' in PAGE_SRC
        assert 'render_math_keypad(target_key="tangent_expr", key_prefix="tan_kp"' in PAGE_SRC
        at = _render("x^2", 1.0)
        assert any(t.key == "tangent_expr" for t in at.text_input)
        assert any(s.key == "tangent_a" for s in at.slider)

    def test_no_new_secant_or_h_control_added(self):
        """Scope guard: this pilot adds no secant plot and no h control."""
        at = _render("x^2", 1.0)
        assert {s.key for s in at.slider} == {"tangent_a"}
        assert len(at.checkbox) == 0  # no "show secant" / "fix h" toggle
        assert PAGE_SRC.count("st.slider(") == 1
        # plot_tangent keeps its existing signature: a single call site
        assert PAGE_SRC.count("plot_tangent(") == 1
        assert "secant=" not in PAGE_SRC
        # absence is documented (later enhancement), not silently claimed as present
        assert "ยังไม่มีการวาดเส้นตัด (secant)" in PAGE_SRC


# ---------------------------------------------------------------------------
# T3 / T4 — truthful wording about h = 0 and stationary points
# ---------------------------------------------------------------------------
class TestTruthfulWording:
    def test_definition_does_not_claim_h_zero_is_valid(self):
        at = _render("x^2", 1.0)
        texts = " ".join(_visible_texts(at))
        assert "ไม่ใช่การแทนค่า" in texts
        assert "h = 0" in texts
        assert "จนเป็นจุดเดียว" not in PAGE_SRC

    def test_stationary_point_is_not_labelled_a_turning_point(self):
        # x^3 at 0: f'(0) = 0 but it is not a turning point.
        at = _render("x^3", 0.0)
        fb = _feedback(at)
        assert "จุดนิ่ง" in fb
        assert "ไม่จำเป็นต้องเป็นจุดวกกลับ" in fb
        assert "แนวนอน" in fb
        # every mention of "จุดวกกลับ" in the page is the corrective statement
        assert PAGE_SRC.count("จุดวกกลับ") == PAGE_SRC.count("ไม่จำเป็นต้องเป็นจุดวกกลับ") == 2
        assert "(จุดวกกลับ/จุดวิกฤต)" not in PAGE_SRC


# ---------------------------------------------------------------------------
# Required cases: polynomial, transcendental, decreasing, stationary,
# non-differentiable, undefined domain, blank input
# ---------------------------------------------------------------------------
class TestRequiredCases:
    def test_polynomial_increasing_case(self):
        at = _render("x^2", 1.0)
        assert [(m.label, m.value) for m in at.metric] == [("ความชันเส้นสัมผัส m = f'(a)", "2.0000")]
        assert "เพิ่มขึ้น" in _feedback(at)
        assert _raw_latex_leaks(at) == []

    def test_valid_transcendental_case(self):
        at = _render("sin(x)", 0.0)
        assert [(m.label, m.value) for m in at.metric] == [("ความชันเส้นสัมผัส m = f'(a)", "1.0000")]
        assert "เพิ่มขึ้น" in _feedback(at)

    def test_decreasing_case_reports_negative_slope(self):
        at = _render("x^3 - 3*x", 0.0)
        assert [m.value for m in at.metric] == ["-3.0000"]
        assert "ลดลง" in _feedback(at)

    def test_stationary_case_reports_zero_slope_and_stationary_point(self):
        at = _render("x^3", 0.0)
        assert [m.value for m in at.metric] == ["0.0000"]
        fb = _feedback(at)
        assert "จุดนิ่ง" in fb
        assert "แนวนอน" in fb

    def test_non_differentiable_abs_case(self):
        at = _render("abs(x)", 0.0)
        assert [m.value for m in at.metric] == ["ไม่มีค่า (หาอนุพันธ์ไม่ได้)"]
        fb = _feedback(at)
        assert "หาอนุพันธ์ไม่ได้" in fb
        assert "ไม่มีเส้นสัมผัส" in fb
        assert len(at.get("image")) >= 1, "curve with the corner point should still be plotted"
        assert _raw_latex_leaks(at) == []

    def test_undefined_domain_point_is_reported(self):
        at = _render("(x**2 - 4)/(x - 2)", 2.0)
        assert [m.value for m in at.metric] == []
        assert any("ไม่นิยาม" in e.value for e in at.error)
        assert "ไม่นิยาม" in _feedback(at)

    def test_out_of_domain_point_is_reported(self):
        at = _render("log(x)", -1.0)
        assert [m.value for m in at.metric] == []
        assert any("ไม่นิยาม" in e.value for e in at.error)

    def test_blank_input_prompts_for_a_function(self):
        at = AppTest.from_file(PAGE, default_timeout=120)
        at.run()
        at.text_input(key="tangent_expr").set_value("")
        at.run()
        assert not at.exception, at.exception
        assert any("กรุณาระบุฟังก์ชัน" in e.value for e in at.info)
        assert [m.value for m in at.metric] == []


# ---------------------------------------------------------------------------
# Controller behaviour + the existing (supported) h-sign solver branch
# ---------------------------------------------------------------------------
class TestControlsAndSupportedHBehaviour:
    def test_moving_tangent_point_updates_the_slope(self):
        assert [m.value for m in _render("x^2", 2.0).metric] == ["4.0000"]
        assert [m.value for m in _render("x^2", 1.0).metric] == ["2.0000"]

    def test_non_differentiable_branch_reports_h_signs_from_existing_api(self):
        """The abs() branch already computes one-sided derivatives as h -> 0^- / 0^+."""
        steps = compute_tangent("abs(x)", 0.0)["steps"]
        joined = " ".join(steps)
        assert "h \\to 0^-" in joined
        assert "h \\to 0^+" in joined
        assert "-1" in joined and "1" in joined


# ---------------------------------------------------------------------------
# Solver-facing sanity (the page consumes only these fields)
# ---------------------------------------------------------------------------
class TestSolverContractUsedByPage:
    @pytest.mark.parametrize(
        "expr,a,status",
        [
            ("x^2", 1.0, "finite"),
            ("sin(x)", 0.0, "finite"),
            ("x^3", 0.0, "finite"),
            ("abs(x)", 0.0, "non_differentiable"),
            ("(x**2 - 4)/(x - 2)", 2.0, "undefined_point"),
            ("log(x)", -1.0, "undefined_point"),
        ],
    )
    def test_status_fields_reported(self, expr, a, status):
        res = compute_tangent(expr, a)
        assert res.get("status") == status
        assert "result" in res and "latex" in res and "steps" in res and "variable" in res
