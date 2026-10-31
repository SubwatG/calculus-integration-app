import math
import sympy as sp
from utils import area_solver as A

x = sp.Symbol('x', real=True)
d = A.compute_area_between("sin(50*x)", "0", 0, 1)
cr = d["crossings"]
print("crossings found:", len(cr))
print("first few:", cr[:4], "exact k*pi/50:", [float(k * math.pi / 50) for k in range(1, 5)])
print("max dev from k*pi/50:", max(abs(c - float((i + 1) * math.pi / 50)) for i, c in enumerate(cr)))
print("A =", d["result"], " exact 2/pi =", 2 / math.pi, " rel err", abs(d["result"] - 2 / math.pi) / (2 / math.pi))

cuts = [sp.Rational(0)] + [sp.Rational(str(round(r, 6))) for r in cr] + [sp.Rational(1)]
tot = sp.S.Zero
for lo, hi in zip(cuts, cuts[1:]):
    v = sp.integrate(sp.sin(50 * x), (x, lo, hi))
    tot += abs(v)
print("recomputed the same way with exact rational cuts:", float(tot.evalf()))
print("sum of |piece| with true cuts (k*pi/50):",
      float(sum(abs(sp.integrate(sp.sin(50 * x), (x, sp.Rational(0), sp.pi / 50))) for _ in range(16)).evalf()))
print("n pieces:", len(cuts) - 1)
