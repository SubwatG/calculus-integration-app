# Calculus Tutor: Integration

Streamlit teaching app สำหรับแคลคูลัสเบื้องต้น เรื่องอินทิเกรต

## สำหรับนักศึกษา

โปรเจกต์นี้ออกแบบให้รันได้ทั้ง Windows และ Linux โดยใช้ Python + Streamlit

เอกสารสำหรับเริ่มต้น:

- [คู่มือเริ่มต้นสำหรับนักศึกษาบน Windows](docs/windows-student-setup.md)
- [Step-by-step: สร้างบทเรียน interactive](docs/student-interactive-lesson-guide.md)
- [แผนบทเรียน interactive (หัวข้อ + ขอบเขต)](docs/interactive-lessons-plan.md)
- [คู่มือ Markdown และ LaTeX สำหรับบทเรียน](docs/markdown-latex-guide.qmd)
  - ดูแบบเว็บ (ออนไลน์): https://htmlpreview.github.io/?https://raw.githubusercontent.com/SubwatG/calculus-integration-app/main/docs/markdown-latex-guide.html
  - ดูแบบ PDF: [docs/markdown-latex-guide.pdf](docs/markdown-latex-guide.pdf)
- [กฎการเขียนโค้ดสำหรับนักศึกษา](AGENTS.md)

## Requirements

- Python 3.11 หรือใหม่กว่า
- Git
- Internet สำหรับติดตั้ง package ครั้งแรก

## Setup on Windows

เปิด PowerShell ในโฟลเดอร์ที่ต้องการเก็บงาน แล้วใช้คำสั่ง:

```powershell
git clone <REPOSITORY_URL>
cd calculus-integration-app
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
streamlit run app.py
```

ถ้า PowerShell ไม่ยอม activate virtual environment ให้รันคำสั่งนี้หนึ่งครั้ง:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

จากนั้นปิด PowerShell แล้วเปิดใหม่ ก่อน activate อีกครั้ง

## Setup on Linux

```bash
git clone <REPOSITORY_URL>
cd calculus-integration-app
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
streamlit run app.py
```

## Run after setup

Windows:

```powershell
.\.venv\Scripts\Activate.ps1
streamlit run app.py
```

Linux:

```bash
source .venv/bin/activate
streamlit run app.py
```

เมื่อรันสำเร็จ เปิดเว็บที่:

```text
http://localhost:8501
```

## Structure

- `app.py`: Main entry point และ router ด้วย `st.navigation` จัดกลุ่มหน้าเป็นภาษาไทย
- `pages/home.py`: หน้าแรกและค้นหาเมนู พร้อมแสดงคะแนน quiz ล่าสุด
- `pages/lessons.py`: หน้าบทเรียน (tab interactive จาก THEORY_CONTENT + tab เอกสารอ้างอิง)
- `pages/topics.py`: เลือกหัวข้อหลักของการเรียนและแมปไปยังบทเรียนที่มีอยู่
- `pages/riemann.py`: บทเรียน interactive ตัวอย่าง (พื้นที่ใต้กราฟ / Riemann Sum) — เสร็จสมบูรณ์
- `pages/tangent.py`, `pages/limit_approach.py`, `pages/substitution.py`,
  `pages/volume_revolution.py`, `pages/area_between.py`, `pages/improper_integrals.py`:
  บทเรียน interactive เพิ่มเติม (skeleton รอ implement)
- `pages/solver.py`: เครื่องคิดเลขแก้โจทย์อินทิเกรต อนุพันธ์ และลิมิตด้วย SymPy
- `pages/quiz.py`: เกมทบทวนความรู้พร้อมเฉลยและคำอธิบายทีละข้อ
- `pages/history.py`: แสดงประวัติคะแนนที่สะสมในเซสชันปัจจุบัน
- `pages/help.py`: คำอธิบายการใช้งาน ไวยากรณ์ SymPy และข้อจำกัด
- `data/lessons/`: เนื้อหาบทเรียนภาษาไทยรูปแบบ Markdown (เอกสารอ้างอิง cal1/cal2)
- `data/quizzes/`: คลังข้อสอบรูปแบบ JSON
- `utils/content_loader.py`: ฟังก์ชันโหลดไฟล์บทเรียนพร้อม cache
- `utils/quiz_engine.py`: Engine สำหรับโหลดและตรวจแบบทดสอบ
- `utils/theme.py`: Custom CSS styling (ธีมขาว plain, Chakra Petch font)
- `utils/sympy_solver.py`: ตัวคำนวณสัญลักษณ์ (SymPy) สำหรับอินทิเกรต อนุพันธ์ และลิมิต
- `utils/theory.py`: เนื้อหาทฤษฎีบทเรียน interactive (THEORY_CONTENT dict)
- `utils/riemann_solver.py` + `utils/{topic}_solver.py`: logic การคำนวณทีละขั้นของแต่ละบทเรียน
- `utils/plotter.py`: วาดกราฟ matplotlib สำหรับบทเรียน interactive
- `utils/math_render.py`: helper จัดการ LaTeX/KaTeX (error guard)
- `tests/`: pytest ครอบ logic ใน utils/ (รันด้วย `pytest tests/ -v`)
- `docs/`: เอกสารสำหรับผู้พัฒนา (คู่มือ Markdown/LaTeX, แผนบทเรียน interactive, step-by-step guide)
- `AGENTS.md`: กฎการเขียนโค้ดสำหรับนักศึกษา developer

## Development notes

- เขียนเนื้อหาเป็นภาษาไทยใน `data/lessons/*.md` (เอกสารอ้างอิง)
- บทเรียน interactive: เนื้อหาทฤษฎีอยู่ใน `utils/theory.py` (THEORY_CONTENT)
  ดู `docs/interactive-lessons-plan.md` และ `docs/student-interactive-lesson-guide.md`
- ใช้ English สำหรับ code, file names, variable names และ comments
- ใช้ `$...$` สำหรับ inline math และ `$$...$$` สำหรับ display math
- Quiz ทุกข้อต้องมี `explanation`
- logic ต้องแยกไป `utils/` ห้ามเขียนยาวในหน้า
- รัน test ก่อนส่ง: `pytest tests/ -v`
- ไม่ใช้ Wolfram API
- อย่า commit ไฟล์ render artifacts (`.pdf`, `.tex`, `.html` ใน docs/) — ถูก ignore แล้ว

## Git workflow สำหรับทีม

ก่อนเริ่มงานทุกครั้ง:

```bash
git pull
```

หลังแก้ไขงาน:

```bash
git status
git add .
git commit -m "Describe your change"
git push
```

ถ้าทำงานหลายคน แนะนำให้แต่ละคนสร้าง branch ของตัวเองก่อนแก้:

```bash
git checkout -b lesson-basic-rules-update
```
