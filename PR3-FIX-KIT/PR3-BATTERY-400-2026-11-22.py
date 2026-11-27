#!/usr/bin/env python3
"""400-case battery: 50 cases per solver.

Usage: python PR3-BATTERY-400-2026-11-22.py <area|improper|limit|tangent|substitution|by_parts|riemann|volume>
Results are written to results-<solver>.json.
"""
import math
import sys

import battery400_lib as b

_orig_area = b.area_cases
b.area_cases = lambda: _orig_area() + [
    ("x**2", "x**3", 0, 1, False),
    ("x**2", "x**3", -1, 1, False),
    ("sin(x)", "sin(2*x)", 0, math.pi, False),
    ("cos(x)", "cos(2*x)", 0, math.pi, False),
    ("exp(x)", "exp(-x)", -1, 1, False),
    ("x", "sin(x)", 0, math.pi, False),
    ("x", "tan(x)", 0, math.pi / 4, False),
    ("1/(1+x)", "1/(1+x**2)", 0, 1, False),
    ("sqrt(x)", "x**2", 0, 1, False),
    ("sqrt(x)", "x", 0, 4, False),
    ("log(x)", "x-1", 1, 2, False),
    ("exp(-x)", "x", 0, 1, False),
    ("sin(x)", "x/2", 0, math.pi, False),
    ("x**3", "x**2", -1, 2, False),
    ("1/x", "1/x**2", 1, 2, False),
    ("x**2", "2*x+3", -2, 4, False),
    ("sin(3*x)", "0", 0, math.pi, False),
    ("cos(3*x)", "0", 0, math.pi, False),
]

_orig_improper = b.improper_cases
b.improper_cases = lambda: _orig_improper() + [
    ("1/x**4", 1, "inf", 1 / 3),
    ("1/x**0.5", 1, "inf", "divergent"),
    ("1/x**0.5", 0, 1, 2.0),
    ("1/x**(1/3)", 0, 1, 1.5),
    ("ln(x)/x", 0, 1, "divergent"),
    ("ln(x)/x**2", 0, 1, "divergent"),
    ("exp(-3*x)", 0, "inf", 1 / 3),
    ("exp(-x/2)", 0, "inf", 2.0),
    ("x*exp(-2*x)", 0, "inf", 0.25),
    ("x**3*exp(-x)", 0, "inf", 6.0),
    ("1/(x**2+4)", "-inf", "inf", math.pi / 2),
    ("1/(x**2+2*x+2)", "-inf", "inf", math.pi),
    ("1/(x*ln(x)**3)", 2, "inf", 1 / (2 * math.log(2) ** 2)),
    ("1/(x*sqrt(ln(x)))", 2, "inf", "divergent"),
    ("1/(1-x)**2", 0, 1, "divergent"),
    ("1/sqrt(1-x**2)", 0, 1, math.pi / 2),
    ("1/sqrt(x*(1-x))", 0, 1, math.pi),
    ("x**(-0.9)", 0, 1, 10.0),
]

_orig_limit = b.limit_cases
b.limit_cases = lambda: _orig_limit() + [
    ("(x**3-27)/(x-3)", 3),
    ("(x**2-9)/(x**2-3*x)", 3),
    ("(x**2-1)/(x**2-3*x+2)", 1),
    ("(sqrt(x)-3)/(x-9)", 9),
    ("(x**(1/3)-2)/(x-8)", 8),
    ("(1-cos(3*x))/x**2", 0),
    ("(1-cos(x))/sin(x)", 0),
    ("sin(4*x)/tan(2*x)", 0),
    ("(exp(3*x)-1)/x", 0),
    ("(exp(x)-1-x)/x**2", 0),
    ("log(1+2*x)/x", 0),
    ("(log(1+x)-x)/x**2", 0),
    ("x**2*sin(1/x)", 0),
    ("x*cos(1/x)", 0),
    ("(2*x**2+1)/(3*x**2-1)", "inf"),
    ("(x**3+2*x)/(2*x**3-x**2)", "inf"),
    ("sqrt(x**2+x)-x", "inf"),
    ("(1+2/x)**x", "inf"),
]

_orig_tangent = b.tangent_cases
b.tangent_cases = lambda: _orig_tangent() + [
    ("x**5", 1, 5.0),
    ("x**5", -1, 5.0),
    ("x**2+2*x", 1, 4.0),
    ("x**3-3*x", 2, 9.0),
    ("1/x**2", 1, -2.0),
    ("1/x**2", -1, 2.0),
    ("sqrt(x)", 9, 1 / 6),
    ("sqrt(x+1)", 0, 0.5),
    ("x*sqrt(x)", 1, 1.5),
    ("x**(2/3)", 1, 2 / 3),
    ("x**(2/3)", -1, -2 / 3),
    ("sin(2*x)", 0, 2.0),
    ("cos(2*x)", 0, 0.0),
    ("tan(2*x)", 0, 2.0),
    ("exp(2*x)", 0, 2.0),
    ("log(2*x)", 0.5, 2.0),
    ("x**2*log(x)", 1, 1.0),
    ("sqrt(4-x**2)", 1, -1 / math.sqrt(3)),
]

