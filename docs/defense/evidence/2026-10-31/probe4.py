import sympy as sp
from utils import improper_solver as I

x = sp.Symbol('x')
print("=== raw SymPy behaviour for poles away from the split point ===")
tests = ["1/(x-1)**2", "x/(x**2+1)", "sin(x)", "1/(x**2-1)", "1/(x-1)", "exp(-x**2)"]
for e in tests:
    ee = sp.sympify(e.replace("**", "^").replace("^", "**"))
    print(f"  int {e} over (-oo,oo) =", sp.integrate(ee, (x, -sp.oo, sp.oo)))

print()
print("=== app verdict ===")
for e in tests:
    d = I.compute_improper(e, "-inf", "inf")
    print(f"  {e:14s} status={d.get('status'):11s} result={d.get('result')} latex={d.get('latex')[:60]}")

print()
print("=== endpoint-singularity classification ===")
cases = [("1/sqrt(x)", 0, 1), ("ln(x)", 0, 1), ("1/x**2", 0, 1), ("1/sqrt(1-x**2)", -1, 1), ("1/x", 0, 1)]
for e, a, b in cases:
    d = I.compute_improper(e, a, b)
    print(f"  int {e:16s} [{a},{b}] status={d.get('status'):11s} result={d.get('result')}")
