import sys
from pathlib import Path
ROOT = Path('/home/kitti/Documents/GitHub/calculus-integration-app')
sys.path.insert(0, str(ROOT))

import sympy as sp
from utils.tangent_solver import compute_tangent
from utils.limit_solver import compute_limit_near
from utils.riemann_solver import compute_riemann
from utils.substitution_solver import solve_substitution
from utils.area_solver import compute_area_between
from utils.improper_solver import compute_improper
from utils.volume_solver import compute_volume
from utils.sympy_solver import integrate, differentiate, compute_limit

def test_module(name, solver_func, test_cases):
    print(f"\n{'='*70}\n[MODULE STRESS-TEST] {name}\n{'='*70}")
    for title, args in test_cases:
        try:
            res = solver_func(*args)
            ok = res.get('ok')
            result = res.get('result')
            status = res.get('status', 'N/A')
            error = res.get('error')
            latex = res.get('latex', '')[:60]
            print(f"CASE: {title}")
            print(f"  Inputs : {args}")
            print(f"  Output : ok={ok}, status={status}, result={result}")
            if error:
                print(f"  Error  : {error}")
            else:
                print(f"  LaTeX  : {latex}...")
        except Exception as e:
            print(f"CASE: {title}")
            print(f"  Inputs : {args}")
            print(f"  CRASH  : {type(e).__name__}: {e}")

# 1. Tangent
tangent_cases = [
    ("Normal: Polynomial", ("x**3 - 3*x + 2", 1.0)),
    ("Normal: Trig", ("sin(x)*cos(x)", 0.0)),
    ("Hard: Rational with quotient", ("(x**2 + 1)/(x - 1)", 2.0)),
    ("Boundary: Inflection point (m=0)", ("x**3", 0.0)),
    ("Boundary: DNE Corner/Cusp", ("abs(x)", 0.0)),
    ("Boundary: Vertical tangent (m=oo)", ("x**(1/3)", 0.0)),
    ("Break: Outside domain", ("log(x)", -1.0)),
    ("Break: Removable singularity", ("(x**2 - 4)/(x - 2)", 2.0)),
]
test_module("1. Tangent & Derivative", compute_tangent, tangent_cases)

# 2. Limit
limit_cases = [
    ("Normal: Rational 0/0", ("(x**2 - 4)/(x - 2)", 2.0)),
    ("Normal: Trig 0/0", ("sin(x)/x", 0.0)),
    ("Hard: L'Hopital multiple times", ("(exp(x) - 1 - x)/x**2", 0.0)),
    ("Hard: 1^inf indeterminate", ("(1 + x)**(1/x)", 0.0)),
    ("Boundary: Left != Right (DNE)", ("1/x", 0.0)),
    ("Boundary: Infinite both sides (+oo)", ("1/x**2", 0.0)),
    ("Boundary: Infinite both sides (-oo)", ("-1/x**2", 0.0)),
    ("Boundary: Essential singularity (Oscillating)", ("sin(1/x)", 0.0)),
    ("Break: One-sided domain (sqrt(x) at 0)", ("sqrt(x)", 0.0)),
    ("Break: Pathological non-isolated", ("floor(x)", 2.0)),
]
test_module("2. Limit at a Point", compute_limit_near, limit_cases)

# 3. Riemann Sum
riemann_cases = [
    ("Normal: Parabola", ("x**2", 0.0, 2.0, 10, "midpoint")),
    ("Normal: Trig", ("sin(x)", 0.0, 3.14159, 20, "left")),
    ("Hard: Large n", ("x**3", 0.0, 1.0, 500, "right")),
    ("Boundary: High frequency oscillation", ("sin(50*x)", 0.0, 1.0, 100, "midpoint")),
    ("Boundary: Non-integer n rejection", ("x**2", 0.0, 1.0, 4.5, "left")),
    ("Break: Singularity inside interval", ("1/x", -1.0, 1.0, 10, "left")),
    ("Break: Negative domain for root", ("sqrt(x)", -2.0, 2.0, 10, "left")),
]
test_module("3. Riemann Sum", compute_riemann, riemann_cases)

