"""utils/tangent_solver.py — เส้นสัมผัสและอนุพันธ์

skeleton สำหรับนักศึกษา project
TODO: ใส่ logic จริงให้ test ใน tests/ ผ่าน
อ้างอิง blueprint: utils/riemann_solver.py และ docs/interactive-lessons-plan.md

โครงสร้างผลลัพธ์ (เหมือน utils/riemann_solver.py):
  {
      "ok": bool,
      "result": float | None,
      "latex": str,          # สูตรผลลัพธ์ LaTeX
      "steps": list[str],    # ขั้นตอน LaTeX
      "expr": sympy.Expr,    # นิพจน์ที่ parse แล้ว
      "error": str | None,
  }
"""
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


H = sp.Symbol("h", real=True)


def _parse_input(expr_str: str) -> sp.Expr:
    clean = (expr_str or "").strip()
    if not clean:
        raise ValueError("Empty input string")
    return parse_expr(clean, transformations=TRANSFORMATIONS, local_dict=LOCAL_MATH_DICT)


def _explain_diff_rule(expr: sp.Expr, var: sp.Symbol) -> str:
    """อธิบายกฎและสูตรการหาอนุพันธ์ที่ใช้กับนิพจน์นี้อย่างเข้าใจง่ายและเน้นสมการ"""
    v_str = str(var.name)
    elementary = (sp.sin, sp.cos, sp.tan, sp.exp, sp.log)
    if expr.func in elementary and expr.args[0] != var:
        inner = expr.args[0]
        inner_derivative = sp.diff(inner, var)
        inner_lat = sp.latex(inner)
        inner_derivative_lat = sp.latex(inner_derivative)
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
            f"\\frac{{d}}{{d{v_str}}}\\left[{sp.latex(expr)}\\right] = {outer_derivative} \\cdot \\left({inner_derivative_lat}\\right)"
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
        return f"กฎเลขชี้กำลัง (Power Rule): $\\frac{{d}}{{d{v_str}}}[{v_str}^n] = n {v_str}^{{n-1}}$"
    if expr.has(sp.Pow):
        for p in expr.atoms(sp.Pow):
            base, _ = p.as_base_exp()
            if base != var and base.has(var):
                return f"กฎลูกโซ่ (Chain Rule): $\\frac{{d}}{{d{v_str}}}[u^n] = n u^{{n-1}} \\frac{{du}}{{d{v_str}}}$"
        return f"กฎเลขชี้กำลัง (Power Rule): $\\frac{{d}}{{d{v_str}}}[{v_str}^n] = n {v_str}^{{n-1}}$"
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
    m_lat = sp.latex(slope_sym)
    fa_lat = sp.latex(fa_sym)
    a_lat = sp.latex(a_sym)
    a_disp = f"({a_lat})" if a_sym < 0 else a_lat
    simp_lat = sp.latex(sp.simplify(tangent_eq))

    if slope_sym == 0:
        lines.append(f"y - ({fa_lat}) = 0")
        lines.append(f"y = {fa_lat}")
        return lines

    lines.append(f"y - ({fa_lat}) = {m_lat}\\left({v_lat} - {a_disp}\\right)")

    if a_sym == 0:
        if fa_sym == 0:
            lines.append(f"y = {simp_lat}")
        else:
            lines.append(f"y - ({fa_lat}) = {m_lat}{v_lat}")
            lines.append(f"y = {m_lat}{v_lat} + ({fa_lat})")
            if simp_lat != f"{m_lat}{v_lat} + ({fa_lat})":
                lines.append(f"y = {simp_lat}")
    else:
        ma_sym = sp.simplify(slope_sym * a_sym)
        ma_lat = sp.latex(ma_sym)
        lines.append(f"y - ({fa_lat}) = {m_lat}{v_lat} - ({ma_lat})")
        if fa_sym == 0:
            lines.append(f"y = {simp_lat}")
        else:
            lines.append(f"y = {m_lat}{v_lat} - ({ma_lat}) + ({fa_lat})")
            lines.append(f"y = {simp_lat}")

    return lines


