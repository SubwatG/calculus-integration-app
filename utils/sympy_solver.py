import re
from typing import Any
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
}

PREFERRED_INDEPENDENT_VARS = ["x", "t", "y", "u", "z", "s", "r", "v", "w", "theta"]
PARAM_CONSTANTS = {"a", "b", "c", "k", "m", "n", "p", "q", "d", "A", "B", "C", "K", "M", "N"}


def _clean_calculus_input(expr_str: str) -> tuple[str, str | None]:
    """ทำความสะอาดข้อความสูตรและสกัดตัวแปรดิฟเฟอเรนเชียล (เช่น '3t^2 dt' -> '3t^2', 't')"""
    clean = (expr_str or "").strip()
    if not clean:
        return "", None

    # ลบเครื่องหมายอินทิกรัลนำหน้า เช่น \int, int, \int_{0}^{1}
    clean = re.sub(
        r"^(?:\\int|int)(?:_\{[^}]*\}\^\{[^}]*\}|_[^\s^]+\^[^\s]+)?\s*",
        "",
        clean,
    ).strip()

    # กรณีผู้ใช้พิมพ์แค่ 'dt' หรือ 'dx' เดี่ยว ๆ
    exact_m = re.match(r"^d([a-zA-Z]+|\\[a-zA-Z]+)$", clean)
    if exact_m:
        var_name = exact_m.group(1).lstrip("\\")
        if var_name.lower() in ("x", "t", "y", "u", "z", "s", "r", "v", "w", "theta", "phi", "a", "b", "c", "k"):
            return "1", var_name

    # ตรวจหาผลคูณต่อท้าย เช่น '3t^2 dt', '3t^2*dt', '3t^2\,dt'
    diff_pattern = r"(?:\\,|[\s*])d([a-zA-Z]+|\\[a-zA-Z]+)\s*$"
    m = re.search(diff_pattern, clean)
    detected_diff_var = None
    if m:
        var_name = m.group(1).lstrip("\\")
        if var_name.lower() in ("x", "t", "y", "u", "z", "s", "r", "v", "w", "theta", "phi", "a", "b", "c", "k"):
            detected_diff_var = var_name
            clean = clean[:m.start()].strip()
            if not clean:
                clean = "1"

    return clean, detected_diff_var


def _parse_input(expr_str: str) -> sp.Expr:
    clean_str = expr_str.strip()
    if not clean_str:
        raise ValueError("Empty input string")
    return parse_expr(clean_str, transformations=TRANSFORMATIONS, local_dict=LOCAL_MATH_DICT)


def _get_variable(expr: sp.Expr, default: str = "x") -> sp.Symbol:
    """ตรวจจับตัวแปรอิสระในนิพจน์ (Auto-detect variable)
    - ถ้าไม่มีตัวแปร (เช่น ค่าคงที่ 5) คืนค่า default (Symbol('x'))
    - ถ้ามีสัญลักษณ์เดียว คืนค่าตัวแปรนั้น (เช่น Symbol('t'))
    - ถ้ามีหลายตัวแปร และมี default ('x') อยู่ ให้เลือก 'x' ก่อนเพื่อความเข้ากันได้
    - ให้ความสำคัญกับตัวแปรอิสระมาตรฐาน (x, t, y, u, z, theta, s, r, v, w) ก่อนค่าคงที่/พารามิเตอร์ (a, b, c, k, m, n)
    - ถ้าไม่มีตัวแปรที่ตรงกับลำดับข้างต้น ให้คัดกรองค่าคงที่แล้วคืนค่าตัวแปรแรก
    """
    free = expr.free_symbols
    if not free:
        return sp.Symbol(default)
    if len(free) == 1:
        return list(free)[0]

    names = {s.name: s for s in free}
    if default in names:
        return names[default]

    for pref in PREFERRED_INDEPENDENT_VARS:
        if pref in names:
            return names[pref]

    non_params = [s for s in free if s.name not in PARAM_CONSTANTS]
    if non_params:
        return sorted(non_params, key=lambda s: s.name)[0]

    sorted_syms = sorted(free, key=lambda s: s.name)
    return sorted_syms[0]


def detect_variable(expr_str: str, default: str = "x") -> str:
    """ตรวจจับชื่อตัวแปรอิสระในข้อความสูตร เช่น '3t^2 + 2t' -> 't', '3t^2 dt' -> 't'"""
    try:
        clean_str, diff_var = _clean_calculus_input(expr_str)
        if diff_var:
            return diff_var
        expr = _parse_input(clean_str)
        return str(_get_variable(expr, default=default).name)
    except Exception:
        return default


