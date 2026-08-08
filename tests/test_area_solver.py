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
        # TODO: ตรวจค่า result ตามหัวข้อ
        assert res["result"] is not None
        assert len(res["steps"]) >= 3

    def test_compute_area_between_invalid_input(self):
        res = compute_area_between('', '', 0, 1)
        assert res["ok"] is False
        assert res["error"]

    def test_compute_area_between_has_latex_result(self):
        res = compute_area_between('x', 'x**2', 0, 1)
        assert res["ok"] is True
        assert res["latex"]
