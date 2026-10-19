"""utils/substitution_solver.py — การอินทิเกรตโดยการแทนตัวแปรและเทคนิคการอินทิเกรต

รองรับการตรวจหาตัวแปร u เชิงสัญลักษณ์, เทคนิคการอินทิเกรตทีละส่วน (Integration by Parts),
และการจำแนกฟังก์ชันที่ไม่เป็นฟังก์ชันมูลฐาน (Non-elementary integrals)
ตามเกณฑ์ Universal Step Contract
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


def _to_latex(sym_obj) -> str:
    """แปลง SymPy object เป็น LaTeX string พร้อมแทนที่ \\log เป็น \\ln ตามมาตรฐานการสอนแคลคูลัส"""
    lat = sp.latex(sym_obj)
    return lat.replace(r"\log", r"\ln")


def _parse_input(expr_str: str) -> sp.Expr:
    clean = (expr_str or "").strip()
    if not clean:
        raise ValueError("Empty input string")
    return parse_expr(clean, transformations=TRANSFORMATIONS, local_dict=LOCAL_MATH_DICT)


def _detect_u_candidate(expr: sp.Expr, var: sp.Symbol = X) -> tuple[sp.Expr | None, sp.Expr | None]:
    """สกัดตัวแปร u = g(var) และ du = g'(var)d(var) ที่กำจัดตัวแปรเดิมได้จริง"""
    candidates = []
    # 1. ฐานของเลขยกกำลัง
    for node in expr.atoms(sp.Pow):
        if node.base != var and node.base.has(var) and not node.base.is_number:
            candidates.append(node.base)
    # 2. ฟังก์ชันภายใน exp, sin, cos, tan
    for node in expr.atoms(sp.exp):
        if node.args[0] != var and node.args[0].has(var):
            candidates.append(node.args[0])
    for cls in (sp.sin, sp.cos, sp.tan):
        for node in expr.atoms(cls):
            if node.args[0] != var and node.args[0].has(var):
                candidates.append(node.args[0])
    # 3. ฟังก์ชัน log
    for node in expr.atoms(sp.log):
        if node.has(var):
            candidates.append(node)
            if node.args[0] != var and node.args[0].has(var):
                candidates.append(node.args[0])

    # 4. ส่วนของเศษส่วน (ตัวส่วน)
    numer, denom = expr.as_numer_denom()
    if denom != 1 and denom.has(var) and denom != var:
        candidates.append(denom)

    # ทดสอบว่า candidate ใดเมื่อหาร du แล้ว ตัดทอนตัวแปรเดิมได้จริง
    u_sym = sp.Symbol("_u_temp")
    for c in candidates:
        du = sp.diff(c, var)
        if du == 0:
            continue
        ratio = sp.simplify(expr / du)
        if not ratio.has(var):
            return c, du
        expr_u = expr.subs(c, u_sym)
        ratio_sub = sp.simplify(expr_u / du)
        if not ratio_sub.has(var):
            return c, du
        ratio_sub2 = sp.simplify(ratio.subs(c, u_sym))
        if not ratio_sub2.has(var):
            return c, du

    return None, None


