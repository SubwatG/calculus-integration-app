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


def _parse_input(expr_str: str) -> sp.Expr:
    clean_str = expr_str.strip()
    if not clean_str:
        raise ValueError("Empty input string")
    return parse_expr(clean_str, transformations=TRANSFORMATIONS, local_dict=LOCAL_MATH_DICT)


def integrate(expr_str: str) -> dict[str, Any]:
    x = sp.Symbol("x")
    try:
        expr = _parse_input(expr_str)
        result = sp.integrate(expr, x)

        steps: list[str] = [
            f"กำหนดโจทย์ปริพันธ์ไม่จำกัดเขต: \\int \\left({sp.latex(expr)}\\right) \\, dx"
        ]

        if not expr.has(x):
            steps.append(
                f"ใช้กฎปริพันธ์ของค่าคงที่: \\int c \\, dx = c x + C \\implies \\int {sp.latex(expr)} \\, dx = {sp.latex(result)} + C"
            )
        elif expr == x:
            steps.append(
                "ใช้กฎกำลัง (Power Rule): \\int x^n \\, dx = \\frac{x^{n+1}}{n+1} + C \\quad (n \\neq -1)"
            )
            steps.append(
                "แทนค่าเลขชี้กำลัง $n = 1$: \\int x \\, dx = \\frac{x^{1+1}}{1+1} + C = \\frac{x^2}{2} + C"
            )
        elif isinstance(expr, sp.Pow) and expr.args[0] == x and expr.args[1].is_number:
            n = expr.args[1]
            if n == -1:
                steps.append(
                    "ใช้กฎปริพันธ์ฟังก์ชันส่วนกลับ: \\int \\frac{1}{x} \\, dx = \\ln|x| + C"
                )
            else:
                steps.append(
                    "ใช้กฎกำลัง (Power Rule): \\int x^n \\, dx = \\frac{x^{n+1}}{n+1} + C \\quad (n \\neq -1)"
                )
                steps.append(
                    f"แทนค่า $n = {sp.latex(n)}$: \\int x^{{{sp.latex(n)}}} \\, dx = \\frac{{x^{{{sp.latex(n+1)}}}}}{{{sp.latex(n+1)}}} + C = {sp.latex(result)} + C"
                )
        elif isinstance(expr, sp.Add):
            terms = expr.as_ordered_terms()
            terms_integrals = " + ".join(f"\\int \\left({sp.latex(t)}\\right) \\, dx" for t in terms)
            steps.append(
                f"ใช้สมบัติเชิงเส้นของการอินทิเกรต (แยกพจน์): \\int \\left({sp.latex(expr)}\\right) \\, dx = {terms_integrals}"
            )
            sub_results = []
            for t in terms:
                sub_res = sp.integrate(t, x)
                sub_results.append(f"\\int \\left({sp.latex(t)}\\right) \\, dx = {sp.latex(sub_res)}")
            steps.append(
                "อินทิเกรตทีละพจน์: " + ", \\quad ".join(sub_results)
            )
            steps.append(
                f"รวมผลลัพธ์ทุกพจน์และบวกค่าคงที่ของการอินทิเกรต C: \\int \\left({sp.latex(expr)}\\right) \\, dx = {sp.latex(result)} + C"
            )
        elif isinstance(expr, sp.sin) and expr.args[0] == x:
            steps.append(
                "ใช้สูตรปริพันธ์ฟังก์ชันไซน์: \\int \\sin(x) \\, dx = -\\cos(x) + C"
            )
        elif isinstance(expr, sp.cos) and expr.args[0] == x:
            steps.append(
                "ใช้สูตรปริพันธ์ฟังก์ชันโคไซน์: \\int \\cos(x) \\, dx = \\sin(x) + C"
            )
        elif isinstance(expr, sp.exp) and expr.args[0] == x:
            steps.append(
                "ใช้สูตรปริพันธ์ฟังก์ชันเอกซ์โพเนนเชียล: \\int e^x \\, dx = e^x + C"
            )
        elif expr == 1 / x:
            steps.append(
                "ใช้กฎปริพันธ์ฟังก์ชันส่วนกลับ: \\int \\frac{1}{x} \\, dx = \\ln|x| + C"
            )
        else:
            u_cand = None
            for node in expr.atoms(sp.Pow):
                if node.base != x and node.base.has(x) and not node.base.is_number:
                    u_cand = node.base
                    break
            if u_cand is None:
                for node in expr.atoms(sp.exp):
                    if node.args[0] != x and node.args[0].has(x):
                        u_cand = node.args[0]
                        break

            if u_cand is not None:
                du = sp.diff(u_cand, x)
                steps.append(
                    f"พิจารณาการเปลี่ยนตัวแปร (u-Substitution): u = {sp.latex(u_cand)} \\implies du = {sp.latex(du)} \\, dx"
                )
                steps.append(
                    f"คำนวณปริพันธ์ผลลัพธ์: \\int \\left({sp.latex(expr)}\\right) \\, dx = {sp.latex(result)} + C"
                )
            else:
                steps.append(
                    f"คำนวณปริพันธ์เชิงสัญลักษณ์: \\int \\left({sp.latex(expr)}\\right) \\, dx = {sp.latex(result)} + C"
                )

        latex_str = f"\\int \\left({sp.latex(expr)}\\right) \\, dx = {sp.latex(result)} + C"
        return {
            "ok": True,
            "result": result,
            "latex": latex_str,
            "steps": steps,
            "error": None,
        }
    except Exception:
        return {
            "ok": False,
            "result": None,
            "latex": "",
            "steps": [],
            "error": "ไม่สามารถอ่านนิพจน์ได้ กรุณาตรวจสอบรูปแบบ เช่น x**2, sin(x), (x**2-4)/(x-2)",
        }