def integrate(expr_str: str, var: str | sp.Symbol | None = None) -> dict[str, Any]:
    try:
        clean_str, diff_var = _clean_calculus_input(expr_str)
        expr = _parse_input(clean_str)
        if var is None:
            if diff_var is not None:
                var_sym = sp.Symbol(diff_var)
            else:
                var_sym = _get_variable(expr)
        elif isinstance(var, str):
            var_sym = sp.Symbol(var)
        else:
            var_sym = var

        result = sp.integrate(expr, var_sym)
        v_lat = sp.latex(var_sym)

        steps: list[str] = [
            f"กำหนดโจทย์ปริพันธ์ไม่จำกัดเขต: \\int \\left({sp.latex(expr)}\\right) \\, d{v_lat}"
        ]

        if not expr.has(var_sym):
            steps.append(
                f"ใช้กฎปริพันธ์ของค่าคงที่: \\int c \\, d{v_lat} = c {v_lat} + C \\implies \\int {sp.latex(expr)} \\, d{v_lat} = {sp.latex(result)} + C"
            )
        elif expr == var_sym:
            steps.append(
                f"ใช้กฎกำลัง (Power Rule): \\int {v_lat}^n \\, d{v_lat} = \\frac{{{v_lat}^{{n+1}}}}{{n+1}} + C \\quad (n \\neq -1)"
            )
            steps.append(
                f"แทนค่าเลขชี้กำลัง $n = 1$: \\int {v_lat} \\, d{v_lat} = \\frac{{{v_lat}^{{1+1}}}}{{1+1}} + C = \\frac{{{v_lat}^2}}{{2}} + C"
            )
        elif isinstance(expr, sp.Pow) and expr.args[0] == var_sym and expr.args[1].is_number:
            n = expr.args[1]
            if n == -1:
                steps.append(
                    f"ใช้กฎปริพันธ์ฟังก์ชันส่วนกลับ: \\int \\frac{{1}}{{{v_lat}}} \\, d{v_lat} = \\ln|{v_lat}| + C"
                )
            else:
                steps.append(
                    f"ใช้กฎกำลัง (Power Rule): \\int {v_lat}^n \\, d{v_lat} = \\frac{{{v_lat}^{{n+1}}}}{{n+1}} + C \\quad (n \\neq -1)"
                )
                steps.append(
                    f"แทนค่า $n = {sp.latex(n)}$: \\int {v_lat}^{{{sp.latex(n)}}} \\, d{v_lat} = \\frac{{{v_lat}^{{{sp.latex(n+1)}}}}}{{{sp.latex(n+1)}}} + C = {sp.latex(result)} + C"
                )
        elif isinstance(expr, sp.Add):
            terms = expr.as_ordered_terms()
            terms_integrals = " + ".join(f"\\int \\left({sp.latex(term)}\\right) \\, d{v_lat}" for term in terms)
            steps.append(
                f"ใช้สมบัติเชิงเส้นของการอินทิเกรต (แยกพจน์): \\int \\left({sp.latex(expr)}\\right) \\, d{v_lat} = {terms_integrals}"
            )
            sub_results = []
            for term in terms:
                sub_res = sp.integrate(term, var_sym)
                sub_results.append(f"\\int \\left({sp.latex(term)}\\right) \\, d{v_lat} = {sp.latex(sub_res)}")
            steps.append(
                "อินทิเกรตทีละพจน์: " + ", \\quad ".join(sub_results)
            )
            steps.append(
                f"รวมผลลัพธ์ทุกพจน์และบวกค่าคงที่ของการอินทิเกรต C: \\int \\left({sp.latex(expr)}\\right) \\, d{v_lat} = {sp.latex(result)} + C"
            )
        elif isinstance(expr, sp.sin) and expr.args[0] == var_sym:
            steps.append(
                f"ใช้สูตรปริพันธ์ฟังก์ชันไซน์: \\int \\sin({v_lat}) \\, d{v_lat} = -\\cos({v_lat}) + C"
            )
        elif isinstance(expr, sp.cos) and expr.args[0] == var_sym:
            steps.append(
                f"ใช้สูตรปริพันธ์ฟังก์ชันโคไซน์: \\int \\cos({v_lat}) \\, d{v_lat} = \\sin({v_lat}) + C"
            )
        elif isinstance(expr, sp.exp) and expr.args[0] == var_sym:
            steps.append(
                f"ใช้สูตรปริพันธ์ฟังก์ชันเอกซ์โพเนนเชียล: \\int e^{{{v_lat}}} \\, d{v_lat} = e^{{{v_lat}}} + C"
            )
        elif expr == 1 / var_sym:
            steps.append(
                f"ใช้กฎปริพันธ์ฟังก์ชันส่วนกลับ: \\int \\frac{{1}}{{{v_lat}}} \\, d{v_lat} = \\ln|{v_lat}| + C"
            )
        else:
            u_cand = None
            for node in expr.atoms(sp.Pow):
                if node.base != var_sym and node.base.has(var_sym) and not node.base.is_number:
                    u_cand = node.base
                    break
            if u_cand is None:
                for node in expr.atoms(sp.exp):
                    if node.args[0] != var_sym and node.args[0].has(var_sym):
                        u_cand = node.args[0]
                        break

            if u_cand is not None:
                du = sp.diff(u_cand, var_sym)
                sub_var_name = "w" if var_sym.name == "u" else "u"
                steps.append(
                    f"พิจารณาการเปลี่ยนตัวแปร ({sub_var_name}-Substitution): {sub_var_name} = {sp.latex(u_cand)} \\implies d{sub_var_name} = {sp.latex(du)} \\, d{v_lat}"
                )
                steps.append(
                    f"คำนวณปริพันธ์ผลลัพธ์: \\int \\left({sp.latex(expr)}\\right) \\, d{v_lat} = {sp.latex(result)} + C"
                )
            else:
                steps.append(
                    f"คำนวณปริพันธ์เชิงสัญลักษณ์: \\int \\left({sp.latex(expr)}\\right) \\, d{v_lat} = {sp.latex(result)} + C"
                )

        latex_str = f"\\int \\left({sp.latex(expr)}\\right) \\, d{v_lat} = {sp.latex(result)} + C"
        return {
            "ok": True,
            "result": result,
            "latex": latex_str,
            "steps": steps,
            "error": None,
            "variable": str(var_sym.name),
        }
    except Exception:
        return {
            "ok": False,
            "result": None,
            "latex": "",
            "steps": [],
            "error": "ไม่สามารถอ่านนิพจน์ได้ กรุณาตรวจสอบรูปแบบ เช่น x**2, sin(x), (x**2-4)/(x-2)",
            "variable": "x",
        }


