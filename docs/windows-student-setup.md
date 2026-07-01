# คู่มือเริ่มต้นสำหรับนักศึกษาบน Windows

เอกสารนี้สำหรับนักศึกษาที่ต้องการดึงโปรเจกต์ `calculus-integration-app` จาก GitHub มารันบน PC หรือ laptop Windows

## 1. สิ่งที่ต้องติดตั้งก่อน

### 1.1 ติดตั้ง Python

ดาวน์โหลด Python จาก:

```text
https://www.python.org/downloads/
```

ระหว่างติดตั้ง ให้เลือกตัวเลือก:

```text
Add python.exe to PATH
```

ตรวจสอบหลังติดตั้งโดยเปิด PowerShell แล้วรัน:

```powershell
py --version
```

ควรเห็น Python 3.11 หรือใหม่กว่า

### 1.2 ติดตั้ง Git for Windows

ดาวน์โหลดจาก:

```text
https://git-scm.com/download/win
```

ตรวจสอบหลังติดตั้ง:

```powershell
git --version
```

### 1.3 ติดตั้ง Visual Studio Code

ดาวน์โหลดจาก:

```text
https://code.visualstudio.com/
```

แนะนำให้ติดตั้ง extension:

- Python
- GitHub Pull Requests

## 2. รับ invitation จาก GitHub

เมื่อนักศึกษาได้รับ invitation จากอาจารย์ ให้กดรับก่อน โดยเข้าได้จาก:

- email ที่ผูกกับ GitHub
- GitHub notification
- หน้า repository ที่อาจารย์ส่งลิงก์ให้

ถ้ายังไม่กดรับ invitation จะ clone private repository ไม่ได้

## 3. Clone โปรเจกต์ลงเครื่อง

เปิด PowerShell แล้วไปยังโฟลเดอร์ที่ต้องการเก็บงาน เช่น Desktop:

```powershell
cd Desktop
```

จากนั้น clone repository:

```powershell
git clone <REPOSITORY_URL>
cd calculus-integration-app
```

ให้แทน `<REPOSITORY_URL>` ด้วย URL จริงของ GitHub repository เช่น:

```text
https://github.com/<OWNER>/calculus-integration-app.git
```

## 4. สร้าง virtual environment

ในโฟลเดอร์โปรเจกต์ ให้รัน:

```powershell
py -m venv .venv
```

จากนั้น activate:

```powershell
.\.venv\Scripts\Activate.ps1
```

ถ้า activate ไม่ได้และ PowerShell แสดงข้อความเกี่ยวกับ execution policy ให้รัน:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

จากนั้นปิด PowerShell เปิดใหม่ เข้าโฟลเดอร์โปรเจกต์อีกครั้ง แล้ว activate ซ้ำ:

```powershell
cd Desktop\calculus-integration-app
.\.venv\Scripts\Activate.ps1
```

เมื่อสำเร็จ จะเห็น `(.venv)` นำหน้าบรรทัดคำสั่ง

## 5. ติดตั้ง package

รันคำสั่ง:

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

ขั้นตอนนี้ต้องใช้อินเทอร์เน็ต

## 6. เปิดเว็บแอป

รัน:

```powershell
streamlit run app.py
```

ถ้าสำเร็จ จะเห็น URL ประมาณนี้:

```text
http://localhost:8501
```

เปิด URL นี้ใน browser เพื่อใช้งานเว็บแอป

## 7. การทำงานรอบต่อไป

ครั้งต่อไปไม่ต้องสร้าง `.venv` ใหม่ ให้เปิด PowerShell แล้วรัน:

```powershell
cd Desktop\calculus-integration-app
.\.venv\Scripts\Activate.ps1
git pull
streamlit run app.py
```

## 8. วิธีส่งงานกลับ GitHub

ก่อนแก้งาน ให้ดึงงานล่าสุด:

```powershell
git pull
```

สร้าง branch ของตัวเอง:

```powershell
git checkout -b your-name-update
```

หลังแก้ไขไฟล์แล้ว ตรวจสถานะ:

```powershell
git status
```

บันทึกการเปลี่ยนแปลง:

```powershell
git add .
git commit -m "Update lesson content"
git push -u origin your-name-update
```

จากนั้นเปิด Pull Request บน GitHub เพื่อให้อาจารย์ตรวจ

## 9. ปัญหาที่พบบ่อย

### `py` command not found

แปลว่า Windows ยังหา Python ไม่เจอ ให้ติดตั้ง Python ใหม่และเลือก `Add python.exe to PATH`

### `git` command not found

แปลว่ายังไม่ได้ติดตั้ง Git for Windows หรือยังไม่ได้เปิด PowerShell ใหม่หลังติดตั้ง

### Activate `.venv` ไม่ได้

ให้รัน:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### `streamlit` command not found

มักเกิดจากยังไม่ได้ activate `.venv` หรือยังไม่ได้ `pip install -r requirements.txt`

### เปิดเว็บไม่ได้

ตรวจว่า terminal ยังรัน `streamlit run app.py` อยู่ และลองเปิด:

```text
http://localhost:8501
```

## 10. กติกาการแก้ไฟล์

- เนื้อหาบทเรียนเขียนภาษาไทยใน `data/lessons/*.md`
- ชื่อไฟล์ โค้ด ตัวแปร และ comment ใช้ English
- สูตร inline ใช้ `$...$`
- สูตรแบบแยกบรรทัดใช้ `$$...$$`
- Quiz อยู่ใน `data/quizzes/*.json`
- Quiz ทุกข้อต้องมี `explanation`
