---
topic: urgent-plan-limit-improper
date: 2026-10-05
model: ocg/deepseek-v4.1-flash
provider: 9router
scope: planning-only
bugs: browser-test-report.md#1 (two-sided limit), #4 (improper bounds/status)
---

# แผนแก้ไขเร่งด่วน: ลิมิตสองด้านและปริพันธ์ไม่ตรงแบบ

> **ร่างนี้ถูกแทนที่แล้ว ห้ามใช้ implementation snippets โดยตรง** ใช้ [แผนฉบับหลัก](../../_hermes/plans/urgent-calculus-correctness-plan.md) ซึ่งแก้ประเด็น numeric root fallback, การเก็บผลผิดเมื่อ DNE, และการแยก unknown domain จาก divergence แล้ว ร่างนี้เก็บไว้เป็นหลักฐานการตรวจเท่านั้น

เอกสารนี้เป็น **แผนอย่างเดียว (planning only)** สำหรับบั๊กเร่งด่วน 2 งานที่ยืนยันบนหน้าจอจริงใน
`docs/testing/browser-test-report.md` (ข้อ 1 ลิมิตสองด้าน และข้อ 4 ขอบเขต/สถานะปริพันธ์ไม่ตรงแบบ)

- **ยังไม่แก้โค้ดผลิตภัณฑ์ ไม่แก้ test เดิม และไม่ commit/push ในเอกสารนี้**
- แต่ละงานเป็น self-contained: มี signature, returned keys, implementation snippet,
  pytest regression snippet, เกณฑ์ผ่าน และ browser acceptance
- ใช้ helper seam เดิมในไฟล์ (`_parse_input`, `TRANSFORMATIONS`, `LOCAL_MATH_DICT`, `X`,
  `sp.limit`, `sp.integrate`, `render_latex`, `render_steps`) ไม่เพิ่ม dependency ภายนอก
  ไม่แตะ parser/ความปลอดภัย ไม่รื้อ `_parse_input`

## 1. สถานะที่เสนอ (status vocabulary)

เพิ่มคีย์ `status` แบบ **additive** ให้ทุก dict ที่คืนค่า (คีย์เดิมทั้งหมดคงอยู่และรูปร่างเดิม)
ค่า `status` เป็นสตริงจำกัดชุดเดียว ใช้ร่วมกันทั้งสองงาน:

| status | ความหมาย | ใช้กับงาน |
|---|---|---|
| `finite` | ลู่เข้าสู่ค่าจริงจำกัด / ปริพันธ์ลู่เข้าเป็นจำนวนจริงจำกัด | A, B |
| `infinite` | ลิมิตสองด้านเท่ากันและเป็น $\pm\infty$ ค่าเดียวที่นิยามได้ | A |
| `dne` | ลิมิตสองด้านไม่มีค่า (ลิมิตซ้ายไม่เท่าขวา รวมกรณี $-\infty$ กับ $+\infty$) | A |
| `divergent` | ปริพันธ์ลู่ออก (ค่าเป็นอนันต์ ไม่จำกัด หรือแกว่งไม่ลู่เข้า) | B |
| `unsupported` | ยังตัดสินไม่ได้ด้วย seam ปัจจุบัน (SymPy ไม่ประเมิน, ไม่ใช่จำนวนจริง, มีสัญลักษณ์อิสระ) | A, B |
| `error` | parse ไม่ได้ หรือเกิด exception ระหว่างคำนวณ | A, B |

หลักการ: `status` **ไม่แทนที่** `result` เดิม — `result` ยังคงเป็น `float | None`
(limit) หรือ `sympy.Expr | None` (symbolic) เหมือนเดิม `status` เป็นข้อมูลวินิจฉัยเพิ่ม

---

## 2. งาน A: ลิมิตสองด้าน (1/x ที่ 0 ต้องเป็น DNE)

### 2.1 หลักฐานบั๊กจริง (รันจาก source ปัจจุบัน)