def differentiate(expr_str: str, var: str | sp.Symbol | None = None) -> dict[str, Any]:
    try:
        clean_str, diff_var = _clean_calculus_input(expr_str)
        expr = _parse_input(clean_str)
        if var is None:
            if diff_var is not None:
                var_sym = sp.Symbol(diff_var)
            else:
                var_sym = _get_variable(expr)
        elif isinstance(var, str):
            var_sym = sp.Symbol(var)
        else:
            var_sym = var

        result = sp.diff(expr, var_sym)
        v_lat = sp.latex(var_sym)

        steps: list[str] = [
            f"กำหนดฟังก์ชันที่ต้องการหาอนุพันธ์: f({v_lat}) = {sp.latex(expr)}"
        ]

        if not expr.has(var_sym):
            steps.append(
                f"ใช้กฎอนุพันธ์ของค่าคงที่: \\frac{{d}}{{d{v_lat}}}[c] = 0 \\implies \\frac{{d}}{{d{v_lat}}}\\left[{sp.latex(expr)}\\right] = 0"
            )
        elif expr == var_sym:
            steps.append(
                f"ใช้กฎอนุพันธ์ของตัวแปร {v_lat}: \\frac{{d}}{{d{v_lat}}}[{v_lat}] = 1"
            )
        elif isinstance(expr, sp.Pow) and expr.args[0] == var_sym and expr.args[1].is_number:
            n = expr.args[1]
            steps.append(
                f"ใช้กฎกำลัง (Power Rule): \\frac{{d}}{{d{v_lat}}}[{v_lat}^n] = n {v_lat}^{{n-1}}"
            )
            steps.append(
                f"แทนค่าเลขชี้กำลัง $n = {sp.latex(n)}$: \\frac{{d}}{{d{v_lat}}}\\left[{sp.latex(expr)}\\right] = {sp.latex(n)} {v_lat}^{{{sp.latex(n-1)}}} = {sp.latex(result)}"
            )
        elif isinstance(expr, sp.Add):
            terms = expr.as_ordered_terms()
            diff_terms_str = " + ".join(f"\\frac{{d}}{{d{v_lat}}}\\left[{sp.latex(term)}\\right]" for term in terms)
            steps.append(
                f"ใช้กฎผลบวกและผลต่างของอนุพันธ์ (แยกหาทีละพจน์): \\frac{{d}}{{d{v_lat}}}\\left[{sp.latex(expr)}\\right] = {diff_terms_str}"
            )
            sub_results = []
            for term in terms:
                sub_res = sp.diff(term, var_sym)
                sub_results.append(f"\\frac{{d}}{{d{v_lat}}}\\left[{sp.latex(term)}\\right] = {sp.latex(sub_res)}")
            steps.append(
                "หาอนุพันธ์ของแต่ละพจน์: " + ", \\quad ".join(sub_results)
            )
            steps.append(
                f"รวมผลลัพธ์อนุพันธ์: \\frac{{d}}{{d{v_lat}}}\\left[{sp.latex(expr)}\\right] = {sp.latex(result)}"
            )
        elif isinstance(expr, sp.Mul):
            var_factors = [f for f in expr.args if f.has(var_sym)]
            if len(var_factors) == 2:
                u, v = var_factors[0], var_factors[1]
                steps.append(
                    f"ใช้กฎผลคูณของอนุพันธ์ (Product Rule): \\frac{{d}}{{d{v_lat}}}[u \\cdot v] = u \\frac{{dv}}{{d{v_lat}}} + v \\frac{{du}}{{d{v_lat}}}"
                )
                steps.append(
                    f"กำหนด $u = {sp.latex(u)}$ และ $v = {sp.latex(v)}$: \\frac{{du}}{{d{v_lat}}} = {sp.latex(sp.diff(u, var_sym))}, \\quad \\frac{{dv}}{{d{v_lat}}} = {sp.latex(sp.diff(v, var_sym))}"
                )
                steps.append(
                    f"แทนค่าและจัดรูปอนุพันธ์: \\frac{{d}}{{d{v_lat}}}\\left[{sp.latex(expr)}\\right] = {sp.latex(result)}"
                )
            else:
                steps.append(
                    f"คำนวณอนุพันธ์เชิงสัญลักษณ์: \\frac{{d}}{{d{v_lat}}}\\left[{sp.latex(expr)}\\right] = {sp.latex(result)}"
                )
        elif isinstance(expr, sp.sin) and expr.args[0] == var_sym:
            steps.append(f"ใช้สูตรอนุพันธ์ของฟังก์ชันไซน์: \\frac{{d}}{{d{v_lat}}}[\\sin({v_lat})] = \\cos({v_lat})")
        elif isinstance(expr, sp.cos) and expr.args[0] == var_sym:
            steps.append(f"ใช้สูตรอนุพันธ์ของฟังก์ชันโคไซน์: \\frac{{d}}{{d{v_lat}}}[\\cos({v_lat})] = -\\sin({v_lat})")
        elif isinstance(expr, sp.tan) and expr.args[0] == var_sym:
            steps.append(f"ใช้สูตรอนุพันธ์ของฟังก์ชันแทนเจนต์: \\frac{{d}}{{d{v_lat}}}[\\tan({v_lat})] = \\sec^2({v_lat})")
        elif isinstance(expr, sp.exp) and expr.args[0] == var_sym:
            steps.append(f"ใช้สูตรอนุพันธ์ของฟังก์ชันเอกซ์โพเนนเชียล: \\frac{{d}}{{d{v_lat}}}[e^{{{v_lat}}}] = e^{{{v_lat}}}")
        elif isinstance(expr, sp.log) and expr.args[0] == var_sym:
            steps.append(f"ใช้สูตรอนุพันธ์ของฟังก์ชันลอการิทึมธรรมชาติ: \\frac{{d}}{{d{v_lat}}}[\\ln({v_lat})] = \\frac{{1}}{{{v_lat}}}")
        else:
            steps.append(
                f"คำนวณอนุพันธ์เชิงสัญลักษณ์: \\frac{{d}}{{d{v_lat}}}\\left[{sp.latex(expr)}\\right] = {sp.latex(result)}"
            )

        latex_str = f"\\frac{{d}}{{d{v_lat}}}\\left[{sp.latex(expr)}\\right] = {sp.latex(result)}"
        return {
            "ok": True,
            "result": result,
            "latex": latex_str,
            "steps": steps,
            "error": None,
            "variable": str(var_sym.name),
        }
    except Exception:
        return {
            "ok": False,
            "result": None,
            "latex": "",
            "steps": [],
            "error": "ไม่สามารถอ่านนิพจน์ได้ กรุณาตรวจสอบรูปแบบ เช่น x**2, sin(x), (x**2-4)/(x-2)",
            "variable": "x",
        }


