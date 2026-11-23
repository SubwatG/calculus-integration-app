"""utils/substitution_solver.py - การอินทิเกรตโดยการแทนตัวแปรและเทคนิคการอินทิเกรต

รองรับการตรวจหาตัวแปร u เชิงสัญลักษณ์, เทคนิคการอินทิเกรตทีละส่วน (Integration by Parts),
และการจำแนกฟังก์ชันที่ไม่เป็นฟังก์ชันมูลฐาน (Non-elementary integrals)
ตามเกณฑ์ Universal Step Contract
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
    """แปลง SymPy object เป็น LaTeX string พร้อมแทนที่ \\log เป็น \\ln และปรับฟังก์ชันตรีโกณผกผันตามมาตรฐานการสอนแคลคูลัส"""
    lat = sp.latex(sym_obj, inv_trig_style="full")
    lat = lat.replace(r"\log", r"\ln")
    lat = re.sub(r"\\operatorname\{a(sin|cos|tan)\}", r"\\arc\1", lat)
    lat = re.sub(r"\\operatorname\{arc(cot|sec|csc)\}", r"\\arc\1", lat)
    lat = re.sub(r"(?<![a-zA-Z\\])a(sin|cos|tan)(?=\s*[\(\{\[_0-9]|\b)", r"\\arc\1", lat)
    lat = re.sub(r"\\ln\{\\left\(\\left\|(.*?)\\right\| \\right\)\}", r"\\ln{\\left|\1\\right|}", lat)
    return lat


def _wrap_new_logs(antideriv: sp.Expr, orig_expr: sp.Expr) -> sp.Expr:
    r"""ใส่วงเล็บค่าสัมบูรณ์ในฟังก์ชัน log ที่เกิดจากการคำนวณปริพันธ์ใหม่ (เช่น \int 1/u du = \ln|u|)"""
    if antideriv is None:
        return None
    orig_logs = orig_expr.atoms(sp.log) if orig_expr is not None else set()

    def repl(node):
        if not isinstance(node, sp.log):
            return node
        arg = node.args[0]
        if getattr(arg, "func", None) is sp.Abs:
            return node
        if node in orig_logs:
            return node
        return sp.log(sp.Abs(arg))

    return antideriv.replace(sp.log, lambda a: repl(sp.log(a)))


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
        return f"เงื่อนไขโดเมน: ขั้นตอนนี้ถูกต้องบนช่วงที่ " + " และ ".join(notes)
    return "เงื่อนไขโดเมน: ฟังก์ชันหาปริพันธ์ได้บนทุกช่วงที่ฟังก์ชันมีความต่อเนื่อง ($x \\in \\mathbb{R}$)"


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

        orig_expr = expr
        simplified_step = None
        if antideriv.has(sp.Integral):
            try:
                trig_rep = expr.replace(sp.tan, lambda a: sp.sin(a) / sp.cos(a))
                trig_rep = trig_rep.replace(sp.cot, lambda a: sp.cos(a) / sp.sin(a))
                trig_rep = trig_rep.replace(sp.sec, lambda a: 1 / sp.cos(a))
                trig_rep = trig_rep.replace(sp.csc, lambda a: 1 / sp.sin(a))
                simp_expr = sp.cancel(trig_rep)
                if simp_expr != expr:
                    res_simp = sp.integrate(simp_expr, var_sym)
                    if not res_simp.has(sp.Integral):
                        expr = simp_expr
                        antideriv = res_simp
                        simplified_step = (
                            f"จัดรูปฟังก์ชันตรีโกณมิติก่อนอินทิเกรต: "
                            f"แปลงรูปฟังก์ชันเพื่อให้หาปฏิยานุพันธ์ได้:\n"
                            f"{_to_latex(orig_expr)} = {_to_latex(simp_expr)}"
                        )
            except Exception:
                pass

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
            f"กำหนดโจทย์อินทิกรัล: $\\int {_to_latex(orig_expr)} \\, d{v_lat}$",
        ]
        if simplified_step:
            steps.append(simplified_step)

        if has_special:
            status = "non_elementary"
            warning = "ฟังก์ชันนี้ไม่มีปฏิยานุพันธ์ในรูปฟังก์ชันมูลฐาน (Non-Elementary Antiderivative)"
            steps.append(
                "ข้อสังเกตเชิงแนวคิด: ฟังก์ชันนี้ไม่มีปฏิยานุพันธ์ในรูปฟังก์ชันมูลฐาน (Non-Elementary Antiderivative) ตามทฤษฎีบทของ Liouville จึงไม่สามารถหาผลลัพธ์ด้วยเทคนิคการเปลี่ยนตัวแปรหรือ By Parts ปกติได้"
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
            if not rem_integral.has(sp.Integral) and antideriv.has(sp.Integral):
                antideriv = u_p * v_p - rem_integral
            antideriv = _wrap_new_logs(antideriv, orig_expr)
            rem_integral_disp = _wrap_new_logs(rem_integral, v_du)

            steps.append(
                f"เลือกวิธี: การอินทิเกรตทีละส่วน (Integration by parts) ตามสูตร $\\int u \\, dv = uv - \\int v \\, du$ ({parts_reason})"
            )
            steps.append(
                f"กำหนดตัวแปร: กำหนดตัวแปรและหาอนุพันธ์กับปฏิยานุพันธ์:\n"
                f"- กำหนด $u = {_to_latex(u_p)} \\implies du = {_to_latex(du_p)} \\, d{v_lat}$\n"
                f"- กำหนด $dv = {_to_latex(dv_p)} \\, d{v_lat} \\implies v = \\int {_to_latex(dv_p)} \\, d{v_lat} = {_to_latex(v_p)}$"
            )
            steps.append(
                f"แทนค่าลงในสูตร By Parts: $\\int u \\, dv = uv - \\int v \\, du = \\left({_to_latex(u_p)}\\right)\\left({_to_latex(v_p)}\\right) - \\int \\left({_to_latex(v_p)}\\right)\\left({_to_latex(du_p)}\\right) \\, d{v_lat}$"
            )
            steps.append(
                f"คำนวณปริพันธ์ที่เหลือ: จัดรูปและหาค่า $\\int v \\, du = \\int {_to_latex(v_du)} \\, d{v_lat} = {_to_latex(rem_integral_disp)}$"
            )
            steps.append(domain_note)
            steps.append(
                f"สรุปผลลัพธ์: $\\int {_to_latex(expr)} \\, d{v_lat} = {_to_latex(antideriv)} + C$"
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
            u_sym = sp.Symbol("u", real=True)
            expr_u = expr.subs(u_cand, u_sym)
            ratio = sp.simplify(expr_u / du_cand)
            integrand_u = ratio if not ratio.has(var_sym) else sp.simplify(sp.simplify(expr / du_cand).subs(u_cand, u_sym))
            integral_u = sp.integrate(integrand_u, u_sym)
            if not integral_u.has(sp.Integral):
                subbed_antideriv = _wrap_new_logs(integral_u.subs(u_sym, u_cand), orig_expr)
                if antideriv.has(sp.Integral) or str(antideriv).count("log") > str(subbed_antideriv).count("log") or "tan" in str(orig_expr):
                    antideriv = subbed_antideriv

            antideriv = _wrap_new_logs(antideriv, orig_expr)
            integral_u_disp = _wrap_new_logs(integral_u, integrand_u)

            steps.append(
                f"เลือกวิธี: การเปลี่ยนตัวแปร (Integration by Substitution) โดยเลือกฟังก์ชันก้อนในที่มีอนุพันธ์คูณร่วมอยู่"
            )
            steps.append(
                f"กำหนดตัวแปร: กำหนดตัวแปร $u = {_to_latex(u_cand)}$ จะได้ $du = {_to_latex(du_cand)} \\, d{v_lat}$ หรือ $d{v_lat} = \\frac{{du}}{{{_to_latex(du_cand)}}}$"
            )
            steps.append(
                f"เปลี่ยนรูปปริพันธ์: แทนค่า $u$ และ $d{v_lat}$ ในโจทย์ ทำให้เหลือเฉพาะตัวแปร $u$:\n$\\int {_to_latex(expr)} \\, d{v_lat} = \\int {_to_latex(integrand_u)} \\, du$"
            )
            steps.append(
                f"คำนวณปริพันธ์เทียบกับตัวแปร u: $\\int {_to_latex(integrand_u)} \\, du = {_to_latex(integral_u_disp)} + C$"
            )
            steps.append(
                f"แทนค่ากลับ: แทนค่า $u = {_to_latex(u_cand)}$ กลับคืน:\n${_to_latex(antideriv)} + C$"
            )
            steps.append(domain_note)
            steps.append(
                f"สรุปผลลัพธ์: $\\int {_to_latex(expr)} \\, d{v_lat} = {_to_latex(antideriv)} + C$"
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
        antideriv = _wrap_new_logs(antideriv, orig_expr)
        steps.append(
            "คำนวณปริพันธ์โดยใช้สูตรพื้นฐานของแคลคูลัส"
        )
        steps.append(domain_note)
        steps.append(
            f"สรุปผลลัพธ์: $\\int {_to_latex(expr)} \\, d{v_lat} = {_to_latex(antideriv)} + C$"
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


def check_standard_form(h: sp.Expr, var: sp.Symbol) -> bool:
    """ตรวจสอบว่านิพจน์ h(var) อยู่ในรูปผลรวมของฟังก์ชันพื้นฐานที่หาอินทิกรัลได้โดยตรงหรือไม่"""
    try:
        expanded = sp.expand(h)
        terms = sp.Add.make_args(expanded)
        for t in terms:
            c, r = t.as_coeff_Mul()
            if r == 1 or r == var:
                continue
            if isinstance(r, sp.Pow) and r.base == var:
                continue
            if r == sp.exp(var):
                continue
            if r in (sp.sin(var), sp.cos(var), sp.sec(var)**2, sp.csc(var)**2):
                continue
            if r == 1 / (var**2 + 1):
                continue
            return False
        return True
    except Exception:
        return False


def get_suggested_u_candidates(expr_str: str, var: str | sp.Symbol | None = None) -> list[str]:
    """สร้างรายการตัวเลือกฟังก์ชัน u ที่น่าสนใจสำหรับโจทย์ที่กำหนด เพื่อให้ผู้เรียนได้ทดลองเลือก"""
    try:
        clean_expr, diff_var = _clean_calculus_input(expr_str)
        expr = _parse_input(clean_expr)
        if var is None:
            var_sym = sp.Symbol(diff_var) if diff_var is not None else _get_variable(expr)
        elif isinstance(var, str):
            var_sym = sp.Symbol(var)
        else:
            var_sym = var

        cands = []
        best_u, _ = _detect_u_candidate(expr, var_sym)
        if best_u is not None:
            cands.append(best_u)

        for node in expr.atoms(sp.Pow):
            if node.base != var_sym and node.base.has(var_sym) and not node.base.is_number:
                cands.append(node.base)
            if node.has(var_sym) and not node.is_number and node != var_sym:
                cands.append(node)

        for cls in (sp.sin, sp.cos, sp.tan):
            for node in expr.atoms(cls):
                if node.args[0] != var_sym and node.args[0].has(var_sym):
                    cands.append(node.args[0])
                cands.append(node)

        for node in expr.atoms(sp.exp):
            if node.args[0] != var_sym and node.args[0].has(var_sym):
                cands.append(node.args[0])
            cands.append(node)

        for node in expr.atoms(sp.log):
            if node.has(var_sym):
                cands.append(node)
                if node.args[0] != var_sym and node.args[0].has(var_sym):
                    cands.append(node.args[0])

        numer, denom = expr.as_numer_denom()
        if denom != 1 and denom.has(var_sym) and denom != var_sym:
            cands.append(denom)

        if expr.is_Mul:
            for f in expr.args:
                if f.has(var_sym) and f != var_sym:
                    cands.append(f)

        seen = set()
        result = []
        for c in cands:
            s_code = str(c)
            if s_code not in seen and c != var_sym:
                seen.add(s_code)
                result.append(s_code)

        result.append(str(var_sym))
        return result[:6]
    except Exception:
        return ["x"]


def verify_user_u_substitution(
    expr_str: str,
    u_str: str,
    var: str | sp.Symbol | None = None,
) -> dict:
    """ตรวจสอบการเลือกตัวแปร u ของผู้ใช้ ว่าทำได้โดยตรง, ต้องจัดรูปก่อน, หรือทำไม่ได้"""
    clean_expr_str = (expr_str or "").strip()
    clean_u_str = (u_str or "").strip()

    if not clean_expr_str or not clean_u_str:
        return {
            "ok": False,
            "status": "error",
            "status_th": "ข้อมูลไม่ครบถ้วน",
            "message": "กรุณาระบุทั้งโจทย์อินทิกรัลและฟังก์ชัน u ที่ต้องการทดสอบ",
            "steps": [],
            "latex": "",
            "result": None,
            "variable": "x",
        }

    try:
        clean_expr, diff_var = _clean_calculus_input(clean_expr_str)
        expr = _parse_input(clean_expr)
        u_expr = _parse_input(clean_u_str)

        if var is None:
            var_sym = sp.Symbol(diff_var) if diff_var is not None else _get_variable(expr)
        elif isinstance(var, str):
            var_sym = sp.Symbol(var)
        else:
            var_sym = var

        v_lat = _to_latex(var_sym)
        domain_note = _get_domain_note(expr, var_sym)

        # ตรวจสอบว่า u มีตัวแปร x หรือไม่
        if not u_expr.has(var_sym):
            return {
                "ok": False,
                "status": "invalid",
                "status_th": "ตัวแปร u ไม่ถูกต้อง",
                "message": f"ตัวแปร $u$ ต้องขึ้นอยู่กับตัวแปร ${v_lat}$ ไม่สามารถเป็นค่าคงที่ได้",
                "steps": [
                    f"โจทย์อินทิกรัล: $\\int {_to_latex(expr)} \\, d{v_lat}$",
                    f"ค่าที่เลือก: $u = {_to_latex(u_expr)}$ เป็นค่าคงที่ ไม่มีตัวแปร ${v_lat}$ จึงไม่สามารถหาอนุพันธ์เทียบกับ ${v_lat}$ ได้",
                ],
                "latex": "",
                "result": None,
                "variable": str(var_sym.name),
            }

        # ตรวจสอบกรณี trivial u = x
        if u_expr == var_sym:
            return {
                "ok": True,
                "status": "trivial",
                "status_th": "ไม่มีการลดทอนความซับซ้อน",
                "message": f"การกำหนด $u = {v_lat}$ เป็นเพียงการเปลี่ยนชื่อตัวอักษร ไม่ได้ช่วยให้อินทิเกรตง่ายขึ้น",
                "steps": [
                    f"โจทย์อินทิกรัล: $\\int {_to_latex(expr)} \\, d{v_lat}$",
                    f"กำหนด $u = {v_lat} \\implies du = d{v_lat}$",
                    f"แทนค่าแล้วได้: $\\int {_to_latex(expr.subs(var_sym, sp.Symbol('u')))} \\, du$ ซึ่งมีความซับซ้อนเท่ากับโจทย์เดิมทุกประการ",
                ],
                "latex": "",
                "result": None,
                "variable": str(var_sym.name),
            }

        du = sp.diff(u_expr, var_sym)
        ratio = sp.simplify(expr / du)
        u_sym = sp.Symbol("u")
        ratio_u = sp.simplify(ratio.subs(u_expr, u_sym))

        # -------------------------------------------------------------
        # 1. กรณี Direct Substitution (ทำได้โดยตรง)
        # -------------------------------------------------------------
        if not ratio_u.has(var_sym):
            antideriv_u = sp.integrate(ratio_u, u_sym)
            if not antideriv_u.has(sp.Integral) and not any(antideriv_u.has(f) for f in SPECIAL_FUNCS):
                antideriv_x = sp.simplify(antideriv_u.subs(u_sym, u_expr))
                steps = [
                    f"กำหนดโจทย์อินทิกรัล: $\\int {_to_latex(expr)} \\, d{v_lat}$",
                    f"ขั้นที่ 1: กำหนดตัวแปรและคำนวณอนุพันธ์\n"
                    f"$$u = {_to_latex(u_expr)} \\implies du = {_to_latex(du)} \\, d{v_lat} \\implies d{v_lat} = \\frac{{du}}{{{_to_latex(du)}}}$$",
                    f"ขั้นที่ 2: แทนค่าลงในอินทิกรัลและสังเกตการตัดทอน\n"
                    f"$$\\int {_to_latex(expr)} \\, d{v_lat} = \\int {_to_latex(expr)} \\cdot \\frac{{du}}{{{_to_latex(du)}}} = \\int {_to_latex(ratio_u)} \\, du$$\n"
                    f"ตัวแปร ${v_lat}$ ถูกตัดทอนหมด เหลือเพียงฟังก์ชันของตัวแปร $u$",
                    f"ขั้นที่ 3: คำนวณปริพันธ์เทียบกับตัวแปร u\n"
                    f"$$\\int {_to_latex(ratio_u)} \\, du = {_to_latex(antideriv_u)} + C$$",
                    f"ขั้นที่ 4: แทนค่า $u = {_to_latex(u_expr)}$ กลับในผลลัพธ์:\n"
                    f"$$= {_to_latex(antideriv_x)} + C$$",
                    domain_note,
                ]
                return {
                    "ok": True,
                    "status": "direct",
                    "status_th": "ทำได้โดยตรง (สำเร็จ)",
                    "message": f"ถูกต้องตามหลักการ: การเลือก $u = {_to_latex(u_expr)}$ ทำให้อนุพันธ์ตัดทอนตัวแปรเดิมได้หมด",
                    "steps": steps,
                    "latex": f"\\int {_to_latex(expr)} \\, d{v_lat} = {_to_latex(antideriv_x)} + C",
                    "result": antideriv_x,
                    "u_expr": u_expr,
                    "du_expr": du,
                    "integrand_u": ratio_u,
                    "variable": str(var_sym.name),
                }

        # -------------------------------------------------------------
        # 2. กรณี Algebraic Adjustment (ต้องจัดรูปพีชคณิตเสริมก่อน)
        # -------------------------------------------------------------
        sols = sp.solve(sp.Eq(u_sym, u_expr), var_sym)
        if sols:
            for x_sol in sols:
                subbed = sp.simplify(ratio_u.subs(var_sym, x_sol))
                if not subbed.has(var_sym):
                    int_u = sp.integrate(subbed, u_sym)
                    if not int_u.has(sp.Integral) and not any(int_u.has(f) for f in SPECIAL_FUNCS):
                        if check_standard_form(subbed, u_sym):
                            antideriv_x = sp.simplify(int_u.subs(u_sym, u_expr))
                            steps = [
                                f"กำหนดโจทย์อินทิกรัล: $\\int {_to_latex(expr)} \\, d{v_lat}$",
                                f"ขั้นที่ 1: กำหนดตัวแปรและหาอนุพันธ์\n"
                                f"$$u = {_to_latex(u_expr)} \\implies du = {_to_latex(du)} \\, d{v_lat} \\implies d{v_lat} = \\frac{{du}}{{{_to_latex(du)}}}$$",
                                f"ขั้นที่ 2: แทนค่าลงในอินทิกรัล (พบตัวแปรตกค้าง)\n"
                                f"$$\\int {_to_latex(expr)} \\, d{v_lat} = \\int \\left({_to_latex(ratio)}\\right) du$$\n"
                                f"สังเกตว่าตัวแปร ${v_lat}$ ด้านหน้ายังตัดทอนไม่หมด",
                                f"ขั้นที่ 3: จัดรูปพีชคณิตเสริมโดยแก้สมการย้อนกลับ\n"
                                f"จาก $u = {_to_latex(u_expr)}$ แก้สมการหาค่า ${v_lat}$ ในรูปของ $u$ ได้เป็น:\n"
                                f"$${v_lat} = {_to_latex(x_sol)}$$\n"
                                f"นำค่า ${v_lat}$ ไปแทนที่ในอินทิกรัล แล้วคูณกระจาย จะได้ฟังก์ชันของ $u$ ล้วน:\n"
                                f"$$\\int {_to_latex(subbed)} \\, du$$",
                                f"ขั้นที่ 4: คำนวณปริพันธ์เทียบกับตัวแปร u\n"
                                f"$$\\int {_to_latex(subbed)} \\, du = {_to_latex(int_u)} + C$$",
                                f"ขั้นที่ 5: แทนค่า $u = {_to_latex(u_expr)}$ กลับในผลลัพธ์:\n"
                                f"$$= {_to_latex(antideriv_x)} + C$$",
                                domain_note,
                            ]
                            return {
                                "ok": True,
                                "status": "algebraic_adjustment",
                                "status_th": "ทำได้โดยต้องจัดรูปพีชคณิตเสริมก่อน",
                                "message": f"ทำได้สำเร็จ: เมื่อแทนค่าแล้วตัวแปร ${v_lat}$ ยังตัดไม่หมด ต้องจัดรูปแก้สมการกลับ ${v_lat} = {_to_latex(x_sol)}$ แทนลงไปเพื่อคูณกระจาย",
                                "steps": steps,
                                "latex": f"\\int {_to_latex(expr)} \\, d{v_lat} = {_to_latex(antideriv_x)} + C",
                                "result": antideriv_x,
                                "u_expr": u_expr,
                                "du_expr": du,
                                "x_sol": x_sol,
                                "integrand_u": subbed,
                                "variable": str(var_sym.name),
                            }

        # -------------------------------------------------------------
        # 3. กรณี Incompatible (ทำไม่ได้ด้วย u นี้) หรือโจทย์ต้องใช้ By Parts
        # -------------------------------------------------------------
        from utils.by_parts_solver import detect_parts_candidate
        parts_c = detect_parts_candidate(expr, var_sym)
        best_u, _ = _detect_u_candidate(expr, var_sym)

        if parts_c is not None and best_u is None:
            return {
                "ok": False,
                "status": "unsuitable_for_substitution",
                "status_th": "ไม่เหมาะกับการแทนตัวแปร u",
                "message": "โจทย์ข้อนี้ไม่สามารถแก้ด้วยการแทนตัวแปร u ได้ เนื่องจากไม่มีพจน์อนุพันธ์ร่วมคูณอยู่ แนะนำให้ใช้วิธีการอินทิเกรตทีละส่วน (Integration by Parts)",
                "steps": [
                    f"กำหนดโจทย์อินทิกรัล: $\\int {_to_latex(expr)} \\, d{v_lat}$",
                    f"ข้อสังเกต: โจทย์ข้อนี้อยู่ในรูปแบบผลคูณของสองฟังก์ชันที่แตกต่างกันอย่างสิ้นเชิง ซึ่งสอดคล้องกับกฎ LIATE แนะนำให้เปิดหน้า \"4. การอินทิเกรตทีละส่วน\"",
                ],
                "latex": "",
                "result": None,
                "variable": str(var_sym.name),
            }

        return {
            "ok": False,
            "status": "incompatible",
            "status_th": "ทำไม่ได้ด้วยตัวแปร u นี้",
            "message": f"การเลือก $u = {_to_latex(u_expr)}$ ไม่สามารถแก้ได้: ตัวแปร ${v_lat}$ ไม่สามารถตัดทอนให้หมดไปได้ (ตัดทอนไม่หมด) และไม่ช่วยลดรูปอินทิกรัล",
            "steps": [
                f"กำหนดโจทย์อินทิกรัล: $\\int {_to_latex(expr)} \\, d{v_lat}$",
                f"ขั้นที่ 1: กำหนดตัวแปรและหาอนุพันธ์: $u = {_to_latex(u_expr)} \\implies du = {_to_latex(du)} \\, d{v_lat}$",
                f"ขั้นที่ 2: เมื่อนำไปแทนค่าในโจทย์จะได้รูป:\n$$\\int {_to_latex(expr)} \\cdot \\frac{{du}}{{{_to_latex(du)}}} = \\int \\left({_to_latex(ratio)}\\right) du$$",
                f"ขั้นที่ 3: สังเกตว่าพจน์ของตัวแปร ${v_lat}$ ยังคงตกค้างอยู่ และไม่สามารถเขียนแทนด้วยตัวแปร $u$ ได้อย่างสะดวก จึงไม่สามารถอินทิเกรตต่อได้",
            ],
            "latex": "",
            "result": None,
            "variable": str(var_sym.name),
        }
    except Exception as e:
        return {
            "ok": False,
            "status": "error",
            "status_th": "เกิดข้อผิดพลาด",
            "message": f"ไม่สามารถคำนวณการแทนค่าได้: {e}",
            "steps": [],
            "latex": "",
            "result": None,
            "variable": "x",
        }

