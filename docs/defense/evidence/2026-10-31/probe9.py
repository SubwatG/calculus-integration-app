import math
from utils import area_solver as A

def true_abs_sin(k):
    """int_0^1 |sin(k x)| dx, computed as (1/k) * sum of half-period areas exactly."""
    n_half = int(math.floor(k / math.pi))
    total = n_half * 2.0
    rem_start = n_half * math.pi
    rem = k - rem_start
    # on [n_half*pi, k], sign of sin alternates; compute numerically with fine quadrature
    steps = 200000
    h = rem / steps
    s = 0.0
    for i in range(steps):
        u = rem_start + (i + 0.5) * h
        s += abs(math.sin(u)) * h
    return (total + s) / k

for k in (50, 200, 300):
    t = true_abs_sin(k)
    app = A.compute_area_between(f"sin({k}*x)", "0", 0, 1)
    ncross = len(app.get("crossings") or [])
    zeros = sum(1 for j in range(1, k) if j * math.pi / k < 1)
    print(f"k={k:4d} true={t:.10f} app={app['result']:.10f} rel_err={(app['result']-t)/t*100:+.3f}% "
          f"crossings_found={ncross}/{zeros}")
