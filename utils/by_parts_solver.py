"""utils/by_parts_solver.py: Integration by Parts solver.

Dedicated module for solving and explaining Integration by Parts problems using the LIATE rule,
separated cleanly from u-substitution.
"""

import re
import sympy as sp
from sympy.parsing.sympy_parser import (
    convert_xor,
    implicit_multiplication_application,
    parse_expr,
    standard_transformations,
)

from utils.substitution_solver import _detect_u_candidate, _get_domain_note, _to_latex, _wrap_new_logs
from utils.sympy_solver import _clean_calculus_input, _get_variable

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


def _is_exponential(f: sp.Expr, var: sp.Symbol) -> bool:
    if f.has(sp.exp):
        return True
    if f.is_Pow and f.exp.has(var) and not f.base.has(var):
        return True
    return False


def _is_trigonometric(f: sp.Expr) -> bool:
    return any(f.has(cls) for cls in (sp.sin, sp.cos, sp.tan, sp.sec, sp.csc, sp.cot))


def _clean_trig(e: sp.Expr) -> sp.Expr:
    if e is None:
        return None
    res = sp.trigsimp(e)
    res = res.replace(
        lambda a: a.is_Pow and getattr(a.base, "func", None) is sp.tan and a.exp == -1,
        lambda a: sp.cot(a.base.args[0]),
    )
    return res


def detect_parts_candidate(expr: sp.Expr, var: sp.Symbol = X) -> tuple[sp.Expr, sp.Expr, str, bool] | None:
    """Identify decomposition expr = u * v' for integration by parts using LIATE rule.

    Returns (u, dv_factor, reason, is_cyclic) or None.
    """
    # 1. Single function: ln(x), arctan(x), arcsin(x)
    if isinstance(expr, sp.log) or expr.func in (sp.atan, sp.asin, sp.acos):
        return expr, sp.Integer(1), "ฟังก์ชันลอการิทึมหรือตรีโกณมิติผกผันเดี่ยว (กำหนด dv = dx)", False

    # 2. Product forms
    factors = list(expr.as_ordered_factors()) if expr.is_Mul else [expr]
    log_factors = [f for f in factors if f.has(sp.log)]
    inv_trig_factors = [f for f in factors if any(f.has(cls) for cls in (sp.atan, sp.asin, sp.acos))]
    poly_factors = [f for f in factors if f.is_polynomial(var)]
    exp_factors = [f for f in factors if _is_exponential(f, var)]
    trig_factors = [f for f in factors if _is_trigonometric(f)]

    # LIATE Rule:
    # L / I before A
    if log_factors:
        u_cand = sp.Mul(*log_factors)
        dv_cand = sp.Mul(*[f for f in factors if f not in log_factors])
        return u_cand, dv_cand, "ตามกฎ LIATE: เลือกฟังก์ชันลอการิทึม (L) เป็น u และส่วนที่เหลือเป็น dv", False
    if inv_trig_factors:
        u_cand = sp.Mul(*inv_trig_factors)
        dv_cand = sp.Mul(*[f for f in factors if f not in inv_trig_factors])
        return u_cand, dv_cand, "ตามกฎ LIATE: เลือกฟังก์ชันตรีโกณมิติผกผัน (I) เป็น u และส่วนที่เหลือเป็น dv", False

    # A before T / E
    if poly_factors and (exp_factors or trig_factors):
        u_cand = sp.Mul(*poly_factors)
        other_factors = [f for f in factors if f not in poly_factors]
        dv_cand = sp.Mul(*other_factors)
        return u_cand, dv_cand, "ตามกฎ LIATE: เลือกฟังก์ชันพีชคณิต (A) เป็น u เพื่อให้ดีกรีลดลงเมื่อหาอนุพันธ์", False

    # Cyclic E * T
    if exp_factors and trig_factors:
        u_cand = sp.Mul(*exp_factors)
        dv_cand = sp.Mul(*trig_factors)
        return u_cand, dv_cand, "ฟังก์ชันเอกซ์โพเนนเชียลคูณกับตรีโกณมิติ (อินทิเกรตแบบวนลูป Cyclic Integration)", True

    return None