def _classify_limit(left: sp.Expr, right: sp.Expr) -> str:
    if isinstance(left, AccumulationBounds) or isinstance(right, AccumulationBounds):
        return "dne"
    if getattr(left, "is_extended_real", None) is not True or getattr(right, "is_extended_real", None) is not True:
        return "unsupported"
    if left == right:
        return "infinite" if left in (sp.oo, -sp.oo) else "finite"
    if getattr(left, "is_number", False) is True and getattr(right, "is_number", False) is True:
        return "dne"
    return "unsupported"


def _format_point_str(pt: float | int) -> str:
    f_pt = float(pt)
    if abs(f_pt - round(f_pt)) < 1e-6:
        return str(int(round(f_pt)))
    return f"{f_pt:g}"


def _format_samples(pt: float | int) -> tuple[str, str]:
    f_pt = float(pt)
    if abs(f_pt - round(f_pt)) < 1e-6:
        a_int = int(round(f_pt))
        s_left = f"{a_int - 0.1:g}, {a_int - 0.01:g}, {a_int - 0.001:g}"
        s_right = f"{a_int + 0.1:g}, {a_int + 0.01:g}, {a_int + 0.001:g}"
    else:
        s_left = f"{f_pt - 0.1:g}, {f_pt - 0.01:g}, {f_pt - 0.001:g}"
        s_right = f"{f_pt + 0.1:g}, {f_pt + 0.01:g}, {f_pt + 0.001:g}"
    return s_left, s_right


