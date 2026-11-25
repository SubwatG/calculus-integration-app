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
        assert res["result"] == pytest.approx(1.0 / 6.0)
        assert len(res["steps"]) >= 3

    def test_compute_area_between_swapped_is_positive(self):
        res = compute_area_between('x**2', 'x', 0, 1)
        assert res["ok"] is True
        assert res["result"] == pytest.approx(1.0 / 6.0)

    def test_compute_area_between_signed_region_geometric_positive(self):
        res = compute_area_between('x', '0', -1, 1)
        assert res["ok"] is True
        assert res["result"] == pytest.approx(1.0)

    def test_compute_area_between_constants(self):
        res = compute_area_between('3', '1', 0, 2)
        assert res["ok"] is True
        assert res["result"] == pytest.approx(4.0)

    def test_compute_area_between_equal_functions(self):
        res = compute_area_between('x', 'x', -1, 1)
        assert res["ok"] is True
        assert res["result"] == pytest.approx(0.0)

    def test_compute_area_between_invalid_bounds(self):
        res = compute_area_between('x', '0', 1, 0)
        assert res["ok"] is False
        assert res["result"] is None
        assert res["error"]

    def test_compute_area_between_invalid_bound_string(self):
        res = compute_area_between('x', 'x**2', 0, 'pi')
        assert res["ok"] is False
        assert res["result"] is None
        assert "ขอบเขตต้องเป็นตัวเลขจริง" in res["error"]
        assert "Invalid bound" not in res["error"]
        assert "could not convert string to float" not in res["error"]

    def test_compute_area_between_invalid_domain_singular(self):
        res = compute_area_between('1/x', '0', -1, 1)
        assert res["ok"] is False
        assert res["result"] is None
        assert res["error"]

    def test_compute_area_between_invalid_input(self):
        res = compute_area_between('', '', 0, 1)
        assert res["ok"] is False
        assert res["error"]

    def test_compute_area_between_has_latex_result(self):
        res = compute_area_between('x', 'x**2', 0, 1)
        assert res["ok"] is True
        assert res["latex"]

    def test_compute_area_between_odd_roots_negative_domain(self):
        res = compute_area_between('x**(1/3)', '0', -1, 1)
        assert res["ok"] is True
        assert res["result"] == pytest.approx(1.5)

    def test_compute_area_between_odd_roots_crossing(self):
        res = compute_area_between('x**(1/3)', 'x', -1, 1)
        assert res["ok"] is True
        assert res["result"] == pytest.approx(0.5)

    def test_compute_area_between_transcendental_crossing(self):
        res = compute_area_between('exp(x)', 'x + 2', -1, 2)
        assert res["ok"] is True
        assert res["result"] == pytest.approx(2.86308, rel=1e-3)
        assert len(res["crossings"]) >= 1

    def test_compute_area_between_trig_crossing(self):
        res = compute_area_between('cos(x)', 'x', 0, 1.5)
        assert res["ok"] is True
        assert res["result"] == pytest.approx(0.92848, rel=1e-3)

    def test_compute_area_between_steps_no_interior_crossings(self):
        res = compute_area_between('x', 'x**2', 0, 1)
        assert res["ok"] is True
        assert res["result"] == pytest.approx(1.0 / 6.0)
        steps_text = " ".join(res["steps"])
        assert "จุดตัด" in steps_text
        assert "\\frac{1}{6}" in steps_text or "1/6" in steps_text or "0.166667" in steps_text

    def test_compute_area_between_steps_swapped(self):
        res = compute_area_between('x**2', 'x', 0, 1)
        assert res["ok"] is True
        assert res["result"] == pytest.approx(1.0 / 6.0)
        steps_text = " ".join(res["steps"])
        assert "ค่าสัมบูรณ์" in steps_text or "Absolute value" in steps_text or "|f" in steps_text
        assert res["result"] > 0

    def test_compute_area_between_steps_polynomial_cubic_crossing(self):
        res = compute_area_between('x**3-6*x**2+8*x', '0', -1, 5)
        assert res["ok"] is True
        assert res["result"] == pytest.approx(20.5)
        assert "\\frac{41}{2}" in res["latex"] or "41/2" in res["latex"] or "20.5" in res["latex"]
        assert len(res["crossings"]) >= 3
        crossings = [round(c, 2) for c in res["crossings"]]
        assert 0.0 in crossings
        assert 2.0 in crossings
        assert 4.0 in crossings
        steps_text = " ".join(res["steps"])
        assert "0" in steps_text and "2" in steps_text and "4" in steps_text
        assert "[-1" in steps_text or "-1" in steps_text

    def test_plot_area_between_figure(self):
        import sympy as sp
        from utils.plotter import plot_area_between, plot_area_between_plotly
        f = sp.sympify("x")
        g = sp.sympify("x**2")
        fig, ax = plot_area_between(f, g, 0.0, 1.0)
        assert fig is not None
        assert ax is not None

        # Matplotlib plot must use solid line, not dashed
        assert ax.lines[1].get_linestyle() in ("-", "solid")

        # Plotly interactive figure test
        fig_plotly = plot_area_between_plotly(f, g, 0.0, 1.0, crossings=[0.0, 1.0])
        assert fig_plotly is not None
        assert len(fig_plotly.data) >= 3

    def test_find_curve_intersections_two_points(self):
        from utils.area_solver import find_curve_intersections
        res = find_curve_intersections("x", "x**2")
        assert res["ok"] is True
        assert res["count"] == 2
        assert res["can_enclose_area"] is True
        assert res["roots"] == [0.0, 1.0]
        assert res["natural_bounds"] == (0.0, 1.0)

    def test_find_curve_intersections_symmetric(self):
        from utils.area_solver import find_curve_intersections
        res = find_curve_intersections("2 - x**2", "x**2")
        assert res["ok"] is True
        assert res["count"] == 2
        assert res["can_enclose_area"] is True
        assert res["roots"] == [-1.0, 1.0]

    def test_find_curve_intersections_no_intersection(self):
        from utils.area_solver import find_curve_intersections
        res = find_curve_intersections("x**2 + 2", "x")
        assert res["ok"] is True
        assert res["count"] == 0
        assert res["can_enclose_area"] is False
        assert res["natural_bounds"] is None

    def test_find_curve_intersections_single_point(self):
        from utils.area_solver import find_curve_intersections
        res = find_curve_intersections("cos(x)", "x")
        assert res["ok"] is True
        assert res["count"] == 1
        assert res["can_enclose_area"] is False

    def test_difference_not_factored_into_product(self):
        res = compute_area_between("x", "x**2", 0, 1)
        assert res["ok"] is True
        steps_text = " ".join(res["steps"])
        # Must show x - x^2 and NOT x(1-x)
        assert "x(1-x)" not in steps_text
        assert "x \\left(1 - x\\right)" not in steps_text
        assert "x - x^{2}" in steps_text or "x - x^2" in steps_text or "- x^{2} + x" in steps_text

    def test_no_absolute_value_bar_outside_integral_in_substeps(self):
        res = compute_area_between("cos(x)", "x", 0, 1.6)
        assert res["ok"] is True
        # Check substeps: no \left| \int
        for s in res["steps"]:
            if "ช่วงย่อยที่" in s:
                assert "\\left| \\int" not in s
                assert "|\\int" not in s

    def test_no_gigantic_fractions_in_numerical_cases(self):
        res = compute_area_between("cos(x)", "x", 0, 1.6)
        assert res["ok"] is True
        steps_text = " ".join(res["steps"])
        # Should not contain 11-digit denominator
        assert "80000000000" not in steps_text
        assert "21849865489" not in steps_text

    def test_no_domain_continuity_step_in_output(self):
        res = compute_area_between("x", "x**2", 0, 1)
        assert res["ok"] is True
        steps_text = " ".join(res["steps"])
        assert "เงื่อนไขความต่อเนื่อง" not in steps_text

    def test_step_formatting_centering_newlines(self):
        res = compute_area_between("x", "x^2", 0, 1)
        assert "\n" in res["steps"][0]
        assert "\n" in res["steps"][2]
        # Should not mention absolute value removal in Thai
        assert "ปลดค่าสัมบูรณ์" not in " ".join(res["steps"])

    def test_odd_roots_piecewise_simplified(self):
        res = compute_area_between("x**(1/3)", "x", -1, 1)
        steps_text = " ".join(res["steps"])
        assert "Piecewise" not in steps_text
        assert "cases" not in steps_text

    def test_math_01_high_frequency_sine_crossing(self):
        import math
        res = compute_area_between("sin(120*pi*x)", "0", 0, 1)
        assert res["ok"] is True
        assert res["result"] == pytest.approx(2.0 / math.pi, rel=1e-5)
        assert len(res["crossings"]) >= 100

    def test_math_02_negative_domain_rejected(self):
        res = compute_area_between("sqrt(x)", "0", -2, -1)
        assert res["ok"] is False
        assert res["result"] is None
        assert "โดเมน" in res["error"] or "ไม่สามารถคำนวณได้" in res["error"]

    def test_math_03_partial_negative_domain_rejected(self):
        res = compute_area_between("sqrt(x)", "0", -1, 1)
        assert res["ok"] is False
        assert res["result"] is None
        assert "โดเมน" in res["error"] or "ไม่สามารถคำนวณได้" in res["error"]

    def test_math_14_tangency_point_not_split(self):
        # MATH-14: x = 0 is a tangency point with no sign change across [-1, 1]
        res = compute_area_between("x**2", "0", -1, 1)
        assert res["ok"] is True
        assert res["result"] == pytest.approx(2.0 / 3.0)
        assert res["crossings"] == []
        assert res.get("touch_points") == [0.0]
        steps_text = " ".join(res["steps"])
        assert "จุดสัมผัส" in steps_text
        assert "ไม่ต้องแบ่งช่วงย่อย" in steps_text
        assert "ช่วงย่อยที่ 1" not in steps_text

    def test_math_14_tangency_with_crossing_mixed(self):
        # Mixed: x = 0 is tangency, x = 2 is true crossing on [-1, 3]
        res = compute_area_between("x**2*(x-2)", "0", -1, 3)
        assert res["ok"] is True
        assert res["crossings"] == [2.0]
        assert res.get("touch_points") == [0.0]
        steps_text = " ".join(res["steps"])
        assert "จุดสัมผัสที่ไม่ตัดสลับฝั่ง" in steps_text
        assert "ช่วงย่อยที่ 1" in steps_text
        assert "ช่วงย่อยที่ 2" in steps_text
        assert "ช่วงย่อยที่ 3" not in steps_text



