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
        sum_heights = sum(terms)

        # -------------------------------------------------------------------
        # 1. Exact Definite Integral & Error Metrics
        # -------------------------------------------------------------------
        exact_val = None
        exact_latex = ""
        error_abs = None
        error_signed = None
        error_pct = None
        direction = "unknown"

        try:
            exact_sym = sp.integrate(expr, (var_sym, sp.nsimplify(a_f), sp.nsimplify(b_f)))
            if exact_sym.is_number and exact_sym.is_real:
                exact_val = float(exact_sym.evalf())
                exact_latex = rf"\int_{{{_fmt_num(a_f)}}}^{{{_fmt_num(b_f)}}} {sp.latex(expr)}\,d{v_lat} = {sp.latex(exact_sym)}"
                if not exact_sym.is_Integer:
                    exact_latex += rf" \approx {exact_val:.6f}"
                error_signed = total - exact_val
                error_abs = abs(error_signed)
                if abs(exact_val) > 1e-12:
                    error_pct = (error_signed / exact_val) * 100.0
                else:
                    error_pct = 0.0

                if abs(error_signed) < 1e-9:
                    direction = "exact"
                elif error_signed < 0:
                    direction = "underestimate"
                else:
                    direction = "overestimate"
        except Exception:
            exact_val = None

        # -------------------------------------------------------------------
        # 2. Methods Comparison (left, right, midpoint)
        # -------------------------------------------------------------------
        methods_comparison = {}
        for m_key in ("left", "right", "midpoint"):
            if m_key == "left":
                m_xs = [a_f + i * dx for i in range(n_i)]
            elif m_key == "right":
                m_xs = [a_f + (i + 1) * dx for i in range(n_i)]
            else:
                m_xs = [a_f + (i + 0.5) * dx for i in range(n_i)]
            try:
                m_terms = [float(expr.subs(var_sym, xv).evalf()) for xv in m_xs]
                m_tot = sum(m_terms) * dx
                m_err = (m_tot - exact_val) if exact_val is not None else None
                m_pct = ((m_err / exact_val) * 100.0) if (m_err is not None and exact_val is not None and abs(exact_val) > 1e-12) else None
                if m_err is not None:
                    m_dir = "exact" if abs(m_err) < 1e-9 else ("underestimate" if m_err < 0 else "overestimate")
                else:
                    m_dir = "unknown"
                methods_comparison[m_key] = {
                    "val": m_tot,
                    "error_signed": m_err,
                    "error_pct": m_pct,
                    "direction": m_dir,
                }
            except Exception:
                pass

        # -------------------------------------------------------------------
        # 3. Net Signed Area Detection
        # -------------------------------------------------------------------
        has_negative = any(t < -1e-9 for t in terms)
        if not has_negative:
            for tp in [a_f + i * (b_f - a_f) / 40 for i in range(41)]:
                try:
                    if float(expr.subs(var_sym, tp).evalf()) < -1e-9:
                        has_negative = True
                        break
                except Exception:
                    pass

        negative_warning = None
        if has_negative:
            negative_warning = (
                f"กราฟของฟังก์ชันมีบางช่วงที่อยู่ใต้แกน {v_lat} ($f({v_lat}) < 0$) "
                f"ความสูงของแท่งสี่เหลี่ยมในบริเวณนั้นจะมีค่าติดลบ ทำให้ผลรวมรีมันน์ที่ได้นี้คือ "
                f"**'พื้นที่คิดเครื่องหมาย' (Net Signed Area)** ซึ่งพื้นที่ส่วนบนและส่วนล่างจะหักล้างกัน "
                f"หากต้องการ **'พื้นที่เรขาคณิตสัมบูรณ์' (Total Geometric Area)** จะต้องคำนวณแยกช่วงหรืออินทิเกรต $|f({v_lat})|$"
            )

        # -------------------------------------------------------------------
        # 4. Table Data (Per-subinterval Breakdown)
        # -------------------------------------------------------------------
        table_data = [
            {
                "i": i + 1,
                "x_val": xs[i],
                "f_val": terms[i],
                "term_area": terms[i] * dx,
            }
            for i in range(n_i)
        ]

        # -------------------------------------------------------------------
        # 5. Analytical Limit for Polynomials (Degree <= 3)
        # -------------------------------------------------------------------
        analytical_limit = None
        try:
            if getattr(expr, "is_polynomial", None) and expr.is_polynomial(var_sym):
                poly = sp.Poly(expr, var_sym)
                if poly.degree() in (1, 2, 3):
                    sym_n = sp.Symbol("n", integer=True, positive=True)
                    sym_i = sp.Symbol("i", integer=True, positive=True)
                    sym_a = sp.nsimplify(a_f)
                    sym_b = sp.nsimplify(b_f)
                    sym_dx = (sym_b - sym_a) / sym_n
                    sym_xi = sym_a + sym_i * sym_dx
                    sym_term = expr.subs(var_sym, sym_xi) * sym_dx
                    sym_sum = sp.summation(sym_term, (sym_i, 1, sym_n))
                    sym_sum_simp = sp.factor(sp.together(sym_sum))
                    sym_lim = sp.limit(sym_sum, sym_n, sp.oo)
                    analytical_limit = {
                        "sum_rn_latex": sp.latex(sym_sum_simp),
                        "limit_latex": sp.latex(sym_lim),
                        "dx_sym_latex": sp.latex(sym_dx),
                        "xi_sym_latex": sp.latex(sym_xi),
                    }
        except Exception:
            analytical_limit = None

        # -------------------------------------------------------------------
        # 6. Step-by-Step LaTeX Explanation
        # -------------------------------------------------------------------
        f_latex = sp.latex(expr)
        term_strs = [f"f({_fmt_num(xv)})" for xv in xs]
        terms_latex = " + ".join(term_strs)
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

        # สูตรจุดสุ่มตัวอย่างและสูตรซิกม่า
        if method == "left":
            sample_rule = f"{sample_symbol} = a + i\\,\\Delta {v_lat} \\quad (i = 0, 1, \\dots, {n_i-1})"
            sample_name = "ขอบซ้าย"
            sigma_formula = (
                f"{method_latex} = \\sum_{{i=0}}^{{{n_i-1}}} f({v_lat}_i)\\,\\Delta {v_lat} = "
                f"\\Delta {v_lat} \\left[ \\sum_{{i=0}}^{{{n_i-1}}} f({v_lat}_i) \\right]"
            )
        elif method == "right":
            sample_rule = f"{sample_symbol} = a + i\\,\\Delta {v_lat} \\quad (i = 1, 2, \\dots, {n_i})"
            sample_name = "ขอบขวา"
            sigma_formula = (
                f"{method_latex} = \\sum_{{i=1}}^{{{n_i}}} f({v_lat}_i)\\,\\Delta {v_lat} = "
                f"\\Delta {v_lat} \\left[ \\sum_{{i=1}}^{{{n_i}}} f({v_lat}_i) \\right]"
            )
        else:
            sample_rule = rf"{sample_symbol} = a + \left(i - \tfrac12\right)\Delta {v_lat} \quad (i = 1, 2, \dots, {n_i})"
            sample_name = "จุดกึ่งกลาง"
            sigma_formula = (
                f"{method_latex} = \\sum_{{i=1}}^{{{n_i}}} f(\\bar{{{v_lat}}}_i)\\,\\Delta {v_lat} = "
                f"\\Delta {v_lat} \\left[ \\sum_{{i=1}}^{{{n_i}}} f(\\bar{{{v_lat}}}_i) \\right]"
            )

        expanded_formula = f"= \\Delta {v_lat} \\left[ {terms_latex} \\right]"

        # การแสดงจุดสุ่มตัวอย่าง
        if n_i <= 8:
            pts_disp = ", ".join(_fmt_num(xv) for xv in xs)
            pts_latex = f"{sample_symbol} \\in \\{{{pts_disp}\\}}"
        else:
            first_few = ", ".join(_fmt_num(xv) for xv in xs[:3])
            pts_latex = f"{sample_symbol} \\in \\{{{first_few}, \\dots, {_fmt_num(xs[-1])}\\}} \\quad (n = {n_i})"

        # การแสดงค่าฟังก์ชันแต่ละจุด
        if n_i <= 6:
            f_eval_list = [f"f({_fmt_num(xv)}) = {_fmt_num(tv)}" for xv, tv in zip(xs, terms)]
            f_eval_str = ", \\quad ".join(f_eval_list)
            sum_terms_str = " + ".join(_fmt_num(tv) for tv in terms)
            heights_lines = f"{f_eval_str}\n\\sum f({sample_symbol}) = {sum_terms_str} = {_fmt_num(sum(terms))}"
        else:
            first_pts = ", \\quad ".join([f"f({_fmt_num(xv)}) = {_fmt_num(tv)}" for xv, tv in zip(xs[:3], terms[:3])])
            last_pt = f"f({_fmt_num(xs[-1])}) = {_fmt_num(terms[-1])}"
            f_eval_str = f"{first_pts}, \\quad \\dots, \\quad {last_pt}"
            sum_terms_str = f"{_fmt_num(terms[0])} + {_fmt_num(terms[1])} + \\cdots + {_fmt_num(terms[-1])}"
            heights_lines = f"{f_eval_str}\n\\sum f({sample_symbol}) = {sum_terms_str} = {_fmt_num(sum(terms))}"

        sum_h_str = _fmt_num(sum(terms))
        calc_line = f"{method_latex} = \\Delta {v_lat} \\cdot \\left(\\sum f({sample_symbol})\\right)"
        sub_line = f"= ({_fmt_num(dx)}) \\cdot ({sum_h_str})"
        res_line = f"= {total:.6f}"

        # เปรียบเทียบกับค่าจริงปริพันธ์จำกัดเขต
        try:
            exact_sym = sp.integrate(expr, (var_sym, a_f, b_f))
            if getattr(exact_sym, "is_real", False) and getattr(exact_sym, "is_finite", False):
                exact_val = float(exact_sym)
                err_val = abs(total - exact_val)
                comp_lines = (
                    f"\\int_{{{_fmt_num(a_f)}}}^{{{_fmt_num(b_f)}}} {sp.latex(expr)}\\,d{v_lat} = "
                    f"{sp.latex(exact_sym)} \\approx {exact_val:.6f}\n"
                    f"|\\text{{Error}}| = |{total:.6f} - {exact_val:.6f}| = {err_val:.6f}"
                )
            else:
                comp_lines = f"\\int_{{{_fmt_num(a_f)}}}^{{{_fmt_num(b_f)}}} {sp.latex(expr)}\\,d{v_lat}"
        except Exception:
            comp_lines = f"\\int_{{{_fmt_num(a_f)}}}^{{{_fmt_num(b_f)}}} {sp.latex(expr)}\\,d{v_lat}"

        if n_i <= 8:
            heights_eval_str = " + ".join(_fmt_num(t) for t in terms)
            step3_text = (
                f"คำนวณความสูง $f({sample_symbol})$ แต่ละจุด แล้วรวมกัน: "
                f"${terms_latex} = {heights_eval_str} = {_fmt_num(sum_heights)}$"
            )
        else:
            step3_text = (
                f"คำนวณความสูง $f({sample_symbol})$ แต่ละจุด แล้วรวมกัน: "
                f"${terms_latex}$ ซึ่งมีผลรวมความสูงเท่ากับ ${_fmt_num(sum_heights)}$"
            )

        if exact_val is not None:
            dir_text = "ประเมินต่ำกว่าจริง (Underestimate)" if direction == "underestimate" else ("ประเมินสูงกว่าจริง (Overestimate)" if direction == "overestimate" else "ตรงกับค่าจริง")
            step5_text = (
                f"ค่าประมาณและเทียบกับค่าจริง: ${method_latex} \\approx {total:.6f}$ โดยค่าจริงคือ ${exact_latex}$ "
                f"(คลาดเคลื่อน {error_signed:+.6f} หรือ {error_pct:+.2f}%, {dir_text})"
            )
        else:
            step5_text = f"ค่าประมาณ: ${method_latex} \\approx {total:.6f}$"

        steps = [
            f"คำนวณความกว้างของแต่ละช่วงย่อย (Subinterval Width: \\Delta {v_lat}): "
            f"แบ่งช่วง $[a, b] = [{_fmt_num(a_f)}, {_fmt_num(b_f)}]$ ออกเป็น $n = {n_i}$ ช่วงย่อยเท่ากัน:\n"
            f"\\Delta {v_lat} = \\frac{{b - a}}{{n}} = \\frac{{{_fmt_num(b_f)} - {_fmt_num(a_f)}}}{{{n_i}}} = {_fmt_num(dx)}",

            f"กำหนดจุดสุ่มตัวอย่าง{sample_name} (Sample Points): "
            f"สูตรพิกัดจุดสุ่มตัวอย่างสำหรับ{sample_name}:\n"
            f"{sample_rule}\n"
            f"{pts_latex}",

            f"ตั้งสูตรผลรวมรีมันน์ (Riemann Sum Formula): "
            f"ผลรวมพื้นที่สี่เหลี่ยมผืนผ้า (ความกว้าง $\\times$ ผลรวมความสูง):\n"
            f"{sigma_formula}\n"
            f"{expanded_formula}",

            f"คำนวณความสูงของแต่ละแท่ง (Evaluate Heights): "
            f"แทนจุดสุ่มตัวอย่างลงใน $f({v_lat}) = {sp.latex(expr)}$:\n"
            f"{heights_lines}",

            f"คำนวณผลรวมพื้นที่รีมันน์ (Total Area): "
            f"นำความกว้าง $\\Delta {v_lat} = {_fmt_num(dx)}$ คูณผลรวมความสูง:\n"
            f"{calc_line}\n"
            f"{sub_line}\n"
            f"{res_line}",

            f"เปรียบเทียบกับปริพันธ์จำกัดเขต (Definite Integral Comparison): "
            f"เปรียบเทียบค่าประมาณ ${method_latex}$ กับค่าจริงจากปริพันธ์จำกัดเขต:\n"
            f"{comp_lines}\n"
            f"ข้อสังเกตมโนทัศน์: เมื่อ $n \\to \\infty$ จะได้ $\\Delta {v_lat} \\to 0$ และค่าผลรวมรีมันน์ ${method_latex} \\to \\int_{{{_fmt_num(a_f)}}}^{{{_fmt_num(b_f)}}} {sp.latex(expr)}\\,d{v_lat}$",
        ]

        return {
            "ok": True,
            "result": total,
            "latex": f"{method_latex} \\approx {total:.6f}",
            "steps": steps,
            "expr": expr,
            "error": None,
            "variable": str(var_sym.name),
            "exact_integral": exact_val,
            "exact_latex": exact_latex,
            "error_abs": error_abs,
            "error_signed": error_signed,
            "error_pct": error_pct,
            "direction": direction,
            "methods_comparison": methods_comparison,
            "has_negative_region": has_negative,
            "negative_warning": negative_warning,
            "table_data": table_data,
            "sum_heights": sum_heights,
            "analytical_limit": analytical_limit,
        }
    except Exception as e:
        return {
            "ok": False,
            "result": None,
            "latex": "",
            "steps": [],
            "expr": None,
            "error": f"ไม่สามารถคำนวณได้: {e}",
            "exact_integral": None,
            "exact_latex": "",
            "error_abs": None,
            "error_signed": None,
            "error_pct": None,
            "direction": "unknown",
            "methods_comparison": {},
            "has_negative_region": False,
            "negative_warning": None,
            "table_data": [],
            "sum_heights": 0.0,
            "analytical_limit": None,
        }
