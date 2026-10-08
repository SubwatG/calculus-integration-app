# Changelog — Calculus Learning Sandbox

บันทึกประวัติการปรับปรุงและพัฒนาโครงการ Calculus Learning Sandbox (`SubwatG/calculus-integration-app`)

---

## [2026-10-08] — Production-Ready Upgrade & Pedagogical Expansion

รอบการปรับปรุงใหญ่เพื่อยกระดับเว็บแอปพลิเคชันให้พร้อมสำหรับระดับ Production ครอบคลุมทั้งความถูกต้องเชิงคณิตศาสตร์ สถาปัตยกรรมซอฟต์แวร์ และการสร้างมโนทัศน์ (Pedagogical Scaffolding)

### 1. การผสานสาขาและแก้ไขการแสดงผล UI/KaTeX (Branch Merge & UI Fixes)
* **Merge `fix/katex-clipping-and-bounds`:** ผนวกการปรับแก้สไตล์ KaTeX clipping ที่นิสิตได้ส่งมา ทำให้ตัวสูตรและกรอบไม่ถูกตัดขอบ
* **Emoji Policy Compliance:** กู้คืน Emoji ที่เป็นมิตรใน UI ของนิสิตทั้งหมดตามเจตนารมณ์ผู้ใช้
* **Defensive Math Formatting (`utils/math_render.py`):**
  * พัฒนาฟังก์ชัน `auto_wrap_bare_latex()` ตรวจจับสัญลักษณ์ LaTeX ลอย ๆ (เช่น `\pi`, `\frac{...}{...}`, `\infty`) ที่อยู่นอก `$ ... $` และห่อหุ้มอัตโนมัติ ป้องกันปัญหา KaTeX ไม่เรนเดอร์ข้ามทุกหน้าจอ
  * จัดการเว้นวรรคช่องว่างระหว่างภาษาไทยและสัญลักษณ์คณิตศาสตร์ด้วย `format_math_spacing()`
* **Popular Points Grid Layout (`pages/limit_approach.py` & `utils/theme.py`):**
  * ปรับโครงสร้างปุ่มจุดยอดนิยมจาก 8 คอลัมน์แถวเดียวที่แคบจนมองไม่เห็นตัวอักษร เป็นแบบกริด 2 แถว $\times$ 4 คอลัมน์ (ความกว้างปุ่ม $\ge 54\text{ px}$)
  * ปรับแต่งตัวอักษรในธีมให้เป็นตัวหนา คมชัด สวยงาม (`font-weight: 700`)

### 2. ขยายขีดความสามารถของโมดูลแคลคูลัส (Core Modules 1–7)
* **โมดูล 1: เส้นสัมผัสและอนุพันธ์ (`pages/tangent.py`):**
  * ติดตั้งแผงปุ่มลัดสัญลักษณ์คณิตศาสตร์ (Shared Math Keypad)
  * เพิ่มขั้นตอนอธิบายมโนทัศน์การประมาณค่าเชิงเส้นเฉพาะที่ (Local Linear Approximation)
* **โมดูล 2: ลิมิตเข้าใกล้จุดและลิมิตที่อนันต์ (`pages/limit_approach.py` & `utils/limit_solver.py`):**
  * เพิ่มการ์ดมโนทัศน์ทิศทาง 2 คอลัมน์ (ซ้าย $x \to a^-$ vs ขวา $x \to a^+$) เปลี่ยนตามจุด $a$ แบบไดนามิก
  * ปลดล็อกการป้อนค่าสัญลักษณ์จำกัด ($\pi, \pi/2, e$) และลิมิตที่อนันต์ ($x \to \pm\infty, \pm\text{oo}$)
  * วาดเส้นกำกับแนวนอน (Horizontal Asymptote) และเพิ่มตารางตรวจสอบเชิงตัวเลขขนาดใหญ่ (Numerical Inspection)
  * แปลงปุ่มทั้งหมดเป็น `on_click` callback แก้ปัญหา `StreamlitWidgetAlreadyInstantiatedError` ได้ 100%
* **โมดูล 3: ผลรวมรีมันน์ (`pages/riemann.py` & `utils/riemann_solver.py`):**
  * ติดตั้ง Math Keypad และปุ่มโจทย์ยอดนิยม
  * เสริมข้อสังเกตมโนทัศน์การลู่เข้าเมื่อ $n \to \infty$ ($\Delta x \to 0$) สู่นิยามปริพันธ์จำกัดเขต $\int_a^b f(x) dx$
