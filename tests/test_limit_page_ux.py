"""UX regression tests for pages/limit_approach.py (limit page only).

Scope: limit page layout/feedback + the limit-specific math-text defects that were
reproduced on the live page at the recorded baseline hashes:

  D1  raw ``\\lim_{x \\to 2}`` leaked as plain text inside a worked-solution step
      (utils/limit_solver.py `_steps_indeterminate_factoring`).
  D2  raw ``\\lim ... \\neq \\lim ...`` leaked as plain text in the 1/x DNE summary
      (utils/limit_solver.py `_steps_infinite_asymptote`) and in the
      absolute-value/piecewise summaries (`_steps_abs_piecewise`).
  D3  long theory sat above the interactive experiment, pushing inputs/graph far
      down the page, and the left-right explanation was repeated per case.
  D4  left-right guidance was overrestrictive (abs/piecewise only) although a
      ``c/0`` vertical-asymptote case such as ``1/x`` also needs two-sided analysis.
  D5  the short per-case feedback invented a method the solver never reported
      (finite => substitution/algebra, infinite => a vanishing denominator,
      dne => unequal one-sided values). The contrasting cases below pin the fix.
  D6  the main concept hierarchy was a fully open ``st.container`` at the bottom
      instead of a named collapsed expander, and page labels carried emoji.

Tests assert behaviour through the page (AppTest) and through the public solver
dict; they do not assert on private helpers.
"""

import re
from pathlib import Path

import pytest
from streamlit.testing.v1 import AppTest

from utils.limit_solver import compute_limit_near

PAGE = str(Path(__file__).resolve().parent.parent / "pages" / "limit_approach.py")
PAGE_SRC = Path(PAGE).read_text(encoding="utf-8")

BARE_LATEX_CMD = re.compile(r"\\[a-zA-Z]{2,}")
INLINE_OR_DISPLAY_MATH = re.compile(r"\$[^$]*\$")
# Emoji / pictograph blocks only (arrows such as U+2192 are covered elsewhere).
EMOJI = re.compile("[\U0001F300-\U0001FAFF\u2600-\u26FF\u2700-\u27BF\u2B00-\u2BFF\uFE0F]")

# Expander names the refactor must expose (instructional content preserved, not deleted)
NAMED_EXPANDERS = {
    "ควรเลือกวิธีหาลิมิตอย่างไร?",
    "รายละเอียดทฤษฎี ข้อควรระวัง และการประยุกต์ใช้เพิ่มเติม",
    "มโนทัศน์ลิมิตซ้าย-ขวา และเหตุใดบางโจทย์จึงต้องแยกพิจารณา",
    "มโนทัศน์: ลิมิตที่อนันต์และเส้นกำกับแนวนอน",
}


def _render(expr: str, a: str) -> AppTest:
    at = AppTest.from_file(PAGE, default_timeout=90)
    at.run()
    assert not at.exception, at.exception
    at.text_input(key="limit_expr").set_value(expr)
    at.text_input(key="limit_a_str").set_value(a)
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
    return out


def _feedback(at: AppTest) -> str:
    """The single short per-case feedback string, identified by its 'สรุปสั้น' marker."""
    found = [v for v in _visible_texts(at) if "สรุปสั้น" in v]
    assert len(found) == 1, found
    return found[0]


def _raw_latex_leaks(at: AppTest) -> list:
    """Bare LaTeX commands rendered as plain text (outside $...$) — the D1/D2 defect."""
    leaks = []
    for text in _visible_texts(at):
        if not text or "<div" in text or "<span" in text or "<style" in text:
            continue
        residue = INLINE_OR_DISPLAY_MATH.sub("", text)
        found = BARE_LATEX_CMD.findall(residue)
        if found:
            leaks.append((sorted(set(found)), text[:160]))
    return leaks


def _multi_line_worked_math_lines(step: str) -> list:
    """Sub-lines of a step that render_steps sends to st.markdown.

    Mirrors utils.math_render.render_steps' multi-line branch: a step whose body
    (after the first ':') contains a newline is split, and Thai-bearing sub-lines
    go through st.markdown (so undelimited LaTeX there leaks as plain text).
    """
    s = str(step).strip()
    if ":" not in s or "\n" not in s:
        return []
    body = s.split(":", 1)[1]
    return [ln.strip() for ln in body.split("\n") if ln.strip() and re.search(r"[\u0e00-\u0e7f]", ln)]


