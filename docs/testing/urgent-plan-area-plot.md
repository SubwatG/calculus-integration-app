---
topic: urgent-plan-area-plot
date: 2026-10-05
status: draft-planning-only
scope: utils/area_solver.py, pages/area_between.py, utils/plotter.py
no_production_edits: true
---

# แผนแก้ไขเร่งด่วน: พื้นที่เรขาคณิต และการพล็อตฟังก์ชันค่าคงที่

> **ร่างนี้ถูกแทนที่แล้ว ห้ามใช้ implementation snippets โดยตรง** ใช้ [แผนฉบับหลัก](../../_hermes/plans/urgent-calculus-correctness-plan.md) ซึ่งแก้ประเด็น numeric root fallback, การเก็บผลผิดเมื่อ DNE, และการแยก unknown domain จาก divergence แล้ว ร่างนี้เก็บไว้เป็นหลักฐานการตรวจเท่านั้น

เอกสารนี้เป็นแผนเท่านั้น ยังไม่แก้โค้ดผลิตภัณฑ์ อ้างอิงปัญหาจริงจาก `docs/testing/browser-test-report.md` (หัวข้อ 2 และ 3) และสืบยืนยันด้วย `.venv` จริง

หลักฐานที่รันซ้ำได้ตอนวางแผน (ค่าจริง):

```text
compute_area_between('x','0',-1,1)   -> result=0.0      (ควรเป็น 1.0)
compute_area_between('x**2','x',0,1) -> result=-0.16666666666666666 (ควรเป็น 1/6 บวก)
plot_area_between(x, 0, -1, 1)       -> ValueError x and y must have same first dimension, but have shapes (400,) and (1,)
```

สาเหตุราก:

- `compute_area_between` ใช้ `A = ∫(f-g) dx` ซึ่งเป็นพื้นที่แบบมีเครื่องหมาย ไม่ใช่พื้นที่เรขาคณิต และไม่ตรวจว่าฟังก์ชันใดอยู่บน/ล่างตลอดช่วง จึงให้ 0 หรือค่าติดลบโดยไม่เตือน
- `sp.lambdify` ของฟังก์ชันค่าคงที่ (`sp.Integer(0)`, `sp.Integer(5)`) คืน Python scalar ไม่ใช่ ndarray ทำให้ `ax.plot`/`fill_between` ได้ shape ไม่ตรงกับ `xs`

งานสองส่วนนี้เป็นอิสระต่อกัน แยก commit/PR ได้ ไม่พึ่งพากัน

---

## Task A: พื้นที่เรขาคณิต `∫_a^b |f-g| dx` บนช่วงจริงจำกัด

### A1. Contract และ signature

คง signature เดิมเป๊ะ (ห้ามเปลี่ยนชื่อ/ลำดับ/ชนิด):

```python
def compute_area_between(f_str: str, g_str: str, a: float, b: float) -> dict:
```

ต้องคืน key เดิมครบทุกตัว: `ok`, `result`, `latex`, `steps`, `expr`, `f_expr`, `g_expr`, `error`
เพิ่มได้เฉพาะ key ใหม่แบบ additive (ห้ามลบ/เปลี่ยนความหมายของ key เดิม): `intersections: list[float]`, `region_count: int`, `warnings: list[str]`

ความหมายใหม่ (raises ต้องกลายเป็น `ok=False` ไม่ใช่ throw):

- คำนวณ `A = ∫_a^b |f(x) - g(x)| dx` โดยแยกช่วงที่จุดตัด `f=g` ภายใน `[a,b]`
- `result` เป็น `float` บวกหรือศูนย์ เมื่อผลเป็นจำนวนจริงจำกัดเท่านั้น
- ต้องปฏิเสธอย่างชัดเจน (`ok=False`, `result=None`, `error` เป็นข้อความไทย) เมื่อ:
  - โดเมนไม่ถูกต้อง: `a` หรือ `b` ไม่ `finite`, หรือ `a >= b`
  - `f`/`g` ไม่ต่อเนื่องจริงบน `[a,b]` หรือตรวจโดเมนจริงไม่สำเร็จ (เช่น เกิด complex/nan จาก `sqrt`/`log`)
  - อินทิกรัลไม่ resolves เป็นจำนวนจริงจำกัด: ผลมี `sp.Integral` ค้าง, `oo`, หรือไม่ real (เช่น `|1/x|` บน `[-1,1]` ให้ `oo + I*pi`)
  - หาจุดตัดไม่สำเร็จอย่างน่าเชื่อถือ
