# รายงานการตรวจทานเชิงมาตรฐาน (STANDARDS Axis Review)

**เป้าหมายการตรวจทาน:** ตรวจสอบความสอดคล้องตามมาตรฐานของคลังโค้ด (`AGENTS.md`), ความถูกต้องเชิงโครงสร้าง, และความเสี่ยงด้านความปลอดภัยใน Pull Request #1 (`feat/worked-solutions-detail`)  
**อ้างอิงรหัสการเปลี่ยนแปลง (Base...Head):** `d36dd7e19dc834a3e572431c9f551a80157c9e9e...fa6761c9e7ee53e55690b8bea5d56e30b04d835e`  
**สถานะการตรวจสอบ:** Snapshot Pinned (`/home/kitti/.hermes/profiles/teaching-orchestrated/cache/scratch/calculus-pr-1-133929`)

---

## 1. ข้อค้นพบหลัก (Key Findings)

### ข้อค้นพบที่ 1: การแก้ไขโมดูล Riemann ขัดแย้งกับคำประกาศใน PR และเสี่ยงต่อการเขียนทับงานพร้อมกัน (Concurrent Work Hazard)

- **ระดับความรุนแรง:** วิกฤต (Critical)
- **ตำแหน่งไฟล์:** `utils/riemann_solver.py:150-241` (commit `4982811`)
- **กฎที่อ้างอิง:** คำประกาศขอบเขตงานใน PR Body ("strictly untouched per instructions concurrent session") และมาตรฐานความปลอดภัยในการทำงานร่วมกัน
- **หลักฐานเชิงประจักษ์:** ใน PR Body ระบุไว้อย่างชัดเจนว่า:
  > *`Note on Riemann Module: Per instructions, the Riemann module (utils/riemann_solver.py, tests/test_riemann_solver.py, pages/riemann.py) was strictly untouched as it is concurrently managed by another session.`*  
  แต่ใน `pr.diff` พบการเพิ่มโค้ด 95 บรรทัด และลบ 7 บรรทัด โดยเขียนทับการคำนวณจุดสุ่มตัวอย่าง, สูตรซิกม่า, ความสูงแท่งสี่เหลี่ยมผืนผ้า, และการเปรียบเทียบค่าจริงปริพันธ์ใน `utils/riemann_solver.py`

- **การแก้ไขขั้นต่ำ (Minimal Repair):** ถอยการแก้ไข (revert) ใน `utils/riemann_solver.py` กลับสู่สภาพตาม commit base (`d36dd7e`) เพื่อป้องกันการทับซ้อนกับอีกเซสชันที่ดูแลโมดูลนี้อยู่

---

### ข้อค้นพบที่ 2: การละเมิดข้อกำหนด UI เรื่องห้ามใช้อีโมจิอย่างแพร่หลาย (Widespread Emoji Constraints Violation)

- **ระดับความรุนแรง:** สูง (High)
- **ตำแหน่งไฟล์:** 
  - `app.py:6, 25-51, 55-66` (ไอคอนหน้า, หัวข้อหมวดหมู่การนำทาง)
  - `pages/creators.py:5, 6, 203, 254, 265, 312, 357` (ไอคอน, แท็ก, และรูปภาพแทนตัว)
  - `pages/survey.py:7, 44, 55, 59, 62, 71, 75, 83`
  - `pages/home.py:230` (พบการใช้ em dash `—` ด้วย)
  - `pages/area_between.py:45, 58, 63`, `pages/improper_integrals.py:37, 50, 55`, `pages/volume_revolution.py:47, 60, 65`

- **กฎที่อ้างอิง:** `AGENTS.md` (Definition of Done บรรทัดที่ 50: *"ภาษาไทยใน UI ถูกต้อง ไม่มี em dash (—), ไม่มีลูกศร Unicode (→), ไม่มี emoji"* และส่วน Matt Pocock บรรทัดที่ 65: *"Zero emoji ใน UI"*)
- **หลักฐานเชิงประจักษ์:** PR มีการ commit เพิ่มอีโมจิโดยเจตนา (เช่น commit `73f166e` ระบุ *"polish creators profile emojis"*) ส่งผลให้อีโมจิหลุดเข้าไปในแถบ Sidebar, Navigation Groups, Expander, และเนื้อหาบทเรียนจำนวนมาก
- **การแก้ไขขั้นต่ำ (Minimal Repair):** ลบพารามิเตอร์ `icon="..."` ทั้งหมดใน `app.py` ตัดอีโมจิออกจากข้อความหัวข้อใน `st.navigation`, หน้าเนื้อหา และหน้า `pages/creators.py` ให้เป็นข้อความวิชาการภาษาไทยล้วน

---

### ข้อค้นพบที่ 3: การปรับแก้ Theme ส่วนกลางและการเพิ่มสไตล์แบบก้าวก่าย (Global Theme Redesign & Scope Creep)