def compute_limit(expr_str: str, point: float | int = 0, var: str | sp.Symbol | None = None) -> dict[str, Any]:
    try:
        clean_str, diff_var = _clean_calculus_input(expr_str)
        expr = _parse_input(clean_str)
        if var is None:
            if diff_var is not None:
                var_sym = sp.Symbol(diff_var)
            else:
                var_sym = _get_variable(expr)
        elif isinstance(var, str):
            var_sym = sp.Symbol(var)
        else:
            var_sym = var

        try:
            left = sp.limit(expr, var_sym, point, dir="-")
            right = sp.limit(expr, var_sym, point, dir="+")
            status = _classify_limit(left, right)
        except Exception:
            left, right = None, None
            status = "unsupported"

        pt_str = _format_point_str(point)
        s_left_ex, s_right_ex = _format_samples(point)
        v_lat = sp.latex(var_sym)

        steps = [
            f"กำหนดโจทย์ลิมิตที่ต้องการหา: ศึกษาพฤติกรรมของค่าฟังก์ชันเมื่อตัวแปร ${v_lat}$ ขยับเข้าใกล้จุด ${v_lat} = {pt_str}$ (โดยที่ ${v_lat} \\neq {pt_str}$)\n\\lim_{{{v_lat} \\to {pt_str}}} \\left({sp.latex(expr)}\\right)"
        ]

        if status == "finite":
            result = sp.limit(expr, var_sym, point)
            res_latex = sp.latex(result)
            latex_str = f"\\lim_{{{v_lat} \\to {pt_str}}} \\left({sp.latex(expr)}\\right) = {res_latex}"

            try:
                direct_val = expr.subs(var_sym, point)
                if direct_val.is_number and direct_val.is_finite:
                    steps.append(
                        f"ทดสอบแทนค่าโดยตรง (Direct Substitution): ฟังก์ชันต่อเนื่องที่จุดนี้ สามารถแทนค่าได้ทันที\nf({pt_str}) = {sp.latex(direct_val)}"
                    )
                else:
                    steps.append(
                        f"พิจารณาลิมิตทางซ้าย (Left-hand limit): สัญลักษณ์ ${v_lat} \\to {pt_str}^-$ หมายถึงให้ค่า ${v_lat}$ ค่อย ๆ ขยับเข้าใกล้ {pt_str} จากฝั่งซ้ายของเส้นจำนวน (ค่าน้อยกว่า {pt_str} เสมอ หรือ ${v_lat} < {pt_str}$ เช่น ${v_lat} = {s_left_ex} \\dots$)\nเมื่อ ${v_lat}$ วิ่งเฉียดเข้าหา {pt_str} ทางซ้าย ค่าของฟังก์ชันมีแนวโน้มลู่เข้าหา {sp.latex(left)}\n\\lim_{{{v_lat} \\to {pt_str}^-}} \\left({sp.latex(expr)}\\right) = {sp.latex(left)}"
                    )
                    steps.append(
                        f"พิจารณาลิมิตทางขวา (Right-hand limit): สัญลักษณ์ ${v_lat} \\to {pt_str}^+$ หมายถึงให้ค่า ${v_lat}$ ค่อย ๆ ขยับเข้าใกล้ {pt_str} จากฝั่งขวาบนเส้นจำนวน (ค่ามากกว่า {pt_str} เสมอ หรือ ${v_lat} > {pt_str}$ เช่น ${v_lat} = {s_right_ex} \\dots$)\nเมื่อ ${v_lat}$ วิ่งเฉียดเข้าหา {pt_str} ทางขวา ค่าของฟังก์ชันมีแนวโน้มลู่เข้าหา {sp.latex(right)}\n\\lim_{{{v_lat} \\to {pt_str}^+}} \\left({sp.latex(expr)}\\right) = {sp.latex(right)}"
                    )
            except Exception:
                steps.append(
                    f"พิจารณาลิมิตทางซ้าย (Left-hand limit): สัญลักษณ์ ${v_lat} \\to {pt_str}^-$ หมายถึงให้ค่า ${v_lat}$ ค่อย ๆ ขยับเข้าใกล้ {pt_str} จากฝั่งซ้ายของเส้นจำนวน (ค่าน้อยกว่า {pt_str} เสมอ หรือ ${v_lat} < {pt_str}$ เช่น ${v_lat} = {s_left_ex} \\dots$)\n\\lim_{{{v_lat} \\to {pt_str}^-}} \\left({sp.latex(expr)}\\right) = {sp.latex(left)}"
                )
                steps.append(
                    f"พิจารณาลิมิตทางขวา (Right-hand limit): สัญลักษณ์ ${v_lat} \\to {pt_str}^+$ หมายถึงให้ค่า ${v_lat}$ ค่อย ๆ ขยับเข้าใกล้ {pt_str} จากฝั่งขวาบนเส้นจำนวน (ค่ามากกว่า {pt_str} เสมอ หรือ ${v_lat} > {pt_str}$ เช่น ${v_lat} = {s_right_ex} \\dots$)\n\\lim_{{{v_lat} \\to {pt_str}^+}} \\left({sp.latex(expr)}\\right) = {sp.latex(right)}"
                )

            steps.append(
                f"สรุปค่าลิมิตสองด้าน: กฎพื้นฐานคือ ลิมิตสองด้านจะมีค่าได้ก็ต่อเมื่อ ลิมิตซ้ายและขวาต้องมุ่งสู่จำนวนจริงเดียวกัน\nเนื่องจากเส้นกราฟจากทั้งสองฝั่งวิ่งมาบรรจบกันที่ระดับความสูงเดียวกัน (${res_latex}$)\n\\lim_{{{v_lat} \\to {pt_str}^-}} f({v_lat}) = \\lim_{{{v_lat} \\to {pt_str}^+}} f({v_lat}) = {res_latex} \\implies \\lim_{{{v_lat} \\to {pt_str}}} \\left({sp.latex(expr)}\\right) = {res_latex}"
            )

        elif status == "infinite":
            result = left
            res_latex = sp.latex(result)
            latex_str = f"\\lim_{{{v_lat} \\to {pt_str}}} \\left({sp.latex(expr)}\\right) = {res_latex}"
            steps.append(
                f"พิจารณาลิมิตทางซ้าย (Left-hand limit): สัญลักษณ์ ${v_lat} \\to {pt_str}^-$ หมายถึงให้ค่า ${v_lat}$ ขยับเข้าใกล้ {pt_str} จากฝั่งซ้าย (${v_lat} < {pt_str}$ เช่น ${v_lat} = {s_left_ex} \\dots$)\n\\lim_{{{v_lat} \\to {pt_str}^-}} \\left({sp.latex(expr)}\\right) = {sp.latex(left)}"
            )
            steps.append(
                f"พิจารณาลิมิตทางขวา (Right-hand limit): สัญลักษณ์ ${v_lat} \\to {pt_str}^+$ หมายถึงให้ค่า ${v_lat}$ ขยับเข้าใกล้ {pt_str} จากฝั่งขวา (${v_lat} > {pt_str}$ เช่น ${v_lat} = {s_right_ex} \\dots$)\n\\lim_{{{v_lat} \\to {pt_str}^+}} \\left({sp.latex(expr)}\\right) = {sp.latex(right)}"
            )
            steps.append(
                f"สรุปผล (ลิมิตทั้งสองข้างลู่ไปสู่อนันต์เดียวกัน): ทั้งสองฝั่งลู่ไปสู่ค่าเดียวกันคือ ${res_latex}$ แต่เนื่องจากอนันต์ไม่ใช่จำนวนจริงจำกัด จึงถือว่าลิมิตลู่ออก\n\\lim_{{{v_lat} \\to {pt_str}}} \\left({sp.latex(expr)}\\right) = {res_latex}"
            )

        elif status == "dne":
            result = None
            latex_str = f"\\lim_{{{v_lat} \\to {pt_str}}} \\left({sp.latex(expr)}\\right) \\quad \\text{{(does not exist)}}"
            steps.append(
                f"พิจารณาลิมิตทางซ้าย (Left-hand limit): สัญลักษณ์ ${v_lat} \\to {pt_str}^-$ หมายถึงให้ค่า ${v_lat}$ ขยับเข้าใกล้ {pt_str} จากฝั่งซ้าย (${v_lat} < {pt_str}$ เช่น ${v_lat} = {s_left_ex} \\dots$)\n\\lim_{{{v_lat} \\to {pt_str}^-}} \\left({sp.latex(expr)}\\right) = {sp.latex(left)}"
            )
            steps.append(
                f"พิจารณาลิมิตทางขวา (Right-hand limit): สัญลักษณ์ ${v_lat} \\to {pt_str}^+$ หมายถึงให้ค่า ${v_lat}$ ขยับเข้าใกล้ {pt_str} จากฝั่งขวา (${v_lat} > {pt_str}$ เช่น ${v_lat} = {s_right_ex} \\dots$)\n\\lim_{{{v_lat} \\to {pt_str}^+}} \\left({sp.latex(expr)}\\right) = {sp.latex(right)}"
            )
            steps.append(
                f"สรุปผล (ไม่มีลิมิตสองด้านเนื่องจากลิมิตซ้ายไม่เท่ากับลิมิตขวา): เส้นกราฟจากฝั่งซ้ายและฝั่งขวาแยกออกจากกันและไม่มาบรรจบกันที่จุดเดียวกัน\n\\lim_{{{v_lat} \\to {pt_str}^-}} f({v_lat}) = {sp.latex(left)} \\neq \\lim_{{{v_lat} \\to {pt_str}^+}} f({v_lat}) = {sp.latex(right)}\n\\lim_{{{v_lat} \\to {pt_str}}} \\left({sp.latex(expr)}\\right) \\quad \\text{{(does not exist)}}"
            )

        else:
            result = None
            latex_str = f"\\lim_{{{v_lat} \\to {point}}} \\left({sp.latex(expr)}\\right) \\quad \\text{{(unsupported)}}"
            steps.append(
                f"ระบบไม่สามารถตัดสินหรือระบุค่าลิมิตได้: \\lim_{{{v_lat} \\to {point}}} \\left({sp.latex(expr)}\\right) \\quad \\text{{(unsupported)}}"
            )

        return {
            "ok": True,
            "result": result,
            "latex": latex_str,
            "steps": steps,
            "error": None,
            "status": status,
            "left_limit": left,
            "right_limit": right,
            "variable": str(var_sym.name),
        }
    except Exception:
        return {
            "ok": False,
            "result": None,
            "latex": "",
            "steps": [],
            "error": "ไม่สามารถอ่านนิพจน์ได้ กรุณาตรวจสอบรูปแบบ เช่น x**2, sin(x), (x**2-4)/(x-2)",
            "status": "error",
            "left_limit": None,
            "right_limit": None,
            "variable": "x",
        }
