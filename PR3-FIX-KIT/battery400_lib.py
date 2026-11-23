#!/usr/bin/env python3
"""Shared helpers and 32-case base for the 400-case battery.

The runner PR3-BATTERY-400-2026-11-22.py extends each case list to 50.
"""
import json
import math
import os
import signal
import sys

import mpmath as mp
import sympy as sp

sys.path.insert(0, os.environ.get("CALC_REPO", "/home/kitti/Projects/calculus-pr3-area"))

from utils.area_solver import compute_area_between
from utils.improper_solver import compute_improper
from utils.limit_solver import compute_limit_near
from utils.tangent_solver import compute_tangent
from utils.substitution_solver import solve_substitution
from utils.by_parts_solver import solve_by_parts
from utils.riemann_solver import compute_riemann
from utils.volume_solver import compute_volume

X = sp.Symbol("x", real=True)
OUT = os.environ.get("BATTERY_OUT", os.path.dirname(os.path.abspath(__file__)))
TIMEOUT = 10
mp.mp.dps = 25


class Timeout(Exception):
    pass


def _alarm(signum, frame):
    raise Timeout()


if hasattr(signal, "SIGALRM"):
    signal.signal(signal.SIGALRM, _alarm)


def run(fn):
    if hasattr(signal, "setitimer"):
        signal.setitimer(signal.ITIMER_REAL, TIMEOUT)
    try:
        return fn(), None
    except Timeout:
        return None, "TIMEOUT"
    except Exception as exc:  # noqa: BLE001
        return None, f"EXC {type(exc).__name__}: {exc}"
    finally:
        if hasattr(signal, "setitimer"):
            signal.setitimer(signal.ITIMER_REAL, 0)


def parse(s):
    local = {
        "x": X, "sin": sp.sin, "cos": sp.cos, "tan": sp.tan,
        "sec": sp.sec, "csc": sp.csc, "cot": sp.cot,
        "exp": sp.exp, "log": sp.log, "ln": sp.log, "sqrt": sp.sqrt,
        "Abs": sp.Abs, "pi": sp.pi, "e": sp.E,
    }
    return sp.sympify(s, locals=local)


def num_fn(expr):
    return sp.lambdify(X, expr, modules=["mpmath"])


def domain_ok(expr, a, b, n=401):
    fn = num_fn(expr)
    for i in range(n + 1):
        xv = a + (b - a) * i / n
        try:
            v = fn(mp.mpf(xv))
        except Exception:
            return False
        try:
            if mp.im(v) != 0 or not mp.isfinite(v) or abs(v) > 1e8:
                return False
        except Exception:
            return False
    return True


def jsonable(value):
    if value is None or isinstance(value, (bool, int, float, str)):
        return value
    try:
        return float(value)
    except Exception:
        return str(value)


def close(actual, expected, tol=1e-6):
    if actual is None:
        return False
    try:
        return abs(float(actual) - float(expected)) <= tol * max(1.0, abs(float(expected)))
    except Exception:
        return False


def scan(rec):
    steps = rec.get("steps") or []
    text = " | ".join(str(s) for s in steps) + " | " + str(rec.get("latex") or "")
    toks = [t for t in ("Piecewise", "zoo", "nan", "Integral(", "Traceback", "None", "Abs(", "log(", "เอกฐาน", "ดิฟ") if t in text]
    return toks, text


