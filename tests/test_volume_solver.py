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

    def test_compute_volume_invalid_bounds(self):
        res = compute_volume('x', 2, 0, 'disk')
        assert res["ok"] is False
        assert res["error"]

    def test_compute_volume_unsupported_method(self):
        res = compute_volume('x', 0, 2, 'washer')
        assert res["ok"] is False
        assert res["error"]

    def test_compute_volume_washer_success(self):
        res = compute_volume('sqrt(x)', 0, 1, 'washer', inner_expr_str='x**2')
        assert res["ok"] is True
        assert res["result"] == pytest.approx(3 * 3.141592653589793 / 10)
        assert res["method"] == "washer"
        assert res["inner_expr"] is not None

    def test_compute_volume_washer_swapped_is_positive(self):
        res = compute_volume('x**2', 0, 1, 'washer', inner_expr_str='sqrt(x)')
        assert res["ok"] is True
        assert res["result"] == pytest.approx(3 * 3.141592653589793 / 10)

    def test_compute_volume_unknown_method(self):
        res = compute_volume('x', 0, 2, 'shell')
        assert res["ok"] is False
        assert res["error"]

    def test_compute_volume_has_latex_result(self):
        res = compute_volume('x', 0, 2, 'disk')
        assert res["ok"] is True
        assert res["latex"]

    def test_plot_volume_figure(self):
        import sympy as sp
        from utils.plotter import plot_volume
        expr = sp.sympify("x")
        fig, ax = plot_volume(expr, 0.0, 2.0, "disk")
        assert fig is not None
        assert ax is not None