def differentiate(expr_str: str) -> dict[str, Any]:
    x = sp.Symbol("x")
    try:
        expr = _parse_input(expr_str)
        result = sp.diff(expr, x)

        steps: list[str] = [
            f"กำหนดฟังก์ชันที่ต้องการหาอนุพันธ์: f(x) = {sp.latex(expr)}"
        ]

        if not expr.has(x):
            steps.append(
                f"ใช้กฎอนุพันธ์ของค่าคงที่: \\frac{{d}}{{dx}}[c] = 0 \\implies \\frac{{d}}{{dx}}\\left[{sp.latex(expr)}\\right] = 0"
            )
        elif expr == x:
            steps.append(
                "ใช้กฎอนุพันธ์ของตัวแปร x: \\frac{d}{dx}[x] = 1"
            )
        elif isinstance(expr, sp.Pow) and expr.args[0] == x and expr.args[1].is_number:
            n = expr.args[1]
            steps.append(
                "ใช้กฎกำลัง (Power Rule): \\frac{d}{dx}[x^n] = n x^{n-1}"
            )
            steps.append(
                f"แทนค่าเลขชี้กำลัง $n = {sp.latex(n)}$: \\frac{{d}}{{dx}}\\left[{sp.latex(expr)}\\right] = {sp.latex(n)} x^{{{sp.latex(n-1)}}} = {sp.latex(result)}"
            )
        elif isinstance(expr, sp.Add):
            terms = expr.as_ordered_terms()
            diff_terms_str = " + ".join(f"\\frac{{d}}{{dx}}\\left[{sp.latex(t)}\\right]" for t in terms)
            steps.append(
                f"ใช้กฎผลบวกและผลต่างของอนุพันธ์ (แยกหาทีละพจน์): \\frac{{d}}{{dx}}\\left[{sp.latex(expr)}\\right] = {diff_terms_str}"
            )
            sub_results = []
            for t in terms:
                sub_res = sp.diff(t, x)
                sub_results.append(f"\\frac{{d}}{{dx}}\\left[{sp.latex(t)}\\right] = {sp.latex(sub_res)}")
            steps.append(
                "หาอนุพันธ์ของแต่ละพจน์: " + ", \\quad ".join(sub_results)
            )
            steps.append(
                f"รวมผลลัพธ์อนุพันธ์: \\frac{{d}}{{dx}}\\left[{sp.latex(expr)}\\right] = {sp.latex(result)}"
            )
        elif isinstance(expr, sp.Mul):
            x_factors = [f for f in expr.args if f.has(x)]
            if len(x_factors) == 2:
                u, v = x_factors[0], x_factors[1]
                steps.append(
                    "ใช้กฎผลคูณของอนุพันธ์ (Product Rule): \\frac{d}{dx}[u \\cdot v] = u \\frac{dv}{dx} + v \\frac{du}{dx}"
                )
                steps.append(
                    f"กำหนด $u = {sp.latex(u)}$ และ $v = {sp.latex(v)}$: \\frac{{du}}{{dx}} = {sp.latex(sp.diff(u, x))}, \\quad \\frac{{dv}}{{dx}} = {sp.latex(sp.diff(v, x))}"
                )
                steps.append(
                    f"แทนค่าและจัดรูปอนุพันธ์: \\frac{{d}}{{dx}}\\left[{sp.latex(expr)}\\right] = {sp.latex(result)}"
                )
            else:
                steps.append(
                    f"คำนวณอนุพันธ์เชิงสัญลักษณ์: \\frac{{d}}{{dx}}\\left[{sp.latex(expr)}\\right] = {sp.latex(result)}"
                )
        elif isinstance(expr, sp.sin) and expr.args[0] == x:
            steps.append("ใช้สูตรอนุพันธ์ของฟังก์ชันไซน์: \\frac{d}{dx}[\\sin(x)] = \\cos(x)")
        elif isinstance(expr, sp.cos) and expr.args[0] == x:
            steps.append("ใช้สูตรอนุพันธ์ของฟังก์ชันโคไซน์: \\frac{d}{dx}[\\cos(x)] = -\\sin(x)")
        elif isinstance(expr, sp.tan) and expr.args[0] == x:
            steps.append("ใช้สูตรอนุพันธ์ของฟังก์ชันแทนเจนต์: \\frac{d}{dx}[\\tan(x)] = \\sec^2(x)")
        elif isinstance(expr, sp.exp) and expr.args[0] == x:
            steps.append("ใช้สูตรอนุพันธ์ของฟังก์ชันเอกซ์โพเนนเชียล: \\frac{d}{dx}[e^x] = e^x")
        elif isinstance(expr, sp.log) and expr.args[0] == x:
            steps.append("ใช้สูตรอนุพันธ์ของฟังก์ชันลอการิทึมธรรมชาติ: \\frac{d}{dx}[\\ln(x)] = \\frac{1}{x}")
        else:
            steps.append(
                f"คำนวณอนุพันธ์เชิงสัญลักษณ์: \\frac{{d}}{{dx}}\\left[{sp.latex(expr)}\\right] = {sp.latex(result)}"
            )

        latex_str = f"\\frac{{d}}{{dx}}\\left[{sp.latex(expr)}\\right] = {sp.latex(result)}"
        return {
            "ok": True,
            "result": result,
            "latex": latex_str,
            "steps": steps,
            "error": None,
        }
    except Exception:
        return {
            "ok": False,
            "result": None,
            "latex": "",
            "steps": [],
            "error": "ไม่สามารถอ่านนิพจน์ได้ กรุณาตรวจสอบรูปแบบ เช่น x**2, sin(x), (x**2-4)/(x-2)",
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


def compute_limit(expr_str: str, point: float | int = 0) -> dict[str, Any]:
    x = sp.Symbol("x")
    try:
        expr = _parse_input(expr_str)
        try:
            left = sp.limit(expr, x, point, dir="-")
            right = sp.limit(expr, x, point, dir="+")
            status = _classify_limit(left, right)
        except Exception:
            left, right = None, None
            status = "unsupported"

        steps = [
            f"กำหนดโจทย์ลิมิตที่ต้องการหา: \\lim_{{x \\to {point}}} \\left({sp.latex(expr)}\\right)"
        ]

        if status == "finite":
            result = sp.limit(expr, x, point)
            latex_str = f"\\lim_{{x \\to {point}}} \\left({sp.latex(expr)}\\right) = {sp.latex(result)}"

            try:
                direct_val = expr.subs(x, point)
                if direct_val.is_number and direct_val.is_finite:
                    steps.append(
                        f"ทดสอบแทนค่าโดยตรง (Direct Substitution): f({point}) = {sp.latex(direct_val)}"
                    )
                else:
                    steps.append(
                        f"พิจารณาลิมิตทางซ้าย (Left-hand limit): \\lim_{{x \\to {point}^-}} \\left({sp.latex(expr)}\\right) = {sp.latex(left)}"
                    )
                    steps.append(
                        f"พิจารณาลิมิตทางขวา (Right-hand limit): \\lim_{{x \\to {point}^+}} \\left({sp.latex(expr)}\\right) = {sp.latex(right)}"
                    )
            except Exception:
                steps.append(
                    f"พิจารณาลิมิตทางซ้าย (Left-hand limit): \\lim_{{x \\to {point}^-}} \\left({sp.latex(expr)}\\right) = {sp.latex(left)}"
                )
                steps.append(
                    f"พิจารณาลิมิตทางขวา (Right-hand limit): \\lim_{{x \\to {point}^+}} \\left({sp.latex(expr)}\\right) = {sp.latex(right)}"
                )

            steps.append(
                f"สรุปค่าลิมิตสองด้าน: \\lim_{{x \\to {point}}} \\left({sp.latex(expr)}\\right) = {sp.latex(result)}"
            )

        elif status == "infinite":
            result = left
            latex_str = f"\\lim_{{x \\to {point}}} \\left({sp.latex(expr)}\\right) = {sp.latex(result)}"
            steps.append(
                f"พิจารณาลิมิตทางซ้าย: \\lim_{{x \\to {point}^-}} \\left({sp.latex(expr)}\\right) = {sp.latex(left)}"
            )
            steps.append(
                f"พิจารณาลิมิตทางขวา: \\lim_{{x \\to {point}^+}} \\left({sp.latex(expr)}\\right) = {sp.latex(right)}"
            )
            steps.append(
                f"ลิมิตทั้งสองข้างลู่ไปสู่อนันต์เดียวกัน: \\lim_{{x \\to {point}}} \\left({sp.latex(expr)}\\right) = {sp.latex(result)}"
            )

        elif status == "dne":
            result = None
            latex_str = f"\\lim_{{x \\to {point}}} \\left({sp.latex(expr)}\\right) \\quad \\text{{(does not exist)}}"
            steps.append(
                f"พิจารณาลิมิตทางซ้าย (Left-hand limit): \\lim_{{x \\to {point}^-}} \\left({sp.latex(expr)}\\right) = {sp.latex(left)}"
            )
            steps.append(
                f"พิจารณาลิมิตทางขวา (Right-hand limit): \\lim_{{x \\to {point}^+}} \\left({sp.latex(expr)}\\right) = {sp.latex(right)}"
            )
            steps.append(
                f"สรุปผล (ไม่มีลิมิตสองด้านเนื่องจากลิมิตซ้ายไม่เท่ากับลิมิตขวา): \\lim_{{x \\to {point}}} \\left({sp.latex(expr)}\\right) \\quad \\text{{(does not exist)}}"
            )

        else:
            result = None
            latex_str = f"\\lim_{{x \\to {point}}} \\left({sp.latex(expr)}\\right) \\quad \\text{{(unsupported)}}"
            steps.append(
                f"ระบบไม่สามารถตัดสินหรือระบุค่าลิมิตได้: \\lim_{{x \\to {point}}} \\left({sp.latex(expr)}\\right) \\quad \\text{{(unsupported)}}"
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
        }