- ห้ามคืนพื้นที่แบบมีเครื่องหมาย และห้ามคืน 0 หลอกๆ เมื่อยังตัดสินใจไม่ได้ ให้ `ok=False` แทน

### A2. pytest ที่ยัง fail (ใช้เป็น regression ก่อนแก้)

เพิ่มใน `tests/test_area_solver.py` (ปัจจุบัน 4 tests ผ่าน แต่ assertion อ่อน จึงไม่จับบั๊ก):

```python
def test_geometric_area_signed_region_returns_positive(self):
    # x บน [-1,1] ใต้แกนครึ่งหนึ่ง เหนือแกนครึ่งหนึ่ง พื้นที่เรขาคณิต = 1 ไม่ใช่ 0
    res = compute_area_between('x', '0', -1, 1)
    assert res['ok'] is True
    assert abs(res['result'] - 1.0) < 1e-9

def test_geometric_area_curves_swapped_is_positive(self):
    # x**2 กับ x บน [0,1] ตัดกันที่ 0 และ 1 พื้นที่ = 1/6 เสมอไม่ว่าสลับ f/g
    res = compute_area_between('x**2', 'x', 0, 1)
    assert res['ok'] is True
    assert abs(res['result'] - (1.0 / 6.0)) < 1e-9

def test_geometric_area_basic_still_ok(self):
    res = compute_area_between('x', 'x**2', 0, 1)
    assert res['ok'] is True
    assert abs(res['result'] - (1.0 / 6.0)) < 1e-9

def test_reject_invalid_domain_order(self):
    res = compute_area_between('x', '0', 1, -1)
    assert res['ok'] is False
    assert res['result'] is None

def test_reject_nonfinite_or_nonreal(self):
    # เอกพจน์ภายในช่วง ทำให้ผลเป็น oo/complex ต้องปฏิเสธ ไม่คืน signed/0
    res = compute_area_between('1/x', '0', -1, 1)
    assert res['ok'] is False
    assert res['result'] is None

def test_preserves_existing_keys(self):
    res = compute_area_between('x', 'x**2', 0, 1)
    for k in ('ok','result','latex','steps','expr','f_expr','g_expr','error'):
        assert k in res
```

ค่าคาดหวังยืนยันด้วย SymPy จริง: `∫_{-1}^{1}|x|dx = 1`, `∫_{0}^{1}|x**2-x|dx = 1/6`, `2-x**2` กับ `x**2` บน `[-1,1]` = `8/3`

### A3. โครง implementation ขั้นต่ำ (bounded, finite real domain)

`sp.solveset` เคยค้างเกิน 300 วินาที (พิสูจน์ตอนวางแผน) ให้ใช้ `sp.solve` แบบมีขอบเขต แทน และมี fallback เป็น numeric sign-change scan ไม่เพิ่ม dependency ใหม่ (มี `numpy`, `sympy` อยู่แล้ว):