# 4. Substitution / Indefinite Integral
substitution_cases = [
    ("Normal: Power of linear", ("(2*x + 3)**5",)),
    ("Normal: Classic u-sub", ("2*x*exp(x**2)",)),
    ("Hard: Trig substitution form", ("1/sqrt(1 - x**2)",)),
    ("Hard: By Parts standard", ("x*exp(x)",)),
    ("Hard: By Parts cyclic", ("exp(x)*sin(x)",)),
    ("Boundary: Partial fractions", ("1/(x**2 - 1)",)),
    ("Break: Non-elementary antiderivative (Gaussian)", ("exp(-x**2)",)),
    ("Break: Non-elementary Li(x)", ("1/ln(x)",)),
    ("Break: Non-elementary Si(x)", ("sin(x)/x",)),
]
test_module("4. Substitution & Integration Solver", solve_substitution, substitution_cases)

# 5. Area between curves
area_cases = [
    ("Normal: Two parabolas", ("2 - x**2", "x**2", -1.0, 1.0)),
    ("Normal: Swapped curves (f < g)", ("x**2", "x", 0.0, 1.0)),
    ("Hard: 3 Crossing points (odd symmetry)", ("x**3", "x", -1.0, 1.0)),
    ("Hard: Transcendental crossing", ("cos(x)", "sin(x)", 0.0, 3.14159)),
    ("Boundary: Disjoint constant curves", ("5", "1", 0.0, 2.0)),
    ("Boundary: Equal functions", ("x**2 + 1", "x**2 + 1", -2.0, 2.0)),
    ("Break: Discontinuous singular curve", ("1/x", "0", -1.0, 1.0)),
    ("Break: Non-polynomial irrational crossings", ("exp(x)", "x + 2", -1.0, 2.0)),
    ("Break: Non-elementary difference", ("exp(-x**2)", "0", 0.0, 1.0)),
]
test_module("5. Area Between Curves", compute_area_between, area_cases)

# 6. Improper Integrals
improper_cases = [
    ("Normal: Type 1 p-integral (p=2)", ("1/x**2", 1.0, None)),
    ("Normal: Exponential decay", ("exp(-x)", 0.0, None)),
    ("Normal: Finite bounds on proper range", ("1/x**2", 1.0, 2.0)),
    ("Hard: Type 2 singular endpoint (converges)", ("1/sqrt(x)", 0.0, 1.0)),
    ("Hard: Harmonic p=1 diverges", ("1/x", 1.0, None)),
    ("Hard: Singular endpoint diverges", ("1/x**2", 0.0, 1.0)),
    ("Boundary: Oscillating non-convergent", ("sin(x)", 0.0, None)),
    ("Boundary: Gaussian full line", ("exp(-x**2)", 0.0, None)),
    ("Break: Interior singularity (Cauchy PV trap)", ("1/x", -1.0, 1.0)),
    ("Break: Unresolved / non-elementary", ("1/(x**3 + 1)", 0.0, None)),
]
test_module("6. Improper Integrals", compute_improper, improper_cases)

# 7. Volume of Solids of Revolution
volume_cases = [
    ("Normal: Cone (R=x)", ("x", 0.0, 2.0, "disk")),
    ("Normal: Paraboloid (R=sqrt(x))", ("sqrt(x)", 0.0, 4.0, "disk")),
    ("Normal: Cylinder (Constant R=3)", ("3", 0.0, 4.0, "disk")),
    ("Hard: Sphere cap (R=sqrt(1-x^2))", ("sqrt(1 - x**2)", 0.0, 1.0, "disk")),
    ("Boundary: Negative function (squared becomes positive)", ("-x", 0.0, 2.0, "disk")),
    ("Boundary: Unsupported Washer method", ("x", 0.0, 2.0, "washer")),
    ("Break: Non-elementary volume integral", ("sqrt(exp(-x**2))", 0.0, 2.0, "disk")),
    ("Break: Infinite bound (not supported)", ("1/x", 1.0, float('inf'), "disk")),
    ("Break: Singularity on interval", ("1/x", -1.0, 1.0, "disk")),
]
test_module("7. Volume of Revolution", compute_volume, volume_cases)
