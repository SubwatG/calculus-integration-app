import sympy as sp
from utils import improper_solver as I, area_solver as A, riemann_solver as R

x = sp.Symbol('x')
e = 1 / (x ** 5 - x + sp.Rational(1, 5))
print("denom =", x**5 - x + sp.Rational(1, 5))
print("solve:", sp.solve(x**5 - x + sp.Rational(1, 5), x))
print("real roots in (-1,1):", [float(r) for r in sp.Poly(x**5 - x + sp.Rational(1,5), x).real_roots() if -1 < float(r) < 1])
print("raw SymPy integral on [-1,1]:", sp.integrate(e, (x, -1, 1)))
print("numeric NIntegral (mpmath quad, pole-splitting skipped):", sp.Integral(e, (x, -1, 1)).evalf())

d = I.compute_improper("1/(x**5-x+1/5)", -1, 1)
print("\nAPP verdict:", d.get("status"), d.get("result"), "|", (d.get("latex") or "")[:100])
print("steps tail:", [s[:120] for s in d.get("steps", [])][-2:])

print("\n=== Riemann on the same pole ===")
d = R.compute_riemann("1/(x**5-x+1/5)", -1, 1, 10, "midpoint")
print("ok:", d["ok"], "result:", d["result"], "exact:", d["exact_integral"], "err:", d.get("error"))

print("\n=== Area on a pole hidden from solve ===")
d = A.compute_area_between("1/(x**5-x+1/5)", "0", -1, 1)
print("ok:", d["ok"], "A:", d["result"], "err:", (d.get("error") or "")[:90])
