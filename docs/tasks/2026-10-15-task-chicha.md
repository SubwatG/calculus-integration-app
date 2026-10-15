# คำสั่งมอบหมายงานสำหรับ Antigravity CLI (agy) — ชิชา (Chicha)

**บทบาท:** Worked-Solution Depth Engineer (วิศวกรยกระดับขั้นตอนเฉลย)
**โปรเจกต์:** `SubwatG/calculus-integration-app`
**วันที่:** 15 ตุลาคม 2569
**กิ่งเป้าหมาย:** `feat/worked-solutions-detail` (แตกจาก `origin/main`)
**สถานะเอกสาร:** คำสั่งงานที่อาจารย์อนุมัติ ส่งต่อให้ชิชาทำบน branch และเปิด PR เท่านั้น

---

## บริบทและเป้าหมายหลัก (Context & Goal)

แอปมี 7 โมดูลการสอนเชิงโต้ตอบ แต่ "วิธีทำทีละขั้น" (worked solution) ใน `steps` ของหลายโมดูลยังเป็น **กล่องดำ (black-box)**: ระบุโจทย์ แล้วกระโดดไปที่คำตอบ โดยไม่แสดงการแทนค่า จัดรูป เงื่อนไขโดเมน หรือที่มาของเครื่องหมาย

งานของชิชาในรอบนี้: **ยกระดับความลึกของขั้นตอนเฉลยในทั้ง 7 โมดูล** ให้ผู้เรียนเดินตามได้จริง และให้ทุกขั้นตรวจสอบได้ทางคณิตศาสตร์ ไม่ใช่แค่ "มีความยาวครบ"

> **ขอบเขตที่ผู้ใช้ย้ำล่าสุด:** งานรอบนี้ **หยุด/ไม่ทำการ redesign layout, ธีม, สี, ฟอนต์ หรือจัดวาง UI ใหม่** การเปลี่ยนฝั่ง UI ที่อนุญาตมีเพียงอย่างเดียว: แสดง `steps` ที่ลึกขึ้นบนหน้าที่มีอยู่แล้ว

---

## 0. ขอบเขต (Scope)

**ทำ (In scope)**
- ปรับ step generator ภายใน `utils/*_solver.py` และ `utils/sympy_solver.py`
- เพิ่ม/แก้ test ใน `tests/test_*_solver.py` และ test การเรนเดอร์ด้วย Streamlit AppTest
- แก้การเรนเดอร์ `steps` ใน `pages/*.py` เฉพาะจุดที่จำเป็นต่อการแสดงขั้นตอนใหม่

**ห้ามทำ (Out of scope)**
- ห้าม redesign layout / ธีม / สี / ฟอนต์ (โดยเฉพาะห้ามแก้ `utils/theme.py` เพื่อเปลี่ยนหน้าตาหน้าอื่น)
- ห้ามเพิ่ม เรียกใช้ หรือทดสอบ **paid API** ใด ๆ และห้ามใส่ API key / secret / token ลงในโค้ดหรือไฟล์ทดสอบ
- ห้าม rewrite solver นอกขอบเขต (ห้ามเปลี่ยน signature ของฟังก์ชันสาธารณะ, ห้ามลบคีย์เดิมใน dict ผลลัพธ์)
- ห้ามแตะ `data/lessons/_archive/`, `.venv/`, `__pycache__/`
- ห้ามแก้ `utils/plotter.py` ยกเว้นกรณีที่ figure ที่มีอยู่เรนเดอร์พังเพราะข้อมูลใหม่ (ให้ระบุเหตุผลใน PR)

---

## 1. เกณฑ์ร่วม: Universal Step Contract

เฉลยแต่ละโจทย์ต้องครอบคลุม **5 องค์ประกอบในขั้นที่เกี่ยวข้อง** ต่อไปนี้ ไม่ต้องย้ำโดเมนหรือคำอธิบายเดิมทุกบรรทัด และไม่เพิ่มข้อความเพื่อให้ยาวโดยไม่มีสาระ:

| # | องค์ประกอบ | สิ่งที่ต้องปรากฏ |
|---|---|---|
| (a) | **เป้าหมาย / กฎที่ใช้ (Goal / Rule)** | บอกว่าขั้นนี้ทำอะไร ด้วยกฎหรือทฤษฎีบทใด เช่น "ใช้กฎกำลัง (Power Rule)" |
| (b) | **นิพจน์หลังแทนค่า (Substituted expression)** | แสดงค่าที่แทนลงไปจริง เช่น $f(a)$, $g'(x)$, $u = x^2$ |
| (c) | **พีชคณิตระหว่างทาง (Intermediate algebra)** | แสดงการจัดรูป/ตัดทอน/เปลี่ยนตัวแปรจริง ไม่กระโดดไปคำตอบ |
| (d) | **เงื่อนไขโดเมน (Domain restriction)** | เงื่อนไขที่ทำให้ขั้นนั้นถูกต้อง เช่น "ขั้นนี้ใช้ได้เพราะ $x \neq 2$", "$u > 0$", "$n \geq 1$" |
| (e) | **ผลลัพธ์แม่นตรง + การตีความ (Exact result / interpretation)** | ค่าในรูปเศษส่วน/พาย/ลอการิทึมเมื่อทำได้ พร้อมตีความ เช่น "$L_n$ ประเมินต่ำกว่าค่าจริง" |

