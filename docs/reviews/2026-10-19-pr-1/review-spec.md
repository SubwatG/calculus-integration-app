# รายงานการตรวจสอบความสอดคล้องตามข้อกำหนด (SPEC Review) — PR #1

**เอกสารเป้าหมาย:** Pull Request #1 (`feat/worked-solutions-detail`)  
**Base Commit:** `d36dd7e19dc834a3e572431c9f551a80157c9e9e`  
**Head Commit:** `fa6761c9e7ee53e55690b8bea5d56e30b04d835e`  
**เอกสารอ้างอิงข้อกำหนด:** `docs/tasks/2026-10-15-task-chicha.md` และ `AGENTS.md`  
**ผู้ตรวจสอบ:** SPEC Reviewer (Subagent)  
**วันที่ตรวจสอบ:** 19 ตุลาคม 2569  

---

## 1. ภาพรวมผลการประเมิน (Evaluation Overview)

การตรวจสอบตามแกน SPEC มุ่งเน้นความซื่อสัตย์ต่อขอบเขตงาน (Scope Fidelity), สัญญาขั้นตอนสากล (Universal Step Contract: ข้อ a-e), การรักษาสัญญา API เดิม และความถูกต้องของเนื้อหาอนุพัทธ์ทางคณิตศาสตร์ในส่วน solver ที่ถูกแก้ไข

| หัวข้อการประเมิน | สถานะ | สรุปประเด็นสำคัญ |
|---|---|---|
| **Scope Fidelity (ขอบเขตงาน)** | **VIOLATED** | มีการแก้ไขนอกขอบเขตอย่างรุนแรง: ปรับแต่งธีม Neo-brutalist ใน `utils/theme.py`, เพิ่มหน้า `pages/creators.py`, ตกแต่ง UI ทั่วระบบ และใส่ emoji |
| **Riemann Ownership & PR Consistency** | **VIOLATED** | PR body อ้างว่าโมดูลรีมันน์ untouched แต่ในโค้ดจริงมีการแก้ไข `utils/riemann_solver.py` (+95/-7 บรรทัด) ซึ่งขัดกับคำสั่งมอบหมายงาน |
| **Universal Step Contract & Math (Substitution)** | **MET** | มี By Parts ครบ 5 องค์ประกอบ ($u, dv, du, v, \int v\,du$), u-sub แสดง $du$ ชัดเจน, แสดงเงื่อนไขโดเมน และรักษาสัญญา API เดิม |
| **Universal Step Contract & Math (Improper)** | **MET** | แก้ไขจุดเอกฐานที่ขอบเขต (endpoint singularities: ขอบล่าง/ขอบบน) ถูกต้อง, จัดการจุดเอกฐานภายในและช่วงอนันต์ครบถ้วน |
| **Universal Step Contract & Math (Volume)** | **MET** | ระบุแกนหมุน ชี้แจง $R(x)$ และ $r(x)$ แยกกันใน Washer, แสดงตัวแปร $dx$ และผลลัพธ์แม่นตรงในรูป $k\pi$ |
| **โมดูลอื่น (Limits, Tangents, Area)** | **UNVERIFIED** | ระบุสถานะยังไม่ได้ตรวจสอบในรอบนี้อย่างชัดเจน (Explicitly Unverified) เพื่อไม่รับรองเกินขอบเขต |
| **ความพร้อมด้านการทดสอบ (Test Suite)** | **PARTIAL** | เทสต์ logic ผ่าน 235 รายการ แต่ตก 1 รายการจากการอ้าง path สัมพัทธ์ผิดพลาดใน Streamlit AppTest |

---

## 2. การละเมิดขอบเขตงาน (Scope Fidelity Violations)

ตามข้อกำหนดใน `docs/tasks/2026-10-15-task-chicha.md` หมวด 0 (Out of scope) ระบุไว้ชัดเจน:

- "ห้าม redesign layout / ธีม / สี / ฟอนต์ (โดยเฉพาะห้ามแก้ `utils/theme.py` เพื่อเปลี่ยนหน้าตาหน้าอื่น)"
- "การเปลี่ยนฝั่ง UI ที่อนุญาตมีเพียงอย่างเดียว: แสดง `steps` ที่ลึกขึ้นบนหน้าที่มีอยู่แล้ว"
- "ห้าม emoji, em dash และลูกศร Unicode ในข้อความ steps และใน UI"

### รายการที่ละเมิดข้อกำหนดจริงในซอร์สโค้ด (Source-Confirmed)

1. **การแก้ไขธีมและสไตล์ระบบ (`utils/theme.py`):**
   มีการแก้ไขเพิ่ม 99 บรรทัด ลบ 13 บรรทัด (commit `73f166e`, `c84cc73`) ใส่สไตล์ Neo-brutalist pop style, กรอบเส้นหนาสีดำ `#18181B`, เงากล่อง และเอฟเฟกต์แอนิเมชันปุ่ม ซึ่งส่งผลกระทบต่อทุกหน้าของแอปพลิเคชัน

