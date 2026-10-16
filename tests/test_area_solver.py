"""Test สำหรับ test_area_solver.py

TODO: นักศึกษา implement solver ให้ test นี้ผ่าน
ค่าคาดหวังอ้างอิงจาก docs/interactive-lessons-plan.md
"""

import pytest

from utils.area_solver import compute_area_between


class TestComputeAreaBetween:
    def test_compute_area_between_basic(self):
        res = compute_area_between('x', 'x**2', 0, 1)
        assert res["ok"] is True
        assert res["result"] == pytest.approx(1.0 / 6.0)
        assert len(res["steps"]) >= 3

    def test_compute_area_between_swapped_is_positive(self):
        res = compute_area_between('x**2', 'x', 0, 1)
        assert res["ok"] is True
        assert res["result"] == pytest.approx(1.0 / 6.0)

    def test_compute_area_between_signed_region_geometric_positive(self):
        res = compute_area_between('x', '0', -1, 1)
        assert res["ok"] is True
        assert res["result"] == pytest.approx(1.0)

    def test_compute_area_between_constants(self):
        res = compute_area_between('3', '1', 0, 2)
        assert res["ok"] is True
        assert res["result"] == pytest.approx(4.0)

    def test_compute_area_between_equal_functions(self):
        res = compute_area_between('x', 'x', -1, 1)
        assert res["ok"] is True
        assert res["result"] == pytest.approx(0.0)

    def test_compute_area_between_invalid_bounds(self):
        res = compute_area_between('x', '0', 1, 0)
        assert res["ok"] is False
        assert res["result"] is None
        assert res["error"]

    def test_compute_area_between_invalid_domain_singular(self):
        res = compute_area_between('1/x', '0', -1, 1)
        assert res["ok"] is False
        assert res["result"] is None
        assert res["error"]

    def test_compute_area_between_invalid_input(self):
        res = compute_area_between('', '', 0, 1)
        assert res["ok"] is False
        assert res["error"]

    def test_compute_area_between_has_latex_result(self):
        res = compute_area_between('x', 'x**2', 0, 1)
        assert res["ok"] is True
        assert res["latex"]

    def test_compute_area_between_odd_roots_negative_domain(self):
        res = compute_area_between('x**(1/3)', '0', -1, 1)
        assert res["ok"] is True
        assert res["result"] == pytest.approx(1.5)

    def test_compute_area_between_odd_roots_crossing(self):
        res = compute_area_between('x**(1/3)', 'x', -1, 1)
        assert res["ok"] is True
        assert res["result"] == pytest.approx(0.5)

    def test_compute_area_between_transcendental_crossing(self):
        res = compute_area_between('exp(x)', 'x + 2', -1, 2)
        assert res["ok"] is True
        assert res["result"] == pytest.approx(2.86308, rel=1e-3)
        assert len(res["crossings"]) >= 1

    def test_compute_area_between_trig_crossing(self):
        res = compute_area_between('cos(x)', 'x', 0, 1.5)
        assert res["ok"] is True
        assert res["result"] == pytest.approx(0.92848, rel=1e-3)

    def test_compute_area_between_steps_no_interior_crossings(self):
        res = compute_area_between('x', 'x**2', 0, 1)
        assert res["ok"] is True
        assert res["result"] == pytest.approx(1.0 / 6.0)
        steps_text = " ".join(res["steps"])
        assert "จุดตัด" in steps_text
        assert "\\frac{1}{6}" in steps_text or "1/6" in steps_text or "0.166667" in steps_text

    def test_compute_area_between_steps_swapped(self):
        res = compute_area_between('x**2', 'x', 0, 1)
        assert res["ok"] is True
        assert res["result"] == pytest.approx(1.0 / 6.0)
        steps_text = " ".join(res["steps"])
        assert "ค่าสัมบูรณ์" in steps_text or "Absolute value" in steps_text or "|f" in steps_text
        assert res["result"] > 0

    def test_compute_area_between_steps_polynomial_cubic_crossing(self):
        res = compute_area_between('x**3-6*x**2+8*x', '0', -1, 5)
        assert res["ok"] is True
        assert res["result"] == pytest.approx(20.5)
        assert "\\frac{41}{2}" in res["latex"] or "41/2" in res["latex"] or "20.5" in res["latex"]
        assert len(res["crossings"]) >= 3
        crossings = [round(c, 2) for c in res["crossings"]]
        assert 0.0 in crossings
        assert 2.0 in crossings
        assert 4.0 in crossings
        steps_text = " ".join(res["steps"])
        assert "0" in steps_text and "2" in steps_text and "4" in steps_text
        assert "[-1" in steps_text or "-1" in steps_text

    def test_plot_area_between_figure(self):
        import sympy as sp
        from utils.plotter import plot_area_between
        f = sp.sympify("x")
        g = sp.sympify("x**2")
        fig, ax = plot_area_between(f, g, 0.0, 1.0)
        assert fig is not None
        assert ax is not None