* **โมดูล 4: เทคนิคการอินทิเกรต (`pages/substitution.py`):**
  * **Decision Compass:** เพิ่มกล่องเข็มทิศการตัดสินใจเปรียบเทียบ u-Sub (กฎลูกโซ่ย้อนกลับ) vs By Parts (กฎผลคูณย้อนกลับ)
  * **u-Substitution Scaffolding:** ขยายคลังโจทย์ฝึกตัดสินใจจาก 1 ข้อ เป็น 4 รูปแบบ (ฟังก์ชันใต้กรณฑ์, ฟังก์ชันเศษส่วน/ลอการิทึม, ฟังก์ชันเลขชี้กำลัง/ตรีโกณ, เทคนิคตัวแปรเหลือเศษ Linear Adjustment $x = u - 1$)
  * **Integration by Parts Scaffolding:** ขยายคลังโจทย์ฝึกตัดสินใจจาก 1 ข้อ เป็น 4 รูปแบบ (ลดดีกรีพีชคณิต, ปลดล็อคตรีโกณ, ลอการิทึมเดี่ยว $dv = dx$, การวนลูป Cyclic Integration)
  * **SymPy CAS Calculator:** เพิ่มปุ่มโหลดโจทย์ลัด 7 รูปแบบ พร้อมตรวจจับ Non-elementary integrals ($e^{-x^2}$)
* **โมดูล 5: พื้นที่ระหว่างเส้นโค้ง (`pages/area_between.py`):**
  * ติดตั้ง Math Keypad สองชุดสำหรับ $f(x)$ และ $g(x)$ พร้อมปุ่มตัวอย่างโจทย์
* **โมดูล 6: ปริพันธ์ไม่ตรงแบบ (`pages/improper_integrals.py` & `utils/improper_solver.py`):**
  * รองรับช่วงอนันต์สองทาง $(-\infty, \infty)$ เช่น $\int_{-\infty}^\infty \frac{1}{1+x^2} dx = \pi$ และช่วง $(-\infty, b]$
  * รองรับการใส่ขอบเขตเป็นตัวเลข สัญลักษณ์ ($\pi, e$) และ $\pm\infty$
  * อัปเกรดการแรเงากราฟสมดุลสองฝั่งใน `utils/plotter.py`
* **โมดูล 7: ปริมาตรของรูปทรงตัน (`pages/volume_revolution.py`):**
  * แปลงปุ่มเป็น Callback Pattern และติดตั้ง Math Keypad

### 3. ระบบแบบทดสอบและแบบประเมิน (Assessment & Diagnostic Tools)
* **แบบทดสอบมโนทัศน์ (`pages/quiz.py` & `data/quizzes/*.json`):**
  * ขยายคลังข้อสอบจาก 15 ข้อ เป็น **30 ข้อ** (10 ข้อ/หมวด: basic_rules, riemann, techniques)
  * ออกแบบระบบตรวจคำตอบ 2 จังหวะ พร้อมปุ่มคำใบ้ชี้นำความคิด (Hint System)
  * แสดงเฉลยอย่างละเอียดพร้อมเน้นสีและไฮไลต์ตัวเลือกที่ถูก (`st.success`) และตัวเลือกที่ผู้เรียนตอบผิด (`st.error`)
* **แบบประเมินความพึงพอใจ (`pages/survey.py`):**
  * กู้คืนระบบแบบสอบถาม System Usability Scale (SUS) 10 ข้อตามมาตรฐานวิชาการ
  * ติดตั้งกล่องลิงก์ Google Forms และ QR Code สำหรับให้นิสิตและผู้ทดลองสแกนประเมิน

### 4. การทดสอบและการรับประกันคุณภาพ (Quality Assurance & Test Suite)
* ขยายชุดทดสอบอัตโนมัติ Unit Tests ใน `tests/` จาก 94 เป็น **99 ข้อทดสอบ**
* ผลการรัน `pytest`: **99/99 passed (100% PASS)**
* ตรวจสอบสดผ่าน Chromium headless (`browser-box`) ทุกหน้าจอ ไม่พบบั๊กหรือคอนฟลิกต์
* บันทึกการเปลี่ยนแปลงขึ้น GitHub `main` เรียบร้อย
