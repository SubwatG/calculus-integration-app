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
        # TODO: ตรวจค่า result ตามหัวข้อ
        assert res["result"] is not None
        assert len(res["steps"]) >= 3

    def test_compute_improper_invalid_input(self):
        res = compute_improper('', 1, None)
        assert res["ok"] is False
        assert res["error"]

    def test_compute_improper_has_latex_result(self):
        res = compute_improper('1/x**2', 1, None)
        assert res["ok"] is True
        assert res["latex"]