def _detect_parts_candidate(expr: sp.Expr, var: sp.Symbol = X) -> tuple[sp.Expr, sp.Expr, str] | None:
    """พิจารณาแยก expr = u * v' เพื่อทำการอินทิเกรตทีละส่วน (Integration by Parts) ตามแนวทาง LIATE

    คืนค่า (u, dv_factor, reason) หรือ None
    """
    # 1. ฟังก์ชันเดี่ยว: ln(x), arctan(x), arcsin(x)
    if isinstance(expr, sp.log) or expr.func in (sp.atan, sp.asin, sp.acos):
        return expr, sp.Integer(1), "ฟังก์ชันลอการิทึมหรือตรีโกณมิติผกผันเดี่ยว (กำหนด dv = dx)"

    # 2. รูปแบบผลคูณ
    factors = list(expr.as_ordered_factors()) if expr.is_Mul else [expr]
    log_factors = [f for f in factors if f.has(sp.log)]
    inv_trig_factors = [f for f in factors if any(f.has(cls) for cls in (sp.atan, sp.asin, sp.acos))]
    poly_factors = [f for f in factors if f.is_polynomial(var)]
    exp_factors = [f for f in factors if f.has(sp.exp)]
    trig_factors = [f for f in factors if any(f.has(cls) for cls in (sp.sin, sp.cos, sp.tan))]

    # LIATE Rule:
    # L / I มาก่อน A
    if log_factors:
        u_cand = sp.Mul(*log_factors)
        dv_cand = sp.Mul(*[f for f in factors if f not in log_factors])
        return u_cand, dv_cand, "ตามแนวทาง LIATE: เลือกฟังก์ชันลอการิทึม (L) เป็น u และฟังก์ชันพีชคณิต (A) เป็น dv"
    if inv_trig_factors:
        u_cand = sp.Mul(*inv_trig_factors)
        dv_cand = sp.Mul(*[f for f in factors if f not in inv_trig_factors])
        return u_cand, dv_cand, "ตามแนวทาง LIATE: เลือกฟังก์ชันตรีโกณมิติผกผัน (I) เป็น u"

    # A มาก่อน T / E
    if poly_factors and (exp_factors or trig_factors):
        u_cand = sp.Mul(*poly_factors)
        other_factors = [f for f in factors if f not in poly_factors]
        dv_cand = sp.Mul(*other_factors)
        return u_cand, dv_cand, "ตามแนวทาง LIATE: เลือกฟังก์ชันพีชคณิต (A) เป็น u เพื่อลดทอนดีกรีผ่านการหาอนุพันธ์"

    # Cyclic E * T
    if exp_factors and trig_factors:
        u_cand = sp.Mul(*exp_factors)
        dv_cand = sp.Mul(*trig_factors)
        return u_cand, dv_cand, "ฟังก์ชันเอกซ์โพเนนเชียลคูณกับฟังก์ชันตรีโกณมิติ (Cyclic Integration)"

    return None


def _get_domain_note(expr: sp.Expr, var: sp.Symbol = X) -> str:
    """สร้างคำอธิบายเงื่อนไขโดเมนตาม Universal Step Contract"""
    notes = []
    if expr.has(sp.log):
        for node in expr.atoms(sp.log):
            notes.append(f"${_to_latex(node.args[0])} > 0$")
    numer, denom = expr.as_numer_denom()
    if denom != 1 and denom.has(var):
        notes.append(f"${_to_latex(denom)} \\neq 0$")
    for node in expr.atoms(sp.Pow):
        if node.exp.is_Rational and node.exp.q % 2 == 0:
            notes.append(f"${_to_latex(node.base)} \\geq 0$")

    if notes:
        return f"เงื่อนไขโดเมน (Domain restriction): ขั้นนี้ถูกต้องบนช่วงที่ " + " และ ".join(notes)
    return "เงื่อนไขโดเมน (Domain restriction): ฟังก์ชันหาปริพันธ์ได้บนทุกช่วงที่ฟังก์ชันมีความต่อเนื่อง ($x \\in \\mathbb{R}$)"


