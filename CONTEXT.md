# Context

## Integration

อินทิเกรต (integration) คือหัวข้อหลักของแอป ใช้ครอบคลุมทั้งแนวคิดปฏิยานุพันธ์และการสะสมในระดับแคลคูลัสเบื้องต้น

## Lesson (interactive)

บทเรียน (lesson) ในปัจจุบันคือบทเรียน interactive ที่ประกอบด้วย 5 ส่วนต่อบท:
theory dict ใน `utils/theory.py`, solver ใน `utils/<topic>_solver.py`,
plotter ใน `utils/plotter.py`, หน้า UI ใน `pages/<topic>.py` และ test ใน `tests/`

บทเรียนตัวอย่างที่สมบูรณ์: Riemann Sum (`pages/riemann.py`)
บทเรียนที่เหลือ (tangent, limit, substitution, volume, area_between, improper)
เป็น skeleton รอ implement ตาม `docs/interactive-lessons-plan.md`

## Reference content

`data/lessons/*.md` (60 ไฟล์ แบ่ง cal1/cal2) คือเอกสารอ้างอิงฉบับเต็ม
ไม่ใช่บทเรียนหลัก เปิดดูได้ใน tab "เอกสารอ้างอิง" ของหน้าเรียน

## Quiz

แบบทดสอบ (quiz) คือชุดคำถาม multiple choice ที่ตรวจด้วยคำตอบที่กำหนดไว้ และต้องมี explanation ทุกข้อ

## Score

คะแนน (score) คือผลรวมคำตอบถูกของ quiz ใน session ปัจจุบัน เก็บผ่าน `st.session_state`
