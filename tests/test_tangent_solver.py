"""Test สำหรับ test_tangent_solver.py

TODO: นักศึกษา implement solver ให้ test นี้ผ่าน
ค่าคาดหวังอ้างอิงจาก docs/interactive-lessons-plan.md
"""

import pytest

from utils.tangent_solver import compute_tangent


class TestComputeTangent:
    def test_compute_tangent_basic(self):
        res = compute_tangent('x**2', 2)
        assert res["ok"] is True
        # TODO: ตรวจค่า result ตามหัวข้อ
        assert res["result"] is not None
        assert len(res["steps"]) >= 3

    def test_compute_tangent_invalid_input(self):
        res = compute_tangent('', 2)
        assert res["ok"] is False
        assert res["error"]

    def test_compute_tangent_has_latex_result(self):
        res = compute_tangent('x**2', 2)
        assert res["ok"] is True
        assert res["latex"]
