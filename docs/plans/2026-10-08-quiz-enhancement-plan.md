# แผนการปรับปรุงหน้า Quiz และคลังโจทย์มโนทัศน์แคลคูลัส (Implementation Plan)

> **Goal:** ปรับปรุงหน้า Quiz ใน `calculus-integration-app`: ขยายโจทย์เป็น 10 ข้อต่อหัวข้อ (รวม 30 ข้อ), กระจายตำแหน่งเฉลยอย่างสมดุล (A/B/C/D), แก้ปัญหาการแสดงผลสูตรคณิตศาสตร์ KaTeX ในตัวเลือก, และยกระดับดีไซน์ UI ให้อ่านง่าย สบายตา และมีขั้นตอนการเรียนรู้ (Pedagogy) ที่ชัดเจน

**Architecture:** 
1. Data Layer: JSON Question Banks ใน `data/quizzes/*.json` กระจายเฉลยแบบสุ่มสมดุล (Shuffled balanced answers) พร้อมคำอธิบายและ Hint ละเอียดระดับมหาวิทยาลัย
2. UI Layer: ปรับปรุง `pages/quiz.py` โดยเปลี่ยนจาก `st.button` (ซึ่งไม่รองรับ KaTeX) มาใช้ `st.radio` หรือ Math-rendered option cards พร้อมระบบตรวจคำตอบ 2 จังหวะ (ตรวจ -> แนะแนวทาง -> เฉลย)
3. Quality Assurance: เพิ่ม automated tests ใน `tests/test_quiz_data.py` ตรวจสอบความถูกต้องของโจทย์ จำนวน 10 ข้อต่อหมวด และการกระจายตัวของตำแหน่งคำตอบ

**Tech Stack:** Python 3.12, Streamlit, KaTeX / LaTeX, SymPy, pytest

---

## Global Constraints & Quality Gates
- **Math Conventions:** นิพจน์คณิตศาสตร์ต้องใช้ `$inline$` และ `$$display$$` ถูกต้อง ไม่หลุด syntax
- **No Answer Leak:** ก่อนกดส่งคำตอบหรือเฉลย ต้องไม่มีการใบ้หรือเฉลยหลุดในตัวเลือก
- **Answer Distribution:** ในแต่ละชุด 10 ข้อ คำตอบที่ถูกต้องต้องกระจายตัวตามตัวเลือก A, B, C, D (ตัวเลือกละประมาณ 2-3 ข้อ) ห้ามเฉลยตกอยู่ที่ A ทั้งหมดเด็ดขาด
- **Anti-Bloat & YAGNI:** ใช้ Standard Library และ Streamlit Native Components เป็นหลัก ไม่เพิ่ม Third-party library เกินจำเป็น
- **No Broken Imports:** โค้ดต้องทำงานได้ทั้งการรันผ่าน `streamlit run app.py` และการรันเฉพาะหน้า `streamlit run pages/quiz.py`

---

## รายละเอียดงาน (Tasks Breakdown)

### Task 1: ขยายคลังข้อสอบเป็น 10 ข้อต่อหัวข้อ และสลับตำแหน่งเฉลยให้กระจายตัว (A/B/C/D)

**Files:**
- Modify: `data/quizzes/basic_rules.json` (เพิ่มจาก 5 เป็น 10 ข้อ, สลับ choices)
- Modify: `data/quizzes/riemann.json` (เพิ่มจาก 5 เป็น 10 ข้อ, สลับ choices)
- Modify: `data/quizzes/techniques.json` (เพิ่มจาก 5 เป็น 10 ข้อ, สลับ choices)

**Requirements:**
1. **Basic Rules (10 ข้อ):**
   - ข้อ 1-5 เดิม: สลับลำดับใน `choices` ให้เฉลยกระจาย ไม่ตกที่ A
   - ข้อ 6-10 ใหม่: เพิ่มโจทย์มโนทัศน์เชิงลึก เช่น
     - ความหมายของปฏิยานุพันธ์และค่าคงตัว $C$
     - คุณสมบัติเชิงเส้นของปริพันธ์ $\int (af(x) + bg(x))dx$
     - ทฤษฎีบทหลักมูลของแคลคูลัสส่วนที่ 1 ($\frac{d}{dx}\int_a^x f(t)dt$)
     - การอินทิเกรตฟังก์ชันพหุนามและข้อยกเว้นกรณี $n = -1$
     - สมมาตรของฟังก์ชันคู่-คี่บนช่วง $[-a, a]$
2. **Riemann Sums & Approximation (10 ข้อ):**
   - ข้อ 1-5 เดิม: สลับลำดับใน `choices` ให้เฉลยกระจาย
   - ข้อ 6-10 ใหม่:
     - Midpoint Rule ($M_n$) กับความเว้าของฟังก์ชัน (Concavity)
     - Simpson's Rule และคุณสมบัติการประมาณด้วยพาราโบลา
     - การเปรียบเทียบ Error Bound ระหว่าง $L_n, R_n, T_n, M_n$
     - นิยามของ Partition และ Norm ของ Partition $\|\mathcal{P}\| \to 0$
     - ตัวอย่างฟังก์ชันที่ไม่สามารถอินทิเกรตแบบรีมันน์ได้ (เช่น Dirichlet function)