```python
import numpy as np

def _real_crossings(diff_expr: sp.Expr, a: float, b: float) -> list[float]:
    """Find real x in [a,b] where diff_expr == 0. Bounded; may return [] if none found."""
    pts: list[float] = []
    try:
        sols = sp.solve(sp.Eq(diff_expr, 0), X)
    except Exception:
        sols = []
    if sols:
        for s in sols:
            try:
                sv = float(s)
            except (TypeError, ValueError):
                continue
            if sp.im(s) == 0 and a - 1e-12 <= sv <= b + 1e-12:
                pts.append(min(max(sv, a), b))
    if not pts:  # numeric fallback on the finite interval only
        xs = np.linspace(a, b, 601)
        with np.errstate(all="ignore"):
            ys = sp.lambdify(X, diff_expr, modules=["numpy"])(xs)
        ys = np.asarray(ys, dtype=float)
        if ys.ndim == 0:
            ys = np.full(xs.shape, float(ys))
        sign = np.sign(ys)
        for i in range(len(xs) - 1):
            if not (np.isfinite(ys[i]) and np.isfinite(ys[i + 1])):
                continue
            if sign[i] != 0 and sign[i + 1] != 0 and sign[i] != sign[i + 1]:
                pts.append(float((xs[i] + xs[i + 1]) / 2.0))
    return sorted(set(round(p, 12) for p in pts))


def _geometric_area(f_expr, g_expr, a: float, b: float):
    """Return (area_float_or_None, intersections, warnings). Reject nonfinite/nonreal."""
    if not (np.isfinite(a) and np.isfinite(b)) or a >= b:
        return None, [], ["ช่วง [a, b] ไม่ถูกต้อง: ต้องเป็นจำนวนจริงจำกัดและ a < b"]
    diff = sp.simplify(f_expr - g_expr)
    warnings: list[str] = []
    cuts = _real_crossings(diff, a, b)
    pts = sorted(set([a, b] + cuts))
    total = sp.Integer(0)
    for x0, x1 in zip(pts, pts[1:]):
        if x1 - x0 < 1e-12:
            continue
        piece = sp.integrate(sp.Abs(diff), (X, x0, x1))
        if piece.has(sp.Integral) or not piece.is_number:
            try:
                piece = sp.N(piece, 15)
            except Exception:
                return None, cuts, ["ตรวจโดเมน/หาค่าบนช่วงจริงไม่สำเร็จ จึงไม่รายงานพื้นที่"]
        if piece.has(sp.Integral) or not (piece.is_real and piece.is_finite):
            return None, cuts, ["ช่วงมีเอกพจน์หรือผลไม่เป็นจำนวนจริงจำกัด จึงไม่รายงานพื้นที่"]
        total += piece
    if not (total.is_real and total.is_finite):
        return None, cuts, ["ผลรวมพื้นที่ไม่เป็นจำนวนจริงจำกัด"]
    if cuts:
        warnings.append(f"ฟังก์ชันตัดกันที่ x = {cuts} จึงแยกช่วงก่อนรวมพื้นที่เรขาคณิต")
    else:
        warnings.append("ไม่พบจุดตัดภายในช่วง ใช้ f, g ตามลำดับที่ให้ในการหา |f-g|")
    return float(total), cuts, warnings
```

ใน `compute_area_between` ให้เรียก `_geometric_area` แล้วประกอบ dict (key เดิมครบ) โดย `latex` แสดง `A = \int_a^b |f-g|dx` และ `steps` ต้องมีขั้นระบุการแยกช่วง/จุดตัดเมื่อ `len(cuts) > 0` ตัวอย่างข้อความไทย: "ตรวจว่าฟังก์ชันตัดกันหรือไม่ แล้วใช้พื้นที่เรขาคณิต ∫|f-g|dx" หลีกเลี่ยงศัพท์ที่ทำให้เข้าใจว่าเป็นพื้นที่ปิดล้อมสุทธิ

### A4. Acceptance ของ Task A

- pytest ข้อ A2 ทั้งหมดผ่าน และ `pytest tests/test_area_solver.py -v` เดิมยังเขียว (4 tests เดิม)
- `x` กับ `0` บน `[-1,1]` คืน `1.0`; `x**2` กับ `x` บน `[0,1]` คืน `1/6` บวกทั้งสองลำดับ f/g
- เคสที่ต้อง `ok=False`: `a>=b`, `a`/`b` ไม่ finite, `1/x` บน `[-1,1]` (ผล `oo + I*pi`), โดเมนที่ระบุไม่ได้
- ไม่มี `st.warning` แนว "ไม่ทราบว่าฟังก์ชันใดอยู่บน" แบบที่ผู้ใช้เข้าใจผิดเมื่อยังคำนวณได้จริง; ถ้าคำนวณไม่ได้ต้องขึ้น `st.error` จาก `res["error"]` ที่ `pages/area_between.py` มีอยู่แล้ว
- ไม่แตะ signature และไม่ลบ key เดิม

### A5. Browser repro (Task A)

1. `.venv/bin/python -m streamlit run app.py --server.address 127.0.0.1 --server.port 8502 --server.headless true --browser.gatherUsageStats false`
2. เปิด `http://127.0.0.1:8502` ไปหน้า "พื้นที่ระหว่างเส้นโค้ง"
3. ใส่ `f = x`, `g = 0`, `a = -1`, `b = 1` แล้วอ่าน LaTeX ผลลัพธ์: ต้องแสดง `A = 1` (เดิม `A = 0`)
4. ใส่ `f = x**2`, `g = x`, `a = 0`, `b = 1`: ต้องได้ `1/6` บวก (เดิม `-0.1666...`)
5. ใส่ `f = 1/x`, `g = 0`, `a = -1`, `b = 1`: ต้องขึ้น error ภาษาไทย ไม่ใช่ค่า 0/oo เงียบๆ

