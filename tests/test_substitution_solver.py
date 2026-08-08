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
        # TODO: ตรวจค่า result ตามหัวข้อ
        assert res["result"] is not None
        assert len(res["steps"]) >= 3

    def test_solve_substitution_invalid_input(self):
        res = solve_substitution('')
        assert res["ok"] is False
        assert res["error"]

    def test_solve_substitution_has_latex_result(self):
        res = solve_substitution('2*x*exp(x**2)')
        assert res["ok"] is True
        assert res["latex"]