- **ระดับความรุนแรง:** สูง (High)
- **ตำแหน่งไฟล์:** `utils/theme.py:272-368`, `pages/creators.py:9-200`
- **กฎที่อ้างอิง:** `AGENTS.md` กฎข้อ 6 (*"อย่าแก้ `utils/theme.py` เพื่อเปลี่ยนสี/ฟอนต์ของหน้าอื่น ใช้ parameter ของฟังก์ชันที่มีอยู่"*) และคำประกาศใน PR (*"without altering layout, theme, color palette, or typography"*)
- **หลักฐานเชิงประจักษ์:** 
  1. ใน `utils/theme.py` เพิ่มสไตล์ Neo-brutalism, แอนิเมชัน `@keyframes celebrationPop`, เปลี่ยนการแสดงผล `div[data-testid="stTabs"]` และบังคับใส่ฟอนต์แปลกปลอม (`Fredoka`, `Mali`, `Outfit`)
  2. ใน `pages/creators.py` มีการแทรกบล็อก `<style>` ขนาดยาวเกือบ 200 บรรทัดลงในหน้าเว็บโดยตรง แทนที่จะใช้ฟังก์ชันกลาง
  3. เกิดการขยายขอบเขตงานอย่างมหาศาล (Scope Creep/Shotgun Surgery) โดยเพิ่มหน้าประวัติผู้จัดทำ (`pages/creators.py` 457 บรรทัด) และแก้โค้ดไปถึง 27 ไฟล์ ทั้งที่หัวข้อ PR คือการปรับปรุง Solver

- **การแก้ไขขั้นต่ำ (Minimal Repair):** ย้ายหรือตัด CSS แอนิเมชัน/Tabs สไตล์แปลกปลอมออกจาก `utils/theme.py` คงโครงสร้างธีมมาตรฐานเดิม และแยกหน้าผู้จัดทำออกไปเป็น PR อิสระ

---

### ข้อค้นพบที่ 4: การอ้างสถานะการทดสอบเสร็จสมบูรณ์ที่คลาดเคลื่อน (Misleading Completion Claim & Broken Test Path)

- **ระดับความรุนแรง:** สูง (High)
- **ตำแหน่งไฟล์:** `tests/test_substitution_solver.py:124-134`
- **กฎที่อ้างอิง:** `AGENTS.md` (Definition of Done: *"`pytest tests/ -v` ผ่านทั้งหมด"*)
- **หลักฐานเชิงประจักษ์:** ใน PR Body อ้างว่าผ่านการทดสอบทั้งหมดแล้ว แต่การรันชุดทดสอบล้มเหลว 1 รายการ:
  `FileNotFoundError: pages/substitution.py` ในฟังก์ชัน `test_substitution_page_apptest_render()` เนื่องจากใช้ Relative Path ใน `AppTest.from_file("pages/substitution.py")` ซึ่ง Streamlit จะ resolve เทียบกับตำแหน่งของไฟล์ทดสอบ (`tests/pages/substitution.py`)

- **การแก้ไขขั้นต่ำ (Minimal Repair):** ย้ายการทดสอบหน้าเว็บไปไว้ที่ `tests/test_pages_apptest.py` หรือกำหนด Path ให้สัมพันธ์กับ root อย่างถูกต้อง เช่น `Path(__file__).parent.parent / "pages/substitution.py"`

---

## 2. การประเมินกลิ่นโค้ดเชิงสถาปัตยกรรม (Fowler Smells Baseline)

1. **Duplicated Code (โค้ดซ้ำซ้อน):** พบฟังก์ชัน `_to_latex(sym_obj)` ถูกเขียนซ้ำใน 4 ไฟล์: `utils/area_solver.py:17`, `utils/improper_solver.py:27`, `utils/substitution_solver.py:49`, `utils/volume_solver.py:25` ควรย้ายไปรวมที่ `utils/sympy_solver.py`

2. **Shotgun Surgery & Divergent Change (การกระจายความรับผิดชอบที่ไม่รวมศูนย์):** การปรับแต่งสไตล์ปุ่มและการตอบสนองแบบกระตุก (dynamic feedback) ถูกแยกใส่ทั้งใน `utils/theme.py`, `pages/quiz.py:220`, และ inline style ใน `pages/creators.py` ทำให้ยากต่อการบำรุงรักษา

3. **Encapsulation Breach / Feature Envy (การเข้าถึงตัวแปรภายใน):** `utils/substitution_solver.py:27` มีการเรียกใช้ private function `from utils.sympy_solver import _clean_calculus_input, _get_variable` ควรปรับเป็น public API หรือจัดสรรโมดูลอินพุตพาร์สเซอร์ให้ชัดเจน

4. **Primitive Obsession & Data Clumps:** ผลลัพธ์ของแต่ละ Solver ส่งกลับเป็น raw dictionary (`dict[str, Any]`) ซึ่งไม่มี schema กำกับแน่นอน ทำให้แต่ละโมดูลส่ง key ไม่สอดคล้องกัน (เช่น บางโมดูลมี `details`, บางโมดูลมี `steps`, บางโมดูลมี `status`)

---

## 3. ขอบเขตที่ยังไม่ได้ตรวจสอบ (Unreviewed Areas)

- **ความถูกต้องทางคณิตศาสตร์เชิงลึกของทุก Step ใน 7 โมดูล:** มุ่งเน้นตรวจสอบความสอดคล้องตามมาตรฐาน (Standards Axis) ไม่ได้พิสูจน์ทฤษฎีบททุกสาขาในเชิงลึก
- **การประเมินการโต้ตอบหน้าเว็บแบบ Manual Dynamic Interaction:** ตรวจสอบผ่านโครงสร้างโค้ดและชุดทดสอบ AppTest ไม่ได้เปิดเบราว์เซอร์กดทดสอบด้วยมือครบทุกเงื่อนไข