def solve_substitution(expr_str: str, var: str | sp.Symbol | None = None) -> dict:
    """คำนวณปริพันธ์ แจกแจงการแทนค่าตัวแปร u-Substitution หรือ By Parts ตาม Universal Step Contract"""
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
        v_lat = _to_latex(var_sym)
        domain_note = _get_domain_note(expr, var_sym)

        if antideriv.has(sp.Integral):
            return {
                "ok": False,
                "result": None,
                "latex": "",
                "steps": [
                    f"กำหนดโจทย์อินทิกรัล: $\\int {_to_latex(expr)} \\, d{v_lat}$",
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

        steps = [
            f"กำหนดโจทย์อินทิกรัล: $\\int {_to_latex(expr)} \\, d{v_lat}$",
        ]

        if has_special:
            status = "non_elementary"
            warning = "ฟังก์ชันนี้ไม่มีปฏิยานุพันธ์ในรูปฟังก์ชันมูลฐาน (Non-Elementary Antiderivative)"
            steps.append(
                "ข้อสังเกตเชิงมโนทัศน์: ฟังก์ชันนี้ไม่มีปฏิยานุพันธ์ในรูปฟังก์ชันมูลฐาน (Non-Elementary Antiderivative) ตามทฤษฎีบทของ Liouville จึงไม่สามารถหาผลลัพธ์ด้วยเทคนิคการเปลี่ยนตัวแปรหรือ By Parts ปกติได้"
            )
            steps.append(
                f"ผลลัพธ์อยู่ในรูปฟังก์ชันพิเศษระดับสูง: $\\int {_to_latex(expr)} \\, d{v_lat} = {_to_latex(antideriv)} + C$"
            )
            steps.append(domain_note)
            return {
                "ok": True,
                "result": antideriv,
                "latex": f"\\int {_to_latex(expr)} \\, d{v_lat} = {_to_latex(antideriv)} + C",
                "steps": steps,
                "expr": expr,
                "u_candidate": None,
                "du_candidate": None,
                "status": status,
                "warning": warning,
                "error": None,
                "variable": str(var_sym.name),
                "method": "non_elementary",
            }

        # -------------------------------------------------------------
        # ตรวจสอบว่าควรแก้ด้วย u-Substitution หรือ By Parts
        # -------------------------------------------------------------
        u_cand, du_cand = _detect_u_candidate(expr, var_sym)
        is_clean_usub = False
        if u_cand is not None and du_cand is not None:
            ratio = sp.simplify(expr / du_cand)
            if not ratio.has(var_sym):
                is_clean_usub = True
            else:
                u_temp = sp.Symbol("_u_temp")
                ratio_sub = sp.simplify(ratio.subs(u_cand, u_temp))
                if not ratio_sub.has(var_sym):
                    is_clean_usub = True

        parts_cand = None
        if not is_clean_usub:
            parts_cand = _detect_parts_candidate(expr, var_sym)

        # เส้นทาง B: การอินทิเกรตทีละส่วน (Integration by Parts)
        if parts_cand is not None:
            u_p, dv_p, parts_reason = parts_cand
            du_p = sp.diff(u_p, var_sym)
            v_p = sp.integrate(dv_p, var_sym)
            v_du = sp.simplify(v_p * du_p)
            rem_integral = sp.integrate(v_du, var_sym)

            steps.append(
                f"เป้าหมาย / กฎที่ใช้ (Goal / Rule): ใช้เทคนิคการอินทิเกรตทีละส่วน (Integration by Parts) ตามสูตร $\\int u \\, dv = uv - \\int v \\, du$ ({parts_reason})"
            )
            steps.append(
                f"นิพจน์หลังแทนค่า (Substituted expression): กำหนดตัวแปรและหาอนุพันธ์กับปฏิยานุพันธ์:\n"
                f"- กำหนด $u = {_to_latex(u_p)} \\implies du = {_to_latex(du_p)} \\, d{v_lat}$\n"
                f"- กำหนด $dv = {_to_latex(dv_p)} \\, d{v_lat} \\implies v = \\int {_to_latex(dv_p)} \\, d{v_lat} = {_to_latex(v_p)}$"
            )
            steps.append(
                f"แทนค่าลงในสูตร By Parts: $\\int u \\, dv = uv - \\int v \\, du = \\left({_to_latex(u_p)}\\right)\\left({_to_latex(v_p)}\\right) - \\int \\left({_to_latex(v_p)}\\right)\\left({_to_latex(du_p)}\\right) \\, d{v_lat}$"
            )
            steps.append(
                f"พีชคณิตระหว่างทาง (Intermediate algebra): จัดรูปอินทิกรัลที่เหลือ $\\int v \\, du = \\int {_to_latex(v_du)} \\, d{v_lat} = {_to_latex(rem_integral)}$"
            )
            steps.append(domain_note)
            steps.append(
                f"ผลลัพธ์แม่นตรง (Exact result): $\\int {_to_latex(expr)} \\, d{v_lat} = {_to_latex(antideriv)} + C$"
            )

            return {
                "ok": True,
                "result": antideriv,
                "latex": f"\\int {_to_latex(expr)} \\, d{v_lat} = {_to_latex(antideriv)} + C",
                "steps": steps,
                "expr": expr,
                "u_candidate": None,
                "du_candidate": None,
                "status": "elementary",
                "warning": None,
                "error": None,
                "variable": str(var_sym.name),
                "method": "by_parts",
                "parts_info": {
                    "u": u_p,
                    "dv": dv_p,
                    "du": du_p,
                    "v": v_p,
                    "remainder": v_du,
                },
            }

        # เส้นทาง A: การแทนค่า u (u-Substitution)
        if u_cand is not None and du_cand is not None:
            u_sym = sp.Symbol("u")
            expr_u = expr.subs(u_cand, u_sym)
            ratio = sp.simplify(expr_u / du_cand)
            integrand_u = ratio if not ratio.has(var_sym) else sp.simplify(sp.simplify(expr / du_cand).subs(u_cand, u_sym))
            integral_u = sp.integrate(integrand_u, u_sym)

            steps.append(
                f"เป้าหมาย / กฎที่ใช้ (Goal / Rule): ใช้เทคนิคการเปลี่ยนตัวแปร (u-Substitution) โดยเลือกฟังก์ชันก้อนในที่มีอนุพันธ์คูณร่วมอยู่"
            )
            steps.append(
                f"นิพจน์หลังแทนค่า (Substituted expression): กำหนดตัวแปร $u = {_to_latex(u_cand)}$ ส่งผลให้หาอนุพันธ์ได้ $du = {_to_latex(du_cand)} \\, d{v_lat}$ หรือ $d{v_lat} = \\frac{{du}}{{{_to_latex(du_cand)}}}$"
            )
            steps.append(
                f"พีชคณิตระหว่างทาง (Intermediate algebra): แทนค่า $u$ และ $d{v_lat}$ ลงในโจทย์ ทำให้ตัวแปร ${v_lat}$ ถูกตัดทอนทั้งหมด: $\\int {_to_latex(expr)} \\, d{v_lat} = \\int {_to_latex(integrand_u)} \\, du$"
            )
            steps.append(
                f"คำนวณปริพันธ์เทียบกับตัวแปร u: $\\int {_to_latex(integrand_u)} \\, du = {_to_latex(integral_u)} + C$"
            )
            steps.append(
                f"แทนค่ากลับ (Back-substitution): แทนค่า $u = {_to_latex(u_cand)}$ คืนสู่ตัวแปรเดิม: ${_to_latex(antideriv)} + C$"
            )
            steps.append(domain_note)
            steps.append(
                f"ผลลัพธ์แม่นตรง (Exact result): $\\int {_to_latex(expr)} \\, d{v_lat} = {_to_latex(antideriv)} + C$"
            )

            return {
                "ok": True,
                "result": antideriv,
                "latex": f"\\int {_to_latex(expr)} \\, d{v_lat} = {_to_latex(antideriv)} + C",
                "steps": steps,
                "expr": expr,
                "u_candidate": u_cand,
                "du_candidate": du_cand,
                "status": "elementary",
                "warning": None,
                "error": None,
                "variable": str(var_sym.name),
                "method": "substitution",
            }

        # เส้นทางทั่วไป (Standard rules)
        steps.append(
            "เป้าหมาย / กฎที่ใช้ (Goal / Rule): คำนวณปริพันธ์โดยใช้สูตรพื้นฐานของแคลคูลัส (Basic Integration Rules)"
        )
        steps.append(domain_note)
        steps.append(
            f"ผลลัพธ์แม่นตรง (Exact result): $\\int {_to_latex(expr)} \\, d{v_lat} = {_to_latex(antideriv)} + C$"
        )

        return {
            "ok": True,
            "result": antideriv,
            "latex": f"\\int {_to_latex(expr)} \\, d{v_lat} = {_to_latex(antideriv)} + C",
            "steps": steps,
            "expr": expr,
            "u_candidate": None,
            "du_candidate": None,
            "status": "elementary",
            "warning": None,
            "error": None,
            "variable": str(var_sym.name),
            "method": "standard",
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
