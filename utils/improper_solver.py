"""utils/improper_solver.py : อินทิกรัลไม่ตรงแบบ (Improper Integrals)

คำนวณอินทิกรัลไม่ตรงแบบผ่านลิมิต ตรวจสอบการลู่เข้า/ลู่ออก (Convergence/Divergence)
รองรับช่วงอนันต์ [a, oo), (-oo, b], (-oo, oo) และจุดเอกฐานที่ขอบเขต (Endpoints) และภายใน (Interior)
ตามเกณฑ์ Universal Step Contract
"""
import math
import re
import sys
import sympy as sp
from sympy.calculus.accumulationbounds import AccumulationBounds
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
    "inf": sp.oo,
    "infinity": sp.oo,
    "oo": sp.oo,
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


def _to_real_roots(e: sp.Expr) -> sp.Expr:
    """แปลงรากที่ติดค่าลบที่มีดัชนีเป็นเลขคี่ ให้เป็นค่าจริงตามหลักแคลคูลัส (เช่น (-1)**(1/3) -> -1)"""
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


def _parse_input(expr_str: str) -> sp.Expr:
    clean = (expr_str or "").strip()
    if not clean:
        raise ValueError("Empty input string")
    parsed = parse_expr(clean, transformations=TRANSFORMATIONS, local_dict=LOCAL_MATH_DICT)
    try:
        parsed = sp.nsimplify(parsed, rational=True)
    except Exception:
        pass
    return parsed


def _classify_improper(res_val: sp.Expr) -> str:
    """Improper-integral status: finite, divergent, unsupported, error."""
    if isinstance(res_val, sp.Integral):
        return "unsupported"
    if res_val is sp.nan or res_val.has(sp.zoo, sp.nan):
        return "divergent"
    if isinstance(res_val, AccumulationBounds):
        return "divergent"
    if res_val.has(sp.oo, -sp.oo):
        return "divergent"
    res_real = _to_real_roots(res_val)
    if getattr(res_real, "is_finite", False) is True and getattr(res_real, "is_real", False) is True:
        return "finite"
    # Special values such as Si(1) carry no is_finite flag, but a finite real
    # numeric value still proves convergence.
    if _safe_float(res_real) is not None:
        return "finite"
    return "unsupported"


def _safe_float(value: sp.Expr):
    """Real float value of a SymPy expression, or None when it is not finite/real."""
    if value is None:
        return None
    try:
        real_val = _to_real_roots(value)
        numeric = complex(real_val.evalf(15))
    except Exception:
        return None
    if abs(numeric.imag) > 1e-12 or not math.isfinite(numeric.real):
        return None
    return float(numeric.real)


def _get_antiderivative(expr: sp.Expr, var: sp.Symbol) -> sp.Expr | None:
    """หาปฏิยานุพันธ์ในรูปฟังก์ชันมูลฐานที่สะอาด ไม่มี Piecewise หรือ Meijer G โดยใช้ manualintegrate ก่อน"""
    try:
        from sympy.integrals.manualintegrate import manualintegrate
        anti = manualintegrate(expr, var)
        if anti is not None and not anti.has(sp.Integral) and not anti.has(sp.meijerg) and not anti.has(sp.Piecewise):
            return _abs_logs(_to_real_roots(anti))
    except Exception:
        pass
    try:
        anti = sp.integrate(expr, var)
        if anti.has(sp.Piecewise):
            try:
                pos_sym = sp.Symbol("_pos_x", positive=True)
                anti_pos = sp.integrate(expr.subs(var, pos_sym), pos_sym).subs(pos_sym, var)
                if not anti_pos.has(sp.Piecewise):
                    anti = anti_pos
            except Exception:
                pass
        return _abs_logs(_to_real_roots(anti))
    except Exception:
        return None


def _format_part_outcome(status: str, part_val) -> str:
    """Format step explanation for a single-sided improper branch in proper Thai math terminology."""
    if status == "finite":
        val_tex = _to_latex(part_val)
        return f"ลู่เข้าสู่ค่าจริงจำกัด เท่ากับ ${val_tex}$"
    elif status == "divergent":
        val_tex = _to_latex(part_val) if part_val is not None else ""
        if val_tex in (r"\infty", r"-\infty"):
            return f"ลู่ออก (Diverges สู่ ${val_tex}$)"
        return "ลู่ออก (Diverges หาค่าไม่ได้)"
    return "ไม่สามารถสรุปค่าได้"


def _parse_bound(val: float | int | str | sp.Expr | None, is_upper: bool = False) -> sp.Expr:
    if val is None:
        return sp.oo if is_upper else -sp.oo
    if isinstance(val, (int, float)):
        return sp.Rational(str(val))
    if isinstance(val, sp.Expr):
        return val
    s = str(val).strip().lower().replace(" ", "")
    if s in ("inf", "+inf", "oo", "+oo", "infinity", "+infinity"):
        return sp.oo
    if s in ("-inf", "-oo", "-infinity"):
        return -sp.oo
    return parse_expr(str(val).strip(), transformations=TRANSFORMATIONS, local_dict=LOCAL_MATH_DICT)


def _format_bound_latex(val: float | int | str | sp.Expr | None) -> str:
    """จัดรูปแบบขอบเขตบน/ล่างเป็น LaTeX"""
    if val is None or val == sp.oo:
        return "\\infty"
    if val == -sp.oo:
        return "-\\infty"
    try:
        f = float(val)
        if f.is_integer():
            return str(int(f))
        return f"{f:g}"
    except Exception:
        pass
    try:
        sp_v = sp.sympify(val)
        if sp_v == sp.oo:
            return "\\infty"
        if sp_v == -sp.oo:
            return "-\\infty"
        return _to_latex(sp_v)
    except Exception:
        return str(val)


