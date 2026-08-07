# Calculus Tutor: Integration

Streamlit teaching app สำหรับแคลคูลัสเบื้องต้น เรื่องอินทิเกรต

## สำหรับนักศึกษา

โปรเจกต์นี้ออกแบบให้รันได้ทั้ง Windows และ Linux โดยใช้ Python + Streamlit

เอกสารสำหรับเริ่มต้นบน Windows:

- [คู่มือเริ่มต้นสำหรับนักศึกษาบน Windows](docs/windows-student-setup.md)
- [Streamlit และ Python Notes สำหรับโปรเจกต์นี้](docs/streamlit-python-notes.md)

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
- `pages/lessons.py`: โหลดเนื้อหาบทเรียนแคลคูลัสจากไฟล์ Markdown
- `pages/topics.py`: เลือกหัวข้อหลักของการเรียนและแมปไปยังบทเรียนที่มีอยู่
- `pages/solver.py`: เครื่องคิดเลขแก้โจทย์อินทิเกรต อนุพันธ์ และลิมิตด้วย SymPy
- `pages/quiz.py`: เกมทบทวนความรู้พร้อมเฉลยและคำอธิบายทีละข้อ
- `pages/history.py`: แสดงประวัติคะแนนที่สะสมในเซสชันปัจจุบัน
- `pages/help.py`: คำอธิบายการใช้งาน ไวยากรณ์ SymPy และข้อจำกัด
- `data/lessons/`: เนื้อหาบทเรียนภาษาไทยรูปแบบ Markdown
- `data/quizzes/`: คลังข้อสอบรูปแบบ JSON
- `utils/content_loader.py`: ฟังก์ชันโหลดไฟล์บทเรียนพร้อม cache
- `utils/quiz_engine.py`: Engine สำหรับโหลดและตรวจแบบทดสอบ
- `utils/theme.py`: Custom CSS styling (Chakra Petch font, lavender sidebar, cards, heroes)
- `utils/sympy_solver.py`: ตัวคำนวณสัญลักษณ์ (SymPy) สำหรับอินทิเกรต อนุพันธ์ และลิมิต

## Development notes

- เขียนเนื้อหาเป็นภาษาไทยใน `data/lessons/*.md`
- ใช้ English สำหรับ code, file names, variable names และ comments
- ใช้ `$...$` สำหรับ inline math และ `$$...$$` สำหรับ display math
- Quiz ทุกข้อต้องมี `explanation`
- ไม่ใช้ Wolfram API

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
