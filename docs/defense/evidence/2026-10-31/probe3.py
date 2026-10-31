import sympy as sp
from utils import riemann_solver as R, area_solver as A, substitution_solver as S, tangent_solver as T

x = sp.Symbol('x')
print("=== R1: Riemann error_pct when exact == 0 ===")
d = R.compute_riemann("x", -1, 1, 1, "left")
print("f=x on [-1,1] n=1 left:", {k: d[k] for k in ("result", "exact_integral", "error_signed", "error_pct", "direction")})
d = R.compute_riemann("x", -1, 1, 8, "left")
print("f=x on [-1,1] n=8 left:", {k: d[k] for k in ("result", "exact_integral", "error_signed", "error_pct", "direction")})

print()
print("=== R2: analytical_limit ignores the chosen method ===")
for m in ("left", "right", "midpoint"):
    d = R.compute_riemann("x^2", 0, 1, 4, m)
    al = d.get("analytical_limit") or {}
    print(f"  method={m:9s} sum_rn={al.get('sum_rn_latex')}  limit={al.get('limit_latex')}")

print()
print("=== R3: discontinuity not verified; 'convergence' claim printed anyway ===")
d = R.compute_riemann("1/(x-1/2)", 0, 1, 3, "midpoint")
print("f=1/(x-1/2) n=3 midpoint:", d["ok"], d["result"], d["exact_integral"])
print("  note step:", d["steps"][5][-120:] if d["steps"] else None)

print()
print("=== R4: rounding of Delta x in the displayed derivation ===")
d = R.compute_riemann("x^2", 0, 1, 3, "left")
print("n=3, dx=1/3 ->")
for s in d["steps"][:5]:
    print("   *", s.replace("\n", " | ")[:200])

print()
print("=== A1: high-frequency crossings missed ===")
for f in ("sin(200*x)", "sin(300*x)"):
    d = A.compute_area_between(f, "0", 0, 1)
    print(f"  {f}: A={d['result']}  ncross={len(d.get('crossings') or [])}  (exact 2/pi=0.63662)")

print()
print("=== A2: identical curves / nested ===")
print("  x vs x+1 on [0,1]:", A.compute_area_between("x", "x+1", 0, 1)["result"], "(expect 1)")
print("  exp(x) vs 0 on [-1,1]:", A.compute_area_between("exp(x)", "0", -1, 1)["result"])

print()
print("=== S1: mislabelled non-elementary ===")
for e in ("erf(x)", "Si(x)", "x*exp(-x^2)"):
    d = S.solve_substitution(e)
    print(f"  int {e} dx: status={d.get('status')} method={d.get('method')} -> {str(d.get('result'))[:70]}")

print()
print("=== T1: piecewise seam vs abs ===")
for e, a in (("Abs(x)", 0), ("Piecewise((x, x<1), (x**2, True))", 1)):
    d = T.compute_tangent(e, a)
    print(f"  {e} at {a}: status={d.get('status')} slope={d.get('result')} latex={d.get('latex')}")

print()
print("=== T2: rational point reconstruction from float ===")
d = T.compute_tangent("x^2", 0.30000000000000004)
print("  x^2 at 0.30000000000000004 -> latex:", d.get("latex")[:120])