def _build_finite_tangent_steps(
    expr: sp.Expr,
    var_sym: sp.Symbol,
    a_sym: sp.Expr,
    fa_sym: sp.Expr,
    df: sp.Expr,
    slope_sym: sp.Expr,
    tangent_eq: sp.Expr,
) -> list[str]:
    v_lat = sp.latex(var_sym)
    a_lat = sp.latex(a_sym)
    a_disp = f"({a_lat})" if a_sym < 0 else a_lat
    slope = float(slope_sym)

    # Step 1: ปัญหาและเป้าหมาย
    step1 = (
        f"กำหนดโจทย์และเป้าหมาย (Problem Setup & Goal): "
        f"กำหนดฟังก์ชันและจุดที่พิจารณา:\n"
        f"f({v_lat}) = {sp.latex(expr)}, \\quad a = {a_lat}\n"
        f"เป้าหมาย: หาสมการเส้นตรงสัมผัส $y - f(a) = f'(a)({v_lat} - a)$"
    )

    # Step 2: จุดสัมผัส
    step2 = (
        f"คำนวณพิกัด y ของจุดสัมผัส (Point of Tangency): "
        f"แทนค่า ${v_lat} = {a_lat}$ ในฟังก์ชัน:\n"
        f"f({a_lat}) = {sp.latex(fa_sym)}\n"
        f"ได้จุดสัมผัส $(a, f(a)) = ({a_lat}, {sp.latex(fa_sym)})$"
    )

    # Step 3: หาฟังก์ชันอนุพันธ์
    rule_desc = _explain_diff_rule(expr, var_sym)
    step3 = (
        f"หาอนุพันธ์ f'({v_lat}) เพื่อเป็นสูตรความชัน (Derivative Function): "
        f"{rule_desc}\n"
        f"f'({v_lat}) = \\frac{{d}}{{d{v_lat}}}\\left[{sp.latex(expr)}\\right] = {sp.latex(df)}"
    )

    # Step 4: คำนวณความชันเฉพาะจุด m = f'(a)
    if slope > 0:
        slope_geo = (
            f"ความหมายเรขาคณิต: ความชัน $m = {slope:.4f} > 0$ กราฟมีแนวโน้มเพิ่มขึ้น (Increasing)"
        )
    elif slope < 0:
        slope_geo = (
            f"ความหมายเรขาคณิต: ความชัน $m = {slope:.4f} < 0$ กราฟมีแนวโน้มลดลง (Decreasing)"
        )
    else:
        slope_geo = (
            f"ความหมายเรขาคณิต: ความชัน $m = 0$ เส้นสัมผัสแนวนอนขนานแกน ${v_lat}$ "
            f"เป็น จุดนิ่ง (Stationary Point) โดยจุดนิ่งไม่จำเป็นต้องเป็นจุดวกกลับเสมอไป"
        )

    step4 = (
        f"แทนค่าจุดสัมผัสหาความชัน m = f'(a) (Evaluate Slope): "
        f"แทนค่า ${v_lat} = {a_lat}$ ในสูตรอนุพันธ์:\n"
        f"m = f'({a_lat}) = {sp.latex(slope_sym)}\n"
        f"{slope_geo}"
    )

    # Step 5: แทนค่าลงในสูตร Point-Slope
    step5 = (
        f"แทนค่าในสมการรูปจุดและความชัน (Point-Slope Form): "
        f"แทนจุด $({a_lat}, {sp.latex(fa_sym)})$ และความชัน $m = {sp.latex(slope_sym)}$ ลงในสูตร $y - f(a) = m({v_lat} - a)$:\n"
        f"y - ({sp.latex(fa_sym)}) = {sp.latex(slope_sym)}\\left({v_lat} - {a_disp}\\right)"
    )

    # Step 6: จัดรูปสมการ Slope-Intercept Form y = mx + c
    algebra_lines = _format_tangent_algebra(v_lat, a_sym, fa_sym, slope_sym, tangent_eq)
    algebra_display = "\n".join(algebra_lines)
    c_val = sp.simplify(tangent_eq.subs(var_sym, 0))
    step6 = (
        f"จัดรูปสมการความชัน-จุดตัดแกน (Slope-Intercept Form: y = mx + c): "
        f"กระจายพจน์และย้ายข้างสมการ:\n"
        f"{algebra_display}\n"
        f"สมการเส้นสัมผัสคือ $y = {sp.latex(sp.simplify(tangent_eq))}$ (จุดตัดแกน $y$ คือ $(0, {sp.latex(c_val)})$)"
    )

    # Step 7: มโนทัศน์เพิ่มเติม Local Linear Approximation และ Normal Line
    if slope_sym != 0:
        normal_m = -1 / slope_sym
        normal_eq = normal_m * (var_sym - a_sym) + fa_sym
        normal_simp = sp.simplify(normal_eq)
        normal_desc = (
            f"2. เส้นแนวฉาก (Normal Line): ความชันตั้งฉาก $m_{{\\perp}} = -\\frac{{1}}{{m}} = {sp.latex(normal_m)}$\n"
            f"y - ({sp.latex(fa_sym)}) = {sp.latex(normal_m)}\\left({v_lat} - {a_disp}\\right) \\implies y = {sp.latex(normal_simp)}"
        )
    else:
        normal_desc = (
            f"2. เส้นแนวฉาก (Normal Line): เส้นตรงแนวดิ่ง ${v_lat} = {a_lat}$"
        )

    step7 = (
        f"มโนทัศน์เพิ่มเติมและเส้นแนวฉาก (Insights & Normal Line): "
        f"1. การประมาณค่าเชิงเส้น: $L({v_lat}) = {sp.latex(sp.simplify(tangent_eq))}$ เมื่อ ${v_lat} \\approx {a_lat}$\n"
        f"{normal_desc}"
    )

    return [step1, step2, step3, step4, step5, step6, step7]


