"""
utils/riemann_solver.py — คำนวณผลรวมรีมันน์ (Riemann sum) ทีละขั้น

สำหรับบทเรียน interactive 3.1 พื้นที่ภายใต้เส้นโค้ง
ใช้ SymPy แปลงนิพจน์จากผู้ใช้ เหมือน utils/sympy_solver.py

รองรับ 3 วิธี:
  - left     : L_n = sum_{i=0}^{n-1} f(x_i) Δx , x_i = a + iΔx
  - right    : R_n = sum_{i=1}^{n}   f(x_i) Δx , x_i = a + iΔx
  - midpoint : M_n = sum_{i=0}^{n-1} f(x̄_i) Δx , x̄_i = a + (i+0.5)Δx
"""

from typing import Any
import math

import sympy as sp
from sympy.parsing.sympy_parser import (
    convert_xor,
    implicit_multiplication_application,
    parse_expr,
    standard_transformations,
)

# NOTE: ห้ามใส่ auto_symbol — พังใน sympy 1.14.0 (เหมือน sympy_solver.py)
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

from utils.sympy_solver import _clean_calculus_input, _get_variable

# วิธีที่รองรับ: key -> (ชื่อไทย, latex subscript ที่ใช้ในสูตร)
METHODS = {
    "left": ("ซ้าย (left)", r"L_n"),
    "right": ("ขวา (right)", r"R_n"),
    "midpoint": ("จุดกึ่งกลาง (midpoint)", r"M_n"),
}


def _parse_input(expr_str: str) -> sp.Expr:
    clean = (expr_str or "").strip()
    if not clean:
        raise ValueError("Empty input string")
    return parse_expr(clean, transformations=TRANSFORMATIONS, local_dict=LOCAL_MATH_DICT)


def _fmt_num(x: float) -> str:
    """จัดรูปแบบตัวเลขให้สั้น ไม่มีเลขศูนย์เกินจำเป็น"""
    if abs(x - round(x)) < 1e-9:
        return str(int(round(x)))
    return f"{x:.4f}".rstrip("0").rstrip(".")


def _point_latex(expr: sp.Expr, x_val: float, var: sp.Symbol = X) -> str:
    """LaTeX ของ f(x_i) เมื่อแทนค่าแล้ว"""
    val = float(expr.subs(var, x_val))
    return _fmt_num(val)


