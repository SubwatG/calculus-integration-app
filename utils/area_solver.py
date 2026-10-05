"""utils/area_solver.py — พื้นที่ระหว่างเส้นโค้ง

คำนวณพื้นที่เรขาคณิต A = ∫_a^b |f(x) - g(x)| dx บนช่วงจริงจำกัด [a, b]
"""
import math
import sympy as sp
from sympy.parsing.sympy_parser import (
    convert_xor,
    implicit_multiplication_application,
    parse_expr,
    standard_transformations,
)

TRANSFORMATIONS = standard_transformations + (
    implicit_multiplication_application,
    convert_xor,
)

LOCAL_MATH_DICT = {
    "e": sp.E,
    "E": sp.E,
    "pi": sp.pi,
    "ln": sp.log,
}

X = sp.Symbol("x")


def _parse_input(expr_str: str) -> sp.Expr:
    clean = (expr_str or "").strip()
    if not clean:
        raise ValueError("Empty input string")
    return parse_expr(clean, transformations=TRANSFORMATIONS, local_dict=LOCAL_MATH_DICT)


def _to_rational_bound(val: float | int | str) -> sp.Rational:
    try:
        fval = float(val)
        if not math.isfinite(fval):
            raise ValueError(f"Bound must be finite, got {val}")
    except (TypeError, ValueError) as e:
        raise ValueError(f"Invalid bound {val}: {e}")
    return sp.Rational(str(val))


def _polynomial_area(diff: sp.Expr, x: sp.Symbol, lower: sp.Rational, upper: sp.Rational) -> sp.Expr:
    try:
        poly = sp.Poly(diff, x)
    except Exception:
        raise ValueError("Not a single-variable polynomial")
    if any(c.is_Rational is not True for c in poly.all_coeffs()):
        raise ValueError("Unsupported polynomial coefficients")
    poly = poly.set_domain(sp.QQ)
    if poly.is_zero:
        return sp.S.Zero
    roots = sorted(set(poly.real_roots()))
    cuts = [lower] + [r for r in roots if lower < r < upper] + [upper]
    primitive = sp.integrate(diff, x)
    total = sp.S.Zero
    for left, right in zip(cuts, cuts[1:]):
        mid = (left + right) / 2
        sign = sp.sign(diff.subs(x, mid))
        if sign not in (sp.S.One, sp.S.NegativeOne):
            raise ValueError("Cannot certify sign on subinterval")
        total += sign * (primitive.subs(x, right) - primitive.subs(x, left))
    return sp.simplify(total)


def compute_area_between(f_str: str, g_str: str, a: float, b: float) -> dict:
    """คำนวณพื้นที่เรขาคณิตระหว่างเส้นโค้ง A = ∫_a^b |f(x) - g(x)| dx"""
    try:
        a_sp = _to_rational_bound(a)
        b_sp = _to_rational_bound(b)
        if a_sp >= b_sp:
            raise ValueError("ขอบล่าง a ต้องน้อยกว่าขอบบน b")

        f_expr = _parse_input(f_str)
        g_expr = _parse_input(g_str)

        free = (f_expr.free_symbols | g_expr.free_symbols) - {X}
        if free:
            raise ValueError(f"พบตัวแปรที่ไม่รองรับ: {free} (รองรับเฉพาะตัวแปร x)")

        diff_expr = sp.simplify(f_expr - g_expr)

        area_val = None
        try:
            val = sp.integrate(sp.Abs(diff_expr), (X, a_sp, b_sp))
            if not val.has(sp.Integral) and getattr(val, "is_real", False) is True and getattr(val, "is_finite", False) is True:
                area_val = val
        except Exception:
            pass

        if area_val is None:
            try:
                val = _polynomial_area(diff_expr, X, a_sp, b_sp)
                if not val.has(sp.Integral) and getattr(val, "is_real", False) is True and getattr(val, "is_finite", False) is True:
                    area_val = val
            except Exception:
                pass

        if area_val is None or not (getattr(area_val, "is_real", False) is True and getattr(area_val, "is_finite", False) is True):
            raise ValueError("ไม่สามารถคำนวณพื้นที่จำกัดได้บนช่วงที่กำหนด (อาจมีจุดเอกฐาน หรือไม่อยู่ในโดเมนจำนวนจริง)")

        res_float = float(area_val)

        steps = [
            f"กำหนดฟังก์ชัน: f(x) = {sp.latex(f_expr)}, \\quad g(x) = {sp.latex(g_expr)}",
            f"ตั้งสูตรอินทิกรัลพื้นที่เรขาคณิต: A = \\int_{{{a}}}^{{{b}}} |f(x) - g(x)| \\, dx",
            f"หาผลต่างของฟังก์ชัน: f(x) - g(x) = {sp.latex(diff_expr)}",
            f"คำนวณพื้นที่เรขาคณิต: A = \\int_{{{a}}}^{{{b}}} \\left|{sp.latex(diff_expr)}\\right| \\, dx = {sp.latex(area_val)}",
        ]

        return {
            "ok": True,
            "result": res_float,
            "latex": f"A = \\int_{{{a}}}^{{{b}}} |{sp.latex(diff_expr)}| \\, dx = {sp.latex(area_val)}",
            "steps": steps,
            "expr": diff_expr,
            "f_expr": f_expr,
            "g_expr": g_expr,
            "error": None,
        }
    except Exception as e:
        return {
            "ok": False,
            "result": None,
            "latex": "",
            "steps": [],
            "expr": None,
            "f_expr": None,
            "g_expr": None,
            "error": f"ไม่สามารถคำนวณได้: {e}",
        }
