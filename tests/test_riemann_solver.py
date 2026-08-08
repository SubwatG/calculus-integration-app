"""Test สำหรับ utils.riemann_solver (ผลรวมรีมันน์)

ครอบ logic บริสุทธิ์ ไม่ต้องเปิด Streamlit
ค่าอ้างอิงคำนวณด้วยมือสำหรับกรณีง่ายๆ
"""

import pytest

from utils.riemann_solver import METHODS, compute_riemann


class TestRiemannLeft:
    def test_x_squared_0_to_2_n2(self):
        # f(x)=x^2, [0,2], n=2, left
        # Δx=1, จุด 0,1 → f(0)=0, f(1)=1 → ผลรวม=1
        res = compute_riemann("x**2", 0, 2, 2, "left")
        assert res["ok"] is True
        assert abs(res["result"] - 1.0) < 1e-9
        assert len(res["steps"]) >= 4

    def test_constant_function(self):
        # f(x)=5, [0,4], n=4, left → แต่ละช่อง 5*1 → รวม 20
        res = compute_riemann("5", 0, 4, 4, "left")
        assert res["ok"] is True
        assert abs(res["result"] - 20.0) < 1e-9


class TestRiemannRight:
    def test_x_squared_0_to_2_n2(self):
        # Δx=1, จุด 1,2 → f(1)=1, f(2)=4 → ผลรวม=5
        res = compute_riemann("x**2", 0, 2, 2, "right")
        assert res["ok"] is True
        assert abs(res["result"] - 5.0) < 1e-9


class TestRiemannMidpoint:
    def test_x_squared_0_to_2_n2(self):
        # Δx=1, จุด 0.5,1.5 → f=0.25, 2.25 → ผลรวม=2.5
        res = compute_riemann("x**2", 0, 2, 2, "midpoint")
        assert res["ok"] is True
        assert abs(res["result"] - 2.5) < 1e-9

    def test_midpoint_more_accurate(self):
        # n=50 midpoint ควรใกล้ค่าจริง 8/3 ≈ 2.6667
        res = compute_riemann("x**2", 0, 2, 50, "midpoint")
        assert res["ok"] is True
        assert abs(res["result"] - 8 / 3) < 0.01


class TestRiemannErrors:
    def test_invalid_expr(self):
        res = compute_riemann("", 0, 1, 4, "left")
        assert res["ok"] is False
        assert res["error"]

    def test_invalid_method(self):
        res = compute_riemann("x", 0, 1, 4, "nope")
        assert res["ok"] is False

    def test_bad_bounds(self):
        res = compute_riemann("x", 2, 1, 4, "left")
        assert res["ok"] is False

    def test_n_zero(self):
        res = compute_riemann("x", 0, 1, 0, "left")
        assert res["ok"] is False


class TestMethodsCatalog:
    def test_has_three_methods(self):
        assert set(METHODS.keys()) == {"left", "right", "midpoint"}
        for k, v in METHODS.items():
            assert len(v) == 2  # (ชื่อไทย, latex subscript)
