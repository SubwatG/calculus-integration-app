"""Test สำหรับ test_limit_solver.py

TODO: นักศึกษา implement solver ให้ test นี้ผ่าน
ค่าคาดหวังอ้างอิงจาก docs/interactive-lessons-plan.md
"""

import pytest

from utils.limit_solver import compute_limit_near


class TestComputeLimitNear:
    def test_compute_limit_near_basic(self):
        res = compute_limit_near('(x**2-4)/(x-2)', 2)
        assert res["ok"] is True
        # TODO: ตรวจค่า result ตามหัวข้อ
        assert res["result"] is not None
        assert len(res["steps"]) >= 3

    def test_compute_limit_near_invalid_input(self):
        res = compute_limit_near('', 2)
        assert res["ok"] is False
        assert res["error"]

    def test_compute_limit_near_has_latex_result(self):
        res = compute_limit_near('(x**2-4)/(x-2)', 2)
        assert res["ok"] is True
        assert res["latex"]