```text
compute_limit_near("1/x", 0)
  result = None
  latex  = \lim_{x \to 0} \frac{1}{x} = \infty
  steps[-1] = "เปรียบเทียบและสรุปค่าลิมิตสองด้าน:
               \lim_{x \to 0^-} f(x) = \lim_{x \to 0^+} f(x) = \infty
               \implies \lim_{x \to 0} (\frac{1}{x}) = \infty"
```

ลิมิตซ้าย ($-\infty$) กับขวา ($+\infty$) ไม่เท่ากัน แต่ขั้นสรุป **hardcode** ว่าทั้งสองข้างเท่ากัน
(ดู `utils/limit_solver.py` บรรทัดที่สร้าง `steps[-1]` ซึ่ง interpolate `lim_val` อย่างเดียว
ไม่ใช้ `lim_left`/`lim_right`) ผลคือหน้าจอสรุปผิดว่าเป็นลิมิตสองด้านที่มีค่า

### 2.2 Signature (ไม่เปลี่ยน)

```python
# utils/limit_solver.py
def compute_limit_near(expr_str: str, a: float) -> dict:
    ...

# utils/sympy_solver.py
def compute_limit(expr_str: str, point: float | int = 0) -> dict[str, Any]:
    ...
```

### 2.3 Returned keys (คงเดิมทุกคีย์ + เพิ่ม `status`)

```python
# compute_limit_near -> dict
{
    "ok": bool,          # คงเดิม
    "result": float | None,   # คงเดิม: เป็น float เฉพาะเมื่อ status == "finite" เท่านั้น (ไม่มี false precision)
    "latex": str,        # คงเดิม
    "steps": list[str],  # คงเดิม (>= 4 เสมอ)
    "expr": sp.Expr | None,   # คงเดิม
    "error": str | None,      # คงเดิม
    "status": str,       # ใหม่: "finite" | "infinite" | "dne" | "unsupported" | "error"
}

# compute_limit -> dict  (คงผลลัพธ์ symbolic เดิมไว้ครบ)
{
    "ok": bool,             # คงเดิม
    "result": sp.Expr | None,   # คงเดิม: sympy object รูปเดิม (เช่น oo, Rational) ห้ามแปลงเป็น float
    "latex": str, "steps": list[str], "error": str | None,   # คงเดิม
    "status": str,          # ใหม่
}
```

> รูปร่างผลลัพธ์ต่างกันโดยเจตนา: `compute_limit` คืน **symbolic** (`sympy.Expr`)
> ส่วน `compute_limit_near` คืน **float** ให้คงไว้ทั้งคู่

### 2.4 Implementation snippet (minimal)

เพิ่ม private helper ในทั้งสองโมดูล (คัดลอกแบบเดียวกับที่ `_parse_input` ถูกคัดลอกอยู่แล้ว
เพื่อไม่สร้าง import edge ใหม่ระหว่างโมดูล):

```python
def _classify_limit(lim_left: sp.Expr, lim_right: sp.Expr) -> str:
    """Two-sided limit status. Additive only; never changes result."""
    if not (getattr(lim_left, "is_number", False) and getattr(lim_right, "is_number", False)):
        return "unsupported"
    if lim_left != lim_right:                 # includes -oo vs +oo
        return "dne"
    if lim_left in (sp.oo, -sp.oo):           # both sides same signed infinity
        return "infinite"
    if getattr(lim_left, "is_finite", False) is True and getattr(lim_left, "is_real", False) is True:
        return "finite"
    return "unsupported"
```

`utils/limit_solver.py` — หลังคำนวณ `lim_left`/`lim_right` แล้ว:

```python
        lim_val = sp.limit(expr, X, a)
        lim_left = sp.limit(expr, X, a, dir="-")
        lim_right = sp.limit(expr, X, a, dir="+")
        status = _classify_limit(lim_left, lim_right)

        steps = [
            f"กำหนดโจทย์ลิมิตที่ต้องการหา: \\lim_{{x \\to {a}}} \\left({sp.latex(expr)}\\right)",
            f"พิจารณาลิมิตทางซ้าย (Left-hand limit): \\lim_{{x \\to {a}^-}} \\left({sp.latex(expr)}\\right) = {sp.latex(lim_left)}",
            f"พิจารณาลิมิตทางขวา (Right-hand limit): \\lim_{{x \\to {a}^+}} \\left({sp.latex(expr)}\\right) = {sp.latex(lim_right)}",
        ]
        # FIX: summary must reflect the actual classification (no blind equality claim)
        if status == "dne":
            steps.append(
                "สรุปผล (ลิมิตซ้ายไม่เท่ากับลิมิตขวา จึงไม่มีลิมิตสองด้าน): "
                f"\\lim_{{x \\to {a}^-}} f(x) = {sp.latex(lim_left)} \\neq "
                f"\\lim_{{x \\to {a}^+}} f(x) = {sp.latex(lim_right)}"
            )
        elif status == "infinite":
            steps.append(
                "สรุปผล (ทั้งสองข้างลู่ไปอนันต์ค่าเดียวกัน): "
                f"\\lim_{{x \\to {a}}} \\left({sp.latex(expr)}\\right) = {sp.latex(lim_val)}"
            )
        else:
            steps.append(
                "เปรียบเทียบและสรุปค่าลิมิตสองด้าน: "
                f"\\lim_{{x \\to {a}^-}} f(x) = \\lim_{{x \\to {a}^+}} f(x) = {sp.latex(lim_val)} "
                f"\\implies \\lim_{{x \\to {a}}} \\left({sp.latex(expr)}\\right) = {sp.latex(lim_val)}"
            )

        return {
            "ok": True,
            "result": float(lim_val) if lim_val.is_number and lim_val.is_real else None,
            "latex": f"\\lim_{{x \\to {a}}} {sp.latex(expr)} = {sp.latex(lim_val)}",
            "steps": steps,
            "expr": expr,
            "error": None,
            "status": status,
        }
```

error path เดิม เพิ่ม `"status": "error"` หนึ่งบรรทัด

`utils/sympy_solver.py::compute_limit` — **ห้ามแก้ `result`** แค่เพิ่ม `status`:

```python
def compute_limit(expr_str: str, point: float | int = 0) -> dict[str, Any]:
    x = sp.Symbol("x")
    try:
        expr = _parse_input(expr_str)
        result = sp.limit(expr, x, point)          # symbolic result คงเดิม
        try:
            left = sp.limit(expr, x, point, dir="-")
            right = sp.limit(expr, x, point, dir="+")
            status = _classify_limit(left, right)
        except Exception:
            status = "unsupported"
        steps = ["คำนวณด้วย SymPy (เครื่องมือเชิงสัญลักษณ์)"]
        latex_str = sp.latex(result)
        return {
            "ok": True, "result": result, "latex": latex_str,
            "steps": steps, "error": None, "status": status,
        }
    except Exception:
        return {
            "ok": False, "result": None, "latex": "", "steps": [],
            "error": "ไม่สามารถอ่านนิพจน์ได้ กรุณาตรวจสอบรูปแบบ เช่น x**2, sin(x), (x**2-4)/(x-2)",
            "status": "error",
        }
```

เหตุที่ `result` ของ `compute_limit("1/x", 0)` ยังเป็น `oo` ได้แม้เป็น `dne`:
SymPy คืน `oo` สำหรับสองด้าน แต่ `status` บอกความจริงว่าไม่มีลิมิตสองด้าน
(คีย์ `result` จึงถูกเก็บรูปเดิมเพื่อ backward compatibility ตามข้อกำหนด)

### 2.5 Regression pytest snippet (ต่อท้ายไฟล์เดิม)