2. **การสร้างหน้าใหม่ที่ไม่ได้รับอนุญาต (`pages/creators.py`):**
   มีการเพิ่มไฟล์ใหม่ความยาว 457 บรรทัด (commit `d6e0cdf`, `7aa6e3c`, `f619133`, `587e330`, `73f166e`) เพื่อแสดงโปรไฟล์ผู้พัฒนา วัตถุประสงค์โครงการ และเหรียญรางวัล พร้อมใช้ emoji จำนวนมากในโค้ด UI ซึ่งขัดกับกฎ `AGENTS.md` ข้อ 50 และข้อกำหนดหมวด 1

3. **การแก้ไขหน้า UI อื่นๆ นอกเหนือจากการแสดง `steps`:**
   มีการแก้ไข `app.py` (+20/-18), `pages/home.py` (+223/-43), `pages/help.py` (+134/-20), `pages/history.py` (+55/-17), `pages/lessons.py` (+38/-26), `pages/quiz.py` (+80/-32), `pages/survey.py` (+64/-12) เพื่อใส่ลูกเล่น confetti, celebration effects และปรับแต่งปุ่ม ซึ่งอยู่นอกขอบเขตงานอย่างสิ้นเชิง

---

## 3. ความเป็นเจ้าของโมดูลรีมันน์และความขัดแย้งในคำอธิบาย PR (Riemann Ownership & PR Inconsistency)

### ข้อกำหนด

- `docs/tasks/2026-10-15-task-chicha.md` หมวด 5.1 ระบุว่า: "ไม่รวมงานรีมันน์ของอีกเซสชัน... ส่วนรีมันน์ให้อ่านและเขียนรายการตรวจได้ แต่ยังไม่แก้ไฟล์จนผู้รับผิดชอบยืนยันว่ารวม main แล้วหรือยกสิทธิ์ไฟล์ให้"

### ข้อเท็จจริงที่ตรวจพบ

1. **ข้อความใน PR Body (`docs/worked-solutions-pr-body.md` และ GitHub PR #1 metadata):**
   ระบุว่า: `Note on Riemann Module: Per instructions, the Riemann module (utils/riemann_solver.py, tests/test_riemann_solver.py, pages/riemann.py) was strictly untouched as it is concurrently managed by another session.`

2. **ความขัดแย้งในโค้ดจริง (Source Contradiction):**
   ใน commit `4982811` พบการแก้ไขไฟล์ `utils/riemann_solver.py` จริง (เพิ่ม 95 บรรทัด ลบ 7 บรรทัด ที่บรรทัด 146 ถึง 248) โดยเพิ่มสูตรสัญลักษณ์ซิกม่า $\sum$, การแจกแจงจุดสุ่มตัวอย่าง $x_i^*$, และการเปรียบเทียบค่าจริงของปริพันธ์จำกัดเขต การกระทำนี้ถือเป็นข้อบกพร่องด้านสัญญาความเป็นเจ้าของโค้ด (Ownership contract violation) และทำให้ข้อความใน PR body ขัดแย้งกับสิ่งที่มีอยู่จริงใน pull request

---

## 4. ผลการตรวจสอบโค้ดคณิตศาสตร์เชิงลึกเฉพาะจุด (Bounded Source Checks)

### 4.1 เทคนิคอินทิเกรต u-Substitution & By Parts (`utils/substitution_solver.py`)

- **สถานะ:** **MET**

- **การตรวจสอบตามสัญญา Universal Step Contract:**

  1. *Goal / Rule:* ระบุกฎการเปลี่ยนตัวแปร หรือสูตร By Parts $\int u\,dv = uv - \int v\,du$ พร้อมเหตุผลตามแนวทาง LIATE

  2. *Substituted Expression:* แสดงการกำหนด $u, dv$ และคำนวณ $du, v$ แยกชัดเจนในบรรทัด 3287-3290; สำหรับ u-sub แสดง $u = g(x)$ และ $du = g'(x)\,dx$ หรือ $dx = \frac{du}{g'(x)}$ ในบรรทัด 3337

  3. *Intermediate Algebra:* แสดงการแทนค่าลงในสูตร และคำนวณอินทิกรัลส่วนที่เหลือ $\int v\,du$ ในบรรทัด 3296; ใน u-sub แสดงการตัดทอนตัวแปรเดิมจนเหลือตัวแปร $u$ ล้วนในบรรทัด 3340

  4. *Domain Restriction:* ฟังก์ชัน `_get_domain_note()` ในบรรทัด 3164-3183 สกัดเงื่อนไข เช่น ฐานลอการิทึม $> 0$, ตัวส่วน $\neq 0$, ฐานรากคู่ $\geq 0$

  5. *Exact Result:* ทุกเส้นทางคำตอบไม่จำกัดเขตลงท้ายด้วย $+C$ และแสดงผลลัพธ์แม่นตรง