def compute_tangent(expr_str: str, a: float) -> dict:
    """คำนวณความชันเส้นสัมผัส f'(a) และสมการเส้นสัมผัส y = f'(a)(x-a) + f(a)"""
    try:
        clean_str, diff_var = _clean_calculus_input(expr_str)
        expr = _parse_input(clean_str)
        if diff_var is not None:
            var_sym = sp.Symbol(diff_var)
        else:
            var_sym = _get_variable(expr)
        v_lat = sp.latex(var_sym)
        a_f = float(a)
        if a_f.is_integer():
            a_sym = sp.Integer(int(a_f))
        else:
            a_sym = sp.Rational(str(a))
        a_lat = sp.latex(a_sym)

        try:
            fa_sym = expr.subs(var_sym, a_sym)
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
                    f"กำหนดฟังก์ชัน $f({v_lat}) = {sp.latex(expr)}$ ที่ ${v_lat} = {a_lat}$",
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
            slope_sym = df.subs(var_sym, a_sym)
        except Exception:
            slope_sym = sp.nan

        if slope_sym.is_real and slope_sym.is_finite:
            status = "finite"
            slope = float(slope_sym)
            tangent_eq = slope_sym * (var_sym - a_sym) + fa_sym
            latex_str = f"y = {sp.latex(sp.simplify(tangent_eq))}"
            steps = _build_finite_tangent_steps(expr, var_sym, a_sym, fa_sym, df, slope_sym, tangent_eq)
        else:
            diff_quot = (expr.subs(var_sym, a_sym + H) - fa_sym) / H
            try:
                left_m = sp.limit(diff_quot, H, 0, dir="-")
                right_m = sp.limit(diff_quot, H, 0, dir="+")
            except Exception:
                left_m, right_m = sp.nan, sp.nan

            if left_m == right_m:
                if left_m in (sp.oo, -sp.oo):
                    status = "vertical"
                    slope = None
                    latex_str = f"{v_lat} = {a_lat}"
                    steps = [
                        f"กำหนดโจทย์และจุดที่พิจารณา: $f({v_lat}) = {sp.latex(expr)}, \\quad a = {a_lat}$",
                        f"คำนวณพิกัดจุดสัมผัส: $f({a_lat}) = {sp.latex(fa_sym)}$ ได้จุด $(a, f(a)) = ({a_lat}, {sp.latex(fa_sym)})$",
                        f"พิจารณาลิมิตของอัตราส่วนผลต่าง: "
                        f"\\lim_{{h \\to 0}} \\frac{{f({a_lat}+h) - f({a_lat})}}{{h}} = {sp.latex(left_m)}",
                        f"วิเคราะห์ความชัน: ความชันลู่สู่อนันต์ (${sp.latex(left_m)}$) เส้นสัมผัสตั้งฉากกับแกน ${v_lat}$ (แนวดิ่ง)",
                        f"สรุปสมการเส้นสัมผัสแนวดิ่ง (Vertical Tangent Line): "
                        f"เส้นสัมผัสแนวดิ่งผ่านจุด $({a_lat}, {sp.latex(fa_sym)})$ มีสมการคือ ${v_lat} = {a_lat}$",
                    ]
                elif getattr(left_m, "is_real", False) and getattr(left_m, "is_finite", False):
                    status = "finite"
                    slope = float(left_m)
                    tangent_eq = left_m * (var_sym - a_sym) + fa_sym
                    latex_str = f"y = {sp.latex(sp.simplify(tangent_eq))}"
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
                steps = [
                    f"กำหนดโจทย์และจุดที่พิจารณา: $f({v_lat}) = {sp.latex(expr)}, \\quad a = {a_lat}$",
                    f"คำนวณพิกัดจุดบนกราฟ: $f({a_lat}) = {sp.latex(fa_sym)}$ ได้จุด $(a, f(a)) = ({a_lat}, {sp.latex(fa_sym)})$",
                    f"เงื่อนไขอนุพันธ์: ฟังก์ชันหาอนุพันธ์ได้ ก็ต่อเมื่อ อนุพันธ์ทางซ้ายเท่ากับอนุพันธ์ทางขวา ($f'_-({a_lat}) = f'_+({a_lat})$)",
                    f"คำนวณอนุพันธ์ทางซ้าย (Left-Hand Derivative as h -> 0^-): "
                    f"f'_-({a_lat}) = \\lim_{{h \\to 0^-}} \\frac{{f({a_lat}+h) - f({a_lat})}}{{h}} = {sp.latex(left_m)}",
                    f"คำนวณอนุพันธ์ทางขวา (Right-Hand Derivative as h -> 0^+): "
                    f"f'_+({a_lat}) = \\lim_{{h \\to 0^+}} \\frac{{f({a_lat}+h) - f({a_lat})}}{{h}} = {sp.latex(right_m)}",
                    f"สรุปผลการวิเคราะห์: "
                    f"เนื่องจาก $f'_-({a_lat}) = {sp.latex(left_m)} \\neq {sp.latex(right_m)} = f'_+({a_lat})$\n"
                    f"กราฟมีลักษณะเป็นจุดมุมหัก (Corner Point) ฟังก์ชันจึงหาอนุพันธ์ไม่ได้และไม่มีเส้นสัมผัส",
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