def solve_by_parts(expr_str: str, var: str | sp.Symbol | None = None) -> dict:
    """Solve and step-by-step explain Integration by Parts problem."""
    clean = (expr_str or "").strip()
    if not clean:
        return {
            "ok": False,
            "result": None,
            "latex": "",
            "steps": [],
            "status": "error",
            "warning": None,
            "error": "กรุณาระบุนิพจน์อินทิกรัลที่ต้องการคำนวณ",
            "variable": "x",
        }

    try:
        clean_expr, diff_var = _clean_calculus_input(clean)
        expr = _parse_input(clean_expr)
        if var is None:
            if diff_var is not None:
                var_sym = sp.Symbol(diff_var)
            else:
                var_sym = _get_variable(expr)
        elif isinstance(var, str):
            var_sym = sp.Symbol(var)
        else:
            var_sym = var

        v_lat = _to_latex(var_sym)
        domain_note = _get_domain_note(expr, var_sym)
        antideriv = sp.integrate(expr, var_sym)

        # Check whether the problem clearly fits u-substitution first
        u_cand, du_cand = _detect_u_candidate(expr, var_sym)
        if u_cand is not None and du_cand is not None:
            ratio = sp.simplify(expr / du_cand)
            u_temp = sp.Symbol("_u_temp")
            ratio_u = ratio.subs(u_cand, u_temp)
            if not ratio.has(var_sym) or not ratio_u.has(var_sym):
                antideriv = _wrap_new_logs(antideriv, expr)
                return {
                    "ok": True,
                    "result": antideriv,
                    "latex": f"\\int {_to_latex(expr)} \\, d{v_lat} = {_to_latex(antideriv)} + C",
                    "steps": [
                        f"กำหนดโจทย์อินทิกรัล: $\\int {_to_latex(expr)} \\, d{v_lat}$",
                        f"ข้อสังเกต: โจทย์ข้อนี้มีพจน์อนุพันธ์ร่วม และเหมาะกับการใช้การแทนตัวแปร u (u-Substitution) มากกว่า โดยเลือก $u = {_to_latex(u_cand)}$",
                        f"ผลลัพธ์การคำนวณ: $\\int {_to_latex(expr)} \\, d{v_lat} = {_to_latex(antideriv)} + C$",
                        domain_note,
                    ],
                    "status": "better_suited_for_substitution",
                    "warning": "โจทย์ข้อนี้เหมาะสมกับการใช้การแทนตัวแปร u มากกว่าการอินทิเกรตทีละส่วน",
                    "error": None,
                    "variable": str(var_sym.name),
                    "parts_info": None,
                }

        parts_cand = detect_parts_candidate(expr, var_sym)
        if parts_cand is None:
            if antideriv.has(sp.Integral):
                return {
                    "ok": False,
                    "result": None,
                    "latex": "",
                    "steps": [
                        f"กำหนดโจทย์อินทิกรัล: $\\int {_to_latex(expr)} \\, d{v_lat}$",
                        "ระบบไม่สามารถหาปฏิยานุพันธ์ของฟังก์ชันนี้ได้ในรูปแบบปิด หรือฟังก์ชันนี้ไม่มีปฏิยานุพันธ์ในรูปฟังก์ชันมูลฐาน",
                    ],
                    "status": "unsupported",
                    "warning": "ไม่สามารถหาปฏิยานุพันธ์ในรูปฟังก์ชันมูลฐานได้",
                    "error": "ฟังก์ชันนี้ไม่มีปฏิยานุพันธ์ในรูปฟังก์ชันมูลฐาน",
                    "variable": str(var_sym.name),
                    "parts_info": None,
                }
            # Does not fit standard By Parts pattern
            antideriv = _wrap_new_logs(antideriv, expr)
            return {
                "ok": True,
                "result": antideriv,
                "latex": f"\\int {_to_latex(expr)} \\, d{v_lat} = {_to_latex(antideriv)} + C",
                "steps": [
                    f"กำหนดโจทย์อินทิกรัล: $\\int {_to_latex(expr)} \\, d{v_lat}$",
                    "ข้อสังเกต: โจทย์ข้อนี้ไม่ได้อยู่ในรูปผลคูณของสองฟังก์ชันที่ต้องใช้วิธี By Parts โดยตรง สามารถอินทิเกรตด้วยสูตรพื้นฐานได้",
                    f"สรุปผลลัพธ์: $\\int {_to_latex(expr)} \\, d{v_lat} = {_to_latex(antideriv)} + C$",
                    domain_note,
                ],
                "status": "standard",
                "warning": None,
                "error": None,
                "variable": str(var_sym.name),
                "parts_info": None,
            }

        u_p, dv_p, parts_reason, is_cyclic = parts_cand
        du_p = sp.diff(u_p, var_sym)
        v_p = _clean_trig(sp.integrate(dv_p, var_sym))
        v_du = _clean_trig(sp.simplify(v_p * du_p))

        if is_cyclic:
            expr_lat = _to_latex(expr)
            u1_lat = _to_latex(u_p)
            v1_lat = _to_latex(v_p)
            du1_lat = _to_latex(du_p)

            u2 = u_p
            du2 = du_p
            dv2 = v_p
            v2 = _clean_trig(sp.integrate(dv2, var_sym))
            u2_lat = _to_latex(u2)
            v2_lat = _to_latex(v2)
            du2_lat = _to_latex(du2)

            antideriv = _clean_trig(antideriv)
            antideriv = _wrap_new_logs(antideriv, expr)

            steps = [
                f"กำหนดโจทย์อินทิกรัล: $\\int {expr_lat} \\, d{v_lat}$",
                f"วิเคราะห์ตามกฎ LIATE: {parts_reason}",
                (
                    f"การอินทิเกรตทีละส่วนรอบที่ 1 (First Integration by Parts):\n"
                    f"กำหนด $I = \\int {expr_lat} \\, d{v_lat}$\n"
                    f"- ให้ $u = {u1_lat} \\implies du = {du1_lat} \\, d{v_lat}$\n"
                    f"- ให้ $dv = {_to_latex(dv_p)} \\, d{v_lat} \\implies v = {v1_lat}$\n"
                    f"แทนค่าลงในสูตร $I = uv - \\int v \\, du$:\n"
                    f"$$I = ({u1_lat})({v1_lat}) - \\int ({v1_lat})({du1_lat}) \\, d{v_lat}$$"
                ),
                (
                    f"การอินทิเกรตทีละส่วนรอบที่ 2 (Second Integration by Parts):\n"
                    f"ทำ By Parts ซ้ำกับก้อนปริพันธ์ $\\int ({v1_lat})({du1_lat}) \\, d{v_lat}$ โดยคงบทบาทตัวแปรเดิม:\n"
                    f"- ให้ $u = {u2_lat} \\implies du = {du2_lat} \\, d{v_lat}$\n"
                    f"- ให้ $dv = {_to_latex(dv2)} \\, d{v_lat} \\implies v = {v2_lat}$\n"
                    f"เมื่อแทนค่าและจัดรูป จะพบว่าปริพันธ์วนกลับมาเป็นพจน์ $I$ ตั้งต้น:\n"
                    f"$$I = ({u1_lat})({v1_lat}) - \\left[ ({u2_lat})({v2_lat}) - \\int ({v2_lat})({du2_lat}) \\, d{v_lat} \\right]$$"
                ),
                (
                    f"แก้สมการเชิงพีชคณิตหาค่า I (Solve for I):\n"
                    f"ย้ายข้างสมการโดยรวมพจน์ $I$ ทั้งหมดไว้ทางซ้ายมือ และหารด้วยสัมประสิทธิ์:\n"
                    f"$$\\int {expr_lat} \\, d{v_lat} = {_to_latex(antideriv)} + C$$"
                ),
                f"สรุปผลลัพธ์: $\\int {_to_latex(expr)} \\, d{v_lat} = {_to_latex(antideriv)} + C$",
                domain_note,
            ]
        else:
            rem_integral = sp.integrate(v_du, var_sym)
            if rem_integral.has(sp.Integral) or antideriv.has(sp.Integral):
                if not rem_integral.has(sp.Integral):
                    antideriv = _clean_trig(u_p * v_p - rem_integral)
                else:
                    return {
                        "ok": False,
                        "result": None,
                        "latex": "",
                        "steps": [
                            f"กำหนดโจทย์อินทิกรัล: $\\int {_to_latex(expr)} \\, d{v_lat}$",
                            f"วิเคราะห์ตามกฎ LIATE: {parts_reason}",
                            f"เมื่อแทนค่าลงในสูตร By Parts ปริพันธ์ที่เหลือ $\\int {_to_latex(v_du)} \\, d{v_lat}$ ไม่สามารถหาปฏิยานุพันธ์ในรูปฟังก์ชันมูลฐานได้",
                        ],
                        "status": "unsupported",
                        "warning": "ไม่สามารถหาปฏิยานุพันธ์ในรูปฟังก์ชันมูลฐานได้",
                        "error": "ฟังก์ชันนี้ไม่มีปฏิยานุพันธ์ในรูปฟังก์ชันมูลฐาน",
                        "variable": str(var_sym.name),
                        "parts_info": {
                            "u": u_p,
                            "dv": dv_p,
                            "du": du_p,
                            "v": v_p,
                            "remainder": v_du,
                        },
                    }
            else:
                antideriv = _clean_trig(antideriv)
            antideriv = _wrap_new_logs(antideriv, expr)
            rem_integral_disp = _wrap_new_logs(_clean_trig(rem_integral), v_du)
            steps = [
                f"กำหนดโจทย์อินทิกรัล: $\\int {_to_latex(expr)} \\, d{v_lat}$",
                f"เลือกวิธี: การอินทิเกรตทีละส่วน (Integration by parts) ตามสูตร $\\int u \\, dv = uv - \\int v \\, du$",
                f"วิเคราะห์ตามกฎ LIATE: {parts_reason}",
                f"กำหนดตัวแปรและหาอนุพันธ์:\n"
                f"- กำหนด $u = {_to_latex(u_p)} \\implies du = {_to_latex(du_p)} \\, d{v_lat}$\n"
                f"- กำหนด $dv = {_to_latex(dv_p)} \\, d{v_lat} \\implies v = \\int {_to_latex(dv_p)} \\, d{v_lat} = {_to_latex(v_p)}$",
                f"แทนค่าลงในสูตร By Parts:\n"
                f"$$\\int u \\, dv = uv - \\int v \\, du$$\n"
                f"$$= \\left({_to_latex(u_p)}\\right)\\left({_to_latex(v_p)}\\right) - \\int \\left({_to_latex(v_p)}\\right)\\left({_to_latex(du_p)}\\right) \\, d{v_lat}$$",
                f"คำนวณปริพันธ์ที่เหลือ: $\\int {_to_latex(v_du)} \\, d{v_lat} = {_to_latex(rem_integral_disp)}$",
                f"สรุปผลลัพธ์: $\\int {_to_latex(expr)} \\, d{v_lat} = {_to_latex(antideriv)} + C$",
                domain_note,
            ]

        return {
            "ok": True,
            "result": antideriv,
            "latex": f"\\int {_to_latex(expr)} \\, d{v_lat} = {_to_latex(antideriv)} + C",
            "steps": steps,
            "status": "elementary",
            "warning": None,
            "error": None,
            "variable": str(var_sym.name),
            "parts_info": {
                "u": u_p,
                "dv": dv_p,
                "du": du_p,
                "v": v_p,
                "remainder": v_du,
            },
        }

    except Exception as e:
        return {
            "ok": False,
            "result": None,
            "latex": "",
            "steps": [],
            "status": "error",
            "warning": None,
            "error": f"ไม่สามารถคำนวณได้: {e}",
            "variable": "x",
        }
