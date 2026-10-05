# แผนการทดสอบระบบ (System Test Plan) — calculus-integration-app

เอกสารนี้เป็น **แผนการทดสอบแบบ manual (คนกดทดสอบเอง)** สำหรับเว็บแอป Streamlit
"Calculus Learning Sandbox" ใช้คู่กับชุดเคสใน [`manual-test-cases.csv`](manual-test-cases.csv)

> **สถานะเอกสาร:** CSV นี้เป็นรายการ planned สำหรับการทดสอบครบชุด ยังไม่ได้รันครบทุกเคส
> ได้ทดลองบางสถานการณ์ผ่าน browser-box แล้ว ดู `browser-test-report.md` และ `browser-evidence.json`
> ผลจาก browser แยกเก็บต่างหาก ไม่เปลี่ยนเคสที่ตรวจเพียงบางส่วนให้เป็นผ่านทั้งเคส

---

## 1. ขอบเขต (Scope)

**ทดสอบ (in scope):** การนำทาง (navigation), วิดเจ็ตอินพุตของบทเรียน interactive,
การวาดกราฟ (plots), สถานะและประวัติของ quiz, หน้าแบบประเมินความพึงพอใจ (survey)
ในโหมดไม่ส่งข้อมูลออกภายนอก, การป้อนข้อมูลผิดรูปแบบ/ค่าขอบเขต (malformed input & domain
boundaries), การเข้าถึง (accessibility) และประสิทธิภาพ (performance)

**ไม่ทดสอบ (out of scope):**

- ความถูกต้องเชิงคณิตศาสตร์ของโจทย์/เฉลยแบบละเอียด (เป็นความรับผิดชอบของ dataset + automated runner แยกต่างหาก)
- การแก้ไขบั๊กหรือปรับพฤติกรรมแอป (เอกสารนี้ไม่แตะ source)
- การทดสอบอัตโนมัติ (pytest/integration) — มีอยู่แล้วใน `tests/`
- การทดสอบ Google Forms ปลายทาง (เป็นระบบภายนอก)

---

## 2. สภาพแวดล้อมอ้างอิง (Environment)

| รายการ | ค่า |
|---|---|
| Entry point | `app.py` (ใช้ `st.navigation`) |
| คำสั่งรัน | `source .venv/bin/activate && streamlit run app.py` |
| Dependencies | `streamlit>=1.58.0`, `sympy>=1.14`, `matplotlib>=3.9`, `numpy>=1.26` |
| บราเซอร์เป้าหมาย | Chromium/Firefox เวอร์ชันล่าสุด + สมาร์ตโฟน 1 เครื่อง (สำหรับหน้า survey/QR) |
| ธีม | `.streamlit/config.toml` (light, primaryColor `#FB7185`) |

---

## 3. ความครอบคลุมหน้า/เส้นทาง (Page & Route Coverage)

เส้นทางที่ลงทะเบียนใน `app.py` (13 หน้าใน 4 กลุ่ม):

| กลุ่ม | หน้า | ไฟล์ |
|---|---|---|
| ภาพรวม | หน้าหลัก | `pages/home.py` |
| ภาพรวม | ภาพรวมบทเรียนและทฤษฎี | `pages/lessons.py` |
| โมดูลการเรียนรู้ (6) | 1. เส้นสัมผัสและอนุพันธ์ | `pages/tangent.py` |
| โมดูลการเรียนรู้ (6) | 2. ลิมิตเข้าใกล้จุด | `pages/limit_approach.py` |
| โมดูลการเรียนรู้ (6) | 3. ผลรวมรีมันน์ | `pages/riemann.py` |
| โมดูลการเรียนรู้ (6) | 4. เทคนิคการอินทิเกรต | `pages/substitution.py` |
| โมดูลการเรียนรู้ (6) | 5. พื้นที่ระหว่างเส้นโค้ง | `pages/area_between.py` |
| โมดูลการเรียนรู้ (6) | 6. ปริพันธ์ไม่ตรงแบบ | `pages/improper_integrals.py` |
| เครื่องมือ | เครื่องคิดเลข SymPy | `pages/solver.py` |
| เครื่องมือ | แบบทดสอบมโนทัศน์ | `pages/quiz.py` |
| เครื่องมือ | แบบประเมินความพึงพอใจ (SUS) | `pages/survey.py` |
| ข้อมูลระบบ | ประวัติคะแนนในเซสชัน | `pages/history.py` |
| ข้อมูลระบบ | คู่มือการใช้งาน | `pages/help.py` |

**หน้าที่มีไฟล์แต่ไม่ถูกนำทาง (unregistered / orphaned):**

