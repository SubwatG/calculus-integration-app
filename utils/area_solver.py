"""utils/area_solver.py — พื้นที่ระหว่างเส้นโค้ง

คำนวณพื้นที่เรขาคณิต A = ∫_a^b |f(x) - g(x)| dx บนช่วงจริงจำกัด [a, b]
พร้อมแสดงขั้นตอนการหาจุดตัด การแบ่งช่วงย่อย และการปลดเครื่องหมายค่าสัมบูรณ์
ตามเกณฑ์ Universal Step Contract
"""
import math
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
    "x": sp.Symbol("x", real=True),
    "e": sp.E,
    "E": sp.E,
    "pi": sp.pi,
    "ln": sp.log,
}

X = sp.Symbol("x", real=True)


def _to_latex(sym_obj) -> str:
    lat = sp.latex(sym_obj)
    return lat.replace(r"\log", r"\ln")


def _parse_input(expr_str: str) -> sp.Expr:
    clean = (expr_str or "").strip()
    if not clean:
        raise ValueError("Empty input string")
    return parse_expr(clean, transformations=TRANSFORMATIONS, local_dict=LOCAL_MATH_DICT)


def _convert_real_roots(expr: sp.Expr) -> sp.Expr:
    """แปลงเลขชี้กำลังเศษส่วนที่เป็นส่วนคี่ เช่น x**(1/3) ให้เป็น real_root เพื่อรักษาสมบัติจำนวนจริงบนย่านลบ"""
    def _replace(node):
        if isinstance(node, sp.Pow) and isinstance(node.exp, sp.Rational):
            p, q = node.exp.p, node.exp.q
            if q % 2 == 1:
                return sp.real_root(node.base, q) ** p
        return node

    return expr.replace(
        lambda n: isinstance(n, sp.Pow) and isinstance(n.exp, sp.Rational) and n.exp.q % 2 == 1,
        _replace,
    )


def _to_rational_bound(val: float | int | str) -> sp.Rational:
    try:
        fval = float(val)
        if not math.isfinite(fval):
            raise ValueError(f"Bound must be finite, got {val}")
    except (TypeError, ValueError) as e:
        raise ValueError(f"Invalid bound {val}: {e}")
    return sp.Rational(str(val))


def _format_bound_latex(val: float | int | sp.Rational) -> str:
    """จัดรูปแบบขอบเขตบน/ล่างเป็น LaTeX ที่กระชับและคมชัด"""
    try:
        f = float(val)
        if f.is_integer():
            return str(int(f))
        return f"{f:g}"
    except Exception:
        return _to_latex(val)


def _find_crossings(diff: sp.Expr, a_val: float, b_val: float, var: sp.Symbol = X) -> list[float]:
    """ค้นหาจุดตัด f(x) - g(x) = 0 บนช่วงเปิด (a, b)"""
    roots = []
    # 1. ตรวจสอบรากพหุนาม
    try:
        poly = sp.Poly(diff, var)
        if all(c.is_Rational for c in poly.all_coeffs()):
            poly = poly.set_domain(sp.QQ)
            for r in poly.real_roots():
                rf = float(r)
                if a_val < rf < b_val and not any(abs(rf - ex) < 1e-4 for ex in roots):
                    roots.append(rf)
            return sorted(roots)
    except Exception:
        pass

    # 2. กรณีฟังก์ชันที่มีรากคี่หรือจุด x = 0 อยู่กลางช่วง
    if a_val < 0.0 < b_val and (diff.has(sp.real_root) or diff.has(sp.sign) or diff.has(sp.Abs)):
        roots.append(0.0)

    # 3. สแกนการเปลี่ยนเครื่องหมายและทำ Bisection
    xs = [a_val + (b_val - a_val) * i / 60.0 for i in range(61)]
    ys = []
    for xi in xs:
        try:
            val_y = float(diff.subs(var, xi).evalf())
            ys.append(val_y)
        except Exception:
            ys.append(float("nan"))

    for i in range(len(xs) - 1):
        y1, y2 = ys[i], ys[i + 1]
        if math.isnan(y1) or math.isnan(y2):
            continue
        if y1 == 0.0:
            if a_val < xs[i] < b_val and not any(abs(xs[i] - r) < 1e-4 for r in roots):
                roots.append(float(xs[i]))
        elif y1 * y2 < 0.0:
            xl, xr = float(xs[i]), float(xs[i + 1])
            yl, yr = y1, y2
            xm = (xl + xr) / 2.0
            for _ in range(30):
                xm = (xl + xr) / 2.0
                try:
                    ym = float(diff.subs(var, xm).evalf())
                except Exception:
                    break
                if abs(ym) < 1e-12 or (xr - xl) < 1e-9:
                    break
                if yl * ym <= 0.0:
                    xr, yr = xm, ym
                else:
                    xl, yl = xm, ym
            if a_val < xm < b_val and not any(abs(xm - r) < 1e-4 for r in roots):
                roots.append(xm)

    return sorted(roots)


