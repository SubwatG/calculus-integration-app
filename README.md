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

## 🚀 ฟังก์ชันหลักที่พัฒนาแล้ว (Core Modules)

### 1. พื้นที่ใต้กราฟและการลู่เข้าของรีมันน์ (Riemann Convergence Sandbox)
* คำนวณผลบวกรีมันน์ 3 วิธี: จุดปลายซ้าย ($L_n$), จุดปลายขวา ($R_n$) และจุดกึ่งกลาง ($M_n$)
* แถบสไลเดอร์ปรับจำนวนช่วงย่อย $n \in [2, 100]$ พร้อมเรนเดอร์แท่งสี่เหลี่ยมแนบกราฟสด
* ตารางเปรียบเทียบความคลาดเคลื่อน ($\text{Error} = |I_{\text{exact}} - I_{\text{approx}}|$) แสดงการลู่เข้าหาค่าจริงอย่างแม่นยำ

### 2. ห้องทดลองการตัดสินใจเลือกเทคนิคการอินทิเกรต (Integration Techniques Scaffolding)
* **การเปลี่ยนตัวแปร ($u$-Substitution):** จำแนกการเลือกตัวแปรเป็น 3 ระดับ  
  *(🟢 เหมาะสมที่สุด / 🟡 ถูกกฎแต่ไม่ช่วยให้ง่ายขึ้น / 🔴 ผิดหลักการ)*
* **การอินทิเกรตทีละส่วน (Integration by Parts & LIATE Rule):**  
  โจทย์ทดสอบ $\int x e^x dx$ จำลองการเลือกคู่ $u, dv$ หากเลือกสลับกัน ระบบจะขึ้นแถบเตือนสีส้มทันทีว่าดีกรีของ $x$ เพิ่มขึ้นเป็น $x^2$ ทำให้เกิดกับดักความซับซ้อน

### 3. แบบทดสอบวัดมโนทัศน์ (Conceptual Diagnostic Quiz with Delayed Feedback)
* รวมคำถามมโนทัศน์ระดับมหาวิทยาลัย 5 ข้อ (รีมันน์, การแทนค่า, โดเมน $1/x$, จุดเอกฐาน, บายพาร์ท)
* **ระบบตรวจคำตอบ 2 จังหวะ:** หากตอบผิดในครั้งแรก ระบบจะไม่เฉลยคำตอบ แต่จะแสดง **"💡 คำใบ้ชี้นำความคิด"** ให้ผู้เรียนได้ฉุกคิดและลองตอบใหม่อีกครั้ง

### 4. ตัวคำนวณเชิงสัญลักษณ์แท้จริง (SymPy CAS Engine)
* แยกการคำนวณคณิตศาสตร์ด้วย SymPy โดยตรง (ไม่พึ่งพา External API ภายนอก)
* สกัดผลลัพธ์เป็นสมการคณิตศาสตร์ $\LaTeX$ คมชัดผ่าน KaTeX

---

## 📂 สถาปัตยกรรมและโครงสร้างโปรเจกต์ (Project Architecture)

โปรเจกต์แยกความรับผิดชอบออกเป็น 5 ชั้นตามหลัก Separation of Concerns (SoC):

```text
calculus-integration-app/
├── app.py                      # Main entry point และ router (st.navigation)
├── pages/                      # หน้าจอส่วนต่อประสานผู้ใช้ (UI Presentation)
│   ├── home.py                 # หน้าแรกและเมนูนำทาง
│   ├── riemann.py              # บทเรียนมโนทัศน์ผลบวกรีมันน์ (เสร็จสมบูรณ์)
│   ├── substitution.py         # เทคนิคการอินทิเกรต (u-Sub & By Parts) (เสร็จสมบูรณ์)
│   ├── solver.py               # เครื่องคิดเลขสัญลักษณ์ SymPy
│   ├── quiz.py                 # เกมทบทวนมโนทัศน์แบบมีคำใบ้ (เสร็จสมบูรณ์)
│   ├── lessons.py              # เอกสารเนื้อหาอ้างอิง
│   └── history.py              # ประวัติคะแนนในเซสชัน
├── utils/                      # ชั้นตรรกะการคำนวณ (Mathematical Logic & Solvers)
│   ├── riemann_solver.py       # ตรรกะคำนวณพื้นที่และตาราง Error ของรีมันน์
│   ├── substitution_solver.py  # ตรรกะคำนวณปริพันธ์และการแทนค่าตัวแปร
│   ├── sympy_solver.py         # ตัวคำนวณสัญลักษณ์ SymPy (diff, int, limit)
│   ├── plotter.py              # วาดกราฟเรขาคณิตด้วย Matplotlib (Agg backend)
│   ├── quiz_engine.py          # ตัวโหลดและตรวจข้อสอบ
│   ├── math_render.py          # ตัวช่วยจัดรูปแบบ LaTeX
│   └── theme.py                # ธีมและการจัดรูปแบบ UI
├── data/
│   ├── lessons/                # บทเรียน Markdown ภาษาไทย
│   └── quizzes/                # คลังข้อสอบ JSON พร้อมคำใบ้และคำอธิบาย
├── tests/                      # ชุดทดสอบ Unit Test อัตโนมัติ (pytest tests/ -v)
└── docs/                       # ศูนย์รวมเอกสารโครงการ (ดูรายละเอียดใน docs/README.md)
    ├── proposal/               # เล่มโครงร่าง, สไลด์นำเสนอ (slide-deck.html), คู่มือสอบ
    ├── architecture/           # พิมพ์เขียวและสถาปัตยกรรมระบบแม่บท
    ├── mockup/                 # ตัวสาธิตต้นแบบ (master-interactive-demo.html)
    └── debate/                 # บันทึกการตรวจสอบความรัดกุมเชิงวิชาการ
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
