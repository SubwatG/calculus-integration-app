from utils import riemann_solver as R

d = R.compute_riemann("x**2", 0, 1, 3, "left")
print("=== displayed derivation, f=x^2 on [0,1], n=3 (dx = 1/3) ===")
for i, s in enumerate(d["steps"], 1):
    print(f"[{i}]", s.replace("\n", "  ||  ")[:400])
print()
print("float total:", d["result"], " exact:", d["exact_integral"])
print("sum_heights:", d["sum_heights"], " -> 0.3333 * 1.8519 ?", 0.3333 * 1.8519)

d2 = R.compute_riemann("x**2", 0, 1, 3, "midpoint")
print("\n=== midpoint form check (n=3) ===")
print(d2["steps"][1].replace("\n", " || ")[:300])
print(d2["steps"][2].replace("\n", " || ")[:300])
