"""Test สำหรับ test_improper_solver.py

TODO: นักศึกษา implement solver ให้ test นี้ผ่าน
ค่าคาดหวังอ้างอิงจาก docs/interactive-lessons-plan.md
"""

import pytest

from utils.improper_solver import compute_improper


class TestComputeImproper:
    def test_compute_improper_basic(self):
        res = compute_improper('1/x**2', 1, None)
        assert res["ok"] is True
        assert res["result"] == pytest.approx(1.0)
        assert res["status"] == "finite"
        assert len(res["steps"]) >= 3

    def test_finite_bounds_use_actual_upper_latex(self):
        res = compute_improper('1/x**2', 1, 2)
        assert res["ok"] is True
        assert res["status"] == "finite"
        assert res["result"] == pytest.approx(0.5)
        assert "\\infty" not in res["latex"]
        assert "2" in res["latex"]

    def test_infinite_upper_convergent(self):
        res = compute_improper('1/x**2', 1, None)
        assert res["status"] == "finite"
        assert res["result"] == pytest.approx(1.0)
        assert "\\infty" in res["latex"]

    def test_harmonic_on_infinite_interval_diverges(self):
        res = compute_improper('1/x', 1, None)
        assert res["ok"] is True
        assert res["status"] == "divergent"
        assert res["result"] is None

    def test_singular_endpoint_finite_range_diverges(self):
        res = compute_improper('1/x**2', 0, 1)
        assert res["ok"] is True
        assert res["status"] == "divergent"
        assert res["result"] is None

    def test_singular_endpoint_convergent(self):
        res = compute_improper('1/sqrt(x)', 0, 1)
        assert res["status"] == "finite"
        assert res["result"] == pytest.approx(2.0)

    def test_interior_singularity_is_not_finite_principal_value(self):
        res = compute_improper('1/x', -1, 1)
        assert res["status"] == "divergent"
        assert res["result"] is None
        assert len(res["interior_singularities"]) >= 1
        assert any("Interior Singularity" in step for step in res["steps"])

    def test_interior_singularity_shifted(self):
        res = compute_improper('1/(x-1)**2', 0, 2)
        assert res["status"] == "divergent"
        assert res["result"] is None
        assert len(res["interior_singularities"]) >= 1

    def test_compute_improper_invalid_input(self):
        res = compute_improper('', 1, None)
        assert res["ok"] is False
        assert res["status"] == "error"
        assert res["error"]

    def test_compute_improper_has_latex_result(self):
        res = compute_improper('1/x**2', 1, None)
        assert res["ok"] is True
        assert res["latex"]

    def test_plot_improper_figure(self):
        import sympy as sp
        from utils.plotter import plot_improper
        expr = sp.sympify("1/x**2")
        fig, ax = plot_improper(expr, 1.0, None)
        assert fig is not None
        assert ax is not None
