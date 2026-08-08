# calculus-integration-app — AGENTS.md

คู่มือสำหรับผู้พัฒนา (นักศึกษา project) ที่จะแก้ไขหรือเพิ่มฟีเจอร์ในแอปนี้

## โครงสร้างโปรเจกต์

```text
app.py                  # entry point, st.navigation router
pages/*.py              # หน้าเว็บแต่ละหน้า
utils/*.py              # logic ที่ใช้ซ้ำ (ไม่ใส่ logic ไว้ใน pages)
data/lessons/           # บทเรียนภาษาไทย รูปแบบ Markdown + LaTeX
data/quizzes/           # ข้อสอบ รูปแบบ JSON
tests/                  # pytest
```

## กฎการเขียนโค้ด (บังคับ)

1. เขียนข้อความผู้ใช้ (UI, บทเรียน, คำอธิบาย) เป็นภาษาไทย
2. เขียน code, ชื่อตัวแปร, ชื่อฟังก์ชัน, ชื่อไฟล์, comment เป็นภาษาอังกฤษ
3. แยก logic ออกจาก UI เสมอ: ถ้าฟังก์ชันคำนวณ/ตรวจคำตอบ/โหลดข้อมูล ต้องไปไว้ใน `utils/`
   แล้ว import เข้ามาใช้ใน `pages/` ห้ามเขียน logic ยาวๆ ไว้ในหน้า
4. ทุกหน้าใช้ `render_hero("ชื่อ", "คำอธิบาย")` จาก `utils.theme` เป็นหัวหน้าแรก
5. state ที่ต้องจำข้าม rerun (คะแนน, คำตอบ, index) ต้องเก็บใน `st.session_state`
   และ init ก่อนใช้เสมอ
6. อย่าแก้ `utils/theme.py` เพื่อเปลี่ยนสี/ฟอนต์ของหน้าอื่น ใช้ parameter ของฟังก์ชันที่มีอยู่
7. ค่าคงที่ที่ใช้ซ้ำ (เช่น ชื่อ quiz topic) ให้ประกาศไว้ด้านบนของไฟล์ ไม่ hardcode ซ้ำในฟังก์ชัน

## กฎ Markdown และ LaTeX ในบทเรียน

- ใช้ `$...$` สำหรับสมการ inline และ `$$...$$` สำหรับสมการ display เท่านั้น
  ห้ามใช้ `\(...\)` หรือ `\[...\]`
- ทุกไฟล์บทเรียนมี frontmatter: title, course, chapter, section, type, source, status
- H1 เดียวต่อไฟล์, เลขหัวข้อห้ามซ้ำ, ตัดบรรทัดไม่เกิน ~500 ตัวอักษร
- คำศัพท์คณิตศาสตร์: ไทยก่อน แล้ววงเล็บภาษาอังกฤษครั้งแรก

## การรันและทดสอบ

```bash
source .venv/bin/activate
streamlit run app.py        # รันแอป
pytest tests/ -v            # รัน test
```

ก่อนส่งงาน (definition of done):

- [ ] `streamlit run app.py` รันได้ ไม่มี error
- [ ] หน้าใหม่/ฟีเจอร์ใหม่ทำงานตามที่โจทย์กำหนด
- [ ] มี test ครอบ logic ใน utils (ถ้าแก้หรือเพิ่ม logic)
- [ ] `pytest tests/ -v` ผ่านทั้งหมด
- [ ] ภาษาไทยใน UI ถูกต้อง ไม่มี em dash (—), ไม่มีลูกศร Unicode (→), ไม่มี emoji
- [ ] commit เป็น branch ของตัวเอง แล้ว push

## งานแรกที่แนะนำ (สำหรับนักศึกษา)

แก้ `utils/content_loader.py` หรือเพิ่มหน้า interactive lesson ใหม่ใน `pages/`
โดยทำตามกฎด้านบน และเพิ่ม test ใน `tests/` ให้ครอบ logic ที่เขียน

## ข้อควรระวัง

- อย่า commit ไฟล์ `.venv/`, `__pycache__/`, ไฟล์ PDF/HTML ที่เกิดจากการ render
- อย่าแก้ไฟล์ใน `data/lessons/_archive/` (เป็นไฟล์เก่าที่เก็บไว้)
- อย่าใส่ API key หรือ secret ลงในโค้ด