def compute_area_between(f_str: str, g_str: str, a: float, b: float) -> dict:
    """คำนวณพื้นที่เรขาคณิตระหว่างเส้นโค้ง A = ∫_a^b |f(x) - g(x)| dx พร้อมแจกแจงขั้นตอนละเอียด"""
    try:
        a_sp = _to_rational_bound(a)
        b_sp = _to_rational_bound(b)
        if a_sp >= b_sp:
            raise ValueError("ขอบล่าง a ต้องน้อยกว่าขอบบน b")

        a_disp = _format_bound_latex(a_sp)
        b_disp = _format_bound_latex(b_sp)

        f_raw = _parse_input(f_str)
        g_raw = _parse_input(g_str)

        f_expr = _convert_real_roots(f_raw)
        g_expr = _convert_real_roots(g_raw)

        all_free = f_expr.free_symbols | g_expr.free_symbols
        if not all_free:
            var_sym = X
        elif len(all_free) == 1:
            var_sym = list(all_free)[0]
        else:
            if any(s.name == "x" for s in all_free):
                var_sym = [s for s in all_free if s.name == "x"][0]
            else:
                var_sym = sorted(all_free, key=lambda s: s.name)[0]
            extra = all_free - {var_sym}
            if extra:
                raise ValueError(f"พบตัวแปรมากกว่า 1 ตัวแปรในสมการ: {all_free} (กรุณาใช้ตัวแปรเดียวกันสำหรับ f และ g)")

        v_lat = _to_latex(var_sym)
        diff_expr = sp.simplify(f_expr - g_expr)

        if diff_expr.is_zero or diff_expr == 0:
            return {
                "ok": True,
                "result": 0.0,
                "latex": f"A = \\int_{{{a_disp}}}^{{{b_disp}}} |{_to_latex(diff_expr)}| \\, d{v_lat} = 0",
                "steps": [
                    f"กำหนดฟังก์ชัน: $f({v_lat}) = {_to_latex(f_raw)}, \\quad g({v_lat}) = {_to_latex(g_raw)}$ บนช่วง $[{a_disp}, {b_disp}]$ ",
                    f"เส้นโค้งทั้งสองทับกันพอดีทั่วทั้งช่วง: $f({v_lat}) - g({v_lat}) = 0$",
                    "พื้นที่ระหว่างเส้นโค้ง: $A = 0$",
                ],
                "expr": diff_expr,
                "f_expr": f_expr,
                "g_expr": g_expr,
                "crossings": [],
                "error": None,
                "variable": str(var_sym.name),
            }

        # ตรวจสอบจุดเอกฐานบนโดเมน (ตัวส่วนเป็นศูนย์ หรือค่าเป็นอนันต์)
        denom_diff = sp.denom(diff_expr.rewrite(sp.cos))
        if denom_diff != 1:
            try:
                for r in sp.solve(denom_diff, var_sym):
                    if getattr(r, "is_real", False) and float(a_sp) <= float(r) <= float(b_sp):
                        raise ValueError(f"ไม่สามารถคำนวณพื้นที่จำกัดได้บนช่วงที่กำหนด (พบจุดเอกฐานที่ {var_sym} = {r})")
            except ValueError:
                raise
            except Exception:
                pass

        check_pts = [float(a_sp), float(b_sp), (float(a_sp) + float(b_sp)) / 2.0]
        if float(a_sp) < 0.0 < float(b_sp):
            check_pts.append(0.0)
        for pt in check_pts:
            val_pt = diff_expr.subs(var_sym, pt)
            if val_pt in (sp.zoo, sp.oo, -sp.oo) or getattr(val_pt, "is_infinite", False):
                raise ValueError("ไม่สามารถคำนวณพื้นที่จำกัดได้บนช่วงที่กำหนด (พบจุดเอกฐาน หรือไม่อยู่ในโดเมนจำนวนจริง)")

        # -------------------------------------------------------------
        # ค้นหาจุดตัด f(x) - g(x) = 0 ทั้งหมดบนช่วงเปิด (a, b)
        # -------------------------------------------------------------
        interior_roots_sym = []
        is_poly = False
        try:
            poly = sp.Poly(diff_expr, var_sym)
            if all(c.is_Rational for c in poly.all_coeffs()):
                is_poly = True
                poly_q = poly.set_domain(sp.QQ)
                interior_roots_sym = [r for r in poly_q.real_roots() if a_sp < r < b_sp]
        except Exception:
            is_poly = False

        if not is_poly or not interior_roots_sym:
            float_roots = _find_crossings(diff_expr, float(a_sp), float(b_sp), var=var_sym)
            if not interior_roots_sym:
                interior_roots_sym = [sp.Rational(str(round(r, 6))) for r in float_roots]

        # จุดแบ่งทั้งหมด
        cuts = [a_sp] + sorted(set(interior_roots_sym)) + [b_sp]
        crossings_float = [float(r) for r in cuts[1:-1]]

        sub_steps = []
        total_area = sp.S.Zero
        piece_areas = []

        for i, (left, right) in enumerate(zip(cuts, cuts[1:]), start=1):
            left_disp = _format_bound_latex(left)
            right_disp = _format_bound_latex(right)
            # ตรวจสอบเครื่องหมายบนช่วงย่อย
            mid = (left + right) / 2
            mid_val = diff_expr.subs(var_sym, mid)
            is_pos = True
            try:
                is_pos = (float(mid_val.evalf()) >= 0)
            except Exception:
                is_pos = True

            piece_integral = sp.integrate(diff_expr, (var_sym, left, right))
            if piece_integral.has(sp.Integral) or not (
                getattr(piece_integral, "is_real", False) and getattr(piece_integral, "is_finite", False)
            ):
                piece_integral = sp.Integral(diff_expr, (var_sym, left, right)).evalf()
            piece_area = abs(piece_integral)
            total_area += piece_area
            piece_areas.append(piece_area)

            sign_desc = f"$f({v_lat}) \\geq g({v_lat})$" if is_pos else f"$g({v_lat}) \\geq f({v_lat})$ (สลับเครื่องหมาย)"
            sub_steps.append(
                f"ช่วงย่อยที่ {i} $[{left_disp}, {right_disp}]$ ({sign_desc}): "
                f"$A_{i} = \\left| \\int_{{{left_disp}}}^{{{right_disp}}} \\left({_to_latex(diff_expr)}\\right) \\, d{v_lat} \\right| = {_to_latex(piece_area)}$"
            )

        area_val = sp.simplify(total_area)
        res_float = float(area_val.evalf() if hasattr(area_val, "evalf") else area_val)

        # -------------------------------------------------------------
        # สร้าง Steps ตาม Universal Step Contract
        # -------------------------------------------------------------
        steps = [
            f"กำหนดฟังก์ชัน: $f({v_lat}) = {_to_latex(f_raw)}, \\quad g({v_lat}) = {_to_latex(g_raw)}$ บนช่วง $[{a_disp}, {b_disp}]$",
            f"เป้าหมาย / กฎที่ใช้ (Goal / Rule): ตั้งสูตรอินทิกรัลพื้นที่เรขาคณิต (Geometric Area) $A = \\int_{{{a_disp}}}^{{{b_disp}}} |f({v_lat}) - g({v_lat})| \\, d{v_lat}$ "
            f"โดยใช้ค่าสัมบูรณ์ (Absolute value) เพื่อไม่ให้พื้นที่บริเวณที่เส้นโค้งสลับบน-ล่างหักล้างกัน",
            f"พีชคณิตระหว่างทาง (Intermediate algebra): หาผลต่างของฟังก์ชัน $f({v_lat}) - g({v_lat}) = {_to_latex(diff_expr)}$",
        ]

        if crossings_float:
            roots_str = ", ".join(f"${v_lat} = {_format_bound_latex(r)}$" for r in cuts[1:-1])
            steps.append(
                f"หาจุดตัด (Intersections): แก้สมการ $f({v_lat}) - g({v_lat}) = 0$ พบจุดตัดภายในช่วงที่ {roots_str} "
                f"จึงแบ่งการคำนวณออกเป็น {len(cuts) - 1} ช่วงย่อยเพื่อปลดเครื่องหมายค่าสัมบูรณ์"
            )
            steps.extend(sub_steps)
            # รวมผลบวกทุกช่วงย่อย
            sum_str = " + ".join(f"A_{i}" for i in range(1, len(cuts)))
            pieces_val_str = " + ".join(f"{_to_latex(p)}" for p in piece_areas)
            steps.append(
                f"รวมพื้นที่ทุกช่วงย่อย: $A = {sum_str} = {pieces_val_str} = {_to_latex(area_val)}$"
            )
        else:
            # ไม่มีจุดตัดภายในช่วง
            mid_full = (a_sp + b_sp) / 2
            mid_val = diff_expr.subs(var_sym, mid_full)
            try:
                is_pos = (float(mid_val.evalf()) >= 0)
            except Exception:
                is_pos = True
            if is_pos:
                steps.append(
                    f"หาจุดตัด (Intersections): แก้สมการ $f({v_lat}) - g({v_lat}) = 0$ ไม่พบจุดตัดภายในช่วงเปิด $({a_disp}, {b_disp})$ "
                    f"โดยบนช่วงนี้ $f({v_lat}) \\geq g({v_lat})$ ดังนั้น $|f({v_lat}) - g({v_lat})| = f({v_lat}) - g({v_lat})$"
                )
            else:
                steps.append(
                    f"หาจุดตัด (Intersections): แก้สมการ $f({v_lat}) - g({v_lat}) = 0$ ไม่พบจุดตัดภายในช่วงเปิด $({a_disp}, {b_disp})$ "
                    f"โดยบนช่วงนี้ $g({v_lat}) \\geq f({v_lat})$ (เส้นโค้ง $g$ อยู่เหนือ $f$) "
                    f"ดังนั้นจึงสลับเครื่องหมายค่าสัมบูรณ์: $|f({v_lat}) - g({v_lat})| = g({v_lat}) - f({v_lat}) = {_to_latex(-diff_expr)}$"
                )
            steps.append(
                f"คำนวณปริพันธ์บนช่วง: $A = \\int_{{{a_disp}}}^{{{b_disp}}} |f({v_lat}) - g({v_lat})| \\, d{v_lat} = {_to_latex(area_val)}$"
            )

        steps.append(
            f"เงื่อนไขโดเมน (Domain restriction): ฟังก์ชันทั้งสองมีความต่อเนื่องบนช่วงปิด $[{a_disp}, {b_disp}]$"
        )
        steps.append(
            f"ผลลัพธ์แม่นตรง (Exact result): คำนวณพื้นที่เรขาคณิตรวม: $A = {_to_latex(area_val)} \\approx {res_float:.6g}$"
        )

        return {
            "ok": True,
            "result": res_float,
            "latex": f"A = \\int_{{{a_disp}}}^{{{b_disp}}} |{_to_latex(diff_expr)}| \\, d{v_lat} = {_to_latex(area_val)}",
            "steps": steps,
            "expr": diff_expr,
            "f_expr": f_expr,
            "g_expr": g_expr,
            "crossings": crossings_float,
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
            "f_expr": None,
            "g_expr": None,
            "crossings": [],
            "error": f"ไม่สามารถคำนวณได้: {e}",
        }