- **API & Status:** คงคีย์เดิมทั้งหมด (`ok`, `result`, `latex`, `steps`, `expr`, `u_candidate`, `du_candidate`, `status`, `warning`, `error`, `variable`) เพิ่มเฉพาะคีย์ไม่ทำลายสัญญาเดิม (`method`, `parts_info`); ค่า `status` คงเดิมเป็น `"elementary"` หรือ `"non_elementary"`

### 4.2 ปริพันธ์ไม่ตรงแบบ (`utils/improper_solver.py`)

- **สถานะ:** **MET**

- **การตรวจสอบจุดบกพร่องตั้งต้นและข้อกำหนดเฉพาะ:**

  1. *Endpoint Singularities (จุดเอกฐานที่ขอบเขต):* แก้ไขฟังก์ชัน `_is_singular_at_point()` ตรวจสอบทั้งลิมิตและค่าไม่นิยาม
     - ขอบล่าง $a$ เป็นเอกฐาน (เช่น $1/\sqrt{x}$ บน $[0, 1]$): บรรทัด 2803-2810 สร้างลิมิต $\lim_{t \to a^+} \int_t^b$ ถูกต้องตามข้อกำหนด (แก้ไขจากเดิมที่เคยสร้างผิดเป็น $t \to b$)
     - ขอบบน $b$ เป็นเอกฐาน (เช่น $1/\sqrt{1-x}$ บน $[0, 1]$): บรรทัด 2844-2851 สร้างลิมิต $\lim_{t \to b^-} \int_a^t$ ถูกต้อง

  2. *Interior Singularities (จุดเอกฐานภายใน):* บรรทัด 2726-2766 แยกช่วงที่จุดเอกฐาน $c \in (a, b)$ ออกเป็นสองลิมิต และมีข้อความระบุชัดเจนว่าหากมีฝั่งใดลู่ออก ทั้งอินทิกรัลจะลู่ออก (ห้ามนำ $\pm\infty$ มาหักล้างกัน)

  3. *Infinite Bounds (ช่วงอนันต์):* รองรับ $(-\infty, \infty)$, $(-\infty, b]$, $[a, \infty)$ ครบถ้วน

  4. *API & Status:* คืนค่า `status` เป็น `"finite"`, `"divergent"` หรือ `"unsupported"` ถูกต้องตรงตามสัญญาเดิม

### 4.3 ปริมาตรทรงตันจากการหมุน (`utils/volume_solver.py`)

- **สถานะ:** **MET**

- **การตรวจสอบตามสัญญา Universal Step Contract:**

  1. *Axis & Radius:* ระบุแกนหมุนคือแกน $x$ ชัดเจนในข้อความขั้นตอน (บรรทัด 4414, 4468); ระบุรัศมีเป็นระยะทางตั้งฉากจากแกนหมุน

  2. *Outer / Inner Radii:* วิธี Washer แจกแจงรัศมีนอก $R(x)$ และรัศมีใน $r(x)$ แยกกันชัดเจนในบรรทัด 4468-4471

  3. *Integration Variable & Order:* ระบุตัวแปรการอินทิเกรต $dx$ และทิศทางการกวาดตามแกน

  4. *Exact Result in $k\pi$:* คำนวณค่า `vol_val = int_val * sp.pi` เชิงสัญลักษณ์ ทำให้ได้คำตอบแม่นตรงติดค่า $\pi$ เช่น $\frac{8\pi}{3}$ ผ่าน `_to_latex(vol_val)`

  5. *Invalid Inputs & Boundary Cases:* ปฏิเสธขอบเขตกลับด้าน $b \le a$ ด้วย `ValueError` (บรรทัด 4366-4368) และปฏิเสธ method ที่ไม่ถูกต้อง (บรรทัด 4371)

---

## 5. สถานะโมดูลที่ไม่ได้ตรวจสอบในรอบนี้ (Explicitly Unverified Modules)

เพื่อปฏิบัติตามหลักการตรวจสอบแบบจำกัดขอบเขต (Bounded review) และไม่รับรองงานส่วนที่ยังไม่ได้สืบค้นโค้ดครบถ้วน โมดูลต่อไปนี้มีสถานะเป็น **UNVERIFIED**:

1. **Module 1 — ลิมิต (`utils/limit_solver.py`):** ยังไม่ได้ตรวจสอบความครบถ้วนของ 4 กลุ่มอาการในโค้ดจริง

