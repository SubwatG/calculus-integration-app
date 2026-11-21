"""Tests for utils/special_functions.py."""

import sympy as sp

from utils.special_functions import (
    SPECIAL_FUNCTIONS,
    describe_special_functions,
    has_special_function,
    latex_names,
    numeric_approximation,
    special_functions_in,
)

x = sp.Symbol("x", real=True)


def test_elementary_expression_is_not_flagged():
    for expr in (x**2, sp.sin(x), sp.exp(x), sp.log(x), 1 / (1 + x**2), sp.Abs(x)):
        assert special_functions_in(expr) == []
        assert has_special_function(expr) is False


def test_error_function_is_detected():
    assert special_functions_in(sp.erf(x)) == ["erf"]
    assert has_special_function(sp.integrate(sp.exp(-x**2), x)) is True


def test_sine_integral_is_detected():
    assert special_functions_in(sp.Si(x)) == ["Si"]


def test_logarithmic_integral_is_detected():
    assert special_functions_in(sp.li(x)) == ["li"]


def test_imaginary_error_function_is_detected():
    assert special_functions_in(sp.erfi(x)) == ["erfi"]


def test_expression_with_several_special_functions_keeps_first_seen_order():
    expr = sp.erf(x) + sp.Si(x) + sp.erf(x)
    assert sorted(special_functions_in(expr)) == ["Si", "erf"]


def test_gamma_function_is_detected():
    assert special_functions_in(sp.gamma(x)) == ["gamma"]


def test_lambert_w_is_detected():
    assert special_functions_in(sp.LambertW(x)) == ["LambertW"]


def test_none_and_string_inputs_are_safe():
    assert special_functions_in(None) == []
    assert special_functions_in("erf(x)") == []
    assert has_special_function(None) is False


def test_description_names_the_function_in_thai():
    text = describe_special_functions(["erf"])
    assert text.startswith("คำตอบนี้ต้องใช้ฟังก์ชันพิเศษ")
    assert "ฟังก์ชันความคลาดเคลื่อน" in text
    assert "erf" in text
    assert "ซึ่งอยู่นอกหลักสูตร Calculus 1" in text


def test_numeric_approximation_of_a_special_value():
    value = sp.Si(1)
    approx = numeric_approximation(value)
    assert approx is not None
    assert abs(float(approx) - 0.9460830704) < 1e-6


def test_numeric_approximation_handles_missing_input():
    assert numeric_approximation(None) is None
    assert numeric_approximation("Si(1)") is None


def test_description_of_empty_list_is_empty():
    assert describe_special_functions([]) == ""


def test_latex_names_are_available_for_every_known_function():
    for name, (_, _, latex_name) in SPECIAL_FUNCTIONS.items():
        assert latex_name
    assert latex_names(["Si", "erf"]) == r"\operatorname{Si}, \operatorname{erf}"
