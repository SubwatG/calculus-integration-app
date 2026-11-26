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
        assert res["result"] == pytest.approx(1.0)
        assert res["status"] == "finite"
        assert len(res["steps"]) >= 3

    def test_finite_bounds_use_actual_upper_latex(self):
        res = compute_improper('1/x**2', 1, 2)
        assert res["ok"] is True
        assert res["status"] == "finite"
        assert res["result"] == pytest.approx(0.5)
        assert "\\infty" not in res["latex"]
        assert "2" in res["latex"]

    def test_infinite_upper_convergent(self):
        res = compute_improper('1/x**2', 1, None)
        assert res["status"] == "finite"
        assert res["result"] == pytest.approx(1.0)
        assert "\\infty" in res["latex"]

    def test_harmonic_on_infinite_interval_diverges(self):
        res = compute_improper('1/x', 1, None)
        assert res["ok"] is True
        assert res["status"] == "divergent"
        assert res["result"] is None

    def test_singular_endpoint_finite_range_diverges(self):
        res = compute_improper('1/x**2', 0, 1)
        assert res["ok"] is True
        assert res["status"] == "divergent"
        assert res["result"] is None

    def test_singular_endpoint_convergent(self):
        res = compute_improper('1/sqrt(x)', 0, 1)
        assert res["status"] == "finite"
        assert res["result"] == pytest.approx(2.0)
        steps_text = " ".join(res["steps"])
        assert "t \\to 0" in steps_text or "\\lim_{t \\to 0^{+}}" in steps_text or "\\lim_{t \\to 0^+}" in steps_text
        assert "\\lim_{t \\to 1}" not in steps_text

    def test_singular_upper_endpoint_convergent(self):
        res = compute_improper('1/sqrt(1-x)', 0, 1)
        assert res["status"] == "finite"
        assert res["result"] == pytest.approx(2.0)
        steps_text = " ".join(res["steps"])
        assert "t \\to 1" in steps_text or "\\lim_{t \\to 1^{-}}" in steps_text or "\\lim_{t \\to 1^-}" in steps_text

    def test_proper_integral_no_infinity(self):
        res = compute_improper('x', 0, 2)
        assert res["ok"] is True
        assert res["status"] == "finite"
        assert res["result"] == pytest.approx(2.0)
        assert "\\infty" not in res["latex"]
        assert "2" in res["latex"]

    def test_interior_singularity_is_not_finite_principal_value(self):
        res = compute_improper('1/x', -1, 1)
        assert res["status"] == "divergent"
        assert res["result"] is None
        assert len(res["interior_singularities"]) >= 1
        assert any("Interior Singularity" in step for step in res["steps"])

    def test_interior_singularity_shifted(self):
        res = compute_improper('1/(x-1)**2', 0, 2)
        assert res["status"] == "divergent"
        assert res["result"] is None
        assert len(res["interior_singularities"]) >= 1

    def test_compute_improper_invalid_input(self):
        res = compute_improper('', 1, None)
        assert res["ok"] is False
        assert res["status"] == "error"
        assert res["error"]

    def test_compute_improper_has_latex_result(self):
        res = compute_improper('1/x**2', 1, None)
        assert res["ok"] is True
        assert res["latex"]

    def test_plot_improper_figure(self):
        import sympy as sp
        from utils.plotter import plot_improper
        expr = sp.sympify("1/x**2")
        fig, ax = plot_improper(expr, 1.0, None)
        assert fig is not None
        assert ax is not None

    def test_improper_both_infinite_convergent(self):
        res = compute_improper('1/(1+x**2)', '-inf', 'inf')
        assert res["ok"] is True
        assert res["status"] == "finite"
        assert res["result"] == pytest.approx(3.14159265)

    def test_improper_lower_infinite_convergent(self):
        res = compute_improper('exp(x)', '-inf', 0)
        assert res["ok"] is True
        assert res["status"] == "finite"
        assert res["result"] == pytest.approx(1.0)

    def test_improper_step_by_step_limit_substitution(self):
        res = compute_improper('1/x**2', 1, None)
        steps_text = " ".join(res["steps"])
        assert "\\lim_{t \\to \\infty}" in steps_text
        assert "- \\frac{1}{x}" in steps_text
        assert "\\lim_{t \\to \\infty}" in res["steps"][3]
        assert "ลู่เข้า (Converges)" in res["steps"][4]

    def test_improper_math_11_cases(self):
        # 1. ln(x)/sqrt(x) on [0, 1] -> -4
        res1 = compute_improper('ln(x)/sqrt(x)', 0, 1)
        assert res1["ok"] is True
        assert res1["status"] == "finite"
        assert res1["result"] == pytest.approx(-4.0)

        # 2. sqrt(x)*ln(x) on [0, 1] -> -4/9
        res2 = compute_improper('sqrt(x)*ln(x)', 0, 1)
        assert res2["ok"] is True
        assert res2["status"] == "finite"
        assert res2["result"] == pytest.approx(-4 / 9)

        # 3. 1/(x-1)**(2/3) on [0, 2] -> 6
        res3 = compute_improper('1/(x-1)**(2/3)', 0, 2)
        assert res3["ok"] is True
        assert res3["status"] == "finite"
        assert res3["result"] == pytest.approx(6.0)

        # 4. 1/x**0.5 on [1, inf] -> divergent
        res4 = compute_improper('1/x**0.5', 1, 'inf')
        assert res4["ok"] is True
        assert res4["status"] == "divergent"
        assert res4["result"] is None

    def test_p0_01_sin_x_over_x_on_symmetric_intervals(self):
        # sin(x)/x on [-1, 1] must be positive and ~1.892166
        res1 = compute_improper('sin(x)/x', -1, 1)
        assert res1["ok"] is True
        assert res1["status"] == "finite"
        assert res1["result"] == pytest.approx(1.8921661407, abs=1e-6)
        assert "0" not in res1["latex"].split("=")[-1]
        steps_text = " ".join(res1["steps"])
        assert "ลู่เข้าสู่ค่าจริงจำกัด" in steps_text

        # sin(x)/x on [-2, 2] must be positive and ~3.210826
        res2 = compute_improper('sin(x)/x', -2, 2)
        assert res2["ok"] is True
        assert res2["status"] == "finite"
        assert res2["result"] == pytest.approx(3.2108259536, abs=1e-6)

    def test_p0_01_one_over_x_diverges_not_cancelled(self):
        res = compute_improper('1/x', -1, 1)
        assert res["ok"] is True
        assert res["status"] == "divergent"
        assert res["result"] is None
        assert "0" not in res["latex"].split("=")[-1]

    def test_p0_01_real_domain_guard_sqrt_complex(self):
        # sqrt(x - 1/2) on [0, 1] is non-real on [0, 0.5)
        res_outside = compute_improper('sqrt(x - 1/2)', 0, 1)
        assert res_outside["ok"] is True
        assert res_outside["status"] in ("outside_domain", "unsupported")
        assert res_outside["result"] is None
        rhs = res_outside["latex"].split("=")[-1].strip()
        assert "\\sqrt{2} i" not in rhs
        assert " i" not in rhs and "+ i" not in rhs
        steps_text = " ".join(res_outside["steps"])
        assert "\\sqrt{2} i" not in steps_text
        assert "ไม่อยู่ในโดเมน" in steps_text or "นอกโดเมน" in steps_text

        # sqrt(x - 1/2) on [0.5, 1] is real and valid: sqrt(2)/6 ~ 0.235702
        res_valid = compute_improper('sqrt(x - 1/2)', 0.5, 1)
        assert res_valid["ok"] is True
        assert res_valid["status"] == "finite"
        assert res_valid["result"] == pytest.approx(0.23570226, abs=1e-6)

    def test_p0_01_tan_preserves_pi_over_two_bound(self):
        res = compute_improper('tan(x)', 0, 'pi/2')
        assert res["ok"] is True
        assert res["status"] == "divergent"
        assert res["result"] is None
        assert "1.5708" not in res["latex"]
        assert "\\pi" in res["latex"]
        steps_text = " ".join(res["steps"])
        assert "1.5708" not in steps_text
        assert "\\pi" in steps_text
