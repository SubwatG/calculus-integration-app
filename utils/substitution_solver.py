"""utils/substitution_solver.py — การอินทิเกรตโดยการแทนตัวแปรและเทคนิคการอินทิเกรต

รองรับการตรวจหาตัวแปร u เชิงสัญลักษณ์ และการจำแนกฟังก์ชันที่ไม่เป็นฟังก์ชันมูลฐาน (Non-elementary integrals)
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

from utils.sympy_solver import _clean_calculus_input, _get_variable

X = sp.Symbol("x")

SPECIAL_FUNCS = (
    sp.erf,
    sp.erfc,
    sp.erfi,
    sp.Si,
    sp.Ci,
    sp.Shi,
    sp.Chi,
    sp.li,
    sp.Ei,
    sp.fresnels,
    sp.fresnelc,
    sp.elliptic_k,
    sp.elliptic_e,
    sp.elliptic_f,
)


def _parse_input(expr_str: str) -> sp.Expr:
    clean = (expr_str or "").strip()
    if not clean:
        raise ValueError("Empty input string")
    return parse_expr(clean, transformations=TRANSFORMATIONS, local_dict=LOCAL_MATH_DICT)


def _detect_u_candidate(expr: sp.Expr, var: sp.Symbol = X) -> tuple[sp.Expr | None, sp.Expr | None]:
    """สกัดตัวแปร u = g(var) และ du = g'(var)d(var) ที่เป็นตัวแทนการแทนค่าตัวแปรที่ดีที่สุด"""
    candidates = []
    for node in expr.atoms(sp.Pow):
        if node.base != var and node.base.has(var) and not node.base.is_number:
            candidates.append(node.base)
    for node in expr.atoms(sp.exp):
        if node.args[0] != var and node.args[0].has(var):
            candidates.append(node.args[0])
    for cls in (sp.sin, sp.cos, sp.tan, sp.log):
        for node in expr.atoms(cls):
            if node.args[0] != var and node.args[0].has(var):
                candidates.append(node.args[0])

    for c in candidates:
        du = sp.diff(c, var)
        ratio = sp.simplify(expr / du)
        if not ratio.has(sp.Derivative):
            return c, du

    if candidates:
        return candidates[0], sp.diff(candidates[0], var)
    return None, None


def solve_substitution(expr_str: str, var: str | sp.Symbol | None = None) -> dict:
    """คำนวณปริพันธ์ แจกแจงการแทนค่าตัวแปร และตรวจจับฟังก์ชันพิเศษ"""
    clean = (expr_str or "").strip()
    if not clean:
        return {
            "ok": False,
            "result": None,
            "latex": "",
            "steps": [],
            "expr": None,
            "u_candidate": None,
            "du_candidate": None,
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

        antideriv = sp.integrate(expr, var_sym)
        v_lat = sp.latex(var_sym)

        if antideriv.has(sp.Integral):
            return {
                "ok": False,
                "result": None,
                "latex": "",
                "steps": [
                    f"กำหนดโจทย์อินทิกรัล: \\int {sp.latex(expr)} \\, d{v_lat}",
                    "ระบบไม่สามารถหาปฏิยานุพันธ์ของฟังก์ชันนี้ได้ในรูปแบบปิด (Unevaluated Integral)",
                ],
                "expr": expr,
                "u_candidate": None,
                "du_candidate": None,
                "status": "unsupported",
                "warning": "ไม่สามารถหาปฏิยานุพันธ์ในรูปปิดได้",
                "error": "ไม่สามารถหาปฏิยานุพันธ์ของฟังก์ชันนี้ได้ในรูปแบบปิด",
                "variable": str(var_sym.name),
            }

        has_special = any(antideriv.has(f) for f in SPECIAL_FUNCS)
        u_cand, du_cand = _detect_u_candidate(expr, var_sym)

        steps = [
            f"กำหนดโจทย์อินทิกรัล: \\int {sp.latex(expr)} \\, d{v_lat}",
        ]

        if has_special:
            status = "non_elementary"
            warning = "ฟังก์ชันนี้ไม่มีปฏิยานุพันธ์ในรูปฟังก์ชันมูลฐาน (Non-Elementary Antiderivative)"
            steps.append(
                "ข้อสังเกตเชิงมโนทัศน์: ฟังก์ชันนี้ไม่มีปฏิยานุพันธ์ในรูปฟังก์ชันมูลฐาน (Non-Elementary) จึงไม่สามารถหาผลลัพธ์ด้วยเทคนิคการเปลี่ยนตัวแปรหรือ By Parts ปกติได้"
            )
            steps.append(
                f"ผลลัพธ์อยู่ในรูปฟังก์ชันพิเศษระดับสูง: \\int {sp.latex(expr)} \\, d{v_lat} = {sp.latex(antideriv)} + C"
            )
        else:
            status = "elementary"
            warning = None
            if u_cand is not None:
                steps.append(
                    f"กำหนดตัวแปร u: u = {sp.latex(u_cand)} \\implies du = {sp.latex(du_cand)} \\, d{v_lat}"
                )
            else:
                steps.append("พิจารณาเลือกเทคนิคการอินทิเกรตที่เหมาะสม (การเปลี่ยนตัวแปร หรือ By Parts)")

            steps.append(
                f"คำนวณปริพันธ์ผลลัพธ์: {sp.latex(antideriv)} + C"
            )

        return {
            "ok": True,
            "result": antideriv,
            "latex": f"\\int {sp.latex(expr)} \\, d{v_lat} = {sp.latex(antideriv)} + C",
            "steps": steps,
            "expr": expr,
            "u_candidate": u_cand,
            "du_candidate": du_cand,
            "status": status,
            "warning": warning,
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
            "u_candidate": None,
            "du_candidate": None,
            "status": "error",
            "warning": None,
            "error": f"ไม่สามารถคำนวณได้: {e}",
        }
