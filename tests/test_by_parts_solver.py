"""tests/test_by_parts_solver.py — การทดสอบ Integration by Parts Solver เฉพาะทาง
"""

import pytest
import sympy as sp

from utils.by_parts_solver import detect_parts_candidate, solve_by_parts


class TestByPartsSolver:
    def test_solve_by_parts_x_exp_x(self):
        res = solve_by_parts("x*exp(x)")
        assert res["ok"] is True
        assert res["status"] == "elementary"
        x = sp.Symbol("x")
        expected = (x - 1) * sp.exp(x)
        assert sp.simplify(res["result"] - expected) == 0
        assert res["parts_info"] is not None
        assert str(res["parts_info"]["u"]) == "x"
        assert str(res["parts_info"]["dv"]) == "exp(x)"
        steps_text = " ".join(res["steps"])
        assert "LIATE" in steps_text
        assert "uv - \\int v \\, du" in steps_text

    def test_solve_by_parts_single_ln_x(self):
        res = solve_by_parts("ln(x)")
        assert res["ok"] is True
        assert res["status"] == "elementary"
        x = sp.Symbol("x")
        expected = x * sp.log(x) - x
        assert sp.simplify(res["result"] - expected) == 0
        assert str(res["parts_info"]["u"]) == "log(x)"
        assert str(res["parts_info"]["dv"]) == "1"

    def test_solve_by_parts_x_sin_x(self):
        res = solve_by_parts("x*sin(x)")
        assert res["ok"] is True
        assert res["status"] == "elementary"
        x = sp.Symbol("x")
        expected = -x * sp.cos(x) + sp.sin(x)
        assert sp.simplify(res["result"] - expected) == 0

    def test_solve_by_parts_warns_when_u_sub_is_better(self):
        # 2x * sqrt(x^2 + 1) is clearly a u-substitution problem
        res = solve_by_parts("2*x*sqrt(x**2 + 1)")
        assert res["ok"] is True
        assert res["status"] == "better_suited_for_substitution"
        assert "u-Substitution" in res["warning"] or "การแทนตัวแปร u" in res["warning"]

    def test_solve_by_parts_cyclic_exp_cos(self):
        res = solve_by_parts("exp(x)*cos(x)")
        assert res["ok"] is True
        assert res["status"] == "elementary"
        steps_text = " ".join(res["steps"])
        assert "Cyclic" in steps_text or "วนลูป" in steps_text
        assert "รอบที่ 1" in steps_text
        assert "รอบที่ 2" in steps_text

    def test_solve_by_parts_cyclic_2_to_x_cos(self):
        res = solve_by_parts("2^x*cos(x)")
        assert res["ok"] is True
        assert res["status"] == "elementary"
        steps_text = " ".join(res["steps"])
        assert "Cyclic" in steps_text or "วนลูป" in steps_text
        assert "รอบที่ 1" in steps_text
        assert "รอบที่ 2" in steps_text
        assert "Solve for I" in steps_text or "แก้สมการ" in steps_text

    def test_solve_by_parts_invalid_input(self):
        res = solve_by_parts("")
        assert res["ok"] is False
        assert res["status"] == "error"
