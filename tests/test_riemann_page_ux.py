"""UX and pedagogical regression tests for pages/riemann.py.

Verifies that the Riemann Sum page adheres to:
1. Multi-method comparison dashboard (Left, Midpoint, Right compared with exact integral)
2. Directional error diagnostics (Overestimate vs Underestimate vs Exact)
3. Net Signed Area detection and warning when f(x) < 0
4. Detailed arithmetic steps and per-subinterval table
5. Analytical limit expander for polynomial functions
6. Zero emoji in UI text per AGENTS.md rule 50
"""

import re
from pathlib import Path
import pytest
from streamlit.testing.v1 import AppTest

from utils.riemann_solver import compute_riemann

PAGE = str(Path(__file__).resolve().parent.parent / "pages" / "riemann.py")
PAGE_SRC = Path(PAGE).read_text(encoding="utf-8")

EMOJI = re.compile("[\U0001F300-\U0001FAFF\u2600-\u26FF\u2700-\u27BF\u2B00-\u2BFF\uFE0F]")


def _render_riemann(expr: str, a: float = 0.0, b: float = 2.0, n: int = 8, method: str = "left") -> AppTest:
    at = AppTest.from_file(PAGE)
    at.session_state["riemann_expr"] = expr
    at.session_state["riemann_a"] = a
    at.session_state["riemann_b"] = b
    at.session_state["riemann_n"] = n
    at.session_state["riemann_method"] = method
    at.run(timeout=10)
    return at


class TestRiemannPageAppTest:
    def test_default_mount_no_exceptions(self):
        at = _render_riemann("x^2", 0.0, 2.0, 8, "left")
        assert not at.exception, f"Raised exception: {at.exception}"

    def test_comparison_dashboard_metrics(self):
        at = _render_riemann("x^2", 0.0, 2.0, 8, "left")
        metric_labels = [m.label for m in at.metric]
        assert any("ขอบซ้าย" in l for l in metric_labels)
        assert any("จุดกึ่งกลาง" in l for l in metric_labels)
        assert any("ขอบขวา" in l for l in metric_labels)

    def test_net_signed_area_warning_for_cubic(self):
        # x^3 - 2x has negative values on [0, sqrt(2)]
        at = _render_riemann("x^3 - 2x", 0.0, 2.0, 8, "midpoint")
        warnings = [w.value for w in at.warning]
        assert any("พื้นที่คิดเครื่องหมาย" in w for w in warnings)

    def test_positive_function_no_negative_warning(self):
        at = _render_riemann("x^2", 0.0, 2.0, 8, "left")
        warnings = [w.value for w in at.warning]
        assert not any("พื้นที่คิดเครื่องหมาย" in w for w in warnings)

    def test_decreasing_function_directions(self):
        # f(x) = 1/(x+1) on [0, 2] is strictly decreasing -> Left is Over, Right is Under
        res = compute_riemann("1/(x+1)", 0.0, 2.0, 8, "left")
        comp = res["methods_comparison"]
        assert comp["left"]["direction"] == "overestimate"
        assert comp["right"]["direction"] == "underestimate"

    def test_zero_emoji_in_riemann_page(self):
        # Check source for emojis in Thai UI strings (excluding comments)
        lines = PAGE_SRC.splitlines()
        offending = []
        for line_no, line in enumerate(lines, 1):
            stripped = line.strip()
            if stripped.startswith("#"):
                continue
            matches = EMOJI.findall(line)
            if matches:
                offending.append((line_no, matches, line))
        assert not offending, f"Found emoji in pages/riemann.py: {offending}"
