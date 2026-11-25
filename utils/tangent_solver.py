"""utils/tangent_solver.py: Tangent lines and derivatives solver.

Computes tangent line equation y = f'(a)(x - a) + f(a) and slope f'(a),
returning structured steps under the Universal Step Contract:
  {
      "ok": bool,
      "result": float | None,
      "latex": str,
      "steps": list[str],
      "expr": sympy.Expr,
      "error": str | None,
  }
"""
import re
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
from utils.sympy_solver import _clean_calculus_input, _get_variable


def _to_latex(sym_obj) -> str:
    lat = sp.latex(sym_obj, inv_trig_style="full")
    lat = lat.replace(r"\log", r"\ln")
    lat = re.sub(r"\\operatorname\{a(sin|cos|tan)\}", r"\\arc\1", lat)
    lat = re.sub(r"\\operatorname\{arc(cot|sec|csc)\}", r"\\arc\1", lat)
    lat = re.sub(r"(?<![a-zA-Z\\])a(sin|cos|tan)(?=\s*[\(\{\[_0-9]|\b)", r"\\arc\1", lat)
    return lat


H = sp.Symbol("h", real=True)


def _parse_input(expr_str: str) -> sp.Expr:
    clean = (expr_str or "").strip()
    if not clean:
        raise ValueError("Empty input string")
    return parse_expr(clean, transformations=TRANSFORMATIONS, local_dict=LOCAL_MATH_DICT)


def _to_real_roots(e: sp.Expr) -> sp.Expr:
    """Convert odd-degree roots of negative numbers to real values (e.g. (-1)**(1/3) -> -1)."""
    if e is None or not isinstance(e, sp.Basic):
        return e

    def repl(node):
        if node.is_Pow and node.exp.is_Rational and node.exp.q % 2 == 1:
            base = node.base
            exp = node.exp
            if base.is_number and base.is_negative:
                return (-1) ** exp.p * sp.Pow(-base, exp)
        return node

    return e.replace(lambda a: a.is_Pow, repl)


