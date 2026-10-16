"""utils/improper_solver.py — อินทิกรัลไม่ตรงแบบ (Improper Integrals)

คำนวณอินทิกรัลไม่ตรงแบบผ่านลิมิต ตรวจสอบการลู่เข้า/ลู่ออก (Convergence/Divergence)
รองรับช่วงอนันต์ [a, oo), (-oo, b], (-oo, oo) และจุดเอกฐานที่ขอบเขต (Endpoints) และภายใน (Interior)
ตามเกณฑ์ Universal Step Contract
"""
import math
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
    lat = sp.latex(sym_obj)
    return lat.replace(r"\log", r"\ln")


def _parse_input(expr_str: str) -> sp.Expr:
    clean = (expr_str or "").strip()
    if not clean:
        raise ValueError("Empty input string")
    return parse_expr(clean, transformations=TRANSFORMATIONS, local_dict=LOCAL_MATH_DICT)


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
    if getattr(res_val, "is_finite", False) is True and getattr(res_val, "is_real", False) is True:
        return "finite"
    return "unsupported"


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
    denom = sp.denom(expr)
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
                f"เป้าหมาย / กฎที่ใช้ (Goal / Rule): อินทิกรัลไม่ตรงแบบชนิดที่ 1 (ช่วงอนันต์สองฝั่ง $(-\\infty, \\infty)$) "
                f"ต้องแยกช่วงที่จุด $c = {c_val}$ ตามนิยาม:\n"
                f"$$\\int_{{-\\infty}}^{{\\infty}} f({v_lat})\\,d{v_lat} = \\lim_{{s \\to -\\infty}} \\int_{{s}}^{{{c_val}}} f({v_lat})\\,d{v_lat} + \\lim_{{t \\to \\infty}} \\int_{{{c_val}}}^{{t}} f({v_lat})\\,d{v_lat}$$"
            )

            left_part = sp.integrate(expr, (var_sym, -sp.oo, c_val))
            right_part = sp.integrate(expr, (var_sym, c_val, sp.oo))
            left_status = _classify_improper(left_part)
            right_status = _classify_improper(right_part)

            steps.append(
                f"พีชคณิตระหว่างทาง (Intermediate algebra): คำนวณลิมิตแต่ละฝั่งแยกกัน:\n"
                f"- ฝั่งซ้าย: $\\lim_{{s \\to -\\infty}} \\int_{{s}}^{{{c_val}}} f({v_lat})\\,d{v_lat}$ มีสถานะ {left_status} ({_to_latex(left_part)})\n"
                f"- ฝั่งขวา: $\\lim_{{t \\to \\infty}} \\int_{{{c_val}}}^{{t}} f({v_lat})\\,d{v_lat}$ มีสถานะ {right_status} ({_to_latex(right_part)})"
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
                result = float(res_val.evalf()) if getattr(res_val, "is_real", False) else None
                value_latex = _to_latex(res_val)
                steps.append(
                    f"ผลลัพธ์แม่นตรง (Exact result): ทั้งสองฝั่งลู่เข้าสู่ค่าจริงจำกัด รวมกันได้: "
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
                "error": None,
                "status": status,
                "interior_singularities": [],
                "variable": str(var_sym.name),
            }

        # -------------------------------------------------------------
        # กรณีที่ 2: ขอบล่างเป็น -oo และขอบบนจำกัด
        # -------------------------------------------------------------
        if lower == -sp.oo and upper != sp.oo:
            steps.append(
                f"เป้าหมาย / กฎที่ใช้ (Goal / Rule): อินทิกรัลไม่ตรงแบบชนิดที่ 1 (ขอบล่างเป็นอนันต์) "
                f"แปลงเป็นรูปลิมิตของอินทิกรัลจำกัดเขตเมื่อตัวแปรเข้าใกล้ $-\\infty$:\n"
                f"$$\\lim_{{t \\to -\\infty}} \\int_{{t}}^{{{bound_latex}}} \\left({_to_latex(expr)}\\right) \\, d{v_lat}$$"
            )
            antideriv = sp.integrate(expr, var_sym)
            steps.append(
                f"พีชคณิตระหว่างทาง (Intermediate algebra): หาปฏิยานุพันธ์ $F({v_lat}) = {_to_latex(antideriv)}$ "
                f"แล้วแทนค่าขอบเขต: $[F({v_lat})]_{{t}}^{{{bound_latex}}} = {_to_latex(antideriv.subs(var_sym, upper))} - \\left({_to_latex(antideriv.subs(var_sym, sp.Symbol('t')))}\\right)$"
            )

            res_val = sp.integrate(expr, (var_sym, -sp.oo, upper))
            status = _classify_improper(res_val)
            if status == "finite":
                result = float(res_val.evalf()) if getattr(res_val, "is_real", False) else None
                value_latex = _to_latex(res_val)
                steps.append(f"ผลลัพธ์แม่นตรง (Exact result): ลิมิตลู่เข้าสู่ค่าจำกัด (Converges) ได้ $V = {value_latex} \\approx {result:.6g}$")
            elif status == "divergent":
                result = None
                value_latex = "\\text{diverges}"
                steps.append("ผลลัพธ์: ลิมิตลู่ออกสู่อนันต์หรือไม่นิยาม จึงสรุปว่า **อินทิกรัลลู่ออก (Diverges)**")
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
                "error": None,
                "status": status,
                "interior_singularities": [],
                "variable": str(var_sym.name),
            }

        # -------------------------------------------------------------
        # กรณีที่ 3: ขอบล่างจำกัด และขอบบนเป็น oo
        # -------------------------------------------------------------
        if lower != -sp.oo and upper == sp.oo:
            steps.append(
                f"เป้าหมาย / กฎที่ใช้ (Goal / Rule): อินทิกรัลไม่ตรงแบบชนิดที่ 1 (ขอบบนเป็นอนันต์) "
                f"แปลงเป็นรูปลิมิตของอินทิกรัลจำกัดเขตเมื่อตัวแปรเข้าใกล้อนันต์:\n"
                f"$$\\lim_{{t \\to \\infty}} \\int_{{{lower_latex}}}^{{t}} \\left({_to_latex(expr)}\\right) \\, d{v_lat}$$"
            )
            antideriv = sp.integrate(expr, var_sym)
            steps.append(
                f"พีชคณิตระหว่างทาง (Intermediate algebra): หาปฏิยานุพันธ์ $F({v_lat}) = {_to_latex(antideriv)}$ "
                f"แล้วแทนค่าขอบเขต: $[F({v_lat})]_{{{lower_latex}}}^{{t}} = \\left({_to_latex(antideriv.subs(var_sym, sp.Symbol('t')))}\\right) - {_to_latex(antideriv.subs(var_sym, lower))}$"
            )

            res_val = sp.integrate(expr, (var_sym, lower, sp.oo))
            status = _classify_improper(res_val)
            if status == "finite":
                result = float(res_val.evalf()) if getattr(res_val, "is_real", False) else None
                value_latex = _to_latex(res_val)
                steps.append(f"ผลลัพธ์แม่นตรง (Exact result): ลิมิตลู่เข้าสู่ค่าจำกัด (Converges) ได้คำตอบ $V = {value_latex} \\approx {result:.6g}$")
            elif status == "divergent":
                result = None
                value_latex = "\\text{diverges}"
                steps.append("ผลลัพธ์: ลิมิตลู่ออกสู่อนันต์ (เช่น พจน์ฮาร์มอนิก $\\ln(t) \\to \\infty$) จึงสรุปว่า **อินทิกรัลลู่ออก (Diverges)**")
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
                f"เป้าหมาย / กฎที่ใช้ (Goal / Rule): อินทิกรัลไม่ตรงแบบชนิดที่ 2 พบจุดเอกฐานภายในช่วง (Interior Singularity) ที่ ${v_lat} = {c_latex}$ "
                f"ซึ่งทำให้ฟังก์ชันไม่ต่อเนื่องและไม่มีขอบเขต จึงต้องแยกช่วงตามนิยาม:\n"
                f"$$\\int_{{{lower_latex}}}^{{{bound_latex}}} f({v_lat})\\,d{v_lat} = "
                f"\\lim_{{t \\to {c_latex}^-}} \\int_{{{lower_latex}}}^{{t}} f({v_lat})\\,d{v_lat} + "
                f"\\lim_{{s \\to {c_latex}^+}} \\int_{{s}}^{{{bound_latex}}} f({v_lat})\\,d{v_lat}$$"
            )

            left_part = sp.integrate(expr, (var_sym, lower, c_sp))
            right_part = sp.integrate(expr, (var_sym, c_sp, upper))
            left_status = _classify_improper(left_part)
            right_status = _classify_improper(right_part)

            steps.append(
                f"พีชคณิตระหว่างทาง (Intermediate algebra): พิจารณาลิมิตแต่ละฝั่งแยกกัน:\n"
                f"- ฝั่งซ้ายเข้าใกล้ ${c_latex}^-$: สถานะเป็น {left_status}\n"
                f"- ฝั่งขวาเข้าใกล้ ${c_latex}^+$: สถานะเป็น {right_status}"
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
                res_val = left_part + right_part
                status = "finite"
                result = float(res_val.evalf()) if getattr(res_val, "is_real", False) else None
                value_latex = _to_latex(res_val)
                steps.append(
                    f"ผลลัพธ์แม่นตรง (Exact result): ทั้งสองฝั่งลู่เข้าสู่ค่าจริงจำกัด รวมกันได้: "
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
                "error": None,
                "status": status,
                "interior_singularities": interior_sings,
                "variable": str(var_sym.name),
            }

        # 4.2 ตรวจสอบจุดเอกฐานที่ขอบเขต (Endpoint Singularities)
        lower_singular = _is_singular_at_point(expr, lower, "+", var=var_sym)
        upper_singular = _is_singular_at_point(expr, upper, "-", var=var_sym)

        # เอกฐานที่ขอบล่าง a เท่านั้น (เช่น 1/sqrt(x) บน [0, 1])
        if lower_singular and not upper_singular:
            steps.append(
                f"เป้าหมาย / กฎที่ใช้ (Goal / Rule): อินทิกรัลไม่ตรงแบบชนิดที่ 2 พบจุดเอกฐานที่ขอบล่าง ${v_lat} = {lower_latex}$ "
                f"โดย $\\lim_{{{v_lat} \\to {lower_latex}^+}} f({v_lat}) = \\infty$ ในขณะที่ฟังก์ชันต่อเนื่องที่ขอบบน ${v_lat} = {bound_latex}$ "
                f"จึงแปลงเป็นรูปลิมิตเข้าใกล้ทางขวา:\n"
                f"$$\\lim_{{t \\to {lower_latex}^+}} \\int_{{t}}^{{{bound_latex}}} \\left({_to_latex(expr)}\\right) \\, d{v_lat}$$"
            )
            antideriv = sp.integrate(expr, var_sym)
            steps.append(
                f"พีชคณิตระหว่างทาง (Intermediate algebra): หาปฏิยานุพันธ์ $F({v_lat}) = {_to_latex(antideriv)}$ "
                f"และแทนค่าขอบเขตในเทอมของ $t$: $[F({v_lat})]_{{t}}^{{{bound_latex}}} = {_to_latex(antideriv.subs(var_sym, upper))} - {_to_latex(antideriv.subs(var_sym, sp.Symbol('t')))}$"
            )

            res_val = sp.integrate(expr, (var_sym, lower, upper))
            status = _classify_improper(res_val)
            if status == "finite":
                result = float(res_val.evalf()) if getattr(res_val, "is_real", False) else None
                value_latex = _to_latex(res_val)
                steps.append(f"ผลลัพธ์แม่นตรง (Exact result): ลิมิตลู่เข้าสู่ค่าจำกัด (Converges): $\\lim_{{t \\to {lower_latex}^+}} \\int_{{t}}^{{{bound_latex}}} f({v_lat})\\,d{v_lat} = {value_latex} \\approx {result:.6g}$")
            elif status == "divergent":
                result = None
                value_latex = "\\text{diverges}"
                steps.append("ผลลัพธ์: ลิมิตลู่ออกสู่อนันต์ จึงสรุปว่า **อินทิกรัลลู่ออก (Diverges)**")
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
                "error": None,
                "status": status,
                "interior_singularities": [],
                "variable": str(var_sym.name),
            }

        # เอกฐานที่ขอบบน b เท่านั้น (เช่น 1/sqrt(1-x) บน [0, 1])
        if upper_singular and not lower_singular:
            steps.append(
                f"เป้าหมาย / กฎที่ใช้ (Goal / Rule): อินทิกรัลไม่ตรงแบบชนิดที่ 2 พบจุดเอกฐานที่ขอบบน ${v_lat} = {bound_latex}$ "
                f"โดย $\\lim_{{{v_lat} \\to {bound_latex}^-}} f({v_lat}) = \\infty$ ในขณะที่ฟังก์ชันต่อเนื่องที่ขอบล่าง ${v_lat} = {lower_latex}$ "
                f"จึงแปลงเป็นรูปลิมิตเข้าใกล้ทางซ้าย:\n"
                f"$$\\lim_{{t \\to {bound_latex}^-}} \\int_{{{lower_latex}}}^{{t}} \\left({_to_latex(expr)}\\right) \\, d{v_lat}$$"
            )
            antideriv = sp.integrate(expr, var_sym)
            steps.append(
                f"พีชคณิตระหว่างทาง (Intermediate algebra): หาปฏิยานุพันธ์ $F({v_lat}) = {_to_latex(antideriv)}$ "
                f"และแทนค่าขอบเขตในเทอมของ $t$: $[F({v_lat})]_{{{lower_latex}}}^{{t}} = {_to_latex(antideriv.subs(var_sym, sp.Symbol('t')))} - {_to_latex(antideriv.subs(var_sym, lower))}$"
            )

            res_val = sp.integrate(expr, (var_sym, lower, upper))
            status = _classify_improper(res_val)
            if status == "finite":
                result = float(res_val.evalf()) if getattr(res_val, "is_real", False) else None
                value_latex = _to_latex(res_val)
                steps.append(f"ผลลัพธ์แม่นตรง (Exact result): ลิมิตลู่เข้าสู่ค่าจำกัด (Converges): $\\lim_{{t \\to {bound_latex}^-}} \\int_{{{lower_latex}}}^{{t}} f({v_lat})\\,d{v_lat} = {value_latex} \\approx {result:.6g}$")
            elif status == "divergent":
                result = None
                value_latex = "\\text{diverges}"
                steps.append("ผลลัพธ์: ลิมิตลู่ออกสู่อนันต์ จึงสรุปว่า **อินทิกรัลลู่ออก (Diverges)**")
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
                "error": None,
                "status": status,
                "interior_singularities": [],
                "variable": str(var_sym.name),
            }

        # 4.3 ไม่มีจุดเอกฐานใด ๆ บนช่วง [a, b] (อินทิกรัลจำกัดเขตปกติ)
        steps.append(
            f"ข้อสังเกตเชิงมโนทัศน์: ฟังก์ชันมีความต่อเนื่องและมีขอบเขตตลอดช่วงปิด $[{lower_latex}, {bound_latex}]$ "
            f"จึงจัดเป็นอินทิกรัลจำกัดเขตปกติ (Proper Definite Integral)"
        )
        antideriv = sp.integrate(expr, var_sym)
        steps.append(
            f"พีชคณิตระหว่างทาง (Intermediate algebra): คำนวณปฏิยานุพันธ์ $F({v_lat}) = {_to_latex(antideriv)}$ "
            f"และแทนค่าขอบเขต: $[F({v_lat})]_{{{lower_latex}}}^{{{bound_latex}}} = {_to_latex(antideriv.subs(var_sym, upper))} - {_to_latex(antideriv.subs(var_sym, lower))}$"
        )
        res_val = sp.integrate(expr, (var_sym, lower, upper))
        status = _classify_improper(res_val)
        result = float(res_val.evalf()) if getattr(res_val, "is_real", False) else None
        value_latex = _to_latex(res_val)

        steps.append(
            f"ผลลัพธ์แม่นตรง (Exact result): $\\int_{{{lower_latex}}}^{{{bound_latex}}} \\left({_to_latex(expr)}\\right) \\, d{v_lat} = {value_latex} \\approx {result:.6g}$"
        )

        latex_str = f"\\int_{{{lower_latex}}}^{{{bound_latex}}} {_to_latex(expr)} \\, d{v_lat} = {value_latex}"
        return {
            "ok": True,
            "result": result,
            "latex": latex_str,
            "steps": steps,
            "expr": expr,
            "error": None,
            "status": status,
            "interior_singularities": [],
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
            "interior_singularities": [],
        }