3. **Integration Techniques (10 ข้อ):**
   - ข้อ 1-5 เดิม: สลับลำดับใน `choices` ให้เฉลยกระจาย
   - ข้อ 6-10 ใหม่:
     - การเลือกแทนค่าด้วยฟังก์ชันตรีโกณมิติ (Trigonometric Substitution เช่น $x = a\sin\theta$)
     - การแยกเศษส่วนย่อย (Partial Fractions) และเงื่อนไขดีกรีเศษ < ดีกรีส่วน
     - เทคนิค Tabular Method (DI method) สำหรับ Integration by Parts ซ้ำหลายรอบ
     - การระบุข้อผิดพลาดคลาสสิกในการแทนค่าขอบเขตของ $u$ ในอินทิกรัลจำกัดเขต
     - การจัดรูปก่อนอินทิเกรต (Completing the square ในตัวส่วน)
4. ทุกข้อต้องมีฟิลด์: `topic`, `question`, `choices` (4 ตัวเลือก), `answer`, `hint`, `explanation` ครบถ้วน 100%

---

### Task 2: ปรับปรุง Test Suite และ Automated Audit Script

**Files:**
- Modify: `tests/test_quiz_data.py`
- Modify: `docs/testing/check-content-and-quiz.py`

**Requirements:**
1. ใน `tests/test_quiz_data.py`:
   - ตรวจสอบว่าแต่ละไฟล์มีโจทย์อย่างน้อย 10 ข้อ (`assert len(data) >= 10`)
   - ตรวจสอบการกระจายตัวของตำแหน่งคำตอบ (Answer Distribution Entropy): ตำแหน่งแรก (Index 0 / Choice A) ต้องไม่เกิน 40% ของจำนวนข้อในแต่ละไฟล์
   - ตรวจสอบว่าค่า `answer` ตรงกับหนึ่งในสมาชิกของ `choices` แบบ Case-sensitive & Verbatim
   - ตรวจสอบความสมบูรณ์ของ LaTeX delimiters (จับคู่ `$` และ `$$` ครบถ้วน)
2. ใน `docs/testing/check-content-and-quiz.py`:
   - ปรับ inventory count คาดหมายให้รองรับ 30 ข้อ
   - รันผ่านทุก Scenario (`all-correct`, `all-wrong`, `blank`, `partial`)

---

### Task 3: ออกแบบหน้าจอ `pages/quiz.py` ใหม่ (UI Redesign & KaTeX Support)

**Files:**
- Modify: `pages/quiz.py`

**Design & UX Enhancements:**
1. **KaTeX-First Option Selection:**
   - เปลี่ยนจากการใช้ `st.button` แสดงตัวเลือกสูตร (ซึ่ง Streamlit ไม่เรนเดอร์ KaTeX ในปุ่ม) มาใช้ `st.radio` พร้อมตัวเลือกที่จัดฟอร์แมตผ่าน `format_math_spacing` หรือการแสดง Markdown card สวยงาม
   - แสดงตัวเลือกเป็น A, B, C, D พร้อมสูตรคณิตศาสตร์ที่เรนเดอร์คมชัด 100%
2. **Visual Hierarchy & Card Design:**
   - ใช้ `render_hero` และ Status Badge แสดงหัวข้อที่เลือกอย่างชัดเจน
   - Progress bar ด้านบนแสดงความคืบหน้า (เช่น ข้อ 3/10) และคะแนนปัจจุบัน
   - กรอบคำถามเด่นชัด พร้อมฉากหลังหรือ Divider ที่แยกเนื้อหาออกจากตัวเลือก
3. **Two-Stage Pedagogical Feedback:**
   - ปุ่มส่งคำตอบ "ยืนยันคำตอบ (Submit)" เด่นชัด
   - **เมื่อตอบผิดครั้งแรก:** กล่องคำแนะนำสีส้ม/เหลือง (Hint Card) แสดงมโนทัศน์ชวนคิด พร้อมให้โอกาสเลือกตอบใหม่อีก 1 ครั้ง หรือกด "ขอดูเฉลยทันที"
   - **เมื่อเฉลย (Revealed):** 
     - แสดง Alert เขียว/แดง ชัดเจน
     - ตัวเลือกที่ถูกต้องแสดงสัญลักษณ์ `✓` และไฮไลต์ชัดเจน
     - กล่องอธิบายเฉลย (Explanation Card) แสดงวิธีคิดทางคณิตศาสตร์อย่างเป็นระบบ
     - ปุ่ม "ข้อถัดไป →" (Primary button) พาไปข้อถัดไป
4. **Summary & Review Screen:**
   - เมื่อทำครบ 10 ข้อ (หรือ 30 ข้อ) แสดงสรุปผลการทดสอบ
   - แสดงเกรด/ระดับความเข้าใจ (เช่น ยอดเยี่ยม, ดีมาก, ควรทบทวนเพิ่ม)
   - มี Accordion/Expander ให้กางดูทบทวนคำตอบของตัวเองเทียบกับเฉลยทีละข้อได้ทั้งหมด
   - ปุ่ม "ลองทำใหม่อีกครั้ง" และ "กลับสู่หน้าบทเรียน"

---

### Task 4: การทดสอบ Verification และ Integration Check

**Verification Steps:**
1. รัน `pytest tests/test_quiz_data.py` ให้ผ่าน 100% เขียวทั้งหมด
2. รัน `python docs/testing/check-content-and-quiz.py` ให้ผ่าน 100% (30 ข้อ 3 ไฟล์)
3. รัน Streamlit AppTest หรือ Code syntax check ให้มั่นใจว่าไม่มี Runtime Exception / Session State error
4. ตรวจสอบการแสดงผลภาษาไทยและการเรนเดอร์ KaTeX ไม่มีสัญลักษณ์แปลกปลอมหลุดรอด
