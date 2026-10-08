# Calculus Learning Sandbox: Interactive Integration App
> **สื่อการเรียนรู้คณิตศาสตร์เชิงโต้ตอบสำหรับแคลคูลัสเบื้องต้น (การอินทิเกรต)**  
> โครงงานระดับปริญญาตรี สาขาวิชาคณิตศาสตร์ประยุกต์ ภาควิชาคณิตศาสตร์ มหาวิทยาลัยเกษตรศาสตร์

[![Python](https://img.shields.io/badge/Python-3.11%2B-blue.svg)](https://www.python.org/)
[![Framework](https://img.shields.io/badge/Framework-Streamlit-red.svg)](https://streamlit.io/)
[![Engine](https://img.shields.io/badge/CAS-SymPy-green.svg)](https://www.sympy.org/)
[![Tests](https://img.shields.io/badge/Tests-Pytest-yellow.svg)](https://pytest.org/)

---

## 📌 วิสัยทัศน์และเป้าหมายของโครงงาน (Project Overview)

ในปัจจุบัน ผู้เรียนมีเครื่องมือแก้โจทย์คณิตศาสตร์หลากหลายประเภท เช่น **ChatGPT, WolframAlpha** หรือ **GeoGebra** แต่เครื่องมือส่วนใหญ่มักเน้นการ **"ให้คำตอบสำเร็จรูป"** หรือเป็นเพียง **"กระดานวาดกราฟว่างเปล่า"** ซึ่งไม่ได้ช่วยส่งเสริมกระบวนการคิดหรือชี้จุดเข้าใจผิดของผู้เรียน

**Calculus Learning Sandbox** ถูกออกแบบขึ้นภายใต้หลักคิด **"ห้องทดลองมโนทัศน์ (Conceptual Sandbox)"** ที่ทำหน้าที่เป็นนั่งร้านทางปัญญา (Pedagogical Scaffolding) เพื่อช่วยให้ผู้เรียน:
1. **สร้างสัญชาตญาณเชิงภาพ (Visual & Geometric Intuition):** เชื่อมโยงความหมายของสูตรคณิตศาสตร์กับภาพเรขาคณิต เช่น การลู่เข้าของผลบวกรีมันน์
2. **ฝึกกระบวนการตัดสินใจ (Decision-Making Scaffolding):** ทดลองเลือกเทคนิคและตัวแปรในการอินทิเกรต โดยระบบจะสะท้อนผลลัพธ์ว่าสมการง่ายขึ้นหรือซับซ้อนกว่าเดิม
3. **ตรวจจับจุดเข้าใจผิดที่พบบ่อย (Misconception Detection):** มีระบบแจ้งเตือนกรณีพิเศษ เช่น จุดไม่ต่อเนื่องที่ตัวหารเป็นศูนย์ หรือการเลือกคู่ตัวแปรที่ผิดทิศทาง
4. **ไม่เฉลยคำตอบในทันที (Delayed Feedback & Active Learning):** แบบทดสอบมีระบบคำใบ้ชี้นำความคิด (Hint) เพื่อเปิดโอกาสให้ผู้เรียนได้คิดทบทวนก่อนเปิดดูเฉลย

---

## ⚖️ ตารางเปรียบเทียบมิติการเรียนรู้ (4-Pillar Comparison Matrix)

| มิติการเปรียบเทียบ | ปัญญาประดิษฐ์สร้างข้อความ<br>*(ChatGPT / Gemini)* | โปรแกรมคำนวณสำเร็จรูป<br>*(WolframAlpha / Symbolab)* | โปรแกรมวาดกราฟทั่วไป<br>*(GeoGebra / Desmos)* | โครงงานของเรา<br>*(Calculus Learning Sandbox)* |
| :--- | :--- | :--- | :--- | :--- |
| **1. หน้าที่หลัก** | ตอบคำถามทั่วไปเชิงข้อความ | แก้โจทย์และคำนวณสำเร็จรูป | กระดานวาดกราฟว่างเปล่า | **ห้องทดลองคณิตศาสตร์สำหรับสร้างมโนทัศน์** |
| **2. การปฏิสัมพันธ์** | ทางเดียว (ถาม $\to$ อ่านคำตอบ) | ทางเดียว (ใส่โจทย์ $\to$ ดูผลลัพธ์) | ปรับกราฟอิสระบนกระดานว่าง | **โต้ตอบสองทางที่มีโครงสร้างนำทาง** |
| **3. การช่วยเหลือ** | บอกวิธีทำทั้งหมดทันที | แสดงผลลัพธ์ทันที (วิธีทำติดค่าบริการ) | ไม่มีระบบการสอนในตัว | **ไม่เฉลยคำตอบทันที มีคำใบ้ชี้นำความคิด** |
| **4. ตรวจจุดเข้าใจผิด** | ตรวจไม่ได้ เสี่ยงแต่งข้อมูลเท็จ | ตรวจไม่ได้ แจ้งเตือนแค่ไวยากรณ์ผิด | ตรวจไม่ได้ วาดตามที่พิมพ์ | **ตรวจจับจุดเข้าใจผิดและแจ้งเตือนตรรกะสด** |
| **5. ความเข้ากับหลักสูตร** | ตอบกว้าง ไม่ตรงบริบทรายวิชา | มีแต่เครื่องคิดเลข ไม่มีสรุปเนื้อหา | แยกส่วนกับเนื้อหา ไม่มีข้อสอบในตัว | **ครบวงจร: สรุปทฤษฎีไทย $\to$ กราฟ $\to$ ข้อสอบ** |
| **6. ต้นทุนการเข้าถึง** | โมเดลคิดวิเคราะห์คิดค่าบริการ | วิธีทำแบบละเอียดคิดค่าบริการสูง | ต้องพิมพ์สูตรเชิงเทคนิคเอง | **โอเพนซอร์ส 100% ใช้งานฟรีผ่านเว็บ** |

---

## 🚀 ฟังก์ชันหลักที่พัฒนาแล้ว (Core Learning Modules 1–7)

### 1. เส้นสัมผัสและอนุพันธ์ (Tangent Lines & Linear Approximation)
* คำนวณความชัน $m = f'(a)$ และสมการเส้นสัมผัส $y - f(a) = m(x - a)$ พร้อมภาพประกอบ
* แผงปุ่มลัดสัญลักษณ์คณิตศาสตร์ (Math Keypad) และปุ่มตัวอย่างโจทย์ยอดนิยม
* อธิบายมโนทัศน์การประมาณค่าเชิงเส้นเฉพาะที่ (Local Linear Approximation)

### 2. ลิมิตเข้าใกล้จุดและลิมิตที่อนันต์ (Limits, Directional Analysis & Asymptotes)
* วิเคราะห์ลิมิตซ้าย ($x \to a^-$) และลิมิตขวา ($x \to a^+$) พร้อมการ์ดมโนทัศน์ทิศทาง 2 คอลัมน์
* รองรับค่าสัญลักษณ์ ($\pi, \pi/2, e$) และลิมิตที่อนันต์ ($x \to \pm\infty$) พร้อมเส้นกำกับแนวนอน (Horizontal Asymptote)
* ตารางวิเคราะห์เชิงตัวเลข (Numerical Inspection) จำลองการบีบเข้าหาค่าลิมิต

### 3. พื้นที่ใต้กราฟและการลู่เข้าของรีมันน์ (Riemann Sums Convergence)
* คำนวณผลบวกรีมันน์ 3 วิธี: จุดปลายซ้าย ($L_n$), จุดปลายขวา ($R_n$) และจุดกึ่งกลาง ($M_n$)
* แถบสไลเดอร์ปรับจำนวนช่วงย่อย $n \in [2, 100]$ พร้อมเรนเดอร์แท่งสี่เหลี่ยมแนบกราฟสด
* ตารางเปรียบเทียบความคลาดเคลื่อน ($\text{Error} = |I_{\text{exact}} - I_{\text{approx}}|$) แสดงการลู่เข้าหาค่าจริงตามนิยาม $\int_a^b f(x)dx$

### 4. ห้องทดลองการตัดสินใจเลือกเทคนิคการอินทิเกรต (Integration Techniques: u-Sub & By Parts)
* **เข็มทิศการตัดสินใจ (Decision Compass):** เปรียบเทียบหลักการเมื่อไหร่ควรใช้ u-Sub (กฎลูกโซ่ย้อนกลับ) vs By Parts (กฎผลคูณย้อนกลับ)
* **การเปลี่ยนตัวแปร ($u$-Substitution Scaffolding):** 4 รูปแบบโจทย์ (ใต้กรณฑ์, เศษส่วน/ลอการิทึม, เลขชี้กำลัง/ตรีโกณ, ตัวแปรเหลือเศษ Linear Adjustment) พร้อมการเตือนกับดักความซับซ้อนและการตรวจสอบย้อนกลับด้วยอนุพันธ์
* **การอินทิเกรตทีละส่วน (Integration by Parts & LIATE Rule):** 4 รูปแบบโจทย์ (ลดดีกรีพีชคณิต, ปลดล็อคตรีโกณ, ลอการิทึมเดี่ยว $dv=dx$, การวนลูป Cyclic Integration)
* **เครื่องคิดเลข SymPy CAS:** 7 ปุ่มตัวอย่างโจทย์ยอดนิยม พร้อมระบบตรวจจับ Non-elementary integrals

### 5. พื้นที่ระหว่างเส้นโค้ง (Area Between Curves)
* คำนวณพื้นที่ปิดล้อม $\int_a^b [f(x) - g(x)] dx$ พร้อมหาจุดตัดอัตโนมัติ
* กราฟแรเงาพื้นที่ระหว่างเส้นโค้ง $f(x)$ และ $g(x)$ พร้อมเส้นแบ่งช่วง

### 6. ปริพันธ์ไม่ตรงแบบ (Improper Integrals)
* คำนวณอินทิกรัลไม่แท้ผ่านลิมิต: ช่วงกึ่งอนันต์ $[a, \infty)$, $(-\infty, b]$ และช่วงอนันต์สองทาง $(-\infty, \infty)$
* ตรวจจับจุดเอกฐานภายในช่วง (Interior Singularities) พร้อมแยกช่วงอินทิเกรต
* ตรวจสอบสถานะ ลู่เข้า (Convergent) หรือ ลู่ออก (Divergent) พร้อมกราฟแรเงา

### 7. ปริมาตรของรูปทรงตันจากการหมุน (Volumes of Revolution)
* คำนวณปริมาตรด้วยวิธีจาน/วงแหวน (Disk & Washer Methods) หมุนรอบแกน X หรือแกน Y
* จำลองภาพตัดขวางและพื้นที่ใต้กราฟก่อนการหมุน

### 8. เครื่องมือและการประเมิน (Tools & Evaluation)
* **เครื่องคิดเลขสัญลักษณ์ SymPy (Solver):** คำนวณ diff, int, limit พร้อม Math Keypad
* **แบบทดสอบมโนทัศน์ (Diagnostic Quiz):** คลังข้อสอบ 30 ข้อ (3 หมวด) พร้อมระบบคำใบ้ 2 จังหวะและการเฉลยพร้อมวิเคราะห์ช้อยส์
* **แบบประเมินความพึงพอใจ (SUS Survey):** แบบสอบถาม System Usability Scale 10 ข้อ ลิงก์ Google Forms และ QR Code

---

## 📂 สถาปัตยกรรมและโครงสร้างโปรเจกต์ (Project Architecture)

โปรเจกต์แยกความรับผิดชอบออกเป็น 5 ชั้นตามหลัก Separation of Concerns (SoC):

```text
calculus-integration-app/
├── app.py                      # Main entry point และ navigation router
├── pages/                      # หน้าจอส่วนต่อประสานผู้ใช้ (UI Presentation)
│   ├── home.py                 # หน้าแรกและเมนูนำทาง
│   ├── tangent.py              # โมดูล 1: เส้นสัมผัสและอนุพันธ์
│   ├── limit_approach.py       # โมดูล 2: ลิมิตเข้าใกล้จุดและลิมิตที่อนันต์
│   ├── riemann.py              # โมดูล 3: ผลรวมรีมันน์
│   ├── substitution.py         # โมดูล 4: เทคนิคการอินทิเกรต (u-Sub & By Parts)
│   ├── area_between.py         # โมดูล 5: พื้นที่ระหว่างเส้นโค้ง
│   ├── improper_integrals.py   # โมดูล 6: ปริพันธ์ไม่ตรงแบบ
│   ├── volume_revolution.py    # โมดูล 7: ปริมาตรของรูปทรงตัน
│   ├── solver.py               # เครื่องคิดเลขสัญลักษณ์ SymPy
│   ├── quiz.py                 # แบบทดสอบมโนทัศน์ 30 ข้อ (พร้อมคำใบ้)
│   ├── survey.py               # แบบประเมินความพึงพอใจ (SUS Questionnaire & QR Code)
│   ├── lessons.py              # เอกสารเนื้อหาและทฤษฎีอ้างอิง
│   └── history.py              # ประวัติคะแนนในเซสชัน
├── utils/                      # ชั้นตรรกะการคำนวณ (Mathematical Logic & Solvers)
│   ├── keypad.py               # แผงปุ่มลัดสัญลักษณ์คณิตศาสตร์ (Shared Math Keypad)
│   ├── tangent_solver.py       # คำนวณความชันและสมการเส้นสัมผัส
│   ├── limit_solver.py         # คำนวณลิมิตสองด้าน, ลิมิตที่อนันต์, กฎโลปีตาล
│   ├── riemann_solver.py       # ตรรกะคำนวณพื้นที่และตาราง Error ของรีมันน์
│   ├── substitution_solver.py  # ตรรกะคำนวณปริพันธ์, u-Sub, ตรวจจับ Non-elementary
│   ├── area_solver.py          # คำนวณพื้นที่ระหว่างเส้นโค้งและจุดตัด
│   ├── improper_solver.py      # คำนวณอินทิกรัลไม่แท้, ช่วง (-inf, inf), จุดเอกฐาน
│   ├── volume_solver.py        # คำนวณปริมาตรการหมุน (Disk & Washer)
│   ├── sympy_solver.py         # เครื่องมือคำนวณ SymPy ทั่วไป
│   ├── plotter.py              # วาดกราฟเรขาคณิตด้วย Matplotlib (Agg backend)
│   ├── quiz_engine.py          # ตัวโหลดและตรวจข้อสอบ
│   ├── math_render.py          # ตัวช่วยจัดรูปแบบ LaTeX / KaTeX ป้องกันข้อความหลุด
│   ├── theory.py               # คลังทฤษฎี ข้อควรระวัง และแนวทางการตัดสินใจ
│   └── theme.py                # ธีมและการจัดรูปแบบ UI
├── data/
│   ├── lessons/                # บทเรียน Markdown ภาษาไทย
│   └── quizzes/                # คลังข้อสอบ JSON (basic_rules, riemann, techniques)
├── tests/                      # ชุดทดสอบ Unit Test อัตโนมัติ (pytest tests/ -v ครบ 99/99 เคส)
└── docs/                       # ศูนย์รวมเอกสารโครงการ (ดูรายละเอียดใน docs/README.md)
```

---

## 📚 ศูนย์รวมเอกสารโครงการ (Documentation Hub)

ดูสารบัญเอกสารทั้งหมดอย่างละเอียดได้ที่ 📄 [docs/README.md](docs/README.md)

| หมวดหมู่เอกสาร | เอกสารสำคัญที่แนะนำ | รายละเอียด |
| :--- | :--- | :--- |
| **การสอบโครงร่าง** | [slide-deck.html](docs/proposal/slide-deck.html) | สไลด์นำเสนอ 20 สไลด์ พร้อม KaTeX |
| | [โครงร่างคณิตศาสตร์ประยุกต์.docx](docs/proposal/โครงร่างคณิตศาสตร์ประยุกต์.docx) | เล่มข้อเสนอโครงงานฉบับทางการ |
| | [proposal-defense-guide.html](docs/proposal/proposal-defense-guide.html) | คู่มือซักซ้อมตอบคำถามกรรมการ |
| **สถาปัตยกรรมระบบ** | [system-architecture-master.html](docs/architecture/system-architecture-master.html) | แผนผังสถาปัตยกรรมระบบแม่บท |
| **ตัวสาธิตต้นแบบ** | [master-interactive-demo.html](docs/mockup/master-interactive-demo.html) | สื่อจำลองแบบ Standalone (Canvas 2D) |
| **คู่มือนักศึกษา** | [windows-student-setup.md](docs/windows-student-setup.md) | ขั้นตอนติดตั้งและรันบน Windows |
| | [student-interactive-lesson-guide.md](docs/student-interactive-lesson-guide.md) | คู่มือการเขียนโค้ดเพิ่มบทเรียนใหม่ |

---

## 🛠️ วิธีการติดตั้งและรันระบบ (Quick Start)

### 1. ความต้องการของระบบ (Requirements)
* Python 3.11 หรือใหม่กว่า
* Git

### 2. รันบน Windows
เปิด PowerShell ในโฟลเดอร์ที่ต้องการ:
```powershell
git clone https://github.com/SubwatG/calculus-integration-app.git
cd calculus-integration-app
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
streamlit run app.py
```

### 3. รันบน Linux / macOS
```bash
git clone https://github.com/SubwatG/calculus-integration-app.git
cd calculus-integration-app
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
streamlit run app.py
```

เปิดเว็บเบราว์เซอร์ที่: `http://localhost:8501`

### 4. การรันชุดทดสอบ (Testing)
```bash
pytest tests/ -v
```

---

## 👥 ข้อมูลโครงงาน
* **สาขาวิชา:** คณิตศาสตร์ประยุกต์ (Applied Mathematics)
* **ภาควิชา:** คณิตศาสตร์ คณะวิทยาศาสตร์ มหาวิทยาลัยเกษตรศาสตร์
* **ที่ปรึกษาโครงงาน:** อ.ดร.กิตติพงษ์ ทรัพย์วัฒนชัย
