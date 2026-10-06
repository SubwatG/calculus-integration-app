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


def _detect_u_candidate(expr: sp.Expr) -> tuple[sp.Expr | None, sp.Expr | None]:
    """สกัดตัวแปร u = g(x) และ du = g'(x)dx ที่เป็นตัวแทนการแทนค่าตัวแปรที่ดีที่สุด"""
    candidates = []
    for node in expr.atoms(sp.Pow):
        if node.base != X and node.base.has(X) and not node.base.is_number:
            candidates.append(node.base)
    for node in expr.atoms(sp.exp):
        if node.args[0] != X and node.args[0].has(X):
            candidates.append(node.args[0])
    for cls in (sp.sin, sp.cos, sp.tan, sp.log):
        for node in expr.atoms(cls):
            if node.args[0] != X and node.args[0].has(X):
                candidates.append(node.args[0])

    for c in candidates:
        du = sp.diff(c, X)
        ratio = sp.simplify(expr / du)
        if not ratio.has(sp.Derivative):
            return c, du

    if candidates:
        return candidates[0], sp.diff(candidates[0], X)
    return None, None


def solve_substitution(expr_str: str) -> dict:
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
        }

    try:
        expr = _parse_input(clean)
        antideriv = sp.integrate(expr, X)

        if antideriv.has(sp.Integral):
            return {
                "ok": False,
                "result": None,
                "latex": "",
                "steps": [
                    f"กำหนดโจทย์อินทิกรัล: \\int {sp.latex(expr)} \\, dx",
                    "ระบบไม่สามารถหาปฏิยานุพันธ์ของฟังก์ชันนี้ได้ในรูปแบบปิด (Unevaluated Integral)",
                ],
                "expr": expr,
                "u_candidate": None,
                "du_candidate": None,
                "status": "unsupported",
                "warning": "ไม่สามารถหาปฏิยานุพันธ์ในรูปปิดได้",
                "error": "ไม่สามารถหาปฏิยานุพันธ์ของฟังก์ชันนี้ได้ในรูปแบบปิด",
            }

        has_special = any(antideriv.has(f) for f in SPECIAL_FUNCS)
        u_cand, du_cand = _detect_u_candidate(expr)

        steps = [
            f"กำหนดโจทย์อินทิกรัล: \\int {sp.latex(expr)} \\, dx",
        ]

        if has_special:
            status = "non_elementary"
            warning = "ฟังก์ชันนี้ไม่มีปฏิยานุพันธ์ในรูปฟังก์ชันมูลฐาน (Non-Elementary Antiderivative)"
            steps.append(
                "ข้อสังเกตเชิงมโนทัศน์: ฟังก์ชันนี้ไม่มีปฏิยานุพันธ์ในรูปฟังก์ชันมูลฐาน (Non-Elementary) จึงไม่สามารถหาผลลัพธ์ด้วยเทคนิคการเปลี่ยนตัวแปรหรือ By Parts ปกติได้"
            )
            steps.append(
                f"ผลลัพธ์อยู่ในรูปฟังก์ชันพิเศษระดับสูง: \\int {sp.latex(expr)} \\, dx = {sp.latex(antideriv)} + C"
            )
        else:
            status = "elementary"
            warning = None
            if u_cand is not None:
                steps.append(
                    f"กำหนดตัวแปร u: u = {sp.latex(u_cand)} \\implies du = {sp.latex(du_cand)} \\, dx"
                )
            else:
                steps.append("พิจารณาเลือกเทคนิคการอินทิเกรตที่เหมาะสม (การเปลี่ยนตัวแปร หรือ By Parts)")

            steps.append(
                f"คำนวณปริพันธ์ผลลัพธ์: {sp.latex(antideriv)} + C"
            )

        return {
            "ok": True,
            "result": antideriv,
            "latex": f"\\int {sp.latex(expr)} \\, dx = {sp.latex(antideriv)} + C",
            "steps": steps,
            "expr": expr,
            "u_candidate": u_cand,
            "du_candidate": du_cand,
            "status": status,
            "warning": warning,
            "error": None,
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