def _explain_diff_rule(expr: sp.Expr, var: sp.Symbol) -> str:
    """Explain differentiation rule applied to expression in clear mathematical notation."""
    v_str = str(var.name)
    elementary = (sp.sin, sp.cos, sp.tan, sp.exp, sp.log)
    if expr.func in elementary and expr.args[0] != var:
        inner = expr.args[0]
        inner_derivative = sp.diff(inner, var)
        inner_lat = _to_latex(inner)
        inner_derivative_lat = _to_latex(inner_derivative)
        if expr.func is sp.sin:
            outer_derivative = rf"\cos\left({inner_lat}\right)"
        elif expr.func is sp.cos:
            outer_derivative = rf"-\sin\left({inner_lat}\right)"
        elif expr.func is sp.tan:
            outer_derivative = rf"\sec^2\left({inner_lat}\right)"
        elif expr.func is sp.exp:
            outer_derivative = rf"e^{{{inner_lat}}}"
        else:
            outer_derivative = rf"\frac{{1}}{{{inner_lat}}}"
        domain_note = f" (เมื่อ ${inner_lat} > 0$)" if expr.func is sp.log else ""
        return (
            f"ใช้กฎลูกโซ่ โดยกำหนด $u = {inner_lat}$ และ $\\frac{{du}}{{d{v_str}}} = {inner_derivative_lat}$; "
            f"อนุพันธ์ฟังก์ชันชั้นนอกคือ ${outer_derivative}${domain_note}; "
            f"คูณอนุพันธ์ชั้นนอกกับอนุพันธ์ชั้นใน:\n"
            f"\\frac{{d}}{{d{v_str}}}\\left[{_to_latex(expr)}\\right] = {outer_derivative} \\cdot \\left({inner_derivative_lat}\\right)"
        )
    if isinstance(expr, sp.sin):
        return f"สูตรอนุพันธ์ไซน์: $\\frac{{d}}{{d{v_str}}}[\\sin({v_str})] = \\cos({v_str})$"
    if isinstance(expr, sp.cos):
        return f"สูตรอนุพันธ์โคไซน์: $\\frac{{d}}{{d{v_str}}}[\\cos({v_str})] = -\\sin({v_str})$"
    if isinstance(expr, sp.tan):
        return f"สูตรอนุพันธ์แทนเจนต์: $\\frac{{d}}{{d{v_str}}}[\\tan({v_str})] = \\sec^2({v_str})$"
    if isinstance(expr, sp.exp):
        return f"สูตรอนุพันธ์เอกซ์โพเนนเชียล: $\\frac{{d}}{{d{v_str}}}[e^{{{v_str}}}] = e^{{{v_str}}}$"
    if isinstance(expr, sp.log):
        return f"สูตรอนุพันธ์ลอการิทึม: $\\frac{{d}}{{d{v_str}}}[\\ln({v_str})] = \\frac{{1}}{{{v_str}}}$ (สำหรับ ${v_str} > 0$)"
    if expr.is_polynomial(var):
        deg = sp.degree(expr, var)
        if deg == 1:
            return f"สูตรอนุพันธ์เชิงเส้น: $\\frac{{d}}{{d{v_str}}}[c\\,{v_str}] = c$ และ $\\frac{{d}}{{d{v_str}}}[c] = 0$"
        return f"กฎยกกำลัง: $\\frac{{d}}{{d{v_str}}}[{v_str}^n] = n {v_str}^{{n-1}}$"
    if expr.has(sp.Pow):
        for p in expr.atoms(sp.Pow):
            base, _ = p.as_base_exp()
            if base != var and base.has(var):
                return f"กฎลูกโซ่: $\\frac{{d}}{{d{v_str}}}[u^n] = n u^{{n-1}} \\frac{{du}}{{d{v_str}}}$"
        return f"กฎยกกำลัง: $\\frac{{d}}{{d{v_str}}}[{v_str}^n] = n {v_str}^{{n-1}}$"
    numer, denom = expr.as_numer_denom()
    if denom != 1 and denom.has(var):
        return (
            f"กฎผลหาร (Quotient Rule): $\\frac{{d}}{{d{v_str}}}\\left[\\frac{{u}}{{v}}\\right] = "
            f"\\frac{{v \\frac{{du}}{{d{v_str}}} - u \\frac{{dv}}{{d{v_str}}}}}{{v^2}}$"
        )
    if expr.is_Mul:
        var_factors = [f for f in expr.args if f.has(var)]
        if len(var_factors) > 1:
            return f"กฎผลคูณ (Product Rule): $\\frac{{d}}{{d{v_str}}}[u \\cdot v] = u \\frac{{dv}}{{d{v_str}}} + v \\frac{{du}}{{d{v_str}}}$"
    if any(expr.has(cls) for cls in (sp.sin, sp.cos, sp.tan)):
        return f"กฎอนุพันธ์ฟังก์ชันตรีโกณมิติร่วมกับกฎลูกโซ่"
    return f"กฎการหาอนุพันธ์พื้นฐานร่วมกับกฎลูกโซ่"