```python
# tests/test_limit_solver.py
class TestComputeLimitNearStatus:
    def test_dne_when_one_sided_limits_differ(self):
        res = compute_limit_near("1/x", 0)
        assert res["ok"] is True
        assert res["status"] == "dne"
        assert res["result"] is None
        # สรุปต้องไม่ยืนยันว่าทั้งสองข้างเท่ากัน
        assert "\\neq" in res["steps"][-1]
        assert "ไม่มีลิมิต" in res["steps"][-1]

    def test_infinite_when_both_sides_same_infinity(self):
        res = compute_limit_near("1/x**2", 0)
        assert res["ok"] is True
        assert res["status"] == "infinite"
        assert res["result"] is None
        assert len(res["steps"]) >= 4

    def test_finite_status_preserved(self):
        res = compute_limit_near("sin(x)/x", 0)
        assert res["status"] == "finite"
        assert res["result"] == pytest.approx(1.0)

    def test_removable_singularity_finite(self):
        res = compute_limit_near("(x**2-4)/(x-2)", 2)
        assert res["status"] == "finite"
        assert res["result"] == 4.0

    def test_error_status_on_empty_input(self):
        res = compute_limit_near("", 0)
        assert res["ok"] is False
        assert res["status"] == "error"
```

```python
# tests/test_sympy_solver.py
class TestComputeLimitSymbolicStatus:
    def test_symbolic_result_preserved_for_dne(self):
        res = compute_limit("1/x", 0)
        assert res["ok"] is True
        # result ยังเป็น sympy object รูปเดิม (ไม่ถูกแปลงเป็น float)
        assert isinstance(res["result"], sp.Basic)
        assert str(res["result"]) in ("oo", "-oo", "zoo")
        assert res["status"] == "dne"

    def test_finite_symbolic_status(self):
        res = compute_limit("x**2", 3)
        assert res["status"] == "finite"
        assert expr_eq(res["result"], "9")

    def test_infinite_status(self):
        res = compute_limit("1/x**2", 0)
        assert res["status"] == "infinite"

    def test_error_status(self):
        res = compute_limit("", 0)
        assert res["status"] == "error"
```

> test เดิม (`test_limit_to_zero` ที่ยอมรับ `oo`/`-oo`/`zoo`, `test_compute_limit_near_*`)
> ยังผ่านทั้งหมดเพราะ `result` และคีย์เดิมไม่ถูกแตะ

### 2.6 Page adjustment (additive, ถ้าต้องการข้อความชัดเจน)

`pages/limit_approach.py` แทนบรรทัด metric ด้วยการใช้ `status` (เดิมเดาว่า
`result is None` = "หาค่าไม่ได้ / อนันต์" ซึ่งกำกวม):

```python
STATUS_LABEL = {
    "finite": lambda v: f"{v:.4f}",
    "infinite": lambda v: "∞ (อนันต์)",      # ข้อความ UI ภาษาไทย
    "dne": lambda v: "ไม่มีลิมิต (DNE)",
    "unsupported": lambda v: "ยังตัดสินไม่ได้",
    "error": lambda v: "เกิดข้อผิดพลาด",
}
...
status = res.get("status", "unsupported")
l_str = STATUS_LABEL.get(status, lambda v: "N/A")(res["result"])
st.metric(label="ค่าลิมิตสองด้าน L", value=l_str)
```

### 2.7 เกณฑ์ผ่านงาน A

- `1/x` ที่ 0 → `status == "dne"`, `result is None`, ขั้นสรุปมี `\neq` และไม่มีข้อความอ้างว่าสองข้างเท่ากัน
- `1/x**2` ที่ 0 → `status == "infinite"` (สองข้างลู่ $+\infty$ เดียวกัน)
- `sin(x)/x` ที่ 0 → `status == "finite"`, `result == 1.0` (ไม่ regress)
- `(x**2-4)/(x-2)` ที่ 2 → `status == "finite"`, `result == 4.0`
- input ว่าง → `ok False`, `status == "error"`
- คีย์เดิมทั้ง 6 ยังอยู่และ `len(steps) >= 4` ทุกกรณีปกติ