def save(solver, rows):
    path = os.path.join(OUT, f"results-{solver}.json")
    json.dump(rows, open(path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    passed = sum(1 for r in rows if r["verdict"] == "PASS")
    print(f"{solver}: {passed}/{len(rows)} pass -> {path}")


# ---------------------------------------------------------------- area
def area_cases():
    return [
        ("x", "x**2", 0, 1, False), ("x**2", "x", -1, 2, False),
        ("sin(x)", "cos(x)", 0, math.pi / 2, False), ("x**3", "x", -1, 1, False),
        ("1/x", "x", 1, 2, False), ("exp(x)", "0", 0, 1, False),
        ("sin(120*pi*x)", "0", 0, 1, False), ("sqrt(x)", "0", -2, -1, True),
        ("sqrt(x)", "0", -1, 1, True), ("x", "2-x", 0, 2, False),
        ("cos(x)", "0", 0, 2 * math.pi, False), ("x**2", "2*x", 0, 2, False),
        ("x**3", "0", -1, 1, False), ("x**2", "0", -1, 1, False),
        ("sin(x)", "0", 0, 2 * math.pi, False), ("1/x", "0", -1, 1, True),
        ("tan(x)", "0", 0, math.pi, True), ("log(x)", "0", 0, 1, True),
        ("x**4", "x**2", -1, 1, False), ("x", "x**3", 0, 1, False),
        ("sin(x)", "x", 0, math.pi / 2, False), ("cos(x)", "1-x**2/2", 0, 1, False),
        ("exp(x)", "1+x", 0, 1, False), ("log(1+x)", "x", 0, 1, False),
        ("sqrt(x)", "x", 0, 1, False), ("1/(1+x**2)", "0", -1, 1, False),
        ("exp(-x**2)", "0", -1, 1, False), ("sin(2*x)", "0", 0, math.pi / 2, False),
        ("cos(2*x)", "0", 0, math.pi / 4, False), ("x**2", "1", -1, 1, False),
        ("x**2", "1", 0, 2, False), ("sin(x)", "cos(x)", 0, 2 * math.pi, False),
    ]


def area_expected(fs, gs, a, b):
    if fs == "sin(120*pi*x)" and gs == "0" and (a, b) == (0, 1):
        return float(2 / mp.pi)
    f, g = parse(fs), parse(gs)
    if not domain_ok(f, a, b) or not domain_ok(g, a, b):
        return "reject"
    f_num, g_num = num_fn(f), num_fn(g)
    try:
        return float(mp.quad(lambda t: abs(f_num(t) - g_num(t)), [a, b], maxdegree=12))
    except Exception:
        return "quad_fail"


def run_area():
    rows = []
    for i, (fs, gs, a, b, reject) in enumerate(area_cases(), 1):
        exp = "reject" if reject else area_expected(fs, gs, a, b)
        rec, err = run(lambda: compute_area_between(fs, gs, a, b))
        row = {"solver": "area", "i": i, "case": f"{fs} vs {gs} on [{a},{b}]", "expected": exp, "run_error": err}
        if rec is None:
            row.update(actual=None, verdict="ERROR", suspicious=[])
        else:
            row.update(actual=jsonable(rec.get("result")), ok=rec.get("ok"), error=rec.get("error"), status=rec.get("status"))
            if exp == "reject":
                verdict = "PASS" if not rec.get("ok") else "WRONG_ACCEPTED"
            elif exp == "quad_fail":
                verdict = "SKIP"
            else:
                verdict = "PASS" if rec.get("ok") and close(row["actual"], exp) else "WRONG"
            row["verdict"] = verdict
            row["suspicious"], _ = scan(rec)
        rows.append(row)
        print(f"{i:02d} {row['verdict']:15} {row['case']} exp={exp} act={row.get('actual')}")
    save("area", rows)


# ---------------------------------------------------------------- improper
def improper_cases():
    return [
        ("1/x**2", 1, "inf", 1.0), ("1/x**3", 1, "inf", 0.5),
        ("1/x**1.5", 1, "inf", 2.0), ("1/x", 1, "inf", "divergent"),
        ("1/sqrt(x)", 0, 1, 2.0), ("1/x**(2/3)", 0, 1, 3.0),
        ("1/x", 0, 1, "divergent"), ("1/x**1.5", 0, 1, "divergent"),
        ("ln(x)", 0, 1, -1.0), ("x*ln(x)", 0, 1, -0.25),
        ("ln(x)/sqrt(x)", 0, 1, -4.0), ("sqrt(x)*ln(x)", 0, 1, -4 / 9),
        ("exp(-x)", 0, "inf", 1.0), ("exp(-2*x)", 0, "inf", 0.5),
        ("exp(-x**2)", "-inf", "inf", math.sqrt(math.pi)),
        ("exp(-x**2/2)", "-inf", "inf", math.sqrt(2 * math.pi)),
        ("1/(1+x**2)", "-inf", "inf", math.pi),
        ("ln(x)/x**2", 1, "inf", 1.0), ("ln(x)/x**3", 1, "inf", 0.25),
        ("1/(x*ln(x))", 2, "inf", "divergent"),
        ("1/(x*ln(x)**2)", 2, "inf", 1 / math.log(2)),
        ("1/sqrt(1-x**2)", -1, 1, math.pi),
        ("1/sqrt(1-x)", 0, 1, 2.0),
        ("1/(1-x)", 0, 1, "divergent"),
        ("1/(x-1)**(2/3)", 0, 2, 6.0),
        ("1/sqrt(Abs(x-1))", 0, 2, 4.0),
        ("1/(x-1)", 0, 2, "divergent"),
        ("sin(x)/x", 0, 1, float(mp.si(1))),
        ("cos(x)/sqrt(x)", 0, 1, float(2 * mp.quad(lambda t: mp.cos(t * t), [0, 1]))),
        ("1/(x**2+1)", 0, "inf", math.pi / 2),
        ("x*exp(-x)", 0, "inf", 1.0), ("x**2*exp(-x)", 0, "inf", 2.0),
    ]


def run_improper():
    rows = []
    for i, (expr, a, b, exp) in enumerate(improper_cases(), 1):
        rec, err = run(lambda: compute_improper(expr, a, b))
        row = {"solver": "improper", "i": i, "case": f"{expr} on [{a},{b}]", "expected": exp, "run_error": err}
        if rec is None:
            row.update(actual=None, verdict="ERROR", suspicious=[])
        else:
            row.update(actual=jsonable(rec.get("result")), ok=rec.get("ok"), status=rec.get("status"), error=rec.get("error"))
            if exp == "divergent":
                verdict = "PASS" if rec.get("status") == "divergent" else "WRONG"
            else:
                verdict = "PASS" if rec.get("ok") and close(row["actual"], exp) else "WRONG"
            row["verdict"] = verdict
            row["suspicious"], _ = scan(rec)
        rows.append(row)
        print(f"{i:02d} {row['verdict']:15} {row['case']} exp={exp} act={row.get('actual')} st={row.get('status')}")
    save("improper", rows)


# ---------------------------------------------------------------- limit
def limit_cases():
    return [
        ("(x**2-1)/(x-1)", 1), ("(x**3-1)/(x-1)", 1), ("(x**2-4)/(x-2)", 2),
        ("(x**2+3*x+2)/(x+1)", -1), ("(x**3-8)/(x-2)", 2),
        ("sin(x)/x", 0), ("sin(2*x)/x", 0), ("sin(3*x)/sin(2*x)", 0),
        ("(1-cos(x))/x**2", 0), ("(1-cos(2*x))/x**2", 0),
        ("tan(x)/x", 0), ("(exp(x)-1)/x", 0), ("(exp(2*x)-1)/x", 0),
        ("log(1+x)/x", 0), ("(sqrt(x+1)-1)/x", 0),
        ("(sqrt(x)-2)/(x-4)", 4), ("(x**(1/3)-1)/(x-1)", 1),
        ("Abs(x)/x", 0), ("Abs(x-1)/(x-1)", 1), ("x/Abs(x)", 0),
        ("sin(1/x)", 0), ("x*sin(1/x)", 0), ("cos(1/x)", 0),
        ("1/x", 0), ("1/x**2", 0),
        ("(2*x**2+3*x)/(x**2-x)", "inf"), ("(3*x**3-1)/(x**3+2)", "inf"),
        ("(1+1/x)**x", "inf"), ("x*log(1+1/x)", "inf"),
        ("(1-1/x)**x", "inf"), ("(x**2-1)/(x**2+1)", "inf"),
        ("(x**2+1)/(x+1)", "inf"),
    ]


def limit_expected(expr_s, a):
    e = parse(expr_s)
    av = sp.oo if a == "inf" else sp.sympify(a)

    def norm(L):
        if isinstance(L, sp.AccumBounds):
            return "DNE"
        if L is sp.oo:
            return "INF"
        if L is -sp.oo:
            return "-INF"
        if getattr(L, "is_real", None) is False:
            return "DNE"
        try:
            return float(L)
        except Exception:
            return "DNE"

    try:
        left = norm(sp.limit(e, X, av, dir="-"))
        right = norm(sp.limit(e, X, av, dir="+"))
    except Exception:
        return "DNE"
    if left != right:
        return "DNE"
    return left


def run_limit():
    rows = []
    for i, (expr, a) in enumerate(limit_cases(), 1):
        exp = limit_expected(expr, a)
        rec, err = run(lambda: compute_limit_near(expr, a))
        row = {"solver": "limit", "i": i, "case": f"{expr} at {a}", "expected": exp, "run_error": err}
        if rec is None:
            row.update(actual=None, verdict="ERROR", suspicious=[])
        else:
            row.update(actual=jsonable(rec.get("result")), ok=rec.get("ok"), status=rec.get("status"),
                       left=jsonable(rec.get("left_limit")), right=jsonable(rec.get("right_limit")), error=rec.get("error"))
            if exp == "DNE":
                verdict = "PASS" if (not rec.get("ok") or rec.get("status") in ("dne", "one_sided_mismatch", "oscillating")) else "WRONG"
            elif exp in ("INF", "-INF"):
                verdict = "PASS" if (rec.get("is_infinite") or rec.get("status") in ("infinite", "divergent")) else "WRONG"
            else:
                verdict = "PASS" if rec.get("ok") and close(row["actual"], exp) else "WRONG"
            row["verdict"] = verdict
            row["suspicious"], _ = scan(rec)
        rows.append(row)
        print(f"{i:02d} {row['verdict']:15} {row['case']} exp={exp} act={row.get('actual')} st={row.get('status')}")
    save("limit", rows)


# ---------------------------------------------------------------- tangent
def tangent_cases():
    return [
        ("x**2", 1, 2.0), ("x**2", -1, -2.0), ("x**3", 1, 3.0), ("x**3", -1, 3.0),
        ("x**4", 1, 4.0), ("1/x", 1, -1.0), ("1/x", -1, -1.0),
        ("sqrt(x)", 4, 0.25), ("sqrt(x)", 0, "vertical_endpoint"),
        ("x**(1/3)", 0, "vertical"), ("x**(1/3)", 1, 1 / 3),
        ("Abs(x)", 0, "corner"), ("Abs(x-1)", 1, "corner"), ("Abs(x)", 1, 1.0),
        ("sin(x)", 0, 1.0), ("sin(x)", math.pi / 2, 0.0),
        ("cos(x)", 0, 0.0), ("cos(x)", math.pi / 2, -1.0),
        ("tan(x)", 0, 1.0), ("tan(x)", math.pi / 4, 2.0),
        ("exp(x)", 0, 1.0), ("exp(x)", 1, math.e),
        ("log(x)", 1, 1.0), ("log(x)", math.e, 1 / math.e),
        ("x*exp(x)", 0, 1.0), ("x**2*exp(x)", 0, 0.0),
        ("x*log(x)", 1, 1.0), ("x/(x+1)", 0, 1.0),
        ("(x+1)/(x-1)", 2, -2.0), ("sqrt(1+x**2)", 0, 0.0),
        ("1/(1+x**2)", 1, -0.5), ("x**(1/3)", -1, 1 / 3),
    ]


def run_tangent():
    rows = []
    for i, (expr, a, exp) in enumerate(tangent_cases(), 1):
        rec, err = run(lambda: compute_tangent(expr, a))
        row = {"solver": "tangent", "i": i, "case": f"{expr} at {a}", "expected": exp, "run_error": err}
        if rec is None:
            row.update(actual=None, verdict="ERROR", suspicious=[])
        else:
            row.update(actual=jsonable(rec.get("result")), ok=rec.get("ok"), status=rec.get("status"), error=rec.get("error"))
            if exp in ("corner", "vertical", "vertical_endpoint"):
                verdict = "PASS" if rec.get("status") == "non_differentiable" else "WRONG"
                if expr.startswith("sqrt") or expr.startswith("x**(1/3)"):
                    row["explanation_issue"] = True
            else:
                verdict = "PASS" if rec.get("ok") and close(row["actual"], exp) else "WRONG"
            row["verdict"] = verdict
            row["suspicious"], _ = scan(rec)
        rows.append(row)
        print(f"{i:02d} {row['verdict']:15} {row['case']} exp={exp} act={row.get('actual')} st={row.get('status')}")
    save("tangent", rows)


# ------------------------------------------------- symbolic derivative check
def sample_points(expr_s):
    if "log" in expr_s or "ln" in expr_s:
        return [0.15, 0.25, 0.5, 0.8, 1.3]
    if "asin" in expr_s or "acos" in expr_s:
        return [-0.4, -0.1, 0.1, 0.3, 0.45]
    if "sqrt" in expr_s:
        return [0.25, 0.5, 1.3, 2.1, 4.0]
    if "tan" in expr_s or "sec" in expr_s or "csc" in expr_s:
        return [0.5, 1.3, 2.1, 4.0]
    return [-1.0, 0.5, 1.3, 2.1, 4.0]


def symbolically_ok(expr_s, rec):
    if not rec.get("ok") or rec.get("result") is None:
        return False
    res = rec["result"]
    if res.has(sp.Integral):
        return False
    e = parse(expr_s)
    var = next(iter(res.free_symbols), X)
    if not getattr(var, "is_real", False):
        real_var = sp.Symbol(var.name, real=True)
        res = res.subs(var, real_var)
        var = real_var
    der = sp.diff(res, var)
    used = 0
    for xv in sample_points(expr_s):
        try:
            fv = complex(e.subs(X, xv).evalf())
            rv = complex(res.subs(var, xv).evalf())
            dv = complex(der.subs(var, xv).evalf())
        except Exception:
            continue
        if not all(math.isfinite(z) for z in (fv.real, fv.imag, rv.real, rv.imag, dv.real, dv.imag)):
            continue
        if abs(fv.imag) > 1e-9:
            continue
        used += 1
        if abs(rv.imag) > 1e-9:
            return False
        if abs(dv - fv) > 1e-5 * max(1.0, abs(fv)):
            return False
    return used >= 2


# ---------------------------------------------------------------- substitution
def sub_cases():
    return [
        "2*x*sqrt(x**2+1)", "x*sqrt(x**2+1)", "x**2*(x**3+5)**4",
        "(2*x+1)/(x**2+x+1)", "cos(x)*exp(sin(x))", "sin(x)*cos(x)",
        "log(x)/x", "1/(x*log(x))", "exp(2*x)", "x*exp(x**2)",
        "sec(x)**2*tan(x)", "tan(x)", "1/x", "1/(2*x+1)", "1/(3*x-2)",
        "(log(x))**2/x", "sqrt(2*x+1)", "x/(x**2+1)", "x**2/(x**3+1)",
        "exp(sqrt(x))/sqrt(x)", "cos(2*x)", "sin(3*x)", "sec(x)**2/tan(x)",
        "1/(x**2+1)", "1/sqrt(1-x**2)", "1/(1+4*x**2)", "x/(1+x**4)",
        "exp(x)/(1+exp(x))", "cos(x)/(1+sin(x))", "1/(x*(log(x))**2)",
        "1/(sqrt(x)*(1+sqrt(x)))", "x**2*exp(x**3)",
    ]


def run_substitution():
    rows = []
    for i, expr in enumerate(sub_cases(), 1):
        rec, err = run(lambda: solve_substitution(expr))
        row = {"solver": "substitution", "i": i, "case": expr, "run_error": err}
        if rec is None:
            row.update(actual=None, verdict="ERROR", suspicious=[])
        else:
            row.update(actual=str(rec.get("result")), ok=rec.get("ok"), status=rec.get("status"), error=rec.get("error"))
            if expr in ("x*tan(x)", "x*sec(x)"):
                is_rejected = (not rec.get("ok") or rec.get("status") in ("unsupported", "non_elementary"))
                no_integral = not (rec.get("result") is not None and rec["result"].has(sp.Integral))
                row["verdict"] = "PASS" if (is_rejected and no_integral) else "WRONG"
            else:
                row["verdict"] = "PASS" if symbolically_ok(expr, rec) else "WRONG"
            row["suspicious"], _ = scan(rec)
        rows.append(row)
        print(f"{i:02d} {row['verdict']:15} {expr} -> {row.get('actual')}")
    save("substitution", rows)


# ---------------------------------------------------------------- by parts
def bp_cases():
    return [
        "x*exp(x)", "x**2*exp(x)", "x**3*exp(x)", "x*sin(x)", "x**2*sin(x)",
        "x*cos(x)", "x**2*cos(x)", "log(x)", "x*log(x)", "x**2*log(x)",
        "atan(x)", "asin(x)", "x*atan(x)", "x*asin(x)", "exp(x)*sin(x)",
        "exp(x)*cos(x)", "exp(2*x)*sin(x)", "exp(2*x)*cos(x)", "x*sec(x)**2",
        "x*csc(x)**2", "x**2*exp(-x)", "x*exp(-x)", "x*sinh(x)", "x*cosh(x)",
        "x*log(x+1)", "x**2*log(x+1)", "x*tan(x)", "x*sec(x)",
        "x*acos(x)", "x**2*atan(x)", "log(x)**2", "x*(log(x))**2",
    ]


def run_by_parts():
    rows = []
    for i, expr in enumerate(bp_cases(), 1):
        rec, err = run(lambda: solve_by_parts(expr))
        row = {"solver": "by_parts", "i": i, "case": expr, "run_error": err}
        if rec is None:
            row.update(actual=None, verdict="ERROR", suspicious=[])
        else:
            row.update(actual=str(rec.get("result")), ok=rec.get("ok"), status=rec.get("status"), error=rec.get("error"))
            if expr in ("x*tan(x)", "x*sec(x)"):
                is_rejected = (not rec.get("ok") or rec.get("status") in ("unsupported", "non_elementary"))
                no_integral = not (rec.get("result") is not None and rec["result"].has(sp.Integral))
                row["verdict"] = "PASS" if (is_rejected and no_integral) else "WRONG"
            else:
                row["verdict"] = "PASS" if symbolically_ok(expr, rec) else "WRONG"
            row["suspicious"], _ = scan(rec)
        rows.append(row)
        print(f"{i:02d} {row['verdict']:15} {expr} -> {row.get('actual')}")
    save("by_parts", rows)


# ---------------------------------------------------------------- riemann
def riemann_cases():
    return [
        ("x", 0, 1, 4, "left"), ("x", 0, 1, 4, "right"), ("x", 0, 1, 4, "midpoint"),
        ("x**2", 0, 1, 4, "left"), ("x**2", 0, 1, 4, "right"), ("x**2", 0, 1, 4, "midpoint"),
        ("x**2", 0, 2, 4, "left"), ("x**2", 0, 2, 4, "right"), ("x**2", 0, 2, 4, "midpoint"),
        ("x**3", 0, 1, 4, "left"), ("x**3", -1, 1, 4, "right"),
        ("sin(x)", 0, math.pi, 4, "midpoint"), ("sin(x)", 0, math.pi, 4, "left"),
        ("cos(x)", 0, math.pi / 2, 4, "left"),
        ("exp(x)", 0, 1, 4, "left"), ("exp(x)", 0, 1, 4, "right"), ("exp(x)", 0, 1, 4, "midpoint"),
        ("1/x", 1, 2, 4, "left"), ("1/x", 1, 2, 4, "right"),
        ("sqrt(x)", 0, 1, 4, "left"), ("sqrt(x)", 0, 1, 4, "right"),
        ("Abs(x)", -1, 1, 4, "midpoint"),
        ("x**2", 0, 1, 8, "left"), ("x**2", 0, 1, 8, "right"), ("x**2", 0, 1, 8, "midpoint"),
        ("x", 0, 1, 10, "left"), ("x", 0, 1, 10, "right"), ("x", 0, 1, 10, "midpoint"),
        ("sin(x)", 0, math.pi, 8, "midpoint"), ("exp(x)", 0, 1, 8, "left"),
        ("1/x", 1, 2, 8, "midpoint"), ("x**3", -1, 1, 8, "midpoint"),
    ]


def riemann_expected(expr, a, b, n, method):
    e = parse(expr)
    h = (b - a) / n
    total = 0.0
    for i in range(n):
        if method == "left":
            xv = a + i * h
        elif method == "right":
            xv = a + (i + 1) * h
        else:
            xv = a + (i + 0.5) * h
        total += float(e.subs(X, xv)) * h
    return total


def run_riemann():
    rows = []
    for i, (expr, a, b, n, method) in enumerate(riemann_cases(), 1):
        exp = riemann_expected(expr, a, b, n, method)
        rec, err = run(lambda: compute_riemann(expr, a, b, n, method))
        row = {"solver": "riemann", "i": i, "case": f"{expr} [{a},{b}] n={n} {method}", "expected": exp, "run_error": err}
        if rec is None:
            row.update(actual=None, verdict="ERROR", suspicious=[])
        else:
            row.update(actual=jsonable(rec.get("result")), ok=rec.get("ok"), error=rec.get("error"))
            row["verdict"] = "PASS" if rec.get("ok") and close(row["actual"], exp) else "WRONG"
            row["suspicious"], _ = scan(rec)
        rows.append(row)
        print(f"{i:02d} {row['verdict']:15} {row['case']} exp={exp} act={row.get('actual')}")
    save("riemann", rows)


# ---------------------------------------------------------------- volume
def volume_cases():
    return [
        ("x", 0, 1, "disk", None), ("x**2", 0, 1, "disk", None),
        ("x**3", 0, 1, "disk", None), ("sqrt(x)", 0, 1, "disk", None),
        ("sqrt(x)", 0, 4, "disk", None), ("sin(x)", 0, math.pi, "disk", None),
        ("cos(x)", 0, math.pi / 2, "disk", None), ("exp(x)", 0, 1, "disk", None),
        ("1/x", 1, 2, "disk", None), ("1/x", 1, 3, "disk", None),
        ("x**2", 0, 2, "disk", None), ("x", 0, 2, "disk", None),
        ("sqrt(x)", 0, 1, "washer", "x**2"), ("x", 0, 1, "washer", "x**2"),
        ("x**2", 0, 1, "washer", "x**3"), ("exp(2*x)", 0, 1, "washer", "exp(x)"),
        ("2", 0, 1, "washer", "x"), ("1", -1, 1, "washer", "x**2"),
        ("x**2", -1, 1, "disk", None), ("sin(x)", 0, math.pi / 2, "disk", None),
        ("cos(x)", 0, math.pi / 2, "disk", None), ("1/(1+x**2)", 0, 1, "disk", None),
        ("sqrt(1-x**2)", -1, 1, "disk", None), ("exp(-x)", 0, 1, "disk", None),
        ("1/x**2", 1, 2, "disk", None), ("sqrt(x)", 0, 1, "washer", "x"),
        ("x", 0, 1, "washer", "x**3"), ("2", 0, 1, "washer", "sqrt(x)"),
        ("x**2", 0, 3, "disk", None), ("1/x", 1, 4, "disk", None),
        ("cos(x)", 0, math.pi / 4, "washer", "sin(x)"), ("exp(2*x)", 0, 1, "disk", None),
    ]


def volume_expected(expr, a, b, method, inner):
    R = parse(expr)
    r = parse(inner) if inner else None
    if not domain_ok(R, a, b) or (r is not None and not domain_ok(r, a, b)):
        return "reject"
    Rf = num_fn(R)
    rf = num_fn(r) if r is not None else None
    if method == "disk":
        f = lambda t: math.pi * float(Rf(t)) ** 2
    else:
        # if R < r anywhere, the setup is invalid
        for i in range(401):
            xv = a + (b - a) * i / 400
            if float(Rf(xv)) < float(rf(xv)) - 1e-9:
                return "reject"
        f = lambda t: math.pi * (float(Rf(t)) ** 2 - float(rf(t)) ** 2)
    try:
        return float(mp.quad(f, [a, b], maxdegree=10))
    except Exception:
        return "quad_fail"


def run_volume():
    rows = []
    for i, (expr, a, b, method, inner) in enumerate(volume_cases(), 1):
        exp = volume_expected(expr, a, b, method, inner)
        rec, err = run(lambda: compute_volume(expr, a, b, method, inner))
        row = {"solver": "volume", "i": i, "case": f"{expr} [{a},{b}] {method}" + (f" inner={inner}" if inner else ""), "expected": exp, "run_error": err}
        if rec is None:
            row.update(actual=None, verdict="ERROR", suspicious=[])
        else:
            row.update(actual=jsonable(rec.get("result")), ok=rec.get("ok"), error=rec.get("error"))
            if exp in ("reject", "quad_fail"):
                verdict = "SKIP"
            else:
                verdict = "PASS" if rec.get("ok") and close(row["actual"], exp) else "WRONG"
            row["verdict"] = verdict
            row["suspicious"], _ = scan(rec)
        rows.append(row)
        print(f"{i:02d} {row['verdict']:15} {row['case']} exp={exp} act={row.get('actual')}")
    save("volume", rows)


if __name__ == "__main__":
    which = sys.argv[1] if len(sys.argv) > 1 else "area"
    fn = {
        "area": run_area, "improper": run_improper, "limit": run_limit,
        "tangent": run_tangent, "substitution": run_substitution,
        "by_parts": run_by_parts, "riemann": run_riemann, "volume": run_volume,
    }.get(which)
    if fn is None:
        raise SystemExit(f"unknown solver {which}")
    fn()
