"""Test สำหรับ test_substitution_solver.py

TODO: นักศึกษา implement solver ให้ test นี้ผ่าน
ค่าคาดหวังอ้างอิงจาก docs/interactive-lessons-plan.md
"""

import pytest

from utils.substitution_solver import solve_substitution


class TestSolveSubstitution:
    def test_solve_substitution_basic(self):
        res = solve_substitution('2*x*exp(x**2)')
        assert res["ok"] is True
        assert res["status"] == "elementary"
        assert res["u_candidate"] is not None
        assert res["result"] is not None
        assert len(res["steps"]) >= 3

    def test_solve_substitution_detects_u_candidate(self):
        res = solve_substitution('(2*x + 1)*(x**2 + x)**5')
        assert res["ok"] is True
        assert res["status"] == "elementary"
        assert str(res["u_candidate"]) == "x**2 + x"
        assert str(res["du_candidate"]) == "2*x + 1"

    def test_solve_substitution_non_elementary_gaussian(self):
        res = solve_substitution('exp(-x**2)')
        assert res["ok"] is True
        assert res["status"] == "non_elementary"
        assert res["warning"] is not None
        assert "erf" in str(res["result"])
        assert "Non-Elementary" in res["steps"][1]

    def test_solve_substitution_non_elementary_sinc(self):
        res = solve_substitution('sin(x)/x')
        assert res["ok"] is True
        assert res["status"] == "non_elementary"
        assert "Si" in str(res["result"])

    def test_solve_substitution_invalid_input(self):
        res = solve_substitution('')
        assert res["ok"] is False
        assert res["status"] == "error"
        assert res["error"]

    def test_solve_substitution_has_latex_result(self):
        res = solve_substitution('2*x*exp(x**2)')
        assert res["ok"] is True
        assert res["latex"]