**กฎเทคนิค (บังคับตาม `AGENTS.md`)**
- สมการใช้ `$...$` (inline) และ `$$...$$` (display) เท่านั้น ห้ามใช้ `\(` `\[`
- Python string ที่มี LaTeX ใช้ raw string/raw f-string เมื่อเหมาะสม หรือ escape backslash ให้ถูกต้อง; ตรวจร่วมกับ `render_steps()` จริง เพราะบางขั้นส่งตรงเข้า `st.latex` ซึ่งไม่ควรมี `$` ซ้อน
- จำนวน `$` ในหนึ่งสตริงต้องเป็นเลขคู่; แทรกภาษาไทยติดสมการให้ผ่าน `format_math_spacing()` ใน `utils/math_render.py`
- ห้าม emoji, em dash (—), และลูกศร Unicode (→) ในข้อความ `steps` และใน UI
- คำศัพท์เทคนิค: ไทยก่อน แล้ววงเล็บอังกฤษครั้งแรก
- **Backward compatibility:** ตรวจ signature, คีย์ผลลัพธ์ และ `status` จาก solver จริงทีละโมดูลก่อนแก้ คงสัญญาเดิมทั้งหมด ไม่สมมติว่าทุกโมดูลมีคีย์เหมือนกัน หากจำเป็นต้องเพิ่มข้อมูล ให้เพิ่มแบบไม่ทำลายผู้เรียกเดิมและมีเทสต์

### ตารางความรับผิดชอบ 7 โมดูล

| # | โมดูล (หน้า) | ไฟล์ solver | ไฟล์ test | quiz |
|---|---|---|---|---|
| 1 | ลิมิตเข้าใกล้จุด (`pages/limit_approach.py`) | `utils/limit_solver.py` | `tests/test_limit_solver.py` | `limits.json` |
| 2 | เส้นสัมผัสและอนุพันธ์ (`pages/tangent.py`) | `utils/tangent_solver.py`, `utils/sympy_solver.py` | `tests/test_tangent_solver.py`, `tests/test_sympy_solver.py` | `tangent.json` |
| 3 | พื้นที่ภายใต้เส้นโค้ง / รีมันน์ (`pages/riemann.py`) | `utils/riemann_solver.py` | `tests/test_riemann_solver.py` | `riemann.json` |
| 4 | เทคนิคอินทิเกรต u-Sub & By Parts (`pages/substitution.py`) | `utils/substitution_solver.py` | `tests/test_substitution_solver.py` | `techniques.json` |
| 5 | พื้นที่ระหว่างเส้นโค้ง (`pages/area_between.py`) | `utils/area_solver.py` | `tests/test_area_solver.py` | `area_between.json` |
| 6 | ปริมาตรทรงตัน (`pages/volume_revolution.py`) | `utils/volume_solver.py` | `tests/test_volume_solver.py` | `volume_revolution.json` |
| 7 | ปริพันธ์ไม่ตรงแบบ (`pages/improper_integrals.py`) | `utils/improper_solver.py` | `tests/test_improper_solver.py` | `improper_integrals.json` |

---

## 2. ข้อกำหนดเฉพาะรายโมดูล (Topic-Specific Requirements)

ข้อสังเกตต่อไปนี้เป็นจุดเริ่มจากการสำรวจ ไม่ใช่ใบรับรองว่า solver ทุกกรณีถูกต้อง ให้ตรวจ source บน `main` ล่าสุดและทำ RED test ยืนยันก่อนแก้ ตัวอย่างเรียกฟังก์ชัน/ชื่อคีย์ให้เทียบกับ API จริง ห้ามสร้างคีย์หรือเปลี่ยน signature เพื่อให้ตรงเอกสารโดยไม่จำเป็น

### โมดูล 1 — ลิมิต (`utils/limit_solver.py`)

**(ก) จุดบกพร่องที่ตรวจแล้ว:** ขั้นตอนครอบคลุมดีขึ้นแล้วสำหรับ $0/0$ และลิมิตอนันต์ แต่ยังต้องยืนยันความครบของ 4 กลุ่ม และห้ามมีข้อความสรุปที่ผิดคณิตศาสตร์