# ---------------------------------------------------------------------------
# D1 / D2 — solver step text must delimit math on Thai-bearing lines
# ---------------------------------------------------------------------------
class TestSolverStepMathDelimiters:
    @pytest.mark.parametrize(
        "expr,a",
        [
            ("(x**2 - 4)/(x - 2)", "2"),
            ("(x**2 - 9)/(x - 3)", "3"),
            ("1/x", "0"),
            ("1/x**2", "0"),
            ("abs(x)/x", "0"),
            ("abs(x)", "0"),
            ("sin(1/x)", "0"),
        ],
    )
    def test_no_bare_latex_on_thai_step_lines(self, expr, a):
        res = compute_limit_near(expr, a)
        assert res["ok"] is True
        offenders = []
        for step in res["steps"]:
            for line in _multi_line_worked_math_lines(step):
                residue = INLINE_OR_DISPLAY_MATH.sub("", line)
                found = BARE_LATEX_CMD.findall(residue)
                if found:
                    offenders.append((sorted(set(found)), line[:140]))
        assert not offenders, offenders

    def test_dne_summary_delimits_both_limits(self):
        """1/x summary: the Thai-bearing line must have lim/neq inside math."""
        step = compute_limit_near("1/x", 0)["steps"][-1]
        thai_lines = [ln for ln in step.split("\n") if re.search(r"[\u0e00-\u0e7f]", ln)]
        assert thai_lines
        for line in thai_lines:
            residue = INLINE_OR_DISPLAY_MATH.sub("", line)
            assert "\\lim" not in residue, line
            assert "\\neq" not in residue, line

    def test_indeterminate_step_does_not_claim_f_a_equals_zero_over_zero(self):
        """The solver must not print f(a) = 0/0 (that is the form, not f(a))."""
        res = compute_limit_near("(x**2 - 4)/(x - 2)", 2)
        joined = "\n".join(res["steps"])
        assert "f(2) = \\frac{0}{0}" not in joined
        assert "f(2) = \\frac{0}{0}" not in joined.replace("$$", "$")


# ---------------------------------------------------------------------------
# D3 / D6 — experiment first, instructional content collapsed into named expanders
# ---------------------------------------------------------------------------
class TestPageLayout:
    def test_experiment_section_precedes_theory_section(self):
        at = _render("(x**2 - 4)/(x - 2)", "2")
        md = [m.value for m in at.markdown]
        idx_experiment = next(i for i, v in enumerate(md) if "ลองสำรวจการลู่เข้าของลิมิต" in v)
        idx_theory = next(i for i, v in enumerate(md) if "ไม่ได้เริ่มด้วยการแยกซ้าย-ขวา" in v)
        assert idx_experiment < idx_theory

    def test_result_metric_appears_before_theory(self):
        at = _render("(x**2 - 4)/(x - 2)", "2")
        md = [m.value for m in at.markdown]
        idx_result = next(i for i, v in enumerate(md) if v.startswith("### ผลลัพธ์ลิมิต"))
        idx_theory = next(i for i, v in enumerate(md) if "ไม่ได้เริ่มด้วยการแยกซ้าย-ขวา" in v)
        assert idx_result < idx_theory

    def test_graph_is_rendered_next_to_delta_control(self):
        at = _render("(x**2 - 4)/(x - 2)", "2")
        assert any(s.key == "limit_delta" for s in at.slider)
        assert len(at.get("image")) >= 1, "graph (st.pyplot) was not rendered"
        # source order: delta control, then the plot call, then the theory divider
        i_delta = PAGE_SRC.index("ระยะ delta ควบคุมช่วงที่กราฟ")
        i_plot = PAGE_SRC.index("st.pyplot(fig)")
        i_theory = PAGE_SRC.index("### มโนทัศน์หลักและทฤษฎี")
        assert i_delta < i_plot < i_theory

    def test_named_expanders_present(self):
        at = _render("(x**2 - 4)/(x - 2)", "2")
        labels = {e.label for e in at.expander}
        assert NAMED_EXPANDERS.issubset(labels)

    def test_main_hierarchy_is_a_named_collapsed_expander(self):
        at = _render("(x**2 - 4)/(x - 2)", "2")
        labels = {e.label for e in at.expander}
        assert "ควรเลือกวิธีหาลิมิตอย่างไร?" in labels
        # It must be an expander, not a fully open container, and start collapsed.
        assert 'st.expander("ควรเลือกวิธีหาลิมิตอย่างไร?", expanded=False):' in PAGE_SRC
        assert "with st.container(border=True):\n    col_badge" not in PAGE_SRC
        # Content preserved inside the expander.
        assert "ลำดับการคิด 3 ขั้น" in " ".join(_visible_texts(at))

    def test_parsed_equation_preview_retained(self):
        at = _render("(x**2 - 4)/(x - 2)", "2")
        assert any("สมการที่ระบบเข้าใจ" in c.value for c in at.caption)

    def test_left_right_explanation_appears_once(self):
        at = _render("(x**2 - 4)/(x - 2)", "2")
        occurrences = [v for v in _visible_texts(at) if "หัวใจสำคัญของการมีลิมิตสองด้าน" in v]
        assert len(occurrences) == 1

    def test_no_emoji_in_page_labels_or_strings(self):
        # The touched page source itself must be emoji-free (all page strings are literals here).
        assert not EMOJI.search(PAGE_SRC), EMOJI.findall(PAGE_SRC)
        # Expander labels the page declares must be emoji-free.
        page_labels = re.findall(r'st\.expander\(\s*"([^"]+)"', PAGE_SRC)
        assert page_labels
        assert [lb for lb in page_labels if EMOJI.search(lb)] == []
        # The rendered short feedback must be emoji-free too.
        fb = _feedback(_render("(x**2 - 4)/(x - 2)", "2"))
        assert not EMOJI.search(fb), fb