---

## Task B: แก้ scalar broadcasting ของฟังก์ชันค่าคงที่ใน `utils/plotter.py`

### B1. Root cause (ยืนยันแล้ว)

`sp.lambdify(X, sp.sympify('0'), modules=["numpy"])` คืน `int` (shape `()`), ขณะที่ `sp.sympify('x')` คืน `ndarray (400,)` การส่ง scalar เข้า `ax.plot(xs, ys)` / `fill_between` ทำให้ matplotlib โยน
`ValueError: x and y must have same first dimension, but have shapes (400,) and (1,)`
`plot_area_between` ไม่มี guard; `plot_tangent` และ `plot_limit_near` มี guard `isinstance(ys,(int,float))` อยู่แล้ว แต่ครอบไม่ถึง 0-d `ndarray`/`numpy` scalar บางชนิด

### B2. Reusable helper (ไม่เพิ่มสถาปัตยกรรมใหม่ แค่ฟังก์ชันเดียวในไฟล์เดิม)

เพิ่ม helper ตัวเดียวใน `utils/plotter.py` แล้วเรียกใช้ซ้ำ — ห้ามสร้าง abstraction/module ใหม่:

```python
def _as_curve(ys, xs: np.ndarray) -> np.ndarray:
    """Broadcast scalar lambdify output to xs shape; keep nonfinite as nan for masked fills."""
    arr = np.asarray(ys, dtype=float)
    if arr.ndim == 0:
        arr = np.full(xs.shape, float(arr), dtype=float)
    return arr
```

หลักการ: ค่าคงที่ถูกกระจาย (broadcast) ให้ยาวเท่า `xs`; ค่า nonfinite (`nan`/`inf`) ถูกเก็บเป็น `nan` เพื่อให้ `fill_between(..., where=...)` จัดการแบบ masked และไม่ทำให้ matplotlib ระเบิด shape

### B3. pytest ที่ยัง fail

เพิ่มใน `tests/test_area_solver.py` (หรือไฟล์ `tests/test_plotter.py` ใหม่ถ้าต้องการแยก):

```python
import sympy as sp
from utils.plotter import plot_area_between

def test_plot_area_between_constant_zero(self):
    # g = 0 เป็นฟังก์ชันค่าคงที่ lambdify ได้ scalar shape () เดิมทำให้ ValueError
    fig, ax = plot_area_between(sp.sympify('x'), sp.sympify('0'), -1.0, 1.0)
    assert fig is not None and ax is not None

def test_plot_area_between_nonzero_constant(self):
    fig, ax = plot_area_between(sp.sympify('5'), sp.sympify('0'), 0.0, 2.0)
    assert fig is not None and ax is not None

def test_plot_area_between_both_constants(self):
    fig, ax = plot_area_between(sp.sympify('3'), sp.sympify('1'), 0.0, 1.0)
    assert fig is not None and ax is not None
```

### B4. จุดที่ต้องแก้ (ครอบทุก plot ที่รับ lambdify)

เรียก `_as_curve` หลัง `lambdify` ทุกจุดที่อาจได้ scalar ค่าคงที่:

- `plot_area_between` (บรรทัด ~388-391): `ys_f_full, ys_g_full, ys_f_area, ys_g_area` — เคสที่รายงานมา ต้องแก้ก่อนเป็นอันดับแรก
- `plot_riemann` (บรรทัด ~52, 63, 92): `ys_smooth, ys_rect, ys_area` — ฟังก์ชันคงที่ เช่น `f(x)=3` จะพังเหมือนกัน
- `plot_volume` (บรรทัด ~327-328): `ys_solid, ys_ext`; ใช้ `float(f(sx))` ในลูปอยู่แล้วจึงไม่พังตรงนี้ แต่ `-ys_solid` (บรรทัด 334, 337) ถ้าเป็น scalar จะพัง — ต้อง broadcast ก่อน
- `plot_improper` (บรรทัด ~459, 467): `ys, ys_shade`
- `plot_tangent` / `plot_limit_near`: มี guard `isinstance(ys,(int,float))` อยู่แล้ว เปลี่ยนมาใช้ `_as_curve` เพื่อความสม่ำเสมอ (ไม่บังคับ แต่แนะนำ)