def _format_tangent_algebra(v_lat: str, a_sym: sp.Expr, fa_sym: sp.Expr, slope_sym: sp.Expr, tangent_eq: sp.Expr) -> list[str]:
    lines = []
    m_lat = _to_latex(slope_sym)
    fa_lat = _to_latex(fa_sym)
    a_lat = _to_latex(a_sym)
    a_disp = f"({a_lat})" if (getattr(a_sym, "is_negative", False) or (a_sym.is_number and a_sym < 0)) else a_lat
    fa_sub_disp = f"({fa_lat})" if (getattr(fa_sym, "is_negative", False) or (fa_sym.is_number and fa_sym < 0)) else fa_lat
    simp_lat = _to_latex(sp.simplify(tangent_eq))

    if slope_sym == 0:
        lines.append(f"y - {fa_sub_disp} = 0")
        lines.append(f"y = {fa_lat}")
        return lines

    lines.append(f"y - {fa_sub_disp} = {m_lat}\\left({v_lat} - {a_disp}\\right)")

    if a_sym == 0:
        if fa_sym == 0:
            lines.append(f"y = {simp_lat}")
        else:
            lines.append(f"y - {fa_sub_disp} = {m_lat}{v_lat}")
            if getattr(fa_sym, "is_negative", False) or (fa_sym.is_number and fa_sym < 0):
                lines.append(f"y = {m_lat}{v_lat} + ({fa_lat})")
            else:
                lines.append(f"y = {m_lat}{v_lat} + {fa_lat}")
            if simp_lat != f"{m_lat}{v_lat} + {fa_lat}" and simp_lat != f"{m_lat}{v_lat} + ({fa_lat})":
                lines.append(f"y = {simp_lat}")
    else:
        ma_sym = sp.simplify(slope_sym * a_sym)
        ma_lat = _to_latex(ma_sym)
        ma_sub_disp = f"({ma_lat})" if (getattr(ma_sym, "is_negative", False) or (ma_sym.is_number and ma_sym < 0)) else ma_lat
        lines.append(f"y - {fa_sub_disp} = {m_lat}{v_lat} - {ma_sub_disp}")
        if fa_sym == 0:
            lines.append(f"y = {simp_lat}")
        else:
            fa_add = f"({fa_lat})" if (getattr(fa_sym, "is_negative", False) or (fa_sym.is_number and fa_sym < 0)) else fa_lat
            lines.append(f"y = {m_lat}{v_lat} - {ma_sub_disp} + {fa_add}")
            lines.append(f"y = {simp_lat}")

    return lines


def _format_substitution(expr: sp.Expr, var_sym: sp.Symbol, a_sym: sp.Expr) -> str:
    """Format evaluation step showing explicit substitution before computed value, e.g. f(0) = 0 + 2 = 2."""
    try:
        val = _to_real_roots(expr.subs(var_sym, a_sym))
        val_lat = _to_latex(val)
        sub_expr = expr.subs(var_sym, sp.UnevaluatedExpr(a_sym))
        sub_lat = _to_latex(sub_expr)
        if sub_lat != val_lat:
            return f"{sub_lat} = {val_lat}"
        return val_lat
    except Exception:
        return _to_latex(_to_real_roots(expr.subs(var_sym, a_sym)))


