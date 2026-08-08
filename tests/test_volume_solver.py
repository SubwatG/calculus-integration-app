"""Test สำหรับ test_volume_solver.py

TODO: นักศึกษา implement solver ให้ test นี้ผ่าน
ค่าคาดหวังอ้างอิงจาก docs/interactive-lessons-plan.md
"""

import pytest

from utils.volume_solver import compute_volume


class TestComputeVolume:
    def test_compute_volume_basic(self):
        res = compute_volume('x', 0, 2, 'disk')
        assert res["ok"] is True
        # TODO: ตรวจค่า result ตามหัวข้อ
        assert res["result"] is not None
        assert len(res["steps"]) >= 3

    def test_compute_volume_invalid_input(self):
        res = compute_volume('', 0, 2, 'disk')
        assert res["ok"] is False
        assert res["error"]

    def test_compute_volume_has_latex_result(self):
        res = compute_volume('x', 0, 2, 'disk')
        assert res["ok"] is True
        assert res["latex"]
