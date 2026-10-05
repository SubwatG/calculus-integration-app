"""Test สำหรับ test_limit_solver.py"""

import pytest
import sympy as sp

from utils.limit_solver import compute_limit_near
from utils.plotter import plot_limit_near


class TestComputeLimitNear:
    def test_compute_limit_near_basic(self):
        res = compute_limit_near("(x**2-4)/(x-2)", 2)
        assert res["ok"] is True
        assert res["result"] == 4.0
        assert res["status"] == "finite"
        assert len(res["steps"]) >= 4

    def test_compute_limit_sin_x_over_x(self):
        res = compute_limit_near("sin(x)/x", 0)
        assert res["ok"] is True
        assert pytest.approx(res["result"]) == 1.0
        assert res["status"] == "finite"

    def test_compute_limit_near_invalid_input(self):
        res = compute_limit_near("", 2)
        assert res["ok"] is False
        assert res["status"] == "error"
        assert res["error"]

    def test_compute_limit_near_has_latex_result(self):
        res = compute_limit_near("(x**2-4)/(x-2)", 2)
        assert res["ok"] is True
        assert "4" in res["latex"]

    def test_plot_limit_near_figure(self):
        expr = sp.sympify("(x**2-4)/(x-2)")
        fig, ax = plot_limit_near(expr, 2.0, delta=0.2)
        assert fig is not None
        assert ax is not None

    def test_two_sided_limit_dne(self):
        res = compute_limit_near("1/x", 0)
        assert res["ok"] is True
        assert res["status"] == "dne"
        assert res["result"] is None
        assert res["left_limit"] == -sp.oo
        assert res["right_limit"] == sp.oo
        assert "\\neq" in res["steps"][-1]
        assert "ไม่มีลิมิต" in res["steps"][-1]

    def test_equal_infinite_sides(self):
        res = compute_limit_near("1/x**2", 0)
        assert res["ok"] is True
        assert res["status"] == "infinite"
        assert res["result"] is None
        assert res["left_limit"] == res["right_limit"] == sp.oo
