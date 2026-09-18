"""Test สำหรับ test_tangent_solver.py"""

import pytest
import sympy as sp

from utils.plotter import plot_tangent
from utils.tangent_solver import compute_tangent


class TestComputeTangent:
    def test_compute_tangent_basic(self):
        res = compute_tangent("x**2", 2)
        assert res["ok"] is True
        assert res["result"] == 4.0
        assert "4" in res["latex"]
        assert len(res["steps"]) >= 4

    def test_compute_tangent_trig(self):
        res = compute_tangent("sin(x)", 0)
        assert res["ok"] is True
        assert pytest.approx(res["result"]) == 1.0

    def test_compute_tangent_invalid_input(self):
        res = compute_tangent("", 2)
        assert res["ok"] is False
        assert res["error"]

    def test_compute_tangent_has_latex_result(self):
        res = compute_tangent("x**2", 2)
        assert res["ok"] is True
        assert res["latex"].startswith("y =")

    def test_plot_tangent_figure(self):
        expr = sp.sympify("x**2")
        fig, ax = plot_tangent(expr, 2.0)
        assert fig is not None
        assert ax is not None
