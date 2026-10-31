import sympy as sp
from utils import limit_solver as L, tangent_solver as T

xr = sp.Symbol('x', real=True)
h = sp.Symbol('h', real=True, positive=True)
pw = sp.Piecewise((xr, xr < 1), (xr ** 2, True))
fl = sp.limit((pw.subs(xr, 1 - h) - 1) / (-h), h, 0, '+')
fr = sp.limit((pw.subs(xr, 1 + h) - 1) / h, h, 0, '+')
print("piecewise seam at 1: f'_-(1) =", fl, " f'_+(1) =", fr)

for a in (0.001, 0.0, 0.0004):
    d = L.compute_limit_near("sqrt(x-0.0005)", a)
    print(f"\nlim sqrt(x-0.0005) -> {a}: status={d.get('status')} result={d.get('result')}")
    print("   latex:", d.get("latex"))
    print("   step2:", d["steps"][1].replace("\n", " | ")[:220] if len(d["steps"]) > 1 else "")

d = T.compute_tangent("Piecewise((x, x<1), (x**2, True))", 1)
print("\nAPP tangent at seam:", d.get("status"), d.get("latex"))
print("   step7:", d["steps"][-1][:200] if d.get("steps") else None)