def _find_interior_singularities(expr: sp.Expr, a_val: float, b_val: float, var: sp.Symbol = X) -> list[float]:
    """ค้นหาจุดเอกฐานภายในช่วงเปิด (a, b) จากรากของตัวส่วน"""
    sings = []
    denom = sp.denom(expr.rewrite(sp.cos))
    if denom != 1:
        try:
            sol = sp.solve(denom, var)
            for s in sol:
                if getattr(s, "is_real", False) and a_val < float(s) < b_val:
                    s_f = float(s)
                    if not any(abs(s_f - ex) < 1e-4 for ex in sings):
                        sings.append(s_f)
        except Exception:
            pass
    return sorted(sings)


def _is_singular_at_point(expr: sp.Expr, pt: sp.Expr, direction: str, var: sp.Symbol = X) -> bool:
    """ตรวจสอบว่าจุด pt เป็นจุดเอกฐานของ expr หรือไม่ จากการหาลิมิตด้านเดียว"""
    try:
        denom = sp.denom(expr)
        if denom != 1 and denom.subs(var, pt) == 0:
            return True
        val = expr.subs(var, pt)
        if val in (sp.zoo, sp.oo, -sp.oo, sp.nan) or getattr(val, "is_infinite", False):
            return True
    except Exception:
        pass

    try:
        lim = sp.limit(expr, var, pt, direction)
        if lim in (sp.oo, -sp.oo, sp.zoo, sp.nan) or lim.has(sp.oo, -sp.oo, sp.zoo):
            return True
    except Exception:
        pass

    return False


def _abs_logs(expr: sp.Expr) -> sp.Expr:
    """Wrap every logarithm argument in |.| so substituting an endpoint stays real.

    SymPy returns log(x - 1) for 1/(x**2 - 1); at x = 0 that evaluates to
    log(-1) = i*pi, which is correct over the complex numbers but confusing in a
    Calculus 1 step-by-step explanation. The textbook form is log|x - 1|.
    """
    return expr.replace(
        lambda node: isinstance(node, sp.log),
        lambda node: sp.log(sp.Abs(node.args[0])),
    )


def _divergence_reason(antideriv: sp.Expr, var: sp.Symbol) -> str:
    """Explain a divergent infinite-bound integral from its own antiderivative."""
    t = sp.Symbol("t", positive=True)
    try:
        at_t = sp.simplify(antideriv.subs(var, t))
    except Exception:
        at_t = antideriv
    if at_t.has(sp.log(sp.log(t))):
        return r"เพราะ $\ln(\ln t) \to \infty$ เมื่อ $t \to \infty$"
    if at_t.has(sp.log(t)):
        return r"เพราะ $\ln t \to \infty$ เมื่อ $t \to \infty$"
    return r"เพราะ $F(t)$ ไม่มีลิมิตจำกัดเมื่อ $t \to \infty$"