**(ข) ต้องครอบคลุม 4 กลุ่ม**
1. **รูป $0/0$:** แสดงการแทนค่าตรงได้ $\frac{0}{0}$ (รูปแบบยังไม่กำหนด) และ **ไม่สรุปค่า** จากนั้นเลือกเทคนิค: แยกตัวประกอบ (Factoring) / คูณสังยุค (Conjugate) / ลิมิตตรีโกณมิติ (Fundamental Trigonometric Limit) แล้วแทนค่ากลับ
2. **ลิมิตหนึ่งด้าน (One-Sided):** เขียนสัญลักษณ์ $x \to a^-$ และ $x \to a^+$ ให้ถูกต้อง แสดงค่าทั้งสองฝั่ง แล้วสรุปตามทฤษฎีบทลิมิตสองด้าน
3. **แกว่งกวัด (Oscillating):** ตรวจ $\sin\frac{1}{x}$ และฟังก์ชันแกว่งกวัดอื่น สรุป DNE พร้อมเหตุผล (ใช้ค่า `is_oscillating`)
4. **ลิมิตอนันต์ (Infinite Limit $c/0$, $c \neq 0$):** วิเคราะห์เครื่องหมายตัวส่วนสองฝั่ง แล้วสรุป $+\infty$, $-\infty$ หรือ DNE

**เกณฑ์ตรวจรับ (รายการตรวจ)**
- `compute_limit_near("(x**2-4)/(x-2)", 2)` → `result = 4`, `status = "finite"`, มีขั้น $0/0$ + แยกตัวประกอบ + ย้ำเงื่อนไข $x \neq 2$ ก่อนตัดทอน
- `compute_limit_near("1/x", 0)` → `status = "dne"`, `result is None`, และ **ห้าม** มีข้อความยืนยันว่า $\lim_{x\to 0^-} f = \lim_{x\to 0^+} f$ (ต้องแสดง $-\infty \neq +\infty$)
- `compute_limit_near("sin(x)/x", 0)` → `result = 1` พร้อมอ้างทฤษฎีบทตรีโกณมิติ
- `compute_limit_near("sin(1/x)", 0)` → `is_oscillating is True`, `status = "dne"`

### โมดูล 2 — อนุพันธ์และเส้นสัมผัส (`utils/sympy_solver.py`, `utils/tangent_solver.py`)

**(ก) จุดบกพร่องที่ตรวจแล้ว:** `tangent_solver` มีขั้นหลักแล้ว แต่ยังไม่รับรองความถูกต้องครบทุกโดเมน; ตรวจกรณีที่รองรับ (เจอ `non_differentiable` สำหรับ $|x|$ ที่ $0$ และ `undefined_point` สำหรับ $1/(x-2)$ ที่ $2$, $\sqrt{x}$ ที่ $-1$) แต่ `sympy_solver.differentiate` ยังตื้น: `differentiate("sin(x**2)")` ให้เพียง 2 ขั้น ไม่ระบุ **กฎลูกโซ่**

**(ข) ต้องครอบคลุม**
1. **ระบุกฎอนุพันธ์ที่ใช้** เป็นข้อความในขั้นเฉลย: กฎกำลัง (Power), กฎผลคูณ (Product), กฎผลหาร (Quotient), กฎลูกโซ่ (Chain)
2. **การแทนค่าที่จุด (Point evaluation):** แสดง $f(a)$ และ $f'(a)$ ทีละขั้น
3. **สมการเส้นสัมผัส:** แสดงการแทนใน $y - f(a) = m(x - a)$ แล้วจัดเป็นรูปชัดแจ้ง $y = mx + b$
4. **จุดไม่หาอนุพันธ์ได้ (Non-differentiable):** ตรวจจุดมุมแหลม/ยอดแหลม (Corner/Cusp) และจุดนอกโดเมน คืน `status` ที่ชัด (`non_differentiable`, `undefined_point`) และ **ไม่** คืนค่าความชันเป็นจำนวนจริงลวง

**เกณฑ์ตรวจรับ**
- `differentiate("sin(x**2)")` → มีขั้นที่ **ระบุชื่อกฎลูกโซ่** และแสดง $2x\cos(x^2)$ พร้อมเหตุผลภายใน
- `differentiate("1/x")` → มีขั้นกฎกำลังที่ $n = -1$ (ปัจจุบันทำได้แล้ว ให้คงไว้)
- `compute_tangent("x**2", 1)` → $m = 2$, $f(1) = 1$, สมการเส้นสัมผัส $y = 2x - 1$
- `compute_tangent("Abs(x)", 0)` → `status = "non_differentiable"`, `result is None`, ไม่มีสมการเส้นสัมผัส
- `compute_tangent("1/(x-2)", 2)` → `status = "undefined_point"`, `ok is False`

### โมดูล 3 — รีมันน์ (`utils/riemann_solver.py`)

**(ก) จุดบกพร่องที่ตรวจแล้ว:** ขั้นปัจจุบันแสดง $\Delta x$, จุดแบ่ง และผลรวมจำนวนแล้ว แต่ **ไม่แสดงสัญลักษณ์ซิกม่า $\sum$**, ไม่ระบุ $x_i^{*}$ และ $dx$ อย่างเป็นทางการ และไม่ชี้แจง net signed area เมื่อ $f(x) < 0$ ในขั้นเฉลย

