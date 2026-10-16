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
            f"กำหนดโจทย์ปริพันธ์ไม่จำกัดเขต (Indefinite Integral): "
            f"หาปฏิยานุพันธ์ของฟังก์ชันเทียบกับตัวแปร ${v_lat}$:\n"
            f"\\int \\left({sp.latex(expr)}\\right) \\, d{v_lat}"
        ]

        if not expr.has(var_sym):
            steps.append(
                f"ดึงค่าคงที่ออกจากเครื่องหมายปริพันธ์: "
                f"ตามสมบัติ $\\int c \\, d{v_lat} = c \\int 1 \\, d{v_lat}$:\n"
                f"\\int {sp.latex(expr)} \\, d{v_lat} = {sp.latex(expr)} \\int 1 \\, d{v_lat}"
            )
            steps.append(
                f"คำนวณปริพันธ์ของ 1: "
                f"ปฏิยานุพันธ์ของ 1 เทียบกับ ${v_lat}$ คือ ${v_lat}$:\n"
                f"\\int 1 \\, d{v_lat} = {v_lat} + C"
            )
            steps.append(
                f"สรุปผลลัพธ์ปริพันธ์: "
                f"นำค่าคงที่คูณกลับและใส่ค่าคงที่ของการอินทิเกรต $C$:\n"
                f"\\int {sp.latex(expr)} \\, d{v_lat} = {sp.latex(result)} + C"
            )
            steps.append(
                f"ตรวจสอบความถูกต้องโดยการหาอนุพันธ์กลับ: "
                f"อนุพันธ์ของคำตอบต้องเท่ากับตัวถูกอินทิเกรตเดิม:\n"
                f"\\frac{{d}}{{d{v_lat}}}\\left[{sp.latex(result)} + C\\right] = {sp.latex(expr)}"
            )
        elif expr == var_sym:
            steps.append(
                f"ระบุกฎเลขชี้กำลัง (Power Rule): "
                f"สำหรับพจน์ยกกำลังหนึ่ง $n = 1$:\n"
                f"\\int {v_lat}^n \\, d{v_lat} = \\frac{{{v_lat}^{{n+1}}}}{{n+1}} + C \\quad (n \\neq -1)"
            )
            steps.append(
                f"แทนค่าเลขชี้กำลัง n = 1: "
                f"เพิ่มเลขชี้กำลังขึ้น 1 และหารด้วยเลขชี้กำลังใหม่:\n"
                f"\\int {v_lat} \\, d{v_lat} = \\frac{{{v_lat}^{{1+1}}}}{{1+1}} + C = \\frac{{{v_lat}^2}}{{2}} + C"
            )
            steps.append(
                f"ตรวจสอบความถูกต้องโดยการหาอนุพันธ์กลับ: "
                f"ดิฟคำตอบกลับเพื่อยืนยันความถูกต้อง:\n"
                f"\\frac{{d}}{{d{v_lat}}}\\left[\\frac{{{v_lat}^2}}{{2}} + C\\right] = \\frac{{2{v_lat}}}{{2}} = {v_lat}"
            )
        elif isinstance(expr, sp.Pow) and expr.args[0] == var_sym and expr.args[1].is_number:
            n = expr.args[1]
            if n == -1:
                steps.append(
                    f"ใช้กฎปริพันธ์ฟังก์ชันส่วนกลับ: "
                    f"เมื่อ $n = -1$ สูตร $\\frac{{{v_lat}^{{n+1}}}}{{n+1}}$ ส่วนจะเป็นศูนย์ จึงใช้นิยามลอการิทึมธรรมชาติ:\n"
                    f"\\int \\frac{{1}}{{{v_lat}}} \\, d{v_lat} = \\ln|{v_lat}| + C \\quad ({v_lat} \\neq 0)"
                )
                steps.append(
                    f"ตรวจสอบความถูกต้องโดยการหาอนุพันธ์กลับ: "
                    f"อนุพันธ์ของ $\\ln|{v_lat}|$ คือ $\\frac{{1}}{{{v_lat}}}$:\n"
                    f"\\frac{{d}}{{d{v_lat}}}[\\ln|{v_lat}| + C] = \\frac{{1}}{{{v_lat}}}"
                )
            else:
                steps.append(
                    f"ระบุกฎเลขชี้กำลัง (Power Rule): "
                    f"สูตรอินทิเกรตฟังก์ชันพหุนามและเลขยกกำลัง:\n"
                    f"\\int {v_lat}^n \\, d{v_lat} = \\frac{{{v_lat}^{{n+1}}}}{{n+1}} + C \\quad (n \\neq -1)"
                )
                steps.append(
                    f"แทนค่าเลขชี้กำลัง $n = {sp.latex(n)}$: "
                    f"คำนวณเลขชี้กำลังใหม่ $n + 1 = {sp.latex(n+1)}$:\n"
                    f"\\int {v_lat}^{{{sp.latex(n)}}} \\, d{v_lat} = \\frac{{{v_lat}^{{{sp.latex(n+1)}}}}}{{{sp.latex(n+1)}}} + C"
                )
                steps.append(
                    f"จัดรูปผลสำเร็จและใส่ค่าคงที่ C: "
                    f"สมการปริพันธ์ในรูปชัดแจ้ง:\n"
                    f"\\int {v_lat}^{{{sp.latex(n)}}} \\, d{v_lat} = {sp.latex(result)} + C"
                )
                steps.append(
                    f"ตรวจสอบความถูกต้องโดยการหาอนุพันธ์กลับ: "
                    f"ทดสอบดิฟผลลัพธ์กลับ:\n"
                    f"\\frac{{d}}{{d{v_lat}}}\\left[{sp.latex(result)} + C\\right] = {sp.latex(expr)}"
                )
        elif isinstance(expr, sp.Add):
            terms = expr.as_ordered_terms()
            terms_integrals = " + ".join(f"\\int \\left({sp.latex(term)}\\right) \\, d{v_lat}" for term in terms)
            steps.append(
                f"ใช้สมบัติเชิงเส้นของการอินทิเกรต (Linearity Property): "
                f"สามารถแยกอินทิเกรตทีละพจน์บวก-ลบได้อิสระ:\n"
                f"\\int \\left({sp.latex(expr)}\\right) \\, d{v_lat} = {terms_integrals}"
            )
            sub_results = []
            for term in terms:
                sub_res = sp.integrate(term, var_sym)
                sub_results.append(f"\\int \\left({sp.latex(term)}\\right) \\, d{v_lat} = {sp.latex(sub_res)}")
            steps.append(
                f"คำนวณอินทิเกรตทีละพจน์: "
                f"หาปฏิยานุพันธ์ของแต่ละส่วนประกอบย่อย:\n"
                + "\n".join(sub_results)
            )
            steps.append(
                f"รวมผลลัพธ์ทุกพจน์และบวกค่าคงที่ C: "
                f"รวมผลการอินทิเกรตทั้งหมดเข้าด้วยกัน:\n"
                f"\\int \\left({sp.latex(expr)}\\right) \\, d{v_lat} = {sp.latex(result)} + C"
            )
            steps.append(
                f"ตรวจสอบความถูกต้องโดยการหาอนุพันธ์กลับ: "
                f"หาอนุพันธ์ของผลรวมกลับคืน:\n"
                f"\\frac{{d}}{{d{v_lat}}}\\left[{sp.latex(result)} + C\\right] = {sp.latex(expr)}"
            )
        elif isinstance(expr, sp.sin) and expr.args[0] == var_sym:
            steps.append(
                f"ใช้สูตรปริพันธ์ฟังก์ชันไซน์: "
                f"เนื่องจาก $\\frac{{d}}{{d{v_lat}}}[\\cos({v_lat})] = -\\sin({v_lat})$:\n"
                f"\\int \\sin({v_lat}) \\, d{v_lat} = -\\cos({v_lat}) + C"
            )
            steps.append(
                f"ตรวจสอบความถูกต้องโดยการหาอนุพันธ์กลับ: "
                f"\\frac{{d}}{{d{v_lat}}}[-\\cos({v_lat}) + C] = -(-\\sin({v_lat})) = \\sin({v_lat})"
            )
        elif isinstance(expr, sp.cos) and expr.args[0] == var_sym:
            steps.append(
                f"ใช้สูตรปริพันธ์ฟังก์ชันโคไซน์: "
                f"เนื่องจาก $\\frac{{d}}{{d{v_lat}}}[\\sin({v_lat})] = \\cos({v_lat})$:\n"
                f"\\int \\cos({v_lat}) \\, d{v_lat} = \\sin({v_lat}) + C"
            )
            steps.append(
                f"ตรวจสอบความถูกต้องโดยการหาอนุพันธ์กลับ: "
                f"\\frac{{d}}{{d{v_lat}}}[\\sin({v_lat}) + C] = \\cos({v_lat})"
            )
        elif isinstance(expr, sp.exp) and expr.args[0] == var_sym:
            steps.append(
                f"ใช้สูตรปริพันธ์ฟังก์ชันเอกซ์โพเนนเชียลธรรมชาติ: "
                f"ฟังก์ชัน $e^{{{v_lat}}}$ มีอัตราการเปลี่ยนแปลงเท่ากับตัวเองเสมอ:\n"
                f"\\int e^{{{v_lat}}} \\, d{v_lat} = e^{{{v_lat}}} + C"
            )
            steps.append(
                f"ตรวจสอบความถูกต้องโดยการหาอนุพันธ์กลับ: "
                f"\\frac{{d}}{{d{v_lat}}}[e^{{{v_lat}}} + C] = e^{{{v_lat}}}"
            )
        elif expr == 1 / var_sym:
            steps.append(
                f"ใช้กฎปริพันธ์ฟังก์ชันส่วนกลับ: "
                f"\\int \\frac{{1}}{{{v_lat}}} \\, d{v_lat} = \\ln|{v_lat}| + C \\quad ({v_lat} \\neq 0)"
            )
            steps.append(
                f"ตรวจสอบความถูกต้องโดยการหาอนุพันธ์กลับ: "
                f"\\frac{{d}}{{d{v_lat}}}[\\ln|{v_lat}| + C] = \\frac{{1}}{{{v_lat}}}"
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
                    f"วิเคราะห์การเปลี่ยนตัวแปร ({sub_var_name}-Substitution): "
                    f"กำหนดฟังก์ชันก้อนในเป็นตัวแปรใหม่:\n"
                    f"{sub_var_name} = {sp.latex(u_cand)}"
                )
                steps.append(
                    f"หาผลต่างสืบเนื่อง d{sub_var_name}: "
                    f"หาอนุพันธ์เทียบกับตัวแปร ${v_lat}$:\n"
                    f"\\frac{{d{sub_var_name}}}{{d{v_lat}}} = {sp.latex(du)} \\implies d{sub_var_name} = {sp.latex(du)} \\, d{v_lat}"
                )
                steps.append(
                    f"คำนวณปริพันธ์และแทนค่ากลับ: "
                    f"แทนค่า ${sub_var_name}$ กลับคืนสู่ตัวแปรเดิม:\n"
                    f"\\int \\left({sp.latex(expr)}\\right) \\, d{v_lat} = {sp.latex(result)} + C"
                )
                steps.append(
                    f"ตรวจสอบความถูกต้องโดยการหาอนุพันธ์กลับ: "
                    f"\\frac{{d}}{{d{v_lat}}}\\left[{sp.latex(result)} + C\\right] = {sp.latex(expr)}"
                )
            else:
                steps.append(
                    f"คำนวณปริพันธ์เชิงสัญลักษณ์: "
                    f"ใช้วิธีการวิเคราะห์ทางแคลคูลัสเชิงสัญลักษณ์:\n"
                    f"\\int \\left({sp.latex(expr)}\\right) \\, d{v_lat} = {sp.latex(result)} + C"
                )
                steps.append(
                    f"ตรวจสอบความถูกต้องโดยการหาอนุพันธ์กลับ: "
                    f"\\frac{{d}}{{d{v_lat}}}\\left[{sp.latex(result)} + C\\right] = {sp.latex(expr)}"
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
            f"กำหนดฟังก์ชันที่ต้องการหาอนุพันธ์: "
            f"คำนวณอัตราการเปลี่ยนแปลงของฟังก์ชันเทียบกับตัวแปร ${v_lat}$:\n"
            f"f({v_lat}) = {sp.latex(expr)}"
        ]

        if not expr.has(var_sym):
            steps.append(
                f"ใช้กฎอนุพันธ์ของค่าคงที่ (Constant Rule): "
                f"ค่าคงที่ไม่ขึ้นกับตัวแปร ${v_lat}$ จึงไม่มีการเปลี่ยนแปลง:\n"
                f"\\frac{{d}}{{d{v_lat}}}[c] = 0 \\implies \\frac{{d}}{{d{v_lat}}}\\left[{sp.latex(expr)}\\right] = 0"
            )
            steps.append(
                f"ความหมายทางเรขาคณิต: "
                f"กราฟของฟังก์ชันคงที่เป็นเส้นตรงแนวนอนขนานแกน ${v_lat}$ จึงมีความชัน $m = 0$ ทุกจุด"
            )
        elif expr == var_sym:
            steps.append(
                f"ใช้กฎอนุพันธ์ของตัวแปรอิสระ: "
                f"อัตราการเปลี่ยนแปลงของตัวแปรเทียบกับตัวเองมีค่าเท่ากับ 1 เสมอ:\n"
                f"\\frac{{d}}{{d{v_lat}}}[{v_lat}] = 1"
            )
            steps.append(
                f"ความหมายทางเรขาคณิต: "
                f"กราฟเป็นเส้นตรง $y = {v_lat}$ มีความชัน $m = 1$ คงที่สม่ำเสมอ"
            )
        elif isinstance(expr, sp.Pow) and expr.args[0] == var_sym and expr.args[1].is_number:
            n = expr.args[1]
            steps.append(
                f"ใช้กฎเลขชี้กำลัง (Power Rule): "
                f"นำเลขชี้กำลังมาคูณข้างหน้าแล้วลดเลขชี้กำลังลง 1:\n"
                f"\\frac{{d}}{{d{v_lat}}}[{v_lat}^n] = n {v_lat}^{{n-1}}"
            )
            steps.append(
                f"แทนค่าเลขชี้กำลัง $n = {sp.latex(n)}$: "
                f"คำนวณ $n - 1 = {sp.latex(n-1)}$:\n"
                f"\\frac{{d}}{{d{v_lat}}}\\left[{sp.latex(expr)}\\right] = {sp.latex(n)} {v_lat}^{{{sp.latex(n-1)}}} = {sp.latex(result)}"
            )
            steps.append(
                f"ความหมายทางเรขาคณิต: "
                f"สูตรความชันของเส้นสัมผัส ณ พิกัด ${v_lat}$ ใดๆ บนกราฟคือ $m = {sp.latex(result)}$"
            )
        elif isinstance(expr, sp.Add):
            terms = expr.as_ordered_terms()
            diff_terms_str = " + ".join(f"\\frac{{d}}{{d{v_lat}}}\\left[{sp.latex(term)}\\right]" for term in terms)
            steps.append(
                f"ใช้กฎผลบวกและผลต่างของอนุพันธ์ (Sum & Difference Rule): "
                f"สามารถแยกหาอนุพันธ์ของแต่ละพจน์ได้:\n"
                f"\\frac{{d}}{{d{v_lat}}}\\left[{sp.latex(expr)}\\right] = {diff_terms_str}"
            )
            sub_results = []
            for term in terms:
                sub_res = sp.diff(term, var_sym)
                sub_results.append(f"\\frac{{d}}{{d{v_lat}}}\\left[{sp.latex(term)}\\right] = {sp.latex(sub_res)}")
            steps.append(
                f"หาอนุพันธ์ของแต่ละพจน์: "
                f"คำนวณอนุพันธ์ย่อยทีละส่วนประกอบ:\n"
                + "\n".join(sub_results)
            )
            steps.append(
                f"รวมผลลัพธ์ทุกพจน์: "
                f"นำผลอนุพันธ์ของแต่ละพจน์มารวมกัน:\n"
                f"\\frac{{d}}{{d{v_lat}}}\\left[{sp.latex(expr)}\\right] = {sp.latex(result)}"
            )
        numer, denom = expr.as_numer_denom()
        if denom != 1 and denom.has(var_sym) and numer.has(var_sym):
            du = sp.diff(numer, var_sym)
            dv = sp.diff(denom, var_sym)
            u_lat = sp.latex(numer)
            denom_lat = sp.latex(denom)
            du_lat = sp.latex(du)
            dv_lat = sp.latex(dv)
            expr_lat = sp.latex(expr)
            res_lat = sp.latex(result)
            steps.append(
                f"ใช้กฎผลหารของอนุพันธ์ (Quotient Rule): "
                f"สูตรอนุพันธ์ของฟังก์ชันเศษส่วน:\n"
                f"\\frac{{d}}{{d{v_lat}}}\\left[\\frac{{u}}{{v}}\\right] = \\frac{{v \\frac{{du}}{{d{v_lat}}} - u \\frac{{dv}}{{d{v_lat}}}}}{{v^2}}"
            )
            steps.append(
                f"กำหนดตัวเศษ u และตัวส่วน v พร้อมหาอนุพันธ์: "
                f"ตัวเศษ $u = {u_lat} \\implies \\frac{{du}}{{d{v_lat}}} = {du_lat}$\n"
                f"ตัวส่วน $v = {denom_lat} \\implies \\frac{{dv}}{{d{v_lat}}} = {dv_lat}$"
            )
            steps.append(
                f"แทนค่าลงในสูตรผลหาร: "
                f"\\frac{{d}}{{d{v_lat}}}\\left[{expr_lat}\\right] = \\frac{{({denom_lat})({du_lat}) - ({u_lat})({dv_lat})}}{{({denom_lat})^2}}"
            )
            steps.append(
                f"จัดรูปผลสำเร็จ: "
                f"กระจายพจน์ตัวเศษและรวมพจน์ที่คล้ายกัน:\n"
                f"\\frac{{d}}{{d{v_lat}}}\\left[{expr_lat}\\right] = {res_lat}"
            )
        elif expr.func in (sp.sin, sp.cos, sp.tan, sp.exp, sp.log, sp.asin, sp.atan, sp.acos) and expr.args[0] != var_sym and expr.args[0].has(var_sym):
            g = expr.args[0]
            du = sp.diff(g, var_sym)
            u_sym = sp.Symbol("u")
            outer_f = expr.func(u_sym)
            df_du = sp.diff(outer_f, u_sym).subs(u_sym, g)
            g_lat = sp.latex(g)
            du_lat = sp.latex(du)
            df_du_lat = sp.latex(df_du)
            expr_lat = sp.latex(expr)
            res_lat = sp.latex(result)
            steps.append(
                f"ใช้กฎลูกโซ่ (Chain Rule): "
                f"สำหรับฟังก์ชันคอมโพสิต $f(g({v_lat}))$:\n"
                f"\\frac{{d}}{{d{v_lat}}}[f(g({v_lat}))] = f'(g({v_lat})) \\cdot g'({v_lat})"
            )
            steps.append(
                f"กำหนดฟังก์ชันก้อนใน: "
                f"u = g({v_lat}) = {g_lat} \\implies \\frac{{du}}{{d{v_lat}}} = {du_lat}"
            )
            steps.append(
                f"หาอนุพันธ์ของฟังก์ชันภายนอก: "
                f"\\frac{{df}}{{du}} = {sp.latex(sp.diff(outer_f, u_sym))} \\implies f'(g({v_lat})) = {df_du_lat}"
            )
            steps.append(
                f"คูณตามกฎลูกโซ่และจัดรูป: "
                f"\\frac{{d}}{{d{v_lat}}}\\left[{expr_lat}\\right] = f'(g({v_lat})) \\cdot \\frac{{du}}{{d{v_lat}}} = \\left({df_du_lat}\\right) \\cdot \\left({du_lat}\\right) = {res_lat}"
            )
        elif isinstance(expr, sp.Pow) and expr.args[0] != var_sym and expr.args[0].has(var_sym) and expr.args[1].is_number:
            g = expr.args[0]
            n = expr.args[1]
            du = sp.diff(g, var_sym)
            g_lat = sp.latex(g)
            n_lat = sp.latex(n)
            nm1_lat = sp.latex(n - 1)
            du_lat = sp.latex(du)
            expr_lat = sp.latex(expr)
            res_lat = sp.latex(result)
            steps.append(
                f"ใช้กฎกำลังร่วมกับกฎลูกโซ่ (General Power Rule / Chain Rule): "
                f"\\frac{{d}}{{d{v_lat}}}[u^n] = n u^{{n-1}} \\frac{{du}}{{d{v_lat}}}"
            )
            steps.append(
                f"กำหนดฟังก์ชันก้อนใน: "
                f"u = {g_lat} \\implies \\frac{{du}}{{d{v_lat}}} = {du_lat} \\quad (n = {n_lat})"
            )
            steps.append(
                f"แทนค่าและคูณอนุพันธ์ก้อนใน: "
                f"\\frac{{d}}{{d{v_lat}}}\\left[{expr_lat}\\right] = {n_lat} ({g_lat})^{{{nm1_lat}}} \\cdot \\left({du_lat}\\right) = {res_lat}"
            )
        elif isinstance(expr, sp.Mul):
            var_factors = [f for f in expr.args if f.has(var_sym)]
            if len(var_factors) == 2:
                u, v = var_factors[0], var_factors[1]
                steps.append(
                    f"ใช้กฎผลคูณของอนุพันธ์ (Product Rule): "
                    f"\\frac{{d}}{{d{v_lat}}}[u \\cdot v] = u \\frac{{dv}}{{d{v_lat}}} + v \\frac{{du}}{{d{v_lat}}}"
                )
                steps.append(
                    f"กำหนดฟังก์ชันย่อย: "
                    f"u = {sp.latex(u)} \\implies \\frac{{du}}{{d{v_lat}}} = {sp.latex(sp.diff(u, var_sym))}\n"
                    f"v = {sp.latex(v)} \\implies \\frac{{dv}}{{d{v_lat}}} = {sp.latex(sp.diff(v, var_sym))}"
                )
                steps.append(
                    f"แทนค่าในสูตรผลคูณและจัดรูป: "
                    f"\\frac{{d}}{{d{v_lat}}}\\left[{sp.latex(expr)}\\right] = {sp.latex(result)}"
                )
            else:
                steps.append(
                    f"คำนวณอนุพันธ์เชิงสัญลักษณ์: "
                    f"\\frac{{d}}{{d{v_lat}}}\\left[{sp.latex(expr)}\\right] = {sp.latex(result)}"
                )
        elif isinstance(expr, sp.sin) and expr.args[0] == var_sym:
            steps.append(
                f"ใช้สูตรอนุพันธ์ของฟังก์ชันไซน์: "
                f"\\frac{{d}}{{d{v_lat}}}[\\sin({v_lat})] = \\cos({v_lat})"
            )
        elif isinstance(expr, sp.cos) and expr.args[0] == var_sym:
            steps.append(
                f"ใช้สูตรอนุพันธ์ของฟังก์ชันโคไซน์: "
                f"\\frac{{d}}{{d{v_lat}}}[\\cos({v_lat})] = -\\sin({v_lat})"
            )
        elif isinstance(expr, sp.tan) and expr.args[0] == var_sym:
            steps.append(
                f"ใช้สูตรอนุพันธ์ของฟังก์ชันแทนเจนต์: "
                f"\\frac{{d}}{{d{v_lat}}}[\\tan({v_lat})] = \\sec^2({v_lat})"
            )
        elif isinstance(expr, sp.exp) and expr.args[0] == var_sym:
            steps.append(
                f"ใช้สูตรอนุพันธ์ของฟังก์ชันเอกซ์โพเนนเชียล: "
                f"\\frac{{d}}{{d{v_lat}}}[e^{{{v_lat}}}] = e^{{{v_lat}}}"
            )
        elif isinstance(expr, sp.log) and expr.args[0] == var_sym:
            steps.append(
                f"ใช้สูตรอนุพันธ์ของฟังก์ชันลอการิทึมธรรมชาติ: "
                f"\\frac{{d}}{{d{v_lat}}}[\\ln({v_lat})] = \\frac{{1}}{{{v_lat}}} \\quad ({v_lat} > 0)"
            )
        else:
            steps.append(
                f"คำนวณอนุพันธ์เชิงสัญลักษณ์: "
                f"\\frac{{d}}{{d{v_lat}}}\\left[{sp.latex(expr)}\\right] = {sp.latex(result)}"
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