def compute_improper(expr_str: str, a: float | int | str | sp.Expr = 0.0, b: float | int | str | sp.Expr | None = None) -> dict:
    """คำนวณอินทิกรัลไม่ตรงแบบผ่านลิมิต ตรวจสอบการลู่เข้า/ลู่ออกตาม Universal Step Contract"""
    try:
        clean_str, diff_var = _clean_calculus_input(expr_str)
        expr = _parse_input(clean_str)
        if diff_var is not None:
            var_sym = sp.Symbol(diff_var)
        else:
            var_sym = _get_variable(expr)
        v_lat = _to_latex(var_sym)

        lower = _parse_bound(a, is_upper=False)
        upper = _parse_bound(b, is_upper=True)

        lower_latex = _format_bound_latex(lower)
        bound_latex = _format_bound_latex(upper)

        steps = [
            f"กำหนดโจทย์อินทิกรัล: $\\int_{{{lower_latex}}}^{{{bound_latex}}} \\left({_to_latex(expr)}\\right) \\, d{v_lat}$",
        ]

        interior_sings: list[float] = []

        # -------------------------------------------------------------
        # กรณีที่ 1: สองฝั่งเป็นอนันต์ (-oo, oo)
        # -------------------------------------------------------------
        if lower == -sp.oo and upper == sp.oo:
            c_val = 0
            denom = sp.denom(expr)
            if denom.subs(var_sym, 0) == 0:
                c_val = 1

            steps.append(
                f"อินทิกรัลไม่ตรงแบบชนิดที่ 1: ช่วงอนันต์สองฝั่ง $(-\\infty, \\infty)$ "
                f"แยกช่วงที่จุด $c = {c_val}$ ตามนิยาม:\n"
                f"$$\\int_{{-\\infty}}^{{\\infty}} f({v_lat})\\,d{v_lat} = \\lim_{{s \\to -\\infty}} \\int_{{s}}^{{{c_val}}} f({v_lat})\\,d{v_lat} + \\lim_{{t \\to \\infty}} \\int_{{{c_val}}}^{{t}} f({v_lat})\\,d{v_lat}$$"
            )

            left_part = _to_real_roots(sp.integrate(expr, (var_sym, -sp.oo, c_val)))
            right_part = _to_real_roots(sp.integrate(expr, (var_sym, c_val, sp.oo)))
            left_status = _classify_improper(left_part)
            right_status = _classify_improper(right_part)
            if left_status == "unsupported" or right_status == "unsupported":
                antideriv = _get_antiderivative(expr, var_sym)
                if antideriv is not None:
                    if left_status == "unsupported":
                        s_sym = sp.Symbol("s", negative=True)
                        lp = _to_real_roots(sp.limit(antideriv.subs(var_sym, c_val) - antideriv.subs(var_sym, s_sym), s_sym, -sp.oo))
                        ls = _classify_improper(lp)
                        if ls != "unsupported":
                            left_part = lp
                            left_status = ls
                    if right_status == "unsupported":
                        t_sym = sp.Symbol("t", positive=True)
                        rp = _to_real_roots(sp.limit(antideriv.subs(var_sym, t_sym) - antideriv.subs(var_sym, c_val), t_sym, sp.oo))
                        rs = _classify_improper(rp)
                        if rs != "unsupported":
                            right_part = rp
                            right_status = rs
            res_val = None

            left_desc = _format_part_outcome(left_status, left_part)
            right_desc = _format_part_outcome(right_status, right_part)
            steps.append(
                f"คำนวณลิมิตแต่ละฝั่งแยกกัน:\n"
                f"- ฝั่งซ้าย: $\\lim_{{s \\to -\\infty}} \\int_{{s}}^{{{c_val}}} f({v_lat})\\,d{v_lat}$ {left_desc}\n"
                f"- ฝั่งขวา: $\\lim_{{t \\to \\infty}} \\int_{{{c_val}}}^{{t}} f({v_lat})\\,d{v_lat}$ {right_desc}"
            )

            if left_status == "divergent" or right_status == "divergent":
                status = "divergent"
                result = None
                value_latex = "\\text{diverges}"
                steps.append(
                    "เงื่อนไขโดเมนและการลู่เข้า: ตามนิยามทางคณิตศาสตร์ หากมีส่วนย่อยอย่างน้อย 1 ฝั่งลู่ออก "
                    "อินทิกรัลทั้งหมดจะถือว่า **ลู่ออก (Diverges)** (ไม่สามารถนำ $\\pm\\infty$ มาหักล้างกันได้)"
                )
                steps.append("ผลลัพธ์: อินทิกรัลลู่ออก (Diverges)")
            elif left_status == "finite" and right_status == "finite":
                res_val = left_part + right_part
                status = "finite"
                result = _safe_float(res_val)
                value_latex = _to_latex(res_val)
                steps.append(
                    f"สรุปผลลัพธ์: ทั้งสองฝั่งลู่เข้าสู่ค่าจริงจำกัด รวมกันได้: "
                    f"$\\int_{{-\\infty}}^{{\\infty}} \\left({_to_latex(expr)}\\right) \\, d{v_lat} = {value_latex} \\approx {result:.6g}$"
                )
            else:
                status = "unsupported"
                result = None
                value_latex = "\\text{unsupported}"
                steps.append("ระบบไม่สามารถคำนวณลิมิตในรูปแบบปิดได้")

            latex_str = f"\\int_{{-\\infty}}^{{\\infty}} {_to_latex(expr)} \\, d{v_lat} = {value_latex}"
            return {
                "ok": True,
                "result": result,
                "latex": latex_str,
                "steps": steps,
                "expr": expr,
                "value_expr": res_val,
                "error": None,
                "status": status,
                "interior_singularities": [],
                "variable": str(var_sym.name),
            }

        # -------------------------------------------------------------
        # กรณีที่ 2: ขอบล่างเป็น -oo และขอบบนจำกัด
        # -------------------------------------------------------------
        if lower == -sp.oo and upper != sp.oo:
            t_sym = sp.Symbol("t", negative=True)
            steps.append(
                f"อินทิกรัลไม่ตรงแบบชนิดที่ 1 (ขอบล่างเป็นอนันต์):\n"
                f"\\lim_{{t \\to -\\infty}} \\int_{{t}}^{{{bound_latex}}} \\left({_to_latex(expr)}\\right) \\, d{v_lat}\n"
                f"(แปลงเป็นรูปลิมิตของอินทิกรัลจำกัดเขตเมื่อขอบล่างเข้าใกล้ $-\\infty$)"
            )
            antideriv = _get_antiderivative(expr, var_sym)
            if antideriv is None:
                antideriv = _abs_logs(sp.integrate(expr, var_sym))
            upper_eval = antideriv.subs(var_sym, upper)
            t_eval = antideriv.subs(var_sym, t_sym)
            diff_t = sp.simplify(upper_eval - t_eval)

            upper_sub_tex = _to_latex(upper_eval)
            t_sub_tex = f"\\left({_to_latex(t_eval)}\\right)" if str(t_eval).startswith("-") else _to_latex(t_eval)
            diff_t_tex = _to_latex(diff_t)
            if diff_t_tex != f"{upper_sub_tex} - {t_sub_tex}":
                bounds_eval_str = f"\\left({upper_sub_tex}\\right) - {t_sub_tex} = {diff_t_tex}"
            else:
                bounds_eval_str = f"\\left({upper_sub_tex}\\right) - {t_sub_tex}"

            steps.append(
                f"หาปฏิยานุพันธ์และแทนค่าขอบเขต $t$:\n"
                f"\\int_{{t}}^{{{bound_latex}}} \\left({_to_latex(expr)}\\right) \\, d{v_lat} = "
                f"\\left[ {_to_latex(antideriv)} \\right]_{{t}}^{{{bound_latex}}} = {bounds_eval_str}"
            )

            res_val = _to_real_roots(sp.integrate(expr, (var_sym, -sp.oo, upper)))
            status = _classify_improper(res_val)
            if status == "unsupported":
                lim_val = _to_real_roots(sp.limit(diff_t, t_sym, -sp.oo))
                lim_status = _classify_improper(lim_val)
                if lim_status != "unsupported":
                    res_val = lim_val
                    status = lim_status
            if status == "finite":
                result = _safe_float(res_val)
                value_latex = _to_latex(res_val)
                steps.append(
                    f"คำนวณค่าลิมิตเมื่อ $t \\to -\\infty$:\n"
                    f"\\lim_{{t \\to -\\infty}} \\left({diff_t_tex}\\right) = {value_latex}"
                )
                steps.append(f"สรุปผลลัพธ์: ลิมิตมีค่าจริงจำกัด เท่ากับ ${value_latex} \\approx {result:.6g}$ ดังนั้นอินทิกรัล **ลู่เข้า (Converges)**")
            elif status == "divergent":
                result = None
                value_latex = "\\text{diverges}"
                steps.append(
                    f"คำนวณค่าลิมิตเมื่อ $t \\to -\\infty$:\n"
                    f"\\lim_{{t \\to -\\infty}} \\left({diff_t_tex}\\right) = \\infty"
                )
                steps.append(
                    r"สรุปผลลัพธ์: ลิมิตไม่มีค่าจำกัดเมื่อ $t \to -\infty$ ดังนั้นอินทิกรัล **ลู่ออก (Diverges)**"
                )
            else:
                result = None
                value_latex = "\\text{unsupported}"
                steps.append("ระบบไม่สามารถคำนวณลิมิตในรูปแบบปิดได้")

            latex_str = f"\\int_{{{lower_latex}}}^{{{bound_latex}}} {_to_latex(expr)} \\, d{v_lat} = {value_latex}"
            return {
                "ok": True,
                "result": result,
                "latex": latex_str,
                "steps": steps,
                "expr": expr,
                "value_expr": res_val,
                "error": None,
                "status": status,
                "interior_singularities": [],
                "variable": str(var_sym.name),
            }

        # -------------------------------------------------------------
        # กรณีที่ 3: ขอบล่างจำกัด และขอบบนเป็น oo
        # -------------------------------------------------------------
        if lower != -sp.oo and upper == sp.oo:
            t_sym = sp.Symbol("t", positive=True)
            steps.append(
                f"อินทิกรัลไม่ตรงแบบชนิดที่ 1 (ขอบบนเป็นอนันต์):\n"
                f"\\lim_{{t \\to \\infty}} \\int_{{{lower_latex}}}^{{t}} \\left({_to_latex(expr)}\\right) \\, d{v_lat}\n"
                f"(แปลงเป็นรูปลิมิตของอินทิกรัลจำกัดเขตเมื่อตัวแปรเข้าใกล้อนันต์)"
            )
            antideriv = _get_antiderivative(expr, var_sym)
            if antideriv is None:
                antideriv = _abs_logs(sp.integrate(expr, var_sym))
            lower_eval = antideriv.subs(var_sym, lower)
            t_eval = antideriv.subs(var_sym, t_sym)
            diff_t = sp.simplify(t_eval - lower_eval)

            lower_sub_tex = f"\\left({_to_latex(lower_eval)}\\right)" if str(lower_eval).startswith("-") else _to_latex(lower_eval)
            t_sub_tex = _to_latex(t_eval)
            diff_t_tex = _to_latex(diff_t)
            if diff_t_tex != f"{t_sub_tex} - {lower_sub_tex}":
                bounds_eval_str = f"\\left({t_sub_tex}\\right) - {lower_sub_tex} = {diff_t_tex}"
            else:
                bounds_eval_str = f"\\left({t_sub_tex}\\right) - {lower_sub_tex}"

            steps.append(
                f"หาปฏิยานุพันธ์และแทนค่าขอบเขต $t$:\n"
                f"\\int_{{{lower_latex}}}^{{t}} \\left({_to_latex(expr)}\\right) \\, d{v_lat} = "
                f"\\left[ {_to_latex(antideriv)} \\right]_{{{lower_latex}}}^{{t}} = {bounds_eval_str}"
            )

            res_val = _to_real_roots(sp.integrate(expr, (var_sym, lower, sp.oo)))
            status = _classify_improper(res_val)
            if status == "unsupported":
                lim_val = _to_real_roots(sp.limit(diff_t, t_sym, sp.oo))
                lim_status = _classify_improper(lim_val)
                if lim_status != "unsupported":
                    res_val = lim_val
                    status = lim_status
            if status == "finite":
                result = _safe_float(res_val)
                value_latex = _to_latex(res_val)
                steps.append(
                    f"คำนวณค่าลิมิตเมื่อ $t \\to \\infty$:\n"
                    f"\\lim_{{t \\to \\infty}} \\left({diff_t_tex}\\right) = {value_latex}"
                )
                steps.append(f"สรุปผลลัพธ์: ลิมิตมีค่าจริงจำกัด เท่ากับ ${value_latex} \\approx {result:.6g}$ ดังนั้นอินทิกรัล **ลู่เข้า (Converges)**")
            elif status == "divergent":
                result = None
                value_latex = "\\text{diverges}"
                steps.append(
                    f"คำนวณค่าลิมิตเมื่อ $t \\to \\infty$:\n"
                    f"\\lim_{{t \\to \\infty}} \\left({diff_t_tex}\\right) = \\infty"
                )
                steps.append(
                    f"สรุปผลลัพธ์: ลิมิตไม่มีค่าจำกัด ({_divergence_reason(antideriv, var_sym)}) "
                    f"ดังนั้นอินทิกรัล **ลู่ออก (Diverges)**"
                )
            else:
                result = None
                value_latex = "\\text{unsupported}"
                steps.append("ระบบไม่สามารถคำนวณลิมิตในรูปแบบปิดได้")

            latex_str = f"\\int_{{{lower_latex}}}^{{{bound_latex}}} {_to_latex(expr)} \\, d{v_lat} = {value_latex}"
            return {
                "ok": True,
                "result": result,
                "latex": latex_str,
                "steps": steps,
                "expr": expr,
                "value_expr": res_val,
                "error": None,
                "status": status,
                "interior_singularities": [],
                "variable": str(var_sym.name),
            }

        # -------------------------------------------------------------
        # กรณีที่ 4: ขอบเขตจำกัดทั้งคู่ [a, b]
        # ตรวจสอบจุดเอกฐาน: ภายใน (Interior) หรือ ที่ขอบเขต (Endpoints)
        # -------------------------------------------------------------
        f_a = float(lower.evalf())
        f_b = float(upper.evalf())
        if f_a >= f_b:
            raise ValueError("ขอบล่าง a ต้องน้อยกว่าขอบบน b")

        interior_sings = _find_interior_singularities(expr, f_a, f_b, var=var_sym)

        # 4.1 มีจุดเอกฐานภายในช่วงเปิด (a, b)
        if interior_sings:
            c_val = interior_sings[0]
            c_sp = sp.nsimplify(c_val)
            c_latex = _format_bound_latex(c_sp)
            steps.append(
                f"อินทิกรัลไม่ตรงแบบชนิดที่ 2: พบจุดที่ฟังก์ชันไม่ต่อเนื่องภายในช่วง (Interior Singularity) ที่ ${v_lat} = {c_latex}$ "
                f"ซึ่งทำให้ฟังก์ชันไม่ต่อเนื่อง จึงแยกช่วงคำนวณตามนิยาม:\n"
                f"$$\\int_{{{lower_latex}}}^{{{bound_latex}}} f({v_lat})\\,d{v_lat} = "
                f"\\lim_{{t \\to {c_latex}^-}} \\int_{{{lower_latex}}}^{{t}} f({v_lat})\\,d{v_lat} + "
                f"\\lim_{{s \\to {c_latex}^+}} \\int_{{s}}^{{{bound_latex}}} f({v_lat})\\,d{v_lat}$$"
            )

            left_part = _to_real_roots(sp.integrate(expr, (var_sym, lower, c_sp)))
            right_part = _to_real_roots(sp.integrate(expr, (var_sym, c_sp, upper)))
            left_status = _classify_improper(left_part)
            right_status = _classify_improper(right_part)
            if left_status == "unsupported" or right_status == "unsupported":
                antideriv = _get_antiderivative(expr, var_sym)
                if antideriv is None:
                    antideriv = _abs_logs(sp.integrate(expr, var_sym))
                if antideriv is not None:
                    if left_status == "unsupported":
                        t_sym = sp.Symbol("t", real=True)
                        f_t = antideriv.subs(var_sym, t_sym)
                        f_low = antideriv.subs(var_sym, lower)
                        lp = _to_real_roots(sp.limit(f_t - f_low, t_sym, c_sp, "-"))
                        ls = _classify_improper(lp)
                        if ls != "unsupported":
                            left_part = lp
                            left_status = ls
                    if right_status == "unsupported":
                        s_sym = sp.Symbol("s", real=True)
                        f_up = antideriv.subs(var_sym, upper)
                        f_s = antideriv.subs(var_sym, s_sym)
                        rp = _to_real_roots(sp.limit(f_up - f_s, s_sym, c_sp, "+"))
                        rs = _classify_improper(rp)
                        if rs != "unsupported":
                            right_part = rp
                            right_status = rs
            res_val = None

            left_desc = _format_part_outcome(left_status, left_part)
            right_desc = _format_part_outcome(right_status, right_part)
            steps.append(
                f"คำนวณลิมิตแต่ละฝั่งแยกกัน:\n"
                f"- ฝั่งซ้าย: $\\lim_{{t \\to {c_latex}^-}} \\int_{{{lower_latex}}}^{{t}} f({v_lat})\\,d{v_lat}$ {left_desc}\n"
                f"- ฝั่งขวา: $\\lim_{{s \\to {c_latex}^+}} \\int_{{s}}^{{{bound_latex}}} f({v_lat})\\,d{v_lat}$ {right_desc}"
            )

            if left_status == "divergent" or right_status == "divergent":
                status = "divergent"
                result = None
                value_latex = "\\text{diverges}"
                steps.append(
                    "เงื่อนไขโดเมนและการลู่เข้า: ตามนิยามทางคณิตศาสตร์ หากมีส่วนย่อยอย่างน้อย 1 ฝั่งลู่ออก "
                    "อินทิกรัลไม่ตรงแบบทั้งหมดจะถือว่า **ลู่ออก (Diverges)** (ไม่สามารถนำ $\\pm\\infty$ มาหักล้างกันได้)"
                )
                steps.append("ผลลัพธ์: อินทิกรัลลู่ออก (Diverges)")
            elif left_status == "finite" and right_status == "finite":
                res_val = _to_real_roots(left_part) + _to_real_roots(right_part)
                status = "finite"
                result = _safe_float(res_val)
                value_latex = _to_latex(res_val)
                steps.append(
                    f"สรุปผลลัพธ์: ทั้งสองฝั่งลู่เข้าสู่ค่าจริงจำกัด รวมกันได้: "
                    f"$\\int_{{{lower_latex}}}^{{{bound_latex}}} f({v_lat})\\,d{v_lat} = {value_latex}$"
                )
            else:
                status = "unsupported"
                result = None
                value_latex = "\\text{unsupported}"
                steps.append("ระบบไม่สามารถคำนวณลิมิตในรูปแบบปิดได้")

            latex_str = f"\\int_{{{lower_latex}}}^{{{bound_latex}}} {_to_latex(expr)} \\, d{v_lat} = {value_latex}"
            return {
                "ok": True,
                "result": result,
                "latex": latex_str,
                "steps": steps,
                "expr": expr,
                "value_expr": res_val,
                "error": None,
                "status": status,
                "interior_singularities": interior_sings,
                "variable": str(var_sym.name),
            }

        # 4.2 ตรวจสอบจุดเอกฐานที่ขอบเขต (Endpoint Singularities)
        lower_singular = _is_singular_at_point(expr, lower, "+", var=var_sym)
        upper_singular = _is_singular_at_point(expr, upper, "-", var=var_sym)

        # ฟังก์ชันไม่ต่อเนื่องที่ขอบล่าง a เท่านั้น (เช่น 1/sqrt(x) บน [0, 1])
        if lower_singular and not upper_singular:
            t_sym = sp.Symbol("t")
            steps.append(
                f"อินทิกรัลไม่ตรงแบบชนิดที่ 2 (จุดไม่ต่อเนื่องที่ขอบล่าง ${v_lat} = {lower_latex}$):\n"
                f"\\lim_{{t \\to {lower_latex}^+}} \\int_{{t}}^{{{bound_latex}}} \\left({_to_latex(expr)}\\right) \\, d{v_lat}\n"
                f"(ฟังก์ชันมีลิมิตเข้าสู่อนันต์ที่ขอบล่าง ในขณะที่ฟังก์ชันต่อเนื่องที่ขอบบน จึงแปลงเป็นรูปลิมิตเข้าใกล้ทางขวา)"
            )
            antideriv = _get_antiderivative(expr, var_sym)
            if antideriv is None:
                antideriv = _abs_logs(sp.integrate(expr, var_sym))
            upper_eval = antideriv.subs(var_sym, upper)
            t_eval = antideriv.subs(var_sym, t_sym)
            diff_t = sp.simplify(upper_eval - t_eval)
            diff_t_tex = _to_latex(diff_t)
            upper_sub_tex = _to_latex(upper_eval)
            t_sub_tex = f"\\left({_to_latex(t_eval)}\\right)" if str(t_eval).startswith("-") else _to_latex(t_eval)

            if diff_t_tex != f"{upper_sub_tex} - {t_sub_tex}":
                bounds_eval_str = f"\\left({upper_sub_tex}\\right) - {t_sub_tex} = {diff_t_tex}"
            else:
                bounds_eval_str = f"\\left({upper_sub_tex}\\right) - {t_sub_tex}"

            steps.append(
                f"หาปฏิยานุพันธ์และแทนค่าขอบเขต $t$:\n"
                f"\\int_{{t}}^{{{bound_latex}}} \\left({_to_latex(expr)}\\right) \\, d{v_lat} = "
                f"\\left[ {_to_latex(antideriv)} \\right]_{{t}}^{{{bound_latex}}} = {bounds_eval_str}"
            )

            res_val = _to_real_roots(sp.integrate(expr, (var_sym, lower, upper)))
            status = _classify_improper(res_val)
            if status == "unsupported":
                lim_val = _to_real_roots(sp.limit(diff_t, t_sym, lower, "+"))
                lim_status = _classify_improper(lim_val)
                if lim_status != "unsupported":
                    res_val = lim_val
                    status = lim_status
            if status == "finite":
                result = _safe_float(res_val)
                value_latex = _to_latex(res_val)
                steps.append(
                    f"คำนวณค่าลิมิตเมื่อ $t \\to {lower_latex}^+$:\n"
                    f"\\lim_{{t \\to {lower_latex}^+}} \\left({diff_t_tex}\\right) = {value_latex}"
                )
                steps.append(f"สรุปผลลัพธ์: ลิมิตมีค่าจริงจำกัด เท่ากับ ${value_latex} \\approx {result:.6g}$ ดังนั้นอินทิกรัล **ลู่เข้า (Converges)**")
            elif status == "divergent":
                result = None
                value_latex = "\\text{diverges}"
                steps.append(
                    f"คำนวณค่าลิมิตเมื่อ $t \\to {lower_latex}^+$:\n"
                    f"\\lim_{{t \\to {lower_latex}^+}} \\left({diff_t_tex}\\right) = \\infty"
                )
                steps.append("สรุปผลลัพธ์: ลิมิตลู่ออกสู่อนันต์ ดังนั้นอินทิกรัล **ลู่ออก (Diverges)**")
            else:
                result = None
                value_latex = "\\text{unsupported}"
                steps.append("ระบบไม่สามารถคำนวณลิมิตในรูปแบบปิดได้")

            latex_str = f"\\int_{{{lower_latex}}}^{{{bound_latex}}} {_to_latex(expr)} \\, d{v_lat} = {value_latex}"
            return {
                "ok": True,
                "result": result,
                "latex": latex_str,
                "steps": steps,
                "expr": expr,
                "value_expr": res_val,
                "error": None,
                "status": status,
                "interior_singularities": [],
                "variable": str(var_sym.name),
            }

        # ฟังก์ชันไม่ต่อเนื่องที่ขอบบน b เท่านั้น (เช่น 1/sqrt(1-x) บน [0, 1])
        if upper_singular and not lower_singular:
            t_sym = sp.Symbol("t")
            steps.append(
                f"อินทิกรัลไม่ตรงแบบชนิดที่ 2 (จุดไม่ต่อเนื่องที่ขอบบน ${v_lat} = {bound_latex}$):\n"
                f"\\lim_{{t \\to {bound_latex}^-}} \\int_{{{lower_latex}}}^{{t}} \\left({_to_latex(expr)}\\right) \\, d{v_lat}\n"
                f"(ฟังก์ชันมีลิมิตเข้าสู่อนันต์ที่ขอบบน ในขณะที่ฟังก์ชันต่อเนื่องที่ขอบล่าง จึงแปลงเป็นรูปลิมิตเข้าใกล้ทางซ้าย)"
            )
            antideriv = _get_antiderivative(expr, var_sym)
            if antideriv is None:
                antideriv = _abs_logs(sp.integrate(expr, var_sym))
            t_eval = antideriv.subs(var_sym, t_sym)
            lower_eval = antideriv.subs(var_sym, lower)
            diff_t = sp.simplify(t_eval - lower_eval)
            diff_t_tex = _to_latex(diff_t)
            lower_sub_tex = f"\\left({_to_latex(lower_eval)}\\right)" if str(lower_eval).startswith("-") else _to_latex(lower_eval)
            t_sub_tex = _to_latex(t_eval)

            if diff_t_tex != f"{t_sub_tex} - {lower_sub_tex}":
                bounds_eval_str = f"\\left({t_sub_tex}\\right) - {lower_sub_tex} = {diff_t_tex}"
            else:
                bounds_eval_str = f"\\left({t_sub_tex}\\right) - {lower_sub_tex}"

            steps.append(
                f"หาปฏิยานุพันธ์และแทนค่าขอบเขต $t$:\n"
                f"\\int_{{{lower_latex}}}^{{t}} \\left({_to_latex(expr)}\\right) \\, d{v_lat} = "
                f"\\left[ {_to_latex(antideriv)} \\right]_{{{lower_latex}}}^{{t}} = {bounds_eval_str}"
            )

            res_val = _to_real_roots(sp.integrate(expr, (var_sym, lower, upper)))
            status = _classify_improper(res_val)
            if status == "unsupported":
                lim_val = _to_real_roots(sp.limit(diff_t, t_sym, upper, "-"))
                lim_status = _classify_improper(lim_val)
                if lim_status != "unsupported":
                    res_val = lim_val
                    status = lim_status
            if status == "finite":
                result = _safe_float(res_val)
                value_latex = _to_latex(res_val)
                steps.append(
                    f"คำนวณค่าลิมิตเมื่อ $t \\to {bound_latex}^-$:\n"
                    f"\\lim_{{t \\to {bound_latex}^-}} \\left({diff_t_tex}\\right) = {value_latex}"
                )
                steps.append(f"สรุปผลลัพธ์: ลิมิตมีค่าจริงจำกัด เท่ากับ ${value_latex} \\approx {result:.6g}$ ดังนั้นอินทิกรัล **ลู่เข้า (Converges)**")
            elif status == "divergent":
                result = None
                value_latex = "\\text{diverges}"
                steps.append(
                    f"คำนวณค่าลิมิตเมื่อ $t \\to {bound_latex}^-$:\n"
                    f"\\lim_{{t \\to {bound_latex}^-}} \\left({diff_t_tex}\\right) = \\infty"
                )
                steps.append("สรุปผลลัพธ์: ลิมิตลู่ออกสู่อนันต์ ดังนั้นอินทิกรัล **ลู่ออก (Diverges)**")
            else:
                result = None
                value_latex = "\\text{unsupported}"
                steps.append("ระบบไม่สามารถคำนวณลิมิตในรูปแบบปิดได้")

            latex_str = f"\\int_{{{lower_latex}}}^{{{bound_latex}}} {_to_latex(expr)} \\, d{v_lat} = {value_latex}"
            return {
                "ok": True,
                "result": result,
                "latex": latex_str,
                "steps": steps,
                "expr": expr,
                "value_expr": res_val,
                "error": None,
                "status": status,
                "interior_singularities": [],
                "variable": str(var_sym.name),
            }

        # 4.2b ฟังก์ชันไม่ต่อเนื่องที่ขอบทั้งสอง (เช่น 1/sqrt(x*(1-x)) บน [0, 1])
        if lower_singular and upper_singular:
            mid = sp.nsimplify((lower + upper) / 2)
            mid_latex = _to_latex(mid)
            steps.append(
                f"อินทิกรัลไม่ตรงแบบชนิดที่ 2: พบจุดที่ฟังก์ชันไม่ต่อเนื่องที่ขอบทั้งสอง "
                f"${v_lat} = {lower_latex}$ และ ${v_lat} = {bound_latex}$ "
                f"จึงแยกช่วงที่จุดกึ่งกลาง ${v_lat} = {mid_latex}$ แล้วรวมสองลิมิต:\n"
                f"$$\\lim_{{t \\to {mid_latex}^-}} \\int_{{{lower_latex}}}^{{t}} f({v_lat})\\,d{v_lat}"
                f" + \\lim_{{s \\to {mid_latex}^+}} \\int_{{s}}^{{{bound_latex}}} f({v_lat})\\,d{v_lat}$$"
            )
            res_val = _to_real_roots(sp.integrate(expr, (var_sym, lower, upper)))
            # A Piecewise antiderivative can leave an unevaluated Integral, a zoo or
            # an imaginary constant; that is not evidence of divergence, so refuse
            # to classify it instead of guessing.
            unreliable = (
                res_val.has(sp.Integral) or res_val.has(sp.zoo)
                or res_val.has(sp.I) or res_val.has(sp.oo, -sp.oo)
            )
            if unreliable:
                antideriv = _get_antiderivative(expr, var_sym)
                if antideriv is not None:
                    t_sym = sp.Symbol("t", real=True)
                    s_sym = sp.Symbol("s", real=True)
                    f_mid = antideriv.subs(var_sym, mid)
                    lp = _to_real_roots(sp.limit(f_mid - antideriv.subs(var_sym, t_sym), t_sym, lower, "+"))
                    rp = _to_real_roots(sp.limit(antideriv.subs(var_sym, s_sym) - f_mid, s_sym, upper, "-"))
                    ls = _classify_improper(lp)
                    rs = _classify_improper(rp)
                    if ls == "finite" and rs == "finite":
                        res_val = lp + rp
                        status = "finite"
                        unreliable = False
                    elif ls == "divergent" or rs == "divergent":
                        status = "divergent"
                        unreliable = False
            if unreliable:
                status = "unsupported"
                result = None
                value_latex = "\\text{unsupported}"
                steps.append("ระบบไม่สามารถหาค่าลิมิตของสองช่วงในรูปแบบปิดได้")
            else:
                status = _classify_improper(res_val)
                if status == "finite":
                    result = _safe_float(res_val)
                    value_latex = _to_latex(res_val)
                    steps.append(
                        f"สรุปผลลัพธ์: สองลิมิตลู่เข้าสู่ค่าจำกัด รวมได้ $V = {value_latex} \\approx {result:.6g}$"
                    )
                elif status == "divergent":
                    result = None
                    value_latex = "\\text{diverges}"
                    steps.append("ผลลัพธ์: มีอย่างน้อยหนึ่งช่วงที่ลู่ออก จึงสรุปว่า **อินทิกรัลลู่ออก (Diverges)**")
                else:
                    result = None
                    value_latex = "\\text{unsupported}"

            latex_str = f"\\int_{{{lower_latex}}}^{{{bound_latex}}} {_to_latex(expr)} \\, d{v_lat} = {value_latex}"
            return {
                "ok": True,
                "result": result,
                "latex": latex_str,
                "steps": steps,
                "expr": expr,
                "value_expr": res_val,
                "error": None,
                "status": status,
                "interior_singularities": [],
                "variable": str(var_sym.name),
            }

        # 4.3 ไม่มีจุดเอกฐานใด ๆ บนช่วง [a, b] (อินทิกรัลจำกัดเขตปกติ)
        steps.append(
            f"ข้อสังเกต: ฟังก์ชันมีความต่อเนื่องตลอดช่วงปิด $[{lower_latex}, {bound_latex}]$ "
            f"จึงจัดเป็นอินทิกรัลจำกัดเขตปกติ (Proper Definite Integral)"
        )
        antideriv = sp.integrate(expr, var_sym)
        steps.append(
            f"หาปฏิยานุพันธ์ $F({v_lat}) = {_to_latex(antideriv)}$ "
            f"และแทนค่าขอบเขต: $[F({v_lat})]_{{{lower_latex}}}^{{{bound_latex}}} = {_to_latex(antideriv.subs(var_sym, upper))} - {_to_latex(antideriv.subs(var_sym, lower))}$"
        )
        res_val = sp.integrate(expr, (var_sym, lower, upper))
        status = _classify_improper(res_val)
        result = _safe_float(res_val)
        value_latex = _to_latex(res_val)

        if status == "divergent":
            result = None
            value_latex = "\\text{diverges}"
            steps.append("ผลลัพธ์: ลิมิตลู่ออกสู่อนันต์ จึงสรุปว่า **อินทิกรัลลู่ออก (Diverges)**")
        elif status == "finite" and result is not None:
            steps.append(
                f"สรุปผลลัพธ์: $\\int_{{{lower_latex}}}^{{{bound_latex}}} \\left({_to_latex(expr)}\\right) \\, d{v_lat} = {value_latex} \\approx {result:.6g}$"
            )
        else:
            steps.append(
                f"สรุปผลลัพธ์: $\\int_{{{lower_latex}}}^{{{bound_latex}}} \\left({_to_latex(expr)}\\right) \\, d{v_lat} = {value_latex}$"
            )

        latex_str = f"\\int_{{{lower_latex}}}^{{{bound_latex}}} {_to_latex(expr)} \\, d{v_lat} = {value_latex}"
        return {
            "ok": True,
            "result": result,
            "latex": latex_str,
            "steps": steps,
            "expr": expr,
            "value_expr": res_val,
            "error": None,
            "status": status,
            "interior_singularities": [],
            "variable": str(var_sym.name),
        }

    except Exception as exc:
        # Keep SymPy internals in the server log; students get a plain Thai message.
        print(f"[improper_solver] {type(exc).__name__}: {exc}", file=sys.stderr)
        return {
            "ok": False,
            "result": None,
            "latex": "",
            "steps": [],
            "expr": None,
            "error": "ไม่สามารถคำนวณปริพันธ์นี้ได้ในรูปแบบปิด",
            "status": "error",
            "interior_singularities": [],
        }
