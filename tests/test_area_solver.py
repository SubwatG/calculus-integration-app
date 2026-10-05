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

    def test_plot_area_between_figure(self):
        import sympy as sp
        from utils.plotter import plot_area_between
        f = sp.sympify("x")
        g = sp.sympify("x**2")
        fig, ax = plot_area_between(f, g, 0.0, 1.0)
        assert fig is not None
        assert ax is not None
