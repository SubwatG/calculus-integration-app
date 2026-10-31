import sympy as sp
from utils import tangent_solver as T, limit_solver as L, area_solver as A, substitution_solver as S

x = sp.Symbol('x', real=True)
print("=== why Abs(x) at 0 is judged non_differentiable ===")
e = sp.Abs(x)
df = sp.diff(e, x)
print("df =", df)
try:
    v = df.subs(x, 0)
    print("df(0) =", v, "is_real:", getattr(v, 'is_real', None), "is_finite:", getattr(v, 'is_finite', None))
except Exception as ex:
    print("subs raised:", type(ex).__name__, ex)

print()
print("=== piecewise derivative at the seam ===")
pw = sp.Piecewise((x, x < 1), (x**2, True))
print("f =", pw, "| f(1) =", pw.subs(x, 1))
d = sp.diff(pw, x)
print("f' =", d, "| f'(1) =", d.subs(x, 1))
print("left lim:", sp.limit((pw.subs(x, 1 + sp.Symbol('h', real=True)) - 1) / sp.Symbol('h', real=True), sp.Symbol('h', real=True), 0, '-'))
print("right lim:", sp.limit((pw.subs(x, 1 + sp.Symbol('h', real=True)) - 1) / sp.Symbol('h', real=True), sp.Symbol('h', real=True), 0, '+'))

print()
print("=== limit solver: fixed delta=0.01 domain probe ===")
cases = [
    ("sqrt(x-0.0005)", 0.0),
    ("sqrt(x)", 0.0),
    ("ln(x)", 0.0),
    ("(1-cos(x))/x^2", 0.0),
    ("x*sin(1/x)", 0.0),
    ("sin(x)/x", 0.0),
    ("(x^2-4)/(x-2)", 2.0),
    ("1/x", 0.0),
    ("x^2", 2.0),
    ("(x**2)**(1/3)", 0.0),
]
for e, a in cases:
    d = L.compute_limit_near(e, a)
    print(f"--- lim {e} -> {a}: status={d.get('status')} result={d.get('result')} ok={d.get('ok')} err={d.get('error')}")

print()
print("=== discontinuous but f(a) defined ===")
d = L.compute_limit_near("Piecewise((0, x==0), (1, True))", 0)
print("piecewise jump at 0:", d.get("status"), d.get("result"))
d = L.compute_limit_near("sqrt(x^2)/x", 0)
print("|x|/x at 0:", d.get("status"), d.get("result"), "| latex:", d.get("latex"))

print()
print("=== substitution / non-elementary ===")
for e in ["exp(-x^2)", "sin(x^2)", "x^x", "1/ln(x)", "exp(x^2)", "sin(x)/x"]:
    d = S.solve_substitution(e)
    print(f"--- int {e} dx: status={d.get('status')} method={d.get('method')} result={str(d.get('result'))[:60]}")