def _build_finite_tangent_steps(
    expr: sp.Expr,
    var_sym: sp.Symbol,
    a_sym: sp.Expr,
    fa_sym: sp.Expr,
    df: sp.Expr,
    slope_sym: sp.Expr,
    tangent_eq: sp.Expr,
) -> list[str]:
    v_lat = _to_latex(var_sym)
    a_lat = _to_latex(a_sym)
    a_disp = f"({a_lat})" if (getattr(a_sym, "is_negative", False) or (a_sym.is_number and a_sym < 0)) else a_lat
    fa_sub_disp = f"({_to_latex(fa_sym)})" if (getattr(fa_sym, "is_negative", False) or (fa_sym.is_number and fa_sym < 0)) else _to_latex(fa_sym)
    slope = float(slope_sym)

    # Step 1: Problem statement and objective
    step1 = (
        f"กำหนดโจทย์และเป้าหมาย: "
        f"กำหนดฟังก์ชันและจุดที่พิจารณา:\n"
        f"f({v_lat}) = {_to_latex(expr)}, \\quad a = {a_lat}\n"
        f"เป้าหมาย: หาสมการเส้นตรงสัมผัส $y - f(a) = f'(a)({v_lat} - a)$"
    )

    # Step 2: Tangency point (substitution into equation)
    sub_fa_lat = _format_substitution(expr, var_sym, a_sym)
    step2 = (
        f"คำนวณพิกัด y ของจุดสัมผัส: "
        f"แทนค่า ${v_lat} = {a_lat}$ ในฟังก์ชัน $f({v_lat})$:\n"
        f"f({a_lat}) = {sub_fa_lat}\n"
        f"ได้จุดสัมผัส $(a, f(a)) = ({a_lat}, {_to_latex(fa_sym)})$"
    )

    # Step 3: Find derivative function
    rule_desc = _explain_diff_rule(expr, var_sym)
    step3 = (
        f"หาอนุพันธ์ f'({v_lat}) เพื่อเป็นสูตรความชัน: "
        f"{rule_desc}\n"
        f"f'({v_lat}) = \\frac{{d}}{{d{v_lat}}}\\left[{_to_latex(expr)}\\right] = {_to_latex(df)}"
    )

    # Step 4: Evaluate point slope m = f'(a)
    sub_df_lat = _format_substitution(df, var_sym, a_sym)
    step4 = (
        f"แทนค่าจุดสัมผัสหาความชัน m = f'(a): "
        f"แทนค่า ${v_lat} = {a_lat}$ ในสูตรอนุพันธ์:\n"
        f"m = f'({a_lat}) = {sub_df_lat}"
    )

    # Step 5: Substitute into Point-Slope formula
    step5 = (
        f"แทนค่าในสมการรูปจุดและความชัน: "
        f"แทนจุด $({a_lat}, {_to_latex(fa_sym)})$ และความชัน $m = {_to_latex(slope_sym)}$ ลงในสูตร $y - f(a) = m({v_lat} - a)$:\n"
        f"y - {fa_sub_disp} = {_to_latex(slope_sym)}\\left({v_lat} - {a_disp}\\right)"
    )

    # Step 6: Rearrange into Slope-Intercept form y = mx + c
    algebra_lines = _format_tangent_algebra(v_lat, a_sym, fa_sym, slope_sym, tangent_eq)
    algebra_display = "\n".join(algebra_lines)
    c_val = sp.simplify(tangent_eq.subs(var_sym, 0))
    step6 = (
        f"จัดรูปสมการความชัน-จุดตัดแกน y = mx + c: "
        f"กระจายพจน์และย้ายข้างสมการ:\n"
        f"{algebra_display}\n"
        f"สมการเส้นสัมผัสคือ $y = {_to_latex(sp.simplify(tangent_eq))}$ (จุดตัดแกน $y$ คือ $(0, {_to_latex(c_val)})$)"
    )

    # Step 7: Additional concepts: Local Linear Approximation and Normal Line
    if slope_sym != 0:
        normal_m = -1 / slope_sym
        normal_eq = normal_m * (var_sym - a_sym) + fa_sym
        normal_simp = sp.simplify(normal_eq)
        normal_desc = (
            f"2. เส้นแนวฉาก: ความชันตั้งฉาก $m_{{\\perp}} = -\\frac{{1}}{{m}} = {_to_latex(normal_m)}$\n"
            f"y - {fa_sub_disp} = {_to_latex(normal_m)}\\left({v_lat} - {a_disp}\\right) \\implies y = {_to_latex(normal_simp)}"
        )
    else:
        normal_desc = (
            f"2. เส้นแนวฉาก: เส้นตรงแนวดิ่ง ${v_lat} = {a_lat}$"
        )

    step7 = (
        f"แนวคิดเพิ่มเติมและเส้นแนวฉาก: "
        f"1. การประมาณค่าเชิงเส้น: $L({v_lat}) = {_to_latex(sp.simplify(tangent_eq))}$ เมื่อ ${v_lat} \\approx {a_lat}$\n"
        f"{normal_desc}"
    )

    # Step 7 (additional concepts and normal line) temporarily hidden per requirements
    return [step1, step2, step3, step4, step5, step6]