**(ข) ต้องครอบคลุม**
1. **$dx$ และ $\Delta x$:** เชื่อมโยง $\Delta x = \frac{b-a}{n}$ กับสัญลักษณ์ $dx$ ในลิมิต $n \to \infty$
2. **$x_i^{*}$ (sample point):** ระบุชัดเจนว่านิยามของ left/right/midpoint ต่างกันที่จุดสุ่มใด เช่น
   - ซ้าย (Left): $x_i^{*} = x_{i-1} = a + (i-1)\Delta x$
   - ขวา (Right): $x_i^{*} = x_i = a + i\,\Delta x$
   - กลาง (Midpoint): $x_i^{*} = a + \left(i - \tfrac{1}{2}\right)\Delta x$
3. **สัญลักษณ์ซิกม่า $\sum$:** เขียน $\sum_{i=1}^{n} f(x_i^{*})\,\Delta x$ เป็นขั้นกลางก่อนแทนตัวเลข
4. **พื้นที่คิดเครื่องหมาย (Net Signed Area) vs พื้นที่เรขาคณิต:** เมื่อมีช่วงที่ $f(x) < 0$ ให้เพิ่มขั้นอธิบายว่าผลรวมติดลบหมายถึงพื้นที่ใต้แกน (ใช้ `has_negative_region` / `negative_warning`)
5. **การลู่เข้า:** เปรียบเทียบกับค่าจริง $\int_a^b f(x)\,dx$ พร้อมค่าคลาดเคลื่อนและทิศทาง (ใช้ `has_negative_region`, `error_abs`, `error_pct`, `direction` ที่มีอยู่)

**เกณฑ์ตรวจรับ**
- `compute_riemann("x**2", 0, 2, 4, "left")` → `result ≈ 1.75`, มีขั้น $\sum$ และการนิยาม $x_i^{*}$ ของ left, และค่าจริง $\frac{8}{3} \approx 2.6667$ พร้อม error ติดลบ (Underestimate)
- `compute_riemann("x**3-2*x", 0, 2, 4, "left")` → `has_negative_region is True` และขั้นเฉลยอธิบาย net signed area
- `compute_riemann("x**2", 0, 2, 100, "midpoint")` → error น้อยกว่า left/right อย่างมีนัยสำคัญ และสอดคล้องกับ `methods_comparison`
- กรณียังมาก: `n = 9` ต้องไม่เหลือตัวแปรตาย (dead local) และขั้นแสดง $\sum$ ได้ถูกต้อง

### โมดูล 4 — เทคนิคอินทิเกรต u-Sub & By Parts (`utils/substitution_solver.py`)

**(ก) ประเด็นตั้งต้นที่ต้องทำซ้ำ (สำคัญ):** ขั้นเฉลยตื้นมาก — `solve_substitution("2*x*cos(x**2)")` ให้เพียง 3 ขั้น (โจทย์, ตั้ง $u$, คำตอบ) **ไม่แสดงการแปลง $dx$ และไม่แสดงการแทนกลับตัวแปรเดิม**; และ **ไม่มีเส้นทางการเฉลยแบบ By Parts เลย** (`solve_substitution("x*ln(x)")` ให้เพียง 3 ขั้นกว้าง ๆ ไม่มี $u, dv, du, v$)

**(ข) ต้องครอบคลุม — สองเส้นทาง**