ห้ามแก้ `utils/theme.py` และห้ามเปลี่ยน signature ของ plot helper ใดๆ

### B5. NumPy masked nonfinite risks (ต้องตรวจใน Task B)

- `fill_between` แบบ `where=(ys_f_area >= ys_g_area)` เมื่อมี `nan`/`inf`: การเปรียบเทียบกับ `nan` ให้ `False` เงียบๆ อาจทิ้งช่วงที่ควรแรเงาและเกิด warning “invalid value encountered” ให้ประเมินผลใน `np.errstate(all="ignore")` ต่อเนื่อง และตรวจว่าไม่มี `RuntimeWarning` โผล่ในเทอร์มินัลตอน plot
- ถ้า `ys` ทั้งช่วงเป็น `nan` (เช่น `log(-x)` บนช่วงบวก) การ `set_ylim` จาก percentile อาจได้ค่า `nan` แล้ว silently ข้าม ให้กันด้วย `np.isfinite` ก่อนใช้ percentile ทุกครั้ง (ปัจจุบันทำอยู่บางจุด)
- `plot_volume` ใช้ `np.max(np.abs(finite_ys))` — ถ้า `finite_ys` ว่าง จะพัง; คง guard `len>0` ไว้
- ตรวจว่า `_as_curve` ไม่กลืน `inf`: `np.asarray(inf,float)` ยังเป็น `inf`; `np.full` กับ `float('inf')` ก็ยัง `inf` — ถ้าต้องการตัด `inf` ในเส้นโค้งให้ `np.where(np.isfinite(arr), arr, np.nan)` เพิ่มได้ตามความเหมาะสมของแต่ละ plot

### B6. Acceptance ของ Task B

- pytest B3 ทั้งสามผ่าน; `pytest tests/ -v` เดิมทั้งหมดยังเขียว
- `plot_area_between` กับ `f` หรือ `g` เป็นค่าคงที่ (0, 5, และทั้งคู่คงที่) ต้องคืน `(fig, ax)` โดยไม่เกิด `ValueError` และแกน x ตรงกับ input `[a,b]`
- ไม่มี RuntimeWarning ใหม่จาก `fill_between`/percentile
- แก้เฉพาะ `utils/plotter.py` (อาจเพิ่ม test) ไม่แตะหน้า `pages/*` และไม่แตะ signature

### B7. Browser repro (Task B)

1. รันแอปด้วยคำสั่งเดิมใน A5
2. หน้า "พื้นที่ระหว่างเส้นโค้ง" ใส่ `f = x`, `g = 0`, `a = -1`, `b = 1` แล้วกดดูกราฟ: ต้องมีภาพ ไม่ขึ้น `ไม่สามารถวาดกราฟได้: x and y must have same first dimension` (เดิมไม่มีภาพ)
3. ลอง `f = 5`, `g = 0`, `a = 0`, `b = 2`: ต้องได้ภาพเส้นตรงนอนและแรเงา
4. ตรวจว่าแกน x ครอบคลุม `[a,b]` และไม่มี warning ในเทอร์มินัล

---

## ลำดับและขอบเขต (ทั้งสอง task อิสระ)

1. Task B ก่อนได้ (เสี่ยงต่ำ แก้จุดเดียว) — ปลดล็อกให้เห็นกราฟก่อน
2. Task A ตาม (แก้ contract พร้อมเพิ่ม regression)

ข้อห้ามร่วม: ไม่ commit/push, ไม่รันแอปในงานนี้, ไม่แตะ working tree ที่ dirty อยู่เดิม, ไม่เพิ่ม dependency, ไม่สร้าง parser ใหม่

## ความเสี่ยงคงค้าง

- `sp.solve`/`sp.integrate` บางนิพจน์อาจช้า ให้จำกัดขอบเขตด้วย finite interval และ fallback numeric; กรณีเกินเวลาต้องคืน `ok=False` ไม่ค้าง
- การแยกช่วงด้วย numeric sign scan ใกล้จุดสัมผัส (tangent, ไม่มี sign change) อาจพลาดจุดตัด — ยอมรับได้ถ้าปฏิเสธอย่างชัดเจนเมื่อไม่แน่ใจ ไม่คืนค่าเดา
- ระยะห่าง shape ระหว่างค่าคงที่และ array ยังกระทบ plot อื่นตาม B4 ต้องแก้ให้ครบก่อนปิดงาน