- `pages/volume_revolution.py` — มีอยู่จริงและถูกอ้างใน `lessons.py`
  (`INTERACTIVE_PAGES["volume"]`) แต่ **ไม่ถูก `st.Page(...)` ใน `app.py`**
  → ปุ่ม "ไปลองเล่นแบบ interactive" ของหัวข้อ volume จะ `st.switch_page` ไปหน้าที่ไม่ได้ลงทะเบียน
  ซึ่ง Streamlit จะ error (ดูเคส `UI-NAV-006`)

- `pages/topics.py` — มีไฟล์แต่ไม่ถูกนำทางและไม่มีปุ่มเชื่อมจากที่ใด (dead page)

> เคสทดสอบใน CSV จึงเจาะจง 13 หน้าหลัก + ตรวจ orphaned 2 หน้าเป็น "ช่องโหว่ที่ทราบ" (ไม่ใช่ expected pass)

---

## 4. กลยุทธ์การทดสอบรายพื้นที่

### 4.1 Navigation (UI-NAV-xxx)
ตรวจโครง sidebar 4 กลุ่ม, การโหลดแต่ละหน้าโดยไม่ error, ปุ่มการ์ดในหน้าหลัก,
การค้นหาเมนู, ปุ่ม `st.switch_page` จากหน้า lessons, ลิงก์ออกภายนอกของ survey
(ตรวจ href แต่ **ห้ามกดส่ง**), และปุ่มกลับหน้าหลักของ quiz

### 4.2 Widgets (UI-WID-xxx)
ตรวจวิดเจ็ตของแต่ละหน้า: preset buttons, text_input, number_input, slider (ช่วง/step),
selectbox, segmented_control, radio ที่ `index=None` (ไม่มีค่าเริ่มต้น),
แท็บในหน้า substitution, และปุ่มคำนวณ `substitution` tab3 (ต้องกด ไม่ live)

### 4.3 Plots (UI-PLT-xxx)
ทุกหน้าใช้ matplotlib (Agg) แล้ว `st.pyplot`. ตรวจว่ากราฟแสดงถูกชนิด
(curve+tangent, เส้นลู่เข้า, สี่เหลี่ยมรีมันน์ 3 วิธี, แรเงาระหว่างโค้ง, การลู่เข้า improper)
และตรวจ fallback: เมื่อวาดไม่ได้ต้องขึ้น `st.warning` ภาษาไทย **ไม่ crash**

### 4.4 Quiz state & history (UI-QUZ/UI-HIS-xxx)
ตรวจ state machine ของ quiz: topic switch → reset, ตอบถูก → +score +reveal,
ตอบผิดครั้งแรก → hint (ยังไม่เฉลย ไม่เพิ่มคะแนน), ตอบผิดครั้งที่สอง → เฉลย,
ปุ่มบังคับดูเฉลย, ปุ่มข้อถัดไป, หน้า done สรุปผล, ปุ่มเล่นใหม่,
และประวัติใน `history.py` ที่อ่าน `st.session_state["quiz_scores"]`
(โดยเก็บถาวรเฉพาะใน session — reload แล้วหาย)

### 4.5 Survey — ไม่ส่งข้อมูลออกภายนอก (UI-SRV-xxx)
หน้า `survey.py` แสดง QR (จาก `docs/calculus-survey-qr.png`) และปุ่มลิงก์ไป Google Forms
**ไม่มีฟอร์มกรอกในแอป** ทดสอบเฉพาะการเรนเดอร์ + ตรวจปลายทางลิงก์
โดย **ห้ามกดลิงก์/ห้ามส่งข้อมูลใด ๆ** และยืนยันว่าไม่มี network request ส่งข้อมูลในตอนโหลดหน้า

### 4.6 Malformed input & domain boundaries (UI-INP-xxx)
ครอบคลุม: อินพุตว่าง, ไวยากรณ์ผิด (`x^^2`, `sin(`), สัญลักษณ์ไม่รู้จัก, implicit multiplication
(`2x`), `^` เทียบ `**`, ขอบเขตโดเมน (b<=a, f=g, f<g, เส้นโค้งตัดกัน, อินทิเกรตลู่ออก,
จุดที่หาอนุพันธ์ไม่ได้, 0/0) และค่าสุดขั้ว (เลขชี้กำลังสูง) — ตรวจว่าคืนข้อความไทย
ไม่ crash และสอดคล้องกับที่ source ระบุ

### 4.7 Accessibility (UI-ACC-xxx)
ตรวจฟอนต์ไทย, KaTeX/MathML, การนำทางด้วยคีย์บอร์ด, contrast, การไม่ใช้ emoji/อักขระต้องห้าม
ตาม Definition of Done ของ `AGENTS.md`, และการขยาย zoom

