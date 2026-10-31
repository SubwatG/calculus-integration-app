import sympy as sp
from utils import riemann_solver as R, improper_solver as I, tangent_solver as T, area_solver as A, limit_solver as L


def show(tag, d, keys=("ok", "result", "status", "error", "exact_integral")):
    print(f"--- {tag}")
    print("   ", {k: d.get(k) for k in keys if k in d})


x = sp.Symbol('x')
print("=== SymPy ground truth ===")
print("integrate 1/(x-1/sqrt2) [0,1] =", sp.integrate(1 / (x - 1 / sp.sqrt(2)), (x, 0, 1)))
print("   numeric:", sp.integrate(1 / (x - 1 / sp.sqrt(2)), (x, 0, 1)).evalf())
print("integrate 1/(x-2)**2 over (-oo,oo) =", sp.integrate(1 / (x - 2) ** 2, (x, -sp.oo, sp.oo)))
print("integrate 1/x over (-1,1) =", sp.integrate(1 / x, (x, -1, 1)))

print()
print("=== Attacking the app ===")
d = R.compute_riemann("1/(x-sqrt(2)/2)", 0, 1, 10, "left")
show("riem 1/(x-sqrt2/2) [0,1] n=10 left", d)
if d.get("steps"):
    print("     steps[5]:", d["steps"][5][:260].replace("\n", " | "))

show("improper 1/(x-2)^2 on (-oo,oo)", I.compute_improper("1/(x-2)**2", "-inf", "inf"))
show("improper 1/(x-sqrt2/2) on [0,1]", I.compute_improper("1/(x-sqrt(2)/2)", 0, 1))
show("improper 1/x^2 on (-1,1)", I.compute_improper("1/x**2", -1, 1))
show("improper 1/x on (-1,1)", I.compute_improper("1/x", -1, 1))

print()
print("=== Tangent non-differentiable ===")
for e, a in [("Abs(x)", 0), ("(x**2)**(1/3)", 0), ("sqrt(Abs(x))", 0),
             ("Piecewise((x,x<1),(x**2,x>=1))", 1), ("x**(1/3)", 0)]:
    d = T.compute_tangent(e, a)
    print(f"--- tangent {e} at {a}: status={d.get('status')} result={d.get('result')} latex={d.get('latex')}")

print()
print("=== Area: undetected crossings ===")
for f, g, a, b in [("sin(50*x)", "0", 0, 1), ("x**2-1", "0", -2, 2), ("1/(x-1/sqrt(2))", "0", 0, 1)]:
    d = A.compute_area_between(f, g, a, b)
    print(f"--- area {f} vs {g} on [{a},{b}]: ok={d['ok']} A={d['result']} crossings={d.get('crossings')} err={d.get('error')}")