---

## 3. งาน B: ปริพันธ์ไม่ตรงแบบ (ขอบบนจริง + สถานะลู่ออก)

### 3.1 หลักฐานบั๊กจริง (รันจาก source ปัจจุบัน)

```text
compute_improper("1/x**2", 1, 2)
  result = 0.5        # ค่าถูก
  latex  = \int_{1}^{\infty} \frac{1}{x^{2}} \, dx = \frac{1}{2}   # ผิด: ขอบบน hardcode \infty

compute_improper("1/x", 1, None)
  ok = True
  result = None
  latex  = \int_{1}^{\infty} \frac{1}{x} \, dx = \infty   # ไม่มีสถานะ "ลู่ออก" ชัดเจน
```

สาเหตุ: บรรทัด `latex` ใน `utils/improper_solver.py` hardcode `^\\{\\infty\\}` ไม่ใช้ `bound_latex`
และไม่มีคีย์สถานะลู่เข้า/ลู่ออก หน้า `pages/improper_integrals.py` จึงแสดงค่า/สมการโดยไม่เตือน

### 3.2 Signature (ไม่เปลี่ยน)

```python
# utils/improper_solver.py
def compute_improper(expr_str: str, a: float, b: float | None = None) -> dict:
    ...
```

### 3.3 Returned keys (คงเดิมทุกคีย์ + เพิ่ม `status`)

```python
{
    "ok": bool,            # คงเดิม: True แม้ลู่ออก (คำนวณสำเร็จ) / False เฉพาะ error
    "result": float | None,     # คงเดิม: float เฉพาะเมื่อ status == "finite"; ลู่ออก/ไม่รองรับ = None
    "latex": str,          # คงเดิม (ฟอร์แมตเปลี่ยนให้ใช้ขอบบนจริง)
    "steps": list[str],    # คงเดิม (>= 3)
    "expr": sp.Expr | None,     # คงเดิม
    "error": str | None,        # คงเดิม
    "status": str,         # ใหม่: "finite" | "divergent" | "unsupported" | "error"
}
```

### 3.4 Implementation snippet (minimal)

```python
from sympy.calculus.accumulationbounds import AccumulationBounds  # stdlib sympy ไม่ใช่ dependency ใหม่


def _classify_improper(res_val: sp.Expr) -> str:
    """Improper-integral status. Additive only; never changes result value."""
    if isinstance(res_val, sp.Integral):          # SymPy left it unevaluated
        return "unsupported"
    if res_val is sp.nan or res_val.has(sp.zoo, sp.nan):
        return "divergent"                        # complex infinity / undefined
    if isinstance(res_val, AccumulationBounds):
        return "divergent"                        # oscillatory, no finite limit (e.g. sin(x) on [0, oo))
    if res_val.has(sp.oo, -sp.oo):
        return "divergent"                        # signed infinity (incl. -li(2)+oo)
    if getattr(res_val, "is_finite", False) is True and getattr(res_val, "is_real", False) is True:
        return "finite"
    return "unsupported"


def compute_improper(expr_str: str, a: float, b: float | None = None) -> dict:
    try:
        expr = _parse_input(expr_str)
        upper = sp.oo if b is None else b
        res_val = sp.integrate(expr, (X, a, upper))

        lower_latex = sp.latex(sp.nsimplify(a))
        bound_latex = "\\infty" if b is None else sp.latex(sp.nsimplify(b))

        status = _classify_improper(res_val)
        if status == "finite":
            result = float(res_val) if res_val.is_real else None
            value_latex = sp.latex(res_val)
        elif status == "divergent":
            result = None
            value_latex = "\\text{diverges}"
        else:  # unsupported
            result = None
            value_latex = "\\text{unsupported}"

        steps = [
            f"กำหนดอินทิกรัลไม่ตรงแบบ: \\int_{{{lower_latex}}}^{{{bound_latex}}} \\left({sp.latex(expr)}\\right) \\, dx",
            f"แปลงเป็นรูปลิมิตของอินทิกรัลจำกัดเขต: \\lim_{{t \\to {bound_latex}}} \\int_{{{lower_latex}}}^{{t}} \\left({sp.latex(expr)}\\right) \\, dx",
            f"คำนวณผลลัพธ์ลิมิต: \\int_{{{lower_latex}}}^{{{bound_latex}}} \\left({sp.latex(expr)}\\right) \\, dx = {value_latex}",
        ]
        return {
            "ok": True,
            "result": result,
            "latex": f"\\int_{{{lower_latex}}}^{{{bound_latex}}} {sp.latex(expr)} \\, dx = {value_latex}",
            "steps": steps,
            "expr": expr,
            "error": None,
            "status": status,
        }
    except Exception as e:
        return {
            "ok": False, "result": None, "latex": "", "steps": [],
            "expr": None, "error": f"ไม่สามารถคำนวณได้: {e}", "status": "error",
        }
```