# ---------------------------------------------------------------------------
# Required cases: default removable discontinuity, 1/x, infinity
# ---------------------------------------------------------------------------
class TestRequiredCases:
    def test_default_removable_discontinuity(self):
        at = _render("(x**2 - 4)/(x - 2)", "2")
        assert [m.value for m in at.metric] == ["4.0000"]
        fb = _feedback(at)
        assert "4.0000" in fb
        assert len(at.get("dataframe")) >= 1, "numeric table missing"
        assert "วิธีทำทีละขั้นตอนฉบับเต็ม (Full Worked Solution)" in {e.label for e in at.expander}
        assert _raw_latex_leaks(at) == []

    def test_one_over_x_needs_two_sided_analysis(self):
        at = _render("1/x", "0")
        assert [m.value for m in at.metric] == ["ลิมิตหาค่าไม่ได้"]
        fb = _feedback(at)
        assert "หาค่าไม่ได้" in fb
        assert _raw_latex_leaks(at) == []

    def test_infinity_case(self):
        at = _render("(2*x**2 + 1)/(3*x**2 - 5)", "inf")
        assert [m.value for m in at.metric] == ["0.6667"]
        labels = {e.label for e in at.expander}
        assert any("ตัวแปรขยายสู่ขนาดใหญ่" in lb for lb in labels)
        assert len(at.get("dataframe")) >= 1
        assert _raw_latex_leaks(at) == []

    def test_absolute_value_case_has_no_raw_latex(self):
        at = _render("abs(x)/x", "0")
        assert _raw_latex_leaks(at) == []


# ---------------------------------------------------------------------------
# D5 — short per-case feedback must not invent a method the solver never used
# ---------------------------------------------------------------------------
class TestShortCaseFeedbackAccuracy:
    def test_removable_discontinuity_shows_undefined_f_a_versus_the_limit(self):
        fb = _feedback(_render("(x**2 - 4)/(x - 2)", "2"))
        assert "4.0000" in fb
        assert "ไม่นิยาม" in fb           # f(2) is undefined (a hole)
        assert "แทนค่าตรง" not in fb       # method must not be invented
        assert "จัดรูปพีชคณิต" not in fb

    def test_finite_transcendental_case_does_not_claim_substitution(self):
        fb = _feedback(_render("sin(x)/x", "0"))
        assert "1.0000" in fb
        assert "ไม่นิยาม" in fb            # sin(0)/0 is a hole, not a value
        assert "แทนค่าตรง" not in fb
        assert "จัดรูปพีชคณิต" not in fb

    def test_infinite_at_remote_target_is_end_behavior_not_vertical_asymptote(self):
        at = _render("x**2", "inf")
        assert [m.value for m in at.metric] == ["∞ (อนันต์)"]
        fb = _feedback(at)
        assert "ลู่ออก" in fb
        assert "เส้นกำกับแนวดิ่ง" not in fb
        assert "ตัวส่วนลู่เข้าศูนย์" not in fb

    def test_oscillating_dne_is_not_reported_as_unequal_one_sided_values(self):
        at = _render("sin(1/x)", "0")
        assert [m.value for m in at.metric] == ["ลิมิตหาค่าไม่ได้"]
        fb = _feedback(at)
        assert "แกว่งกวัด" in fb
        assert "หาค่าไม่ได้" in fb
        assert "ลิมิตทางซ้าย" not in fb     # not caused by unequal one-sided limits

    def test_one_over_x_reports_both_infinite_one_sided_limits(self):
        fb = _feedback(_render("1/x", "0"))
        assert "หาค่าไม่ได้" in fb
        assert "-∞" in fb and "+∞" in fb

    def test_domain_boundary_case_is_right_sided_only(self):
        at = _render("log(x)", "0")
        assert [m.value for m in at.metric] == ["หาค่าไม่ได้"]
        fb = _feedback(at)
        assert "ทางขวา" in fb
        assert "เส้นกำกับแนวดิ่ง" not in fb
        assert "ตัวส่วนลู่เข้าศูนย์" not in fb

    def test_finite_limit_at_infinity_mentions_remote_behaviour(self):
        fb = _feedback(_render("(2*x**2 + 1)/(3*x**2 - 5)", "inf"))
        assert "0.6667" in fb
        assert "พฤติกรรมระยะไกล" in fb
        assert "แทนค่าตรง" not in fb


# ---------------------------------------------------------------------------
# D4 — left-right guidance must not be overrestrictive, and 0/0 wording precise
# ---------------------------------------------------------------------------
class TestGuidanceWording:
    def test_left_right_note_mentions_vertical_asymptote_case(self):
        at = _render("1/x", "0")
        texts = " ".join(_visible_texts(at))
        assert "ตัวส่วนลู่เข้าศูนย์" in texts

    def test_zero_over_zero_wording_is_precise(self):
        at = _render("(x**2 - 4)/(x - 2)", "2")
        texts = " ".join(_visible_texts(at))
        assert "ไม่ได้หมายความว่าค่าฟังก์ชัน" in texts