### 4.8 Performance (UI-PRF-xxx)
วัดเวลาโหลดหน้าแรก, การ recompute แบบ live ตอนพิมพ์, การวาดกราฟ, และโฟลว์ quiz
**เกณฑ์ทั้งหมดเป็นข้อเสนอเบื้องต้น (provisional) ต้องวัดจริงก่อนยืนยัน** (ดูข้อ 5)

---

## 5. เกณฑ์ประสิทธิภาพ — ข้อเสนอเบื้องต้น (PROVISIONAL)

> ตัวเลขทั้งหมดด้านล่างเป็น **ข้อเสนอเบื้องต้น ยังไม่ผ่านการวัดจริง**
> ห้ามอ้างเป็นผลทดสอบ ให้วัดบนเครื่องทดสอบแล้วบันทึกค่าจริงใน CSV

| รหัส | ตัวชี้วัด | เกณฑ์เสนอ (provisional) | วิธีวัด |
|---|---|---|---|
| UI-PRF-001 | โหลดหน้าแรก (cold, cache ว่าง) | ≤ 5.0 วินาที | DevTools Network/DOMContentLoaded |
| UI-PRF-002 | live recompute ต่อการพิมพ์ 1 ครั้ง | ≤ 1.0 วินาที | สังเกตการ rerun บนหน้า tangent/riemann |
| UI-PRF-003 | เรนเดอร์กราฟ 1 กราฟ | ≤ 2.0 วินาที | เวลาที่ `st.pyplot` ปรากฏ |
| UI-PRF-004 | riemann n=50 (คำนวณ+วาด) | ≤ 2.5 วินาที | ป้อน x^2, n=50 |
| UI-PRF-005 | ตอบ 1 ข้อใน quiz | ≤ 0.8 วินาที | จากคลิกถึงผลลัพธ์ |
| UI-PRF-006 | เปิดแอปแบบออฟไลน์ (บล็อก Google Fonts) | ยังใช้งานได้ มีฟอนต์ fallback | ปิด network แล้วเปิดหน้า |

---

## 6. เกณฑ์ผ่าน/ไม่ผ่าน (Pass/Fail)

- **ผ่าน:** พฤติกรรมตรงกับ "ผลคาดหวัง" ใน CSV, UI ภาษาไทยถูกต้อง, ไม่ crash, ไม่มี
  ข้อความ error ดิบของ Python หลุดถึงผู้ใช้

- **ไม่ผ่าน:** crash / traceback หลุด UI / ลิงก์ส่งข้อมูลออกนอกโดยไม่ตั้งใจ /
  state ผิด (คะแนนรีเซ็ตเอง, เฉลยก่อนตอบ) / กราฟวาดไม่ได้โดยไม่มี fallback

## 7. ช่องโหว่ที่ทราบจากการอ่าน source (Known Gaps)

1. **Orphaned pages**: `pages/volume_revolution.py` และ `pages/topics.py` ไม่ถูกนำทาง
   (`UI-NAV-006`, `UI-NAV-009`) — ปุ่ม volume ใน `lessons.py` เสี่ยง error

2. **improper latex ฮาร์ดโค้ด ∞**: `utils/improper_solver.py` ใช้ `\\infty` ใน `latex`
   เสมอ แม้เลือกขอบเขตจำกัด (`UI-INP-012`)

3. **area คืนค่า net signed**: `compute_area_between` ไม่ใส่ค่าสัมบูรณ์ ให้พื้นที่ติดลบ /
   ค่าตัดกันเป็นค่าสุทธิ (สอดคล้อง theory caution แต่ต้องยืนยันพฤติกรรม) (`UI-INP-008/009`)

4. **emoji/อักขระต้องห้าม**: `survey.py` และ `theme.py` มี emoji (📱🔒📝) และสัญลักษณ์
   ตกแต่ง ขัด Definition of Done ของ `AGENTS.md` (`UI-ACC-005`)

5. **ฟอนต์จาก CDN**: Google Fonts โหลดจากอินเทอร์เน็ต อาจกระทบ offline/performance (`UI-PRF-006`)
6. **history key ไม่ครบ**: `topic_titles` ใน `history.py` map เฉพาะ `basic_rules`
   หัวข้ออื่นจะแสดง key ดิบ (`UI-HIS-003`)

## 8. ความเชื่อมโยงกับ Definition of Done (`AGENTS.md`)

เคสที่รองรับ DoD: รันแอปไม่มี error (`UI-NAV-002`), ภาษาไทยถูกต้อง/ไม่มี emoji (`UI-ACC-005`),
SymPy parsing ถูก (`UI-INP-002/004/013`), กราฟแสดงได้ (`UI-PLT-001..005`)