### 3.5 Page adjustment (additive)

`pages/improper_integrals.py` — หลัง `render_latex(res["latex"])` เพิ่ม:

```python
        status = res.get("status")
        if status == "divergent":
            st.warning("ปริพันธ์นี้ลู่ออก (divergent) ไม่ลู่เข้าสู่ค่าจำกัด")
        elif status == "unsupported":
            st.info("ยังไม่สามารถหาค่าปริพันธ์นี้ในรูปแบบปิดได้")
```

### 3.6 Regression pytest snippet (ต่อท้ายไฟล์เดิม)

```python
# tests/test_improper_solver.py
class TestComputeImproperBoundsAndStatus:
    def test_finite_bounds_use_actual_upper_latex(self):
        res = compute_improper("1/x**2", 1, 2)
        assert res["ok"] is True
        assert res["status"] == "finite"
        assert res["result"] == pytest.approx(0.5)
        assert "\\infty" not in res["latex"]      # ต้องไม่แสดง \infty เมื่อขอบบนจำกัด
        assert "2" in res["latex"]

    def test_infinite_upper_convergent(self):
        res = compute_improper("1/x**2", 1, None)
        assert res["status"] == "finite"
        assert res["result"] == pytest.approx(1.0)
        assert "\\infty" in res["latex"]

    def test_harmonic_on_infinite_interval_diverges(self):
        res = compute_improper("1/x", 1, None)
        assert res["ok"] is True                    # คำนวณสำเร็จ แต่ผลลู่ออก
        assert res["status"] == "divergent"
        assert res["result"] is None

    def test_singular_endpoint_finite_range_diverges(self):
        res = compute_improper("1/x", 0, 1)
        assert res["status"] == "divergent"
        assert res["result"] is None

    def test_singular_endpoint_convergent(self):
        res = compute_improper("1/sqrt(x)", 0, 1)
        assert res["status"] == "finite"
        assert res["result"] == pytest.approx(2.0)

    def test_oscillatory_diverges(self):
        res = compute_improper("sin(x)", 0, None)
        assert res["status"] == "divergent"
        assert res["result"] is None

    def test_unsupported_when_unevaluated(self):
        import sympy as sp
        from utils.improper_solver import _classify_improper
        x = sp.Symbol("x")
        unevaluated = sp.Integral(1 / sp.log(x), (x, 2, sp.oo))
        assert _classify_improper(unevaluated) == "unsupported"

    def test_error_status_on_empty_input(self):
        res = compute_improper("", 1, None)
        assert res["ok"] is False
        assert res["status"] == "error"
```

> `_classify_improper` ผ่านการตรวจกับ SymPy จริงแล้ว: `1/x**2 [1,2] -> finite`,
> `1/x [1,oo) -> divergent`, `1/x [0,1] -> divergent`, `1/sqrt(x) [0,1] -> finite`,
> `sin(x) [0,oo) -> divergent`, unevaluated Integral -> unsupported