def compute_riemann(
    expr_str: str,
    a: float,
    b: float,
    n: int | float,
    method: str = "left",
) -> dict[str, Any]:
    """คำนวณผลรวมรีมันน์และคืน steps เป็น LaTeX

    Returns dict {ok, result, latex, steps, error}
    """
    try:
        clean_str, diff_var = _clean_calculus_input(expr_str)
        expr = _parse_input(clean_str)
        if diff_var is not None:
            var_sym = sp.Symbol(diff_var)
        else:
            var_sym = _get_variable(expr)
        v_lat = sp.latex(var_sym)

        a_f, b_f = float(a), float(b)
        try:
            n_f = float(n)
            if not n_f.is_integer() or n_f < 1:
                raise ValueError("n must be an integer >= 1")
            n_i = int(n_f)
        except (TypeError, ValueError):
            raise ValueError("n must be an integer >= 1")
        if b_f <= a_f:
            raise ValueError("b must be > a")
        if method not in METHODS:
            raise ValueError(f"Unknown method: {method}")

        dx = (b_f - a_f) / n_i
        method_latex = METHODS[method][1]

        # หา sample points
        if method == "left":
            xs = [a_f + i * dx for i in range(n_i)]
        elif method == "right":
            xs = [a_f + (i + 1) * dx for i in range(n_i)]
        else:  # midpoint
            xs = [a_f + (i + 0.5) * dx for i in range(n_i)]

        terms = []
        for xv in xs:
            val_sub = expr.subs(var_sym, xv)
            if val_sub in (sp.zoo, sp.oo, -sp.oo) or getattr(val_sub, "is_infinite", False):
                raise ValueError(f"ฟังก์ชันมีจุดเอกฐาน (หารด้วยศูนย์) ที่จุดสุ่มตัวอย่าง {v_lat} = {_fmt_num(xv)}")
            try:
                f_val = float(val_sub.evalf())
                if not math.isfinite(f_val):
                    raise ValueError(f"ฟังก์ชันไม่จำกัดเขตที่จุด {v_lat} = {_fmt_num(xv)}")
                terms.append(f_val)
            except Exception:
                raise ValueError(f"ไม่สามารถคำนวณค่าฟังก์ชันบนจุดสุ่มตัวอย่าง {v_lat} = {_fmt_num(xv)} ได้")

        total = sum(terms) * dx

        # สร้าง LaTeX ของผลรวม
        f_latex = sp.latex(expr)
        term_strs = []
        for i, xv in enumerate(xs):
            term_strs.append(f"f({_fmt_num(xv)})")
        terms_latex = " + ".join(term_strs)
        # ใช้สัญลักษณ์ผลรวมถ้า n ใหญ่
        if n_i > 8:
            first = _point_latex(expr, xs[0], var=var_sym)
            last = _point_latex(expr, xs[-1], var=var_sym)
            if method == "midpoint":
                index_note = rf"\bar{{{v_lat}}}_i = a + \left(i-\tfrac12\right)\Delta {v_lat}"
                terms_latex = f"f(\\bar{{{v_lat}}}_1)+\\cdots+f(\\bar{{{v_lat}}}_{{{n_i}}})"
            elif method == "right":
                index_note = f"{v_lat}_i = a + i\\,\\Delta {v_lat}"
                terms_latex = f"f({v_lat}_1)+\\cdots+f({v_lat}_{{{n_i}}})"
            else:
                index_note = f"{v_lat}_i = a + i\\,\\Delta {v_lat}"
                terms_latex = f"f({v_lat}_0)+\\cdots+f({v_lat}_{{{n_i-1}}})"

        sample_symbol = rf"\bar{{{v_lat}}}_i" if method == "midpoint" else f"{v_lat}_i"
        sample_label = "จุดกึ่งกลางช่วง" if method == "midpoint" else "จุดแบ่งช่วง"

        steps = [
            f"หาความกว้างของแต่ละช่วง: $\\Delta {v_lat} = \\frac{{b-a}}{{n}} = \\frac{{{_fmt_num(b_f)}-{_fmt_num(a_f)}}}{{{n_i}}} = {_fmt_num(dx)}$",
            f"{sample_label} ${sample_symbol}$: ${', '.join(_fmt_num(xv) for xv in xs)}$",
            f"คำนวณ $f({sample_symbol})$ แต่ละจุด แล้วรวมกัน: ${terms_latex}$",
            f"คูณด้วย $\\Delta {v_lat}$: ${method_latex} = \\left({terms_latex}\\right)\\cdot {_fmt_num(dx)}$",
            f"ค่าประมาณ: ${method_latex} \\approx {total:.6f}$",
            f"ข้อสังเกตมโนทัศน์: เมื่อเพิ่มจำนวนช่วง $n \\to \\infty$ ความกว้าง $\\Delta {v_lat} \\to 0$ ค่าผลรวมรีมันน์ {method_latex} จะลู่เข้าสู่ค่าพื้นที่จริงตามนิยามปริพันธ์จำกัดเขต $\\int_a^b f({v_lat})\\,d{v_lat}$",
        ]

        return {
            "ok": True,
            "result": total,
            "latex": f"{method_latex} \\approx {total:.6f}",
            "steps": steps,
            "expr": expr,
            "error": None,
            "variable": str(var_sym.name),
        }
    except Exception as e:
        return {
            "ok": False,
            "result": None,
            "latex": "",
            "steps": [],
            "expr": None,
            "error": f"ไม่สามารถคำนวณได้: {e}",
        }