2. **Module 2 — อนุพันธ์และเส้นสัมผัส (`utils/tangent_solver.py`, `utils/sympy_solver.py`):** ยังไม่ได้ตรวจสอบการระบุกฎลูกโซ่และจุดไม่หาอนุพันธ์ได้

3. **Module 5 — พื้นที่ระหว่างเส้นโค้ง (`utils/area_solver.py`):** ยังไม่ได้ตรวจสอบการแจกแจงจุดตัดและการแบ่งช่วงย่อย

---

## 6. ข้อบกพร่องที่ยืนยันจากโค้ด (Source-Confirmed Defects)

### 6.1 ข้อบกพร่องด้านการทดสอบที่ผลิตซ้ำได้จริง (Reproduced Failure)

- **ตำแหน่ง:** `tests/test_substitution_solver.py:126`

- **ข้อกำหนดที่ละเมิด:** Definition of Done ข้อ 49 ("`pytest tests/ -v` ผ่านทั้งหมด")

- **อาการที่พบ:**
  ```text
  FAILED tests/test_substitution_solver.py::test_substitution_page_apptest_render
  FileNotFoundError: AppTest script not found at .../tests/pages/substitution.py.
  Relative paths are resolved against the file that calls AppTest.from_file().
  ```

- **สาเหตุ:** การเรียก `AppTest.from_file("pages/substitution.py")` ส่งสตริงสัมพัทธ์เข้าไป ทำให้ Streamlit ตีความเทียบกับตำแหน่งไฟล์เทสต์ในโฟลเดอร์ `tests/` กลายเป็น `tests/pages/substitution.py` ซึ่งไม่มีอยู่จริง

### 6.2 ข้อบกพร่องด้านความสอดคล้องของเอกสาร (Documentation Contradiction)

- **ตำแหน่ง:** `docs/worked-solutions-pr-body.md` เทียบกับ `utils/riemann_solver.py:146-248`

- **ข้อกำหนดที่ละเมิด:** คำสั่งมอบหมายงานหมวด 4.4 และ 5.1 (การรายงานความจริงเกี่ยวกับโมดูลรีมันน์)

- **อาการที่พบ:** PR body ประกาศว่าไม่ได้แตะโมดูลรีมันน์เลย แต่ใน commit `4982811` มีการแก้โค้ดจริง 95 บรรทัด

### 6.3 ข้อบกพร่องด้านการขยายขอบเขตนอกคำสั่ง (Scope Creep)

- **ตำแหน่ง:** `utils/theme.py`, `pages/creators.py`, และ UI pages อื่นๆ

- **ข้อกำหนดที่ละเมิด:** คำสั่งมอบหมายงานหมวด 0 (Out of scope)

---

## 7. ข้อเสนอแนะการแก้ไขขั้นต่ำ (Minimal Proposed Repairs)

1. **แก้ไข Path ในเทสต์ `tests/test_substitution_solver.py:126`:**
   ปรับให้อ้างอิงพาธแบบ absolute เช่นเดียวกับ `tests/test_pages_apptest.py`:
   ```python
   from pathlib import Path
   PAGES_DIR = Path(__file__).resolve().parent.parent / "pages"
   at = AppTest.from_file(str(PAGES_DIR / "substitution.py"))
   ```

2. **แก้ไขข้อความใน PR Body ให้ตรงกับความจริง:**
   แก้ไข `docs/worked-solutions-pr-body.md` ให้ระบุว่ามีการปรับปรุงขั้นตอนใน `utils/riemann_solver.py` หรือทำการ revert การแก้ไขใน `utils/riemann_solver.py` หากต้องการยกสิทธิ์ให้ session อื่นดูแลตามข้อตกลงเดิม

3. **พิจารณาแยกหรือ Revert การเปลี่ยนแปลง UI/Theme:**
   ตัดไฟล์ `pages/creators.py` และการแก้สไตล์ Neo-brutalist ใน `utils/theme.py` ออกจาก PR นี้ เพื่อให้ PR #1 มุ่งเน้นเฉพาะการเพิ่มความลึกของ solver steps ตามที่ได้รับอนุมัติ

---

## 8. ข้อจำกัดของการตรวจสอบ (Review Limitations)

1. การตรวจสอบนี้ดำเนินการบนสแนปช็อต commit `fa6761c9e7ee53e55690b8bea5d56e30b04d835e`
2. การตรวจโค้ดเชิงลึกจำกัดเฉพาะ 3 โมดูล solver (substitution, improper, volume) และการตรวจเช็คโมดูลรีมันน์ตามคำสั่งมอบหมายงานเท่านั้น
3. โมดูลลิมิต, อนุพันธ์/เส้นสัมผัส, และพื้นที่ระหว่างเส้นโค้ง ไม่ได้รับการตรวจสอบในรอบนี้ จึงไม่สามารถรับรองความสมบูรณ์ของทั้ง 7 โมดูลได้