### 3.7 เกณฑ์ผ่านงาน B

- `1/x**2` บน `[1, 2]` → `latex` มีขอบบน `2`, ไม่มี `\infty`, `result == 0.5`, `status == "finite"`
- `1/x` บน `[1, ∞)` → `status == "divergent"`, หน้าแสดงคำเตือนลู่ออก, ไม่มีค่า float
- `1/x` บน `[0, 1]` → `status == "divergent"`
- `1/sqrt(x)` บน `[0, 1]` → `status == "finite"`, `result == 2.0`
- input ว่าง → `ok False`, `status == "error"`
- คีย์เดิมทั้ง 6 ยังอยู่และ `len(steps) >= 3`

---

## 4. Browser repro / acceptance

ขั้นตอนทดสอบหน้าจอจริง (ทำหลัง implement เท่านั้น — เอกสารนี้ไม่เปิด server):

1. เปิดแอป: `.venv/bin/python -m streamlit run app.py --server.address 127.0.0.1 --server.port 8502 --server.headless true --browser.gatherUsageStats false`
   รอ health endpoint `ok` แล้วเปิด `http://127.0.0.1:8502`
2. กรอกด้วย native HTMLInputElement value setter + ส่ง `input` event + กด Enter
   (ตามวิธีใน `browser-test-report.md` — helper ตรง ๆ บางครั้ง Streamlit ยังไม่รับค่า)
   แล้วอ่านกลับ: ค่าใน input, KaTeX annotation ของสมการ และข้อความ metric/warning

| # | หน้า | input | ผลที่ต้องเห็น (หลังแก้) |
|---|---|---|---|
| 1 | ลิมิตเข้าใกล้จุด | f=`1/x`, a=`0` | ไม่มีขั้นสรุปอ้างว่าสองข้างเท่ากัน; มี `\neq`; metric แสดง "ไม่มีลิมิต (DNE)" |
| 2 | ลิมิตเข้าใกล้จุด | f=`1/x**2`, a=`0` | metric แสดง ∞ (อนันต์); ขั้นสรุปบอกทั้งสองข้างลู่ $+\infty$ ตรงกัน |
| 3 | ลิมิตเข้าใกล้จุด | f=`sin(x)/x`, a=`0` | metric `1.0000` (regression ต้องไม่พัง) |
| 4 | ปริพันธ์ไม่ตรงแบบ | f=`1/x**2`, a=`1`, ขอบบน "จำนวนจำกัด" b=`2` | สมการหลักขอบบนเป็น `2` (ไม่ใช่ `\infty`), ค่า `1/2`, ไม่มีคำเตือนลู่ออก |
| 5 | ปริพันธ์ไม่ตรงแบบ | f=`1/x`, a=`1`, ขอบบน "อนันต์ (inf)" | แสดงคำเตือนลู่ออก (divergent); ไม่โชว์ค่าจำกัดที่ทำให้เข้าใจผิด |
| 6 | ปริพันธ์ไม่ตรงแบบ | f=`1/x`, a=`0`, ขอบบน "จำนวนจำกัด" b=`1` | แสดงคำเตือนลู่ออก (จุดเอกฐานที่ขอบล่าง) |

เกณฑ์รับ: ไม่มีสมการที่อ้างว่าลิมิตซ้ายเท่าขวาเมื่อจริงไม่เท่า, ขอบบนในสมการตรงกับ b ที่ป้อน,
กรณีลู่ออกมีคำเตือนชัดเจน, และกรณีปกติ (`sin(x)/x -> 1`, `1/x**2` จำกัด -> `1/2`) ยังถูกต้อง

---

## 5. Caveats (ข้อควรระวังเชิงคณิตศาสตร์)

