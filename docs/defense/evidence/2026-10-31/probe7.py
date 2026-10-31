import math
import sympy as sp

x = sp.Symbol('x')
print("=== float accumulation vs exact midpoint formula, f=x^2 on [0,2] ===")
for n in (100, 1000, 10000):
    a, b = 0.0, 2.0
    dx = (b - a) / n
    terms = [float((a + (i + 0.5) * dx) ** 2) for i in range(n)]
    naive = sum(terms) * dx
    fsum = math.fsum(terms) * dx
    exact = sp.Rational(8, 3)
    M_n = sp.Rational(8, 3) + sp.Rational(1, 6) * (sp.Rational(b - a, n)) ** 2  # midpoint error term for x^2
    print(f"  n={n:6d} naive={naive:.15f} fsum={fsum:.15f} err_naive={float(naive-exact):+.3e} "
          f"err_fsum={float(fsum-exact):+.3e} |M_n-8/3|={float(M_n-exact):.3e} "
          f"rel={abs(float(fsum-exact)/float(exact)):.2e}")