_orig_sub = b.sub_cases
b.sub_cases = lambda: _orig_sub() + [
    "x*sqrt(x**2+4)",
    "(3*x**2+2*x)/(x**3+x**2+1)",
    "sin(2*x)*cos(2*x)",
    "exp(3*x+1)",
    "1/(5*x+2)",
    "1/(4*x-3)",
    "x**3*sqrt(x**4+1)",
    "log(2*x)/x",
    "1/(x*log(2*x))",
    "sec(3*x)**2",
    "tan(2*x)",
    "cos(x)*sin(x)**3",
    "x/(x**2+9)",
    "x**2/(x**3+8)",
    "exp(cos(x))*sin(x)",
    "1/(sqrt(x)*(1+sqrt(x))**2)",
    "sqrt(1+x)",
    "x*exp(-x**2)",
]

_orig_bp = b.bp_cases
b.bp_cases = lambda: _orig_bp() + [
    "x**2*exp(2*x)",
    "x**3*exp(-x)",
    "x**2*sin(2*x)",
    "x**2*cos(2*x)",
    "x**3*log(x)",
    "log(x+1)",
    "x*log(2*x)",
    "x*atan(2*x)",
    "x*asin(2*x)",
    "exp(3*x)*sin(2*x)",
    "exp(3*x)*cos(2*x)",
    "x*sinh(2*x)",
    "x*cosh(2*x)",
    "x**2*acos(x)",
    "x**2*exp(-2*x)",
    "x*sec(2*x)**2",
    "x*csc(2*x)**2",
    "x**2*asin(x)",
]

_orig_riemann = b.riemann_cases
b.riemann_cases = lambda: _orig_riemann() + [
    ("x**3", 0, 2, 4, "left"),
    ("x**3", 0, 2, 4, "right"),
    ("x**3", 0, 2, 4, "midpoint"),
    ("1/x", 1, 3, 4, "left"),
    ("1/x", 1, 3, 4, "right"),
    ("1/x", 1, 3, 4, "midpoint"),
    ("cos(x)", 0, math.pi / 2, 4, "right"),
    ("cos(x)", 0, math.pi / 2, 4, "midpoint"),
    ("sin(x)", 0, math.pi / 2, 4, "left"),
    ("sin(x)", 0, math.pi / 2, 4, "right"),
    ("sin(x)", 0, math.pi / 2, 4, "midpoint"),
    ("exp(x)", 0, 1, 10, "left"),
    ("exp(x)", 0, 1, 10, "right"),
    ("exp(x)", 0, 1, 10, "midpoint"),
    ("x**2", 0, 2, 8, "left"),
    ("x**2", 0, 2, 8, "right"),
    ("x**2", 0, 2, 8, "midpoint"),
    ("Abs(x)", -1, 1, 4, "left"),
]

_orig_volume = b.volume_cases
b.volume_cases = lambda: _orig_volume() + [
    ("x**3", 0, 1, "disk", None),
    ("x**3", 0, 2, "disk", None),
    ("sqrt(x)", 0, 9, "disk", None),
    ("sin(x)", 0, math.pi / 2, "disk", None),
    ("cos(x)", 0, math.pi, "disk", None),
    ("exp(2*x)", 0, 0.5, "disk", None),
    ("exp(-2*x)", 0, 1, "disk", None),
    ("1/(x+1)", 0, 1, "disk", None),
    ("1/(x+1)", 1, 2, "disk", None),
    ("x**2", 0, 1, "washer", "x**4"),
    ("sqrt(x)", 0, 1, "washer", "x**3"),
    ("exp(x)", 0, 1, "washer", "1"),
    ("1", 0, 1, "washer", "x**3"),
    ("2", 0, 1, "washer", "x**2"),
    ("x", 0, 2, "washer", "x**2/2"),
    ("sin(x)", 0, math.pi / 2, "washer", "x/2"),
    ("cos(x)", 0, math.pi / 4, "disk", None),
    ("x**2", 0, 1, "disk", None),
]

if __name__ == "__main__":
    which = sys.argv[1] if len(sys.argv) > 1 else "area"
    fn = {
        "area": b.run_area, "improper": b.run_improper, "limit": b.run_limit,
        "tangent": b.run_tangent, "substitution": b.run_substitution,
        "by_parts": b.run_by_parts, "riemann": b.run_riemann, "volume": b.run_volume,
    }.get(which)
    if fn is None:
        raise SystemExit(f"unknown solver {which}")
    fn()