- **โดเมนจริง**: จำแนกในช่วงจำนวนจริง การที่ SymPy คืน `zoo`/ค่าซับซ้อนไม่ควรถูกตีความเป็นค่าจริง
  ให้ `unsupported` (limit) หรือ `divergent`/`unsupported` (improper) ตามคลาส ไม่เดาเป็นจำนวนจริง
- **ลิมิตซ้ายไม่เท่าขวา = DNE**: แม้ `sp.limit` สองด้านจะคืน `oo` (เช่น `1/x` ที่ 0)
  ต้องใช้ `_classify_limit` จากลิมิตด้านเดียว ตัดสิน `dne` ห้ามสรุปว่ามีค่า
- **อนันต์สองข้าง**: `infinite` เกิดเฉพาะเมื่อลิมิตซ้ายและขวาเป็นอนันต์ "เครื่องหมายเดียวกัน" เท่านั้น
  ถ้าเป็น $-\infty$ กับ $+\infty$ ให้เป็น `dne` (ห้ามยุบเป็น `\infty` เดียว)
- **ไม่มี false precision**: อย่าพิมพ์ค่า float จากการสุ่มตัวอย่างเชิงตัวเลขแทนลิมิต/ปริพันธ์ที่ลู่ออก
  `result` เป็น float เฉพาะกรณี `finite`; กรณีอื่นเป็น `None` พร้อม `status`
- **Cauchy principal value**: ห้ามรายงาน PV แทนค่าปริพันธ์ไม่ตรงแบบ
  เช่น $\int_{-1}^{1} 1/x\,dx$ สมมาตรได้ PV = 0 แต่ปริพันธ์ไม่ตรงแบบ **ลู่ออก** ให้รายงาน `divergent`
- **ขอบบนจริงใน LaTeX**: ใช้ `sp.nsimplify(b)` เพื่อคงรูปที่อ่านง่าย (เช่น `2`, `\frac{3}{2}`)
  แทนการ hardcode `\infty`; กรณี `b is None` จึงใช้ `\infty`
- **`\text{...}` ต้องเป็น ASCII**: ข้อความไทย (เช่น "ไม่มีลิมิต", "ลู่ออก") ให้อยู่ใน label ฝั่ง markdown
  (ส่วนหน้า `:` ของ step) หรือ `st.warning` ไม่ใส่ไทยใน `\text{}` ของ KaTeX

## 6. ขอบเขตที่ไม่ทำในงานนี้

- ไม่รื้อหรือเพิ่มความปลอดภัยของ `_parse_input` / parser (ไม่แตะ `parse_expr`, ไม่เพิ่ม dependency)
- ไม่แก้ area/plot e-sign/shape bugs ที่แยกเป็นบั๊กอื่นใน `browser-test-report.md` (ข้อ 2, 3)
- ไม่แก้การจัดการ "ไม่มีประวัติ" ระหว่างทำ quiz (ระบุในรายงานว่าไม่ใช่ bug)
- ไม่ commit/push ไม่เปิด server ในเอกสารนี้ — เป็นแผนอย่างเดียว
- dirty tree ที่มีอยู่ถูกเก็บไว้ทั้งหมด (ไม่ stash, ไม่ reset, ไม่แก้ไฟล์ tracked)

## 7. ลำดับการทำงานที่เสนอ (TDD)

1. เพิ่ม regression test งาน A → รัน `pytest tests/test_limit_solver.py tests/test_sympy_solver.py -v` (แดงตามคาด)
2. implement `_classify_limit` + แก้ steps สรุป + เพิ่ม `status` ใน `limit_solver.py` และ `sympy_solver.py`
3. รัน pytest งาน A จนเขียว รวม test เดิม
4. ทำซ้ำข้อ 1-3 กับงาน B (`test_improper_solver.py`, `improper_solver.py`)
5. ปรับหน้า `limit_approach.py`, `improper_integrals.py` แบบ additive (ไม่ลบโค้ดเดิม)
6. รัน `pytest tests/ -v` เต็มชุด แล้วทำ browser acceptance ตามข้อ 4