*เส้นทาง A: การแทนค่า $u$ (u-Substitution)*
1. เลือก $u = g(x)$ และให้เหตุผล (มี $g(x)$ และ $g'(x)$ ปรากฏในโจทย์)
2. **แปลง differential:** แสดง $du = g'(x)\,dx$ และจับคู่พจน์ที่ถูกแทนอย่างชัดเจน ไม่จำเป็นต้องหารด้วย $g'(x)$; ถ้าหารต้องพิจารณาจุดที่ $g'(x)=0$ ก่อน
3. แทนทุกพจน์ให้เหลือตัวแปร $u$ ล้วน (ย้ำว่า $x$ ต้องถูกตัดทอน 100%)
4. อินทิเกรตในตัวแปร $u$
5. **แทนกลับ (Back-substitution):** แทน $u = g(x)$ คืนตัวแปรเดิม แล้วบวก $+C$
6. ถ้าเป็นปริพันธ์จำกัดเขต: แปลงลิมิตเป็นค่าของ $u$ ด้วย และระบุว่าไม่ต้องแทนกลับ

*เส้นทาง B: การอินทิเกรตทีละส่วน (Integration by Parts)*
1. เลือก $u$ และ $dv$ พร้อมเหตุผล โดย LIATE เป็นเพียงแนวช่วยเลือก ไม่ใช่ทฤษฎีบทที่รับประกันผล
2. หา $du$ และ $v$ ทีละขั้น ให้เห็นการอินทิเกรต $v = \int dv$
3. แทนในสูตร $\int u\,dv = uv - \int v\,du$ ให้เห็นทุกพจน์
4. แสดง **เศษที่เหลือ (remainder)** $\int v\,du$ และวิธีจัดการ (อินทิเกรตซ้ำ / วนซ้ำ / ได้รูปเดิมย้ายข้าง)
5. สรุปคำตอบพร้อม $+C$

**เกณฑ์ตรวจรับ**
- `solve_substitution("2*x*cos(x**2)")` → ผลลัพธ์ $\sin(x^2) + C$ และมีขั้นแสดง $du = 2x\,dx$ เป็นขั้นแยก (ปัจจุบันมี ให้ยืนยันว่ายังมีหลังแก้)
- `solve_substitution("x*ln(x)")` → ผลลัพธ์ $\frac{x^2 \ln x}{2} - \frac{x^2}{4} + C$ และมีขั้น By Parts ครบ: $u = \ln x$, $dv = x\,dx$, $du = \frac{1}{x}dx$, $v = \frac{x^2}{2}$, แล้วแทนใน $uv - \int v\,du$, และแสดงเศษที่เหลือ
- `solve_substitution("e^(x**2)")` → `status = "non_elementary"` (หรือเทียบเท่า) ไม่คืนคำตอบปลอม
- ทุกคำตอบไม่จำกัดเขตต้องลงท้ายด้วย $+C$ ใน `latex` และในขั้นสรุป

### โมดูล 5 — พื้นที่ระหว่างเส้นโค้ง (`utils/area_solver.py`)

**(ก) จุดบกพร่องที่ตรวจแล้ว:** การคำนวณผลลัพธ์เป็นพื้นที่เรขาคณิตถูกต้องแล้ว (ใช้ $|f - g|$) แต่ **ขั้นเฉลยไม่แสดงจุดตัด** และไม่แสดงการแบ่งช่วง (ปัจจุบันมี `_find_crossings` และ `crossings` แล้ว แต่ไม่ปรากฏใน `steps`); ตัวอย่าง `compute_area_between("x**3-6*x**2+8*x", "0", -1, 5)` ให้ผล $\frac{41}{2} = 20.5$ ใน 4 ขั้น โดยไม่โชว์จุดตัด $x = 0, 2, 4$

**(ข) ต้องครอบคลุม**
1. **หาจุดตัด:** แก้ $f(x) = g(x)$ แล้วแสดงรากจริง (intersections) เป็นขั้น
2. **แบ่งช่วง (Splitting):** เมื่อมีจุดตัดภายใน $[a, b]$ ให้แบ่งเป็นช่วงย่อยและอินทิเกรตแยกช่วง
3. **ค่าสัมบูรณ์ (Absolute value):** เขียน $|f(x) - g(x)|$ และอธิบายว่าทำไมต้องแยกช่วง/ใส่ค่าสัมบูรณ์ เพื่อไม่ให้พื้นที่หักล้างกัน
4. **ผลรวม:** รวมพื้นที่ทุกช่วงย่อยเป็นคำตอบสุดท้าย

**เกณฑ์ตรวจรับ**
- `compute_area_between("x", "x**2", 0, 1)` → $\frac{1}{6}$ และมีขั้นแสดงจุดตัด (ไม่มีจุดตัดภายใน) + เงื่อนไข $f \geq g$ บนช่วง
- `compute_area_between("x**2", "x", 0, 1)` → ต้องได้ $\frac{1}{6}$ **บวก** (ไม่ใช่ค่าลบ) พร้อมขั้นอธิบายการสลับเครื่องหมาย
- `compute_area_between("x**3-6*x**2+8*x", "0", -1, 5)` → $\frac{41}{2}$ และขั้นแสดงจุดตัด $x = 0, 2, 4$ พร้อมการแบ่งช่วง $[-1,0], [0,2], [2,4], [4,5]$
- `compute_area_between("x", "x", -1, 1)` → $0$ (ฟังก์ชันเท่ากัน)

### โมดูล 6 — ปริมาตรทรงตัน (`utils/volume_solver.py`)

**(ก) จุดบกพร่องที่ตรวจแล้ว:** `compute_volume` รองรับเฉพาะ `method="disk"` และ `"washer"` (ต้องส่ง `inner_expr_str` เมื่อเป็น washer) และ **หมุนรอบแกน $x$ เท่านั้น**; ขั้นเฉลยตื้น — `compute_volume("x", 0, 2, "disk")` ให้ 3 ขั้น (รัศมี, สูตร, คำตอบ) ไม่แสดงแกนหมุน ไม่แจกแจง $R(x)$ กับ $r(x)$ แยกกัน และไม่ระบุตัวแปรการอินทิเกรต

**(ข) ต้องครอบคลุม**
1. **แกนหมุน (Axis):** ระบุแกนที่ API ปัจจุบันรองรับจริงในเฉลย ห้ามเพิ่มแกนหมุนหรือวิธีใหม่ในงานนี้ รัศมีต้องเป็นระยะจากแกนหมุน ไม่ใช้ค่าฟังก์ชันติดลบแทนระยะโดยไม่อธิบาย
2. **รัศมี (Radii):** Disk แสดง $R(x)$; Washer แสดง **รัศมีนอก $R(x)$ และรัศมีใน $r(x)$ แยกกัน**
3. **Disk vs Washer:** แสดงเหตุผลการเลือกวิธี (washer ใช้เมื่อมีช่องว่างตรงกลาง)
4. **ลำดับ/ตัวแปรการอินทิเกรต (Order):** เขียน $dx$ (หรือ $dy$) ให้ชัด และบอกทิศทางการกวาดจานตามแกน
5. คำตอบในรูป $k\pi$ เมื่อทำได้

**เกณฑ์ตรวจรับ**
- `compute_volume("x", 0, 2, "disk")` → $\frac{8\pi}{3} \approx 8.3776$ พร้อมขั้นระบุแกน $x$, $R(x) = x$ และ $dx$
- `compute_volume("x**2", 0, 2, "washer")` → ต้อง **ไม่** คืน `ok=True` ลอย ๆ (ปัจจุบันตอบ `ok=False` เมื่อไม่มีรัศมีใน); ให้คืน error/ข้อความไทยที่บอกว่าต้องระบุรัศมีใน
- `compute_volume("x", 0, 2, "washer", inner_expr_str="0")` หรือกรณีที่เหมาะสม → แสดง $R(x)$ และ $r(x)$ แยกกัน
- `compute_volume("x", 0, 2, "bogus")` → `ok is False` พร้อมข้อความไทย (ห้ามรับวิธีที่ไม่รู้จัก)
- `compute_volume("x", 2, 0, "disk")` → `ok is False` (ขอบเขตกลับด้าน)

### โมดูล 7 — ปริพันธ์ไม่ตรงแบบ (`utils/improper_solver.py`)

**(ก) จุดบกพร่องที่ตรวจแล้ว (ต้องแก้):** ตรรกะแยกช่วงที่ **จุดเอกฐานภายใน** ถูกต้องแล้ว (`compute_improper("1/(x-1)", 0, 2)` แสดง $\lim_{t\to 1^-}$ และ $\lim_{s\to 1^+}$ ถูกต้อง) แต่ **จุดเอกฐานที่ขอบเขต (endpoint)** ไม่ถูกตรวจจับ: `_find_interior_singularities` ตรวจเฉพาะช่วงเปิด $(a, b)$ ทำให้ `compute_improper("1/sqrt(x)", 0, 1)` สร้างสัญลักษณ์ลิมิตผิดเป็น $\lim_{t \to 1} \int_0^t$ (ควรเป็น $\lim_{t \to 0^+} \int_t^1$) ทั้งที่ฟังก์ชันต่อเนื่องที่ $x = 1$

**(ข) ต้องครอบคลุม**
1. **สัญลักษณ์ลิมิตให้ถูก endpoint:**
   - ขอบบนเป็นอนันต์: $\lim_{b \to \infty} \int_a^b$
   - ขอบล่างเป็นอนันต์: $\lim_{a \to -\infty} \int_a^b$
   - เอกฐานที่ขอบล่าง $a$ (เช่น $1/\sqrt{x}$ ที่ $0$): $\lim_{t \to a^+} \int_t^b$
   - เอกฐานที่ขอบบน $b$ (เช่น $1/\sqrt{1-x}$ ที่ $1$): $\lim_{t \to b^-} \int_a^t$
   - เอกฐานภายใน $c$: แยกสองช่วง $\lim_{t\to c^-}\int_a^t + \lim_{s\to c^+}\int_s^b$ (ทำได้แล้ว ให้คงไว้)
2. **การแยกช่วงเมื่อเอกฐานภายใน:** หากฝั่งใดลู่ออก ทั้งอินทิกรัลลู่ออก (ห้ามนำ $\pm\infty$ มาหักล้างกัน) — ต้องมีข้อความย้ำ
3. **สรุปการลู่เข้า/ลู่ออก:** ระบุ `status` = `finite` หรือ `divergent` ให้ตรงกับค่าจริง และแสดงค่าลิมิตที่คำนวณได้

**เกณฑ์ตรวจรับ**
- `compute_improper("1/x", 1, None)` → `status = "divergent"`, `result is None`
- `compute_improper("1/sqrt(x)", 0, 1)` → `result = 2`, `status = "finite"`, และสัญลักษณ์ลิมิตต้องเป็น $\lim_{t \to 0^+}\int_t^1$ (**ไม่ใช่** $t \to 1$)
- `compute_improper("1/(x-1)", 0, 2)` → `status = "divergent"` พร้อมขั้นแยกช่วงที่ $x = 1$
- `compute_improper("x", 0, 2)` → `latex` ต้องแสดงขอบเขตบนเป็น $2$ (ไม่ใช่ $\infty$)
- `compute_improper("1/x**2", 1, None)` → `result = 1`, `status = "finite"`

---

## 3. เกณฑ์การทดสอบ (Testing Contract)

**ห้ามตรวจ "จำนวนคำ/ความยาว" แทนความถูกต้อง** — การยืนยันที่เดิมใช้ `assert len(res["steps"]) >= 3` หรือ `assert res["result"] is not None` **ไม่เพียงพอ** ต้องตรวจ **เนื้อทางคณิตศาสตร์**:

1. **ตรวจค่าตัวเลข/สัญลักษณ์:** ใช้ `pytest.approx(...)` สำหรับค่าจริง และ `sp.simplify(a - b) == 0` สำหรับผลลัพธ์เชิงสัญลักษณ์
2. **ตรวจเนื้อขั้นตอน:** ตรวจว่าขั้นที่จำเป็นปรากฏจริง เช่น ค้นหาสตริงย่อยที่ระบุสูตรสำคัญ (เช่น `du = 2 x`, `\sum`, `\lim_{t \to 0^+}`, `x = 2`) — assert แบบนี้ยอมรับได้ **เมื่อคู่กับ** การตรวจค่าคณิตศาสตร์อย่างน้อยหนึ่งรายการในเทสต์เดียวกัน
3. **ตรวจ `status`:** assert ค่าของ `status` ให้ตรงตามที่ระบุในเกณฑ์ตรวจรับของแต่ละโมดูล
4. **กรณีขอบเขตและกรณีผิด (boundary / invalid):** ทุกโมดูลต้องมีอย่างน้อย 1 เทสต์กรณีผิด (อินพุตว่าง, ขอบเขตกลับด้าน, วิธีไม่รู้จัก) และ 1 เทสต์กรณีขอบเขต (ฟังก์ชันเท่ากัน, ค่าที่ทำให้ส่วนเป็นศูนย์, ขอบเป็นอนันต์)
5. **ตรวจการเรนเดอร์ด้วย Streamlit AppTest:** เพิ่ม/ขยายเทสต์เรนเดอร์หน้า (ตามแบบ `tests/test_pages_apptest.py`) ให้ตรวจว่า
   - หน้า mount ได้โดยไม่ raise: `assert not at.exception`
   - หน้าที่แสดง steps มีข้อความขั้นตอนใหม่ปรากฏ (เช่น ตรวจจาก `at.markdown` / `at.latex` ว่ามีสูตรที่ต้องการ) สำหรับโมดูลที่แก้

**ห้าม** เขียนเทสต์ที่เขียวได้แม้ตรรกะจะผิด (weak smoke test) และห้าม `xfail`/`skip` กลบความล้มเหลว

---

## 4. ขั้นตอนการทำงานและเกตคุณภาพ (Workflow & Quality Gates)

**4.1 ดึงงานตั้งต้น (สำคัญเรื่องความสะอาดของ clone)**
- working tree ของเครื่องอาจารย์มีงานอีกเซสชันค้างอยู่ **ห้ามคัดลอกหรือ reset/stash งานนั้น** ให้ใช้โค้ดที่ push บน GitHub `main` เท่านั้น
- เริ่มจาก **clone สะอาดใหม่** ของ `origin/main` (หรือ fork แล้ว clone) เท่านั้น:
  ```bash
  git clone https://github.com/SubwatG/calculus-integration-app.git
  cd calculus-integration-app
  git fetch origin
  git checkout -b feat/worked-solutions-detail origin/main
  ```
- **ห้าม** `git push origin main` และ **ห้าม** commit ตรงเข้า `main` ตลอดงาน

**4.2 ลำดับงาน (TDD)**
1. เขียน/ขยายเทสต์ก่อน (Red) ตามเกณฑ์ตรวจรับแต่ละโมดูล
2. แก้ solver จนเทสต์ผ่าน (Green)
3. ปรับการเรนเดอร์ `steps` ใน `pages/*.py` เฉพาะที่จำเป็น
4. รันทั้งชุด: `pytest tests/ -v` — ต้องผ่านทั้งหมด (เกณฑ์: All Green) และไม่ทำลายเทสต์เดิม

**4.3 Definition of Done**
- [ ] `streamlit run app.py` รันได้ ไม่มี error
- [ ] ทั้ง 7 โมดูลแสดงขั้นตอนเฉลยตาม Universal Step Contract (ครบ 5 องค์ประกอบในขั้นที่เกี่ยวข้อง)
- [ ] เกณฑ์ตรวจรับรายโมดูล (ข้อ 2) ผ่านจริง
- [ ] `pytest tests/ -v` ผ่าน 100%; เทสต์ใหม่ตรวจความถูกต้องทางคณิตศาสตร์ (ไม่ใช่ความยาว)
- [ ] เทสต์เรนเดอร์ด้วย AppTest ผ่าน
- [ ] ไม่มี emoji, em dash, ลูกศร Unicode และไม่มี secret/paid API ในโค้ดและเทสต์
- [ ] ไม่มีการ redesign layout/ธีม/UI และไม่มีการ rewrite solver นอกขอบเขต
- [ ] ไม่มี `.venv/`, `__pycache__/`, ไฟล์ render (`.pdf`/`.html`) ถูก commit

**4.4 การส่งงาน (PR)**
```bash
git status --short
# Stage only the exact files you changed; do not use git add . or whole directories.
# Example: git add -- utils/substitution_solver.py tests/test_substitution_solver.py
# Replace the example with your reviewed explicit file list.
git commit -m "feat(solver): deepen worked solutions across seven teaching modules"
git push origin feat/worked-solutions-detail
gh pr create --base main --head feat/worked-solutions-detail \
  --title "feat(solver): deepen worked solution steps across 7 modules" \
  --body-file docs/worked-solutions-pr-body.md
```
- ก่อนเปิด PR ให้เขียน `docs/worked-solutions-pr-body.md` พร้อมสรุปรายโมดูล โจทย์ก่อน/หลัง สูตรกลางที่เพิ่ม คำสั่งทดสอบ+ผลจริง ข้อจำกัด และภาพส่วนเฉลยที่เปิดแล้ว ตรวจ PR ซ้ำด้วย `gh pr list --head feat/worked-solutions-detail --base main`
- ใช้ `gh pr create --base main` ระบุ base ให้ชัดเจนเสมอ พร้อม `--title` และ `--body` ที่ระบุไฟล์ที่แก้และผลการทดสอบ
- **ห้าม auto-merge** ปล่อยให้อาจารย์รีวิว
- **ต้อง disclosing ผลเทสต์ตามจริง:** หากมีเทสต์ใดยังไม่ผ่าน ให้ระบุใน PR body ตรง ๆ (ชื่อเทสต์ + สาเหตุ) ห้ามซ่อนหรือลบเทสต์เพื่อให้เขียว

---

## 5. ความเสี่ยงและหมายเหตุ (Risks / Notes)

1. **งานคู่ขนาน:** ชุดส่งต่อนี้รวมลิมิตและอนุพันธ์ที่อาจารย์ตรวจแล้ว แต่ไม่รวมงานรีมันน์ของอีกเซสชัน เริ่มจากเทคนิคอินทิเกรต/อนุพันธ์/พื้นที่/ปริมาตร/ปริพันธ์ไม่ตรงแบบก่อน ตรวจลิมิตเฉพาะช่องว่างที่ยังเหลือ ส่วนรีมันน์ให้อ่านและเขียนรายการตรวจได้ แต่ยังไม่แก้ไฟล์จนผู้รับผิดชอบยืนยันว่ารวม main แล้วหรือยกสิทธิ์ไฟล์ให้ ห้ามอ้างรายงานในเครื่องว่าเป็นโค้ดที่ push แล้ว
2. **สโคป UI:** งานนี้ **ไม่** ปรับ layout/ธีม/การจัดวางใหม่ตามที่ผู้ใช้ย้ำล่าสุด — ถ้าพบว่าการแสดง steps ต้องเปลี่ยนโครงหน้า ให้ถามก่อน ห้ามตัดสินใจเอง
3. **ค่า `status` เป็นสัญญาระหว่าง UI กับ solver:** ห้ามเปลี่ยนความหมายค่าเดิม เพราะหน้า UI และเทสต์อื่นอ้างอิงอยู่
4. **ไม่ใช้ paid API / secret:** งานทั้งหมดใช้ SymPy ในเครื่องเท่านั้น

---

## Prompt สำหรับวางใน agy

> อ่าน AGENTS.md และ docs/tasks/2026-10-15-task-chicha.md ให้ครบ จากนั้นตรวจ main ล่าสุดและทำงานตามขอบเขตนี้โดยเริ่มจากเฉลยเทคนิคอินทิเกรต เขียน RED test ก่อนปรับ steps คงหน้าตาเดิมและ API เดิม ไม่แตะรีมันน์ที่ยังมีเจ้าของงาน เมื่อผ่านเทสต์และตรวจการแสดงผลแล้ว push เฉพาะ branch feat/worked-solutions-detail และเปิด Pull Request เข้า SubwatG/calculus-integration-app base main ห้าม push ตรง main หรือ merge เอง ส่ง URL PR พร้อมผลทดสอบจริงให้อาจารย์

## Fork และสิทธิ์ส่ง PR

ถ้าไม่มี write permission ให้ fork บัญชีตนเอง ตั้ง upstream เป็น https://github.com/SubwatG/calculus-integration-app.git สร้าง branch จาก upstream/main แล้ว push เข้า fork ของตน เปิดด้วย `gh pr create --repo SubwatG/calculus-integration-app --base main --head YOUR_GITHUB_USERNAME:feat/worked-solutions-detail --title "feat(solver): deepen worked solution steps" --body-file docs/worked-solutions-pr-body.md` โดยแทน YOUR_GITHUB_USERNAME ด้วยบัญชีจริง ตรวจ URL และ base/head ด้วย `gh pr view --json url,baseRefName,headRefName,state` และตรวจ `gh pr checks` ถ้าไม่มี CI ให้แจ้งว่าไม่มี อย่าอ้าง CI ผ่าน

## Stopping gate

ไม่ต้องเปิด PR ว่างตอนเริ่มงาน ถ้าทำครบไม่ทันให้ส่ง Draft PR ของส่วนที่ทดสอบแล้ว พร้อม checklist งานที่ยังไม่เสร็จ ห้ามรายงานว่าครบทั้ง 7 โมดูลหรือผ่าน DoD จนกว่าจะมีหลักฐานจริง แยก bug ที่ทำให้เฉลยผิดออกจากความละเอียด และแก้เฉพาะ minimal defect ที่มี regression test หากต้องเปลี่ยนสูตร/สัญญา API หรือขยายคุณสมบัติ ให้แจ้งก่อน