def compute_tangent(expr_str: str, a: float) -> dict:
    """Compute tangent line slope f'(a) and equation y = f'(a)(x - a) + f(a)."""
    try:
        clean_str, diff_var = _clean_calculus_input(expr_str)
        expr = _parse_input(clean_str)
        if diff_var is not None:
            var_sym = sp.Symbol(diff_var)
        else:
            var_sym = _get_variable(expr)
        v_lat = _to_latex(var_sym)
        a_f = float(a)
        if a_f.is_integer():
            a_sym = sp.Integer(int(a_f))
        else:
            a_sym = sp.Rational(str(a))
        a_lat = _to_latex(a_sym)
        is_vertical = False

        try:
            fa_sym = _to_real_roots(expr.subs(var_sym, a_sym))
        except Exception as e:
            return {
                "ok": False,
                "result": None,
                "latex": "",
                "steps": [],
                "expr": expr,
                "error": f"ไม่สามารถแทนค่า f({a_lat}) ได้: {e}",
                "status": "error",
                "variable": str(var_sym.name),
            }

        if not (getattr(fa_sym, "is_real", False) and getattr(fa_sym, "is_finite", False)):
            return {
                "ok": False,
                "result": None,
                "latex": "",
                "steps": [
                    f"พิจารณาจุดที่ต้องการหาสัมผัส: {v_lat} = {a_lat}\n"
                    f"กำหนดฟังก์ชัน $f({v_lat}) = {_to_latex(expr)}$ ที่ ${v_lat} = {a_lat}$",
                    f"ตรวจสอบโดเมนของฟังก์ชัน: "
                    f"แทนค่า ${v_lat} = {a_lat}$ พบว่า $f({a_lat})$ ไม่นิยาม หรือไม่อยู่ในโดเมนจำนวนจริง",
                    f"สรุปผล: "
                    f"เนื่องจากฟังก์ชัน $f({v_lat})$ ไม่นิยามที่จุด ${v_lat} = {a_lat}$ จึงไม่มีจุดบนกราฟและไม่มีเส้นสัมผัส",
                ],
                "expr": expr,
                "error": f"ฟังก์ชัน f({v_lat}) ไม่นิยามที่จุด {v_lat} = {a_lat} (หรือไม่อยู่ในโดเมนจำนวนจริง)",
                "status": "undefined_point",
                "variable": str(var_sym.name),
            }

        df = sp.diff(expr, var_sym)
        try:
            slope_sym = _to_real_roots(df.subs(var_sym, a_sym))
        except Exception:
            slope_sym = sp.nan

        if slope_sym.is_real and slope_sym.is_finite:
            status = "finite"
            slope = float(slope_sym)
            tangent_eq = slope_sym * (var_sym - a_sym) + fa_sym
            latex_str = f"y = {_to_latex(sp.simplify(tangent_eq))}"
            steps = _build_finite_tangent_steps(expr, var_sym, a_sym, fa_sym, df, slope_sym, tangent_eq)
        else:
            diff_quot = (expr.subs(var_sym, a_sym + H) - fa_sym) / H
            try:
                left_m = _to_real_roots(sp.limit(diff_quot, H, 0, dir="-"))
                right_m = _to_real_roots(sp.limit(diff_quot, H, 0, dir="+"))
            except Exception:
                left_m, right_m = sp.nan, sp.nan

            is_vertical = False
            if left_m == right_m:
                if left_m in (sp.oo, -sp.oo):
                    status = "non_differentiable"
                    is_vertical = True
                    slope = None
                    latex_str = f"{v_lat} = {a_lat}"
                    steps = [
                        f"กำหนดโจทย์และจุดที่พิจารณา: $f({v_lat}) = {_to_latex(expr)}, \\quad a = {a_lat}$",
                        f"คำนวณพิกัดจุดสัมผัส: $f({a_lat}) = {_to_latex(fa_sym)}$ ได้จุด $(a, f(a)) = ({a_lat}, {_to_latex(fa_sym)})$",
                        f"พิจารณาลิมิตของอัตราส่วนผลต่าง: "
                        f"\\lim_{{h \\to 0}} \\frac{{f({a_lat}+h) - f({a_lat})}}{{h}} = {_to_latex(left_m)}",
                        f"วิเคราะห์ความชัน: ความชันลู่สู่อนันต์ (${_to_latex(left_m)}$) เส้นสัมผัสตั้งฉากกับแกน ${v_lat}$ (แนวดิ่ง)",
                        f"สรุปสมการเส้นสัมผัสแนวดิ่ง (Vertical Tangent Line): "
                        f"เส้นสัมผัสแนวดิ่งผ่านจุด $({a_lat}, {_to_latex(fa_sym)})$ มีสมการคือ ${v_lat} = {a_lat}$",
                    ]
                elif getattr(left_m, "is_real", False) and getattr(left_m, "is_finite", False):
                    status = "finite"
                    slope = float(left_m)
                    tangent_eq = left_m * (var_sym - a_sym) + fa_sym
                    latex_str = f"y = {_to_latex(sp.simplify(tangent_eq))}"
                    steps = _build_finite_tangent_steps(expr, var_sym, a_sym, fa_sym, df, left_m, tangent_eq)
                else:
                    status = "unsupported"
                    slope = None
                    latex_str = r"\text{(unsupported)}"
                    steps = ["ระบบไม่สามารถระบุเส้นสัมผัสได้อย่างแน่ชัด"]
            elif left_m != right_m:
                status = "non_differentiable"
                slope = None
                latex_str = r"\text{(does not exist)}"
                left_real = getattr(left_m, "is_real", False) and not getattr(left_m, "has", lambda _: False)(sp.I)
                right_real = getattr(right_m, "is_real", False) and not getattr(right_m, "has", lambda _: False)(sp.I)
                left_inf = left_m in (sp.oo, -sp.oo)
                right_inf = right_m in (sp.oo, -sp.oo)

                if not left_real and (right_inf or right_real):
                    right_desc = f"ความชันทางขวาลู่สู่อนันต์ (${_to_latex(right_m)}$) เส้นสัมผัสแนวดิ่งทางขวา" if right_inf else f"อนุพันธ์ทางขวาเป็นจำนวนจริงจำกัด (${_to_latex(right_m)}$)"
                    steps = [
                        f"กำหนดโจทย์และจุดที่พิจารณา: $f({v_lat}) = {_to_latex(expr)}, \\quad a = {a_lat}$",
                        f"คำนวณพิกัดจุดบนกราฟ: $f({a_lat}) = {_to_latex(fa_sym)}$ ได้จุด $(a, f(a)) = ({a_lat}, {_to_latex(fa_sym)})$",
                        f"พิจารณาความต่อเนื่องและโดเมน: ฟังก์ชันไม่นิยามในระบบจำนวนจริงทางซ้ายของจุด $a = {a_lat}$ (ไม่อยู่ในโดเมนจำนวนจริงเมื่อ $h < 0$) จึงไม่มีอนุพันธ์ทางซ้าย",
                        f"คำนวณอนุพันธ์ทางขวา (Right-Hand Derivative as h -> 0^+): "
                        f"f'_+({a_lat}) = \\lim_{{h \\to 0^+}} \\frac{{f({a_lat}+h) - f({a_lat})}}{{h}} = {_to_latex(right_m)}",
                        f"สรุปผลการวิเคราะห์: {right_desc} แต่ฟังก์ชันหาอนุพันธ์แบบสองข้างทั่วไปไม่ได้ที่จุดขอบเขตนี้",
                    ]
                elif not right_real and (left_inf or left_real):
                    left_desc = f"ความชันทางซ้ายลู่สู่อนันต์ (${_to_latex(left_m)}$) เส้นสัมผัสแนวดิ่งทางซ้าย" if left_inf else f"อนุพันธ์ทางซ้ายเป็นจำนวนจริงจำกัด (${_to_latex(left_m)}$)"
                    steps = [
                        f"กำหนดโจทย์และจุดที่พิจารณา: $f({v_lat}) = {_to_latex(expr)}, \\quad a = {a_lat}$",
                        f"คำนวณพิกัดจุดบนกราฟ: $f({a_lat}) = {_to_latex(fa_sym)}$ ได้จุด $(a, f(a)) = ({a_lat}, {_to_latex(fa_sym)})$",
                        f"คำนวณอนุพันธ์ทางซ้าย (Left-Hand Derivative as h -> 0^-): "
                        f"f'_-({a_lat}) = \\lim_{{h \\to 0^-}} \\frac{{f({a_lat}+h) - f({a_lat})}}{{h}} = {_to_latex(left_m)}",
                        f"พิจารณาความต่อเนื่องและโดเมน: ฟังก์ชันไม่นิยามในระบบจำนวนจริงทางขวาของจุด $a = {a_lat}$ (ไม่อยู่ในโดเมนจำนวนจริงเมื่อ $h > 0$) จึงไม่มีอนุพันธ์ทางขวา",
                        f"สรุปผลการวิเคราะห์: {left_desc} แต่ฟังก์ชันหาอนุพันธ์แบบสองข้างทั่วไปไม่ได้ที่จุดขอบเขตนี้",
                    ]
                elif left_real and right_real and getattr(left_m, "is_finite", False) and getattr(right_m, "is_finite", False):
                    steps = [
                        f"กำหนดโจทย์และจุดที่พิจารณา: $f({v_lat}) = {_to_latex(expr)}, \\quad a = {a_lat}$",
                        f"คำนวณพิกัดจุดบนกราฟ: $f({a_lat}) = {_to_latex(fa_sym)}$ ได้จุด $(a, f(a)) = ({a_lat}, {_to_latex(fa_sym)})$",
                        f"เงื่อนไขอนุพันธ์: ฟังก์ชันหาอนุพันธ์ได้ ก็ต่อเมื่อ อนุพันธ์ทางซ้ายเท่ากับอนุพันธ์ทางขวา ($f'_-({a_lat}) = f'_+({a_lat})$)",
                        f"คำนวณอนุพันธ์ทางซ้าย (Left-Hand Derivative as h -> 0^-): "
                        f"f'_-({a_lat}) = \\lim_{{h \\to 0^-}} \\frac{{f({a_lat}+h) - f({a_lat})}}{{h}} = {_to_latex(left_m)}",
                        f"คำนวณอนุพันธ์ทางขวา (Right-Hand Derivative as h -> 0^+): "
                        f"f'_+({a_lat}) = \\lim_{{h \\to 0^+}} \\frac{{f({a_lat}+h) - f({a_lat})}}{{h}} = {_to_latex(right_m)}",
                        f"สรุปผลการวิเคราะห์: "
                        f"เนื่องจาก $f'_-({a_lat}) = {_to_latex(left_m)} \\neq {_to_latex(right_m)} = f'_+({a_lat})$\n"
                        f"กราฟมีลักษณะเป็นจุดมุมหัก (Corner Point) ฟังก์ชันจึงหาอนุพันธ์ไม่ได้และไม่มีเส้นสัมผัส",
                    ]
                else:
                    left_txt = f"{_to_latex(left_m)}" if left_real else "ไม่อยู่ในโดเมนจำนวนจริง"
                    right_txt = f"{_to_latex(right_m)}" if right_real else "ไม่อยู่ในโดเมนจำนวนจริง"
                    steps = [
                        f"กำหนดโจทย์และจุดที่พิจารณา: $f({v_lat}) = {_to_latex(expr)}, \\quad a = {a_lat}$",
                        f"คำนวณพิกัดจุดบนกราฟ: $f({a_lat}) = {_to_latex(fa_sym)}$ ได้จุด $(a, f(a)) = ({a_lat}, {_to_latex(fa_sym)})$",
                        f"คำนวณอนุพันธ์ทางซ้าย: $f'_-({a_lat}) = {left_txt}$",
                        f"คำนวณอนุพันธ์ทางขวา: $f'_+({a_lat}) = {right_txt}$",
                        f"สรุปผลการวิเคราะห์: อนุพันธ์ทางซ้ายและทางขวาไม่สอดคล้องกัน ฟังก์ชันจึงหาอนุพันธ์ไม่ได้ที่จุดนี้",
                    ]
            else:
                status = "unsupported"
                slope = None
                latex_str = r"\text{(unsupported)}"
                steps = ["ระบบไม่สามารถระบุเส้นสัมผัสได้อย่างแน่ชัด"]

        return {
            "ok": True,
            "result": slope,
            "latex": latex_str,
            "steps": steps,
            "expr": expr,
            "error": None,
            "status": status,
            "is_vertical": is_vertical,
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
            "status": "error",
        }
