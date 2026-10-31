#!/usr/bin/env python3
"""
build_defense_deck.py
---------------------
สร้างสไลด์นำเสนอสอบโครงงาน (20 นาที) เป็น single-file HTML
โดยดึง CSS ธีมและ nav JS จากสไลด์สอบโครงร่างเดิม (docs/proposal/slide-deck.html)
มาใช้ซ้ำ เพื่อความต่อเนื่องทางภาพและลดความเสี่ยงจากการเขียน CSS ใหม่

ใช้งาน:
    python3 build_defense_deck.py

ผลลัพธ์:
    slide-deck-defense.html  (เปิดในเบราว์เซอร์ได้ทันที)
"""

import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPORT_DIR = HERE.parent
PROPOSAL_DECK = REPORT_DIR / "proposal" / "slide-deck.html"
THEME_CSS = HERE / "deck-theme-bauhaus.css"
OUT_PATH = HERE / "slide-deck-defense.html"

APP_URL = "https://calculus-integration-app-dwdsz8vq2omsddezfjvday.streamlit.app/"

# ----------------------------------------------------------------------------
# 1. โหลดธีม Bauhaus Pop (mirror ของ utils/theme.py) + nav JS จาก deck เดิม
# ----------------------------------------------------------------------------


def extract_theme(deck_path: Path) -> tuple[str, str]:
    """คืน (css, nav_js)

    css มาจาก deck-theme-bauhaus.css ซึ่งคัดลอกค่า token จาก utils/theme.py ของเว็บแอปจริง
    nav_js ดึงจากสไลด์สอบโครงร่างเดิม เพราะเป็นกลไกนำทางที่ทดสอบแล้ว
    """
    if not THEME_CSS.exists():
        sys.exit(f"[ERROR] ไม่พบไฟล์ธีม: {THEME_CSS}")
    css = THEME_CSS.read_text(encoding="utf-8")

    html = deck_path.read_text(encoding="utf-8")
    scripts = re.findall(r"<script>(.*?)</script>", html, flags=re.DOTALL)
    if not scripts:
        sys.exit("[ERROR] หา <script> nav ใน deck เดิมไม่พบ")
    nav_js = max(scripts, key=len)

    return css, nav_js


def patch_nav_js(nav_js: str) -> str:
    """ปรับ nav JS ให้เหมาะกับ deck ใหม่ (ไม่มีสไลด์สำรองแล้ว)"""
    nav_js = nav_js.replace(
        "const isBackup = index >= 15;",
        "const isBackup = index >= DEFENSE_BACKUP_FROM;",
    )
    # ถ้าไม่พบแพตเทิร์นเดิม ให้ถือว่าไม่มี slide สำรอง
    if "DEFENSE_BACKUP_FROM" in nav_js and "const DEFENSE_BACKUP_FROM" not in nav_js:
        nav_js = "const DEFENSE_BACKUP_FROM = 999;\n" + nav_js
    return nav_js


# ----------------------------------------------------------------------------
# 2. นิยามสไลด์
# ----------------------------------------------------------------------------


def slide(label: str, title: str, body: str, counter: str = "") -> str:
    return f"""      <div class="slide">
        <div class="slide-header">
          <div>
            <div class="section-label">{label}</div>
            <div class="main-title">{title}</div>
          </div>
          <div class="slide-counter-chip">{counter}</div>
        </div>
        <div class="slide-body">
{body}
        </div>
      </div>"""


def cover_slide(label: str, title: str, subtitle: str, meta_html: str) -> str:
    return f"""      <div class="slide">
        <div class="slide-header">
          <div>
            <div class="section-label">{label}</div>
            <div class="main-title" style="font-size:2.35rem; line-height:1.35; margin-top:0.5rem;">{title}</div>
            <p style="font-size:1.15rem; color:var(--text-secondary); margin-top:0.9rem; font-weight:500;">{subtitle}</p>
          </div>
          <div class="slide-counter-chip">01 / 20</div>
        </div>
        <div class="slide-body">
{meta_html}
        </div>
      </div>"""


# --- Act 1 -------------------------------------------------------------------

S1 = cover_slide(
    "รายงานโครงงานคณิตศาสตร์ประยุกต์ ประจำปีการศึกษา 2569",
    "การพัฒนาเว็บแอปพลิเคชันช่วยเรียนคณิตศาสตร์<br>สำหรับแคลคูลัสเบื้องต้น",
    "จากมโนทัศน์ที่มองไม่เห็น สู่การทดลองที่จับต้องได้",
    """          <div class="grid-3">
            <div class="academic-card">
              <div class="card-heading">ผู้จัดทำ</div>
              <p style="font-size:0.95rem; color:var(--text-secondary); margin-top:0.5rem;">
                นิสิตสาขาวิชาคณิตศาสตร์ประยุกต์
              </p>
            </div>
            <div class="academic-card">
              <div class="card-heading">อาจารย์ที่ปรึกษา</div>
              <p style="font-size:0.95rem; color:var(--text-secondary); margin-top:0.5rem;">
                อาจารย์กิตติพงศ์ ทรัพย์วัฒนาชัย
              </p>
            </div>
            <div class="academic-card">
              <div class="card-heading">ภาควิชา</div>
              <p style="font-size:0.95rem; color:var(--text-secondary); margin-top:0.5rem;">
                วิทยาการคำนวณและเทคโนโลยีดิจิทัล<br>คณะศิลปศาสตร์และวิทยาศาสตร์
              </p>
            </div>
          </div>
          <div class="academic-card highlight" style="margin-top:0.4rem;">
            <p style="font-size:0.92rem; color:var(--text-secondary);">
              <strong>ขอบเขตการนำเสนอ</strong> ปัญหามโนทัศน์ &rarr; กลไกการสอนที่ออกแบบ &rarr;
              หลักฐานเชิงประจักษ์ &rarr; ข้อจำกัดและแนวทางต่อยอด
            </p>
          </div>""",
)

S2 = slide(
    "1. ที่มาและความสำคัญ · ปัญหามโนทัศน์",
    "สามจุดที่ผู้เรียนแคลคูลัสมองไม่เห็น แม้จะคำนวณได้",
    """          <div class="grid-3">
            <div class="academic-card">
              <div class="card-heading">จุดที่ 1 · ลิมิต</div>
              <p style="font-size:0.88rem; color:var(--text-secondary); margin-top:0.35rem;">
                รูปแบบยังไม่กำหนด $\\frac{0}{0}$ ถูกสอนให้ "แยกตัวประกอบแล้วแทนค่า"
                แต่ผู้เรียนไม่เคยเห็นว่าค่าลู่เข้า 4 จริงหรือไม่
              </p>
              <div class="math-box">$$\\lim_{x\\to 2}\\frac{x^2-4}{x-2} = 4$$</div>
            </div>
            <div class="academic-card">
              <div class="card-heading">จุดที่ 2 · อนุพันธ์</div>
              <p style="font-size:0.88rem; color:var(--text-secondary); margin-top:0.35rem;">
                เส้นตัดกลายเป็นเส้นสัมผัสในจังหวะใด คำว่า $h\\to 0$ เป็นนามธรรม
                ที่ไม่มีภาพรองรับในหนังสือเรียน
              </p>
              <div class="math-box">$$f'(a)=\\lim_{h\\to 0}\\frac{f(a+h)-f(a)}{h}$$</div>
            </div>
            <div class="academic-card">
              <div class="card-heading">จุดที่ 3 · ปริพันธ์</div>
              <p style="font-size:0.88rem; color:var(--text-secondary); margin-top:0.35rem;">
                ผลบวกของสี่เหลี่ยมผืนผ้ากลายเป็นพื้นที่ใต้เส้นโค้งได้อย่างไร
                ตัวเชื่อมคือการลู่เข้า ไม่ใช่สูตร
              </p>
              <div class="math-box">$$\\lim_{n\\to\\infty}\\sum_{i=1}^{n} f(x_i)\\,\\Delta x = \\int_a^b f(x)\\,dx$$</div>
            </div>
          </div>
          <div class="academic-card highlight">
            <div class="card-heading">ข้อสังเกตที่นำไปสู่โครงงาน</div>
            <p style="font-size:0.9rem; color:var(--text-secondary); margin-top:0.35rem;">
              ปัญหาไม่ใช่ "ผู้เรียนคำนวณไม่เป็น" แต่คือ <strong>ไม่มีเครื่องมือให้ทดลองปรับค่าและเห็นผลทันที</strong>
              จนเกิดภาพในหัว (Concept Image) ที่ตรงกับนิยาม (Concept Definition)
            </p>
          </div>""",
)

S3 = slide(
    "1. ที่มาและความสำคัญ · ช่องว่างของเครื่องมือ",
    "เครื่องมือที่มีอยู่ตอบ \"เท่าไร\" ได้ แต่ไม่ได้จัดลำดับการช่วยเหลือ",
    """          <table class="table-academic">
            <thead>
              <tr>
                <th style="width:20%;">ประเภทเครื่องมือ</th>
                <th style="width:24%;">สิ่งที่ทำได้</th>
                <th style="width:28%;">สิ่งที่ยังขาด</th>
                <th style="width:28%;">ผลต่อการเกิดมโนทัศน์</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td><strong>AI สร้างข้อความ</strong><br><span class="key-badge">ChatGPT, Gemini</span></td>
                <td>ตอบคำถามและแสดงวิธีทำได้ทันที</td>
                <td>ไม่มีที่ให้ทดลอง และคำตอบมาจากความน่าจะเป็นของภาษา</td>
                <td>ผู้เรียนอ่านคำตอบ ไม่ได้สร้างความเข้าใจ</td>
              </tr>
              <tr>
                <td><strong>โปรแกรมคำนวณสำเร็จรูป</strong><br><span class="key-badge">WolframAlpha</span></td>
                <td>คำนวณเชิงสัญลักษณ์ได้ถูกต้อง</td>
                <td>ขั้นตอนละเอียดต้องจ่ายเงิน และไม่มีระบบจับจุดเข้าใจผิด</td>
                <td>ได้คำตอบ แต่ไม่เห็นเหตุผลระหว่างทาง</td>
              </tr>
              <tr>
                <td><strong>โปรแกรมวาดกราฟ</strong><br><span class="key-badge">GeoGebra, Desmos</span></td>
                <td>กราฟพลวัตที่ปรับค่าได้อิสระ</td>
                <td>ไม่มีโจทย์ ไม่มีเฉลย ไม่มีการชี้จุดที่มักเข้าใจผิด</td>
                <td>เป็นกระดานทดลอง ไม่ใช่บทเรียน</td>
              </tr>
              <tr style="background:var(--accent-blue-light);">
                <td><strong>ระบบที่นำเสนอ</strong></td>
                <td>ทดลองปรับค่า + เห็นกราฟ + เห็นวิธีทำทีละขั้น + คำใบ้</td>
                <td>จำกัดขอบเขตฟังก์ชันมูลฐาน (ระบุในข้อจำกัด)</td>
                <td><strong>เห็นภาพ → เข้าใจขั้นตอน → ตรวจสอบตนเอง</strong></td>
              </tr>
            </tbody>
          </table>
          <p style="font-size:0.9rem; color:var(--text-secondary);">
            ช่องว่างจึงไม่ใช่เรื่อง "ความสามารถของเครื่องมือ" แต่เป็นเรื่อง <strong>การจัดลำดับความช่วยเหลือ (Scaffolding)</strong>
            ที่พาผู้เรียนจาก "ดู" ไปสู่ "ทำเอง" อย่างเป็นขั้น
          </p>""",
)

S4 = slide(
    "2. วัตถุประสงค์และขอบเขต",
    "วัตถุประสงค์ 5 ข้อ และขอบเขตเนื้อหา 7 โมดูล",
    """          <div class="grid-2">
            <div class="academic-card">
              <div class="card-heading">วัตถุประสงค์</div>
              <ol style="font-size:0.88rem; color:var(--text-secondary); margin-top:0.5rem; padding-left:1.2rem; line-height:1.75;">
                <li>พัฒนาเว็บแอปพลิเคชันช่วยเรียนแคลคูลัสเบื้องต้นด้วย Python + Streamlit</li>
                <li>รวบรวมเนื้อหา ตัวอย่าง และแบบฝึกหัด 7 โมดูลไว้ในระบบเดียว</li>
                <li>พัฒนาระบบคำนวณเชิงสัญลักษณ์ที่แสดงวิธีทำได้อย่างถูกต้อง</li>
                <li>ออกแบบกลไกป้องกันข้อผิดพลาดที่พบบ่อย (Misconceptions)</li>
                <li>ประเมินความพึงพอใจและความสะดวกในการใช้งานตามเกณฑ์สากล</li>
              </ol>
            </div>
            <div class="academic-card">
              <div class="card-heading">ขอบเขตเนื้อหา</div>
              <div class="grid-2" style="margin-top:0.5rem; gap:0.5rem;">
                <div style="font-size:0.85rem; color:var(--text-secondary);">
                  <div class="key-badge">M1</div> ลิมิตและความต่อเนื่อง<br>
                  <div class="key-badge">M2</div> เส้นสัมผัสและอนุพันธ์<br>
                  <div class="key-badge">M3</div> ผลรวมรีมันน์<br>
                  <div class="key-badge">M4</div> เทคนิคการอินทิเกรต
                </div>
                <div style="font-size:0.85rem; color:var(--text-secondary);">
                  <div class="key-badge">M5</div> พื้นที่ระหว่างเส้นโค้ง<br>
                  <div class="key-badge">M6</div> ปริมาตรทรงตันจากการหมุน<br>
                  <div class="key-badge">M7</div> ปริพันธ์ไม่ตรงแบบ<br>
                  <div class="key-badge">+</div> Solver และคลังข้อสอบ 80 ข้อ
                </div>
              </div>
              <p style="font-size:0.82rem; color:var(--text-muted); margin-top:0.6rem;">
                ขอบเขตที่จำกัดโดยเจตนา: รองรับฟังก์ชันมูลฐาน, ปริมาตรหมุนรอบแกน $x$ เท่านั้น
              </p>
            </div>
          </div>""",
)

# --- Act 2 -------------------------------------------------------------------

S5 = slide(
    "3. วิธีดำเนินงาน · หลักการออกแบบ",
    "นั่งร้านทางปัญญา 4 ระดับ ที่ทุกโมดูลต้องทำได้",
    """          <div class="grid-4">
            <div class="academic-card">
              <div class="key-badge">ระดับ 1</div>
              <div class="card-heading" style="margin-top:0.5rem;">เห็นภาพ</div>
              <p style="font-size:0.84rem; color:var(--text-secondary); margin-top:0.35rem;">
                ปรับค่าได้ด้วยสไลเดอร์และเห็นกราฟเปลี่ยนทันที
              </p>
            </div>
            <div class="academic-card">
              <div class="key-badge">ระดับ 2</div>
              <div class="card-heading" style="margin-top:0.5rem;">เห็นโครงสร้าง</div>
              <p style="font-size:0.84rem; color:var(--text-secondary); margin-top:0.35rem;">
                วิธีทำทีละขั้นตามสัญญาข้อมูลเดียวกันทุกโมดูล
              </p>
            </div>
            <div class="academic-card">
              <div class="key-badge">ระดับ 3</div>
              <div class="card-heading" style="margin-top:0.5rem;">ลองเอง</div>
              <p style="font-size:0.84rem; color:var(--text-secondary); margin-top:0.35rem;">
                แบบทดสอบที่มีคำใบ้ ไม่บอกคำตอบทันที
              </p>
            </div>
            <div class="academic-card">
              <div class="key-badge">ระดับ 4</div>
              <div class="card-heading" style="margin-top:0.5rem;">ตรวจจุดผิด</div>
              <p style="font-size:0.84rem; color:var(--text-secondary); margin-top:0.35rem;">
                แจ้งเตือน $\frac{0}{0}$, จุดโปร่ง, จุดมุมแหลม, จุดเอกฐาน
              </p>
            </div>
          </div>
          <div class="academic-card highlight">
            <div class="card-heading">เหตุใดต้องมีครบทั้ง 4 ระดับ</div>
            <p style="font-size:0.9rem; color:var(--text-secondary); margin-top:0.35rem;">
              ถ้ามีแต่กราฟ ผู้เรียนได้แค่ภาพ แต่ไม่รู้ว่าเขียนอย่างไร &nbsp;·&nbsp;
              ถ้ามีแต่เฉลย ผู้เรียนได้แค่คำตอบ แต่ไม่เห็นว่าตัวเองเข้าใจผิดตรงไหน &nbsp;·&nbsp;
              การมีทั้งสี่ระดับคือการออกแบบให้ผู้เรียน <strong>ตรวจสอบตนเองได้</strong> ไม่ใช่รอผู้สอนบอก
            </p>
          </div>""",
)

S6 = slide(
    "3. วิธีดำเนินงาน · การสาธิตสด",
    "สาธิตการใช้งาน 5 นาที: ลิมิต → เส้นสัมผัส → ผลรวมรีมันน์",
    f"""          <div class="grid-2">
            <div class="academic-card">
              <div class="card-heading">ลำดับการสาธิต และจุดที่ต้องชี้ให้เห็น</div>
              <ol style="font-size:0.84rem; color:var(--text-secondary); margin-top:0.45rem; padding-left:1.15rem; line-height:1.7;">
                <li><strong>ลิมิต</strong> &nbsp;ป้อน $\\frac{{x^2-4}}{{x-2}}$ เลื่อนเข้าใกล้ $x=2$
                    &rarr; ชี้ที่ <em>จุดโปร่ง</em> $(2,4)$ ว่าฟังก์ชันไม่นิยาม แต่ค่าลู่เข้า</li>
                <li><strong>เส้นสัมผัส</strong> &nbsp;ลด $h$ ลงทีละขั้น
                    &rarr; ชี้ว่าเส้นตัดค่อย ๆ หมุนเข้าหาเส้นสัมผัส ไม่ได้กระโดด</li>
                <li><strong>ผลรวมรีมันน์</strong> &nbsp;เพิ่ม $n$ จาก 4 เป็น 50
                    &rarr; ชี้ที่ตัวเลขความคลาดเคลื่อนที่ลดลง ไม่ใช่แค่ภาพแท่งที่ถี่ขึ้น</li>
                <li><strong>แบบทดสอบ</strong> &nbsp;เปิดคำใบ้หนึ่งข้อ
                    &rarr; ชี้ว่าคำใบ้ไม่เฉลยคำตอบ ซึ่งคือหัวใจของนั่งร้านทางปัญญา</li>
              </ol>
              <div style="margin-top:0.7rem; display:flex; gap:0.55rem; flex-wrap:wrap;">
                <a href="{APP_URL}" target="_blank" rel="noopener"
                   style="background:var(--primary-blue); color:#fff; text-decoration:none; padding:0.45rem 0.95rem; border-radius:6px; font-size:0.82rem; font-weight:600;">
                  เปิดเว็บแอปในแท็บใหม่
                </a>
                <span style="font-size:0.75rem; color:var(--text-muted); align-self:center;">
                  สลับหน้าจอด้วย Alt + Tab
                </span>
              </div>
              <p style="font-size:0.74rem; color:var(--text-muted); margin-top:0.55rem; line-height:1.5;">
                เตรียมตัว: เปิดแอปทิ้งไว้ก่อนเข้าห้อง 10 นาที เพราะ Streamlit Cloud ใช้เวลาปลุกครั้งแรก 40&ndash;60 วินาที
                หากไม่มีอินเทอร์เน็ต ให้ใช้สกรีนช็อตทั้งสี่ภาพด้านขวาแทนได้ทันที
              </p>
            </div>
            <div class="academic-card">
              <div class="card-heading">ภาพที่ผู้ฟังจะเห็นบนจอ (สกรีนช็อตจริง)</div>
              <div class="grid-2" style="margin-top:0.45rem; gap:0.45rem;">
                <figure style="margin:0;">
                  <img src="../report/figures/screenshot-limit.png" alt="โมดูลลิมิต"
                       style="width:100%; max-height:104px; object-fit:cover; object-position:top; border:1px solid var(--border-medium); border-radius:5px;">
                  <figcaption style="font-size:0.7rem; color:var(--text-muted); text-align:center; margin-top:0.15rem;">ลิมิต · จุดโปร่ง</figcaption>
                </figure>
                <figure style="margin:0;">
                  <img src="../report/figures/screenshot-tangent.png" alt="โมดูลเส้นสัมผัส"
                       style="width:100%; max-height:104px; object-fit:cover; object-position:top; border:1px solid var(--border-medium); border-radius:5px;">
                  <figcaption style="font-size:0.7rem; color:var(--text-muted); text-align:center; margin-top:0.15rem;">เส้นตัด → เส้นสัมผัส</figcaption>
                </figure>
                <figure style="margin:0;">
                  <img src="../report/figures/screenshot-riemann.png" alt="โมดูลผลรวมรีมันน์"
                       style="width:100%; max-height:104px; object-fit:cover; object-position:top; border:1px solid var(--border-medium); border-radius:5px;">
                  <figcaption style="font-size:0.7rem; color:var(--text-muted); text-align:center; margin-top:0.15rem;">ผลรวมรีมันน์</figcaption>
                </figure>
                <figure style="margin:0;">
                  <img src="../report/figures/screenshot-quiz.png" alt="หน้าจอแบบทดสอบ"
                       style="width:100%; max-height:104px; object-fit:cover; object-position:top; border:1px solid var(--border-medium); border-radius:5px;">
                  <figcaption style="font-size:0.7rem; color:var(--text-muted); text-align:center; margin-top:0.15rem;">คำใบ้ที่ไม่เฉลย</figcaption>
                </figure>
              </div>
            </div>
          </div>""",
)

S7 = slide(
    "4. ผลการดำเนินงาน · หลักฐานเชิงตัวเลข",
    "การลู่เข้าของผลรวมรีมันน์ เมื่อจำนวนช่วงย่อยเพิ่มขึ้น",
    """          <table class="table-academic" style="font-size:0.8rem;">
            <thead>
              <tr>
                <th>$n$</th>
                <th>ผลรวมซ้าย $L_n$</th>
                <th>คลาดเคลื่อน</th>
                <th>ผลรวมขวา $R_n$</th>
                <th>คลาดเคลื่อน</th>
                <th>จุดกึ่งกลาง $M_n$</th>
                <th>คลาดเคลื่อน</th>
              </tr>
            </thead>
            <tbody>
              <tr><td>4</td><td>1.7500</td><td>-34.38%</td><td>3.7500</td><td>+40.63%</td><td>2.6250</td><td>-1.56%</td></tr>
              <tr><td>10</td><td>2.2800</td><td>-14.50%</td><td>3.0800</td><td>+15.50%</td><td>2.6600</td><td>-0.25%</td></tr>
              <tr><td>20</td><td>2.4700</td><td>-7.38%</td><td>2.8700</td><td>+7.63%</td><td>2.6650</td><td>-0.06%</td></tr>
              <tr><td>50</td><td>2.5872</td><td>-2.98%</td><td>2.7472</td><td>+3.02%</td><td>2.6664</td><td>-0.01%</td></tr>
              <tr><td>100</td><td>2.6268</td><td>-1.50%</td><td>2.7068</td><td>+1.50%</td><td>2.6666</td><td>&lt; 0.01%</td></tr>
            </tbody>
          </table>
          <p style="font-size:0.88rem; font-weight:600;">
            ค่าปริพันธ์จริง $\\int_0^2 x^2\\,dx = \\frac{8}{3} \\approx 2.6667$ และทั้งสามวิธีลู่เข้าสู่ค่านี้
          </p>
          <div class="grid-2">
            <div class="academic-card">
              <div class="card-heading">สิ่งที่ตารางนี้บอก</div>
              <p style="font-size:0.87rem; color:var(--text-secondary); margin-top:0.3rem;">
                ทั้งสามวิธีลู่เข้า $\\frac{8}{3}$ เมื่อ $n$ เพิ่มขึ้น ยืนยันว่าอัลกอริทึมสอดคล้องนิยามของปริพันธ์จริง
              </p>
            </div>
            <div class="academic-card">
              <div class="card-heading">ผลเชิงการสอน</div>
              <p style="font-size:0.87rem; color:var(--text-secondary); margin-top:0.3rem;">
                ผู้เรียนเห็นความคลาดเคลื่อนลดลงเป็นลำดับ คือทฤษฎีบทหลักมูลในรูปที่จับต้องได้
              </p>
            </div>
          </div>""",
)

S8 = slide(
    "4. ผลการดำเนินงาน · ความซื่อสัตย์เชิงสัญลักษณ์",
    "ระบบเลือกที่จะบอกว่า \"ทำไม่ได้\" ดีกว่าคำนวณค่าลวงออกมา",
    """          <div class="grid-2">
            <div class="academic-card">
              <div class="card-heading">ความแม่นยำเชิงสัญลักษณ์</div>
              <p style="font-size:0.87rem; color:var(--text-secondary); margin-top:0.35rem;">
                ผลลัพธ์คงรูปเศษส่วนและค่าคงตัว ไม่แปลงเป็นทศนิยม
                จึงไม่เกิดความคลาดเคลื่อนสะสมจากการปัดเศษ
              </p>
              <div class="math-box">$$\\int_0^2 (2x - x^2)\\,dx = \\frac{4}{3}\\ \\text{ตารางหน่วย}$$</div>
              <p style="font-size:0.82rem; color:var(--text-muted); margin-top:0.3rem;">
                ไม่ใช่ $1.333$ และไม่ใช่ $1.33$
              </p>
            </div>
            <div class="academic-card">
              <div class="card-heading">Fail-safe 4 กรณีที่ระบบปฏิเสธอย่างถูกต้อง</div>
              <ul style="font-size:0.85rem; color:var(--text-secondary); margin-top:0.4rem; padding-left:1.1rem; line-height:1.75;">
                <li>ลิมิตซ้ายและขวาไม่เท่ากัน &rarr; รายงาน $\\text{DNE}$</li>
                <li>จุดมุมแหลม $|x|$ ที่ $x=0$ &rarr; ไม่วาดเส้นสัมผัสลวง</li>
                <li>ปริพันธ์ลู่ออก &rarr; ระบุสถานะชัดเจน ไม่คืนค่าตัวเลข</li>
                <li>ไม่มีปฏิยานุพันธ์ในรูปฟังก์ชันมูลฐาน &rarr; แจ้งและหยุด</li>
              </ul>
            </div>
          </div>
          <div class="academic-card highlight">
            <p style="font-size:0.9rem; color:var(--text-secondary);">
              สำหรับสื่อการเรียนรู้คณิตศาสตร์ <strong>การตอบผิดอย่างมั่นใจเป็นอันตรายกว่าการยอมรับว่าทำไม่ได้</strong>
              ระบบจึงออกแบบให้ยอมแพ้อย่างชัดเจนเมื่ออยู่นอกขอบเขตที่พิสูจน์แล้ว
            </p>
          </div>""",
)

S9 = slide(
    "4. ผลการดำเนินงาน · ความถูกต้องทางเทคนิค",
    "หลักฐานการทดสอบ: 250 กรณีหน่วยย่อย, 144 กรณีขอบเขต, 15 หน้าจอ",
    """          <div class="grid-3">
            <div class="academic-card" style="text-align:center;">
              <div style="font-size:2.6rem; font-weight:700; color:var(--primary-blue);">250</div>
              <div class="card-heading" style="justify-content:center;">Pytest</div>
              <p style="font-size:0.84rem; color:var(--text-secondary); margin-top:0.3rem;">
                กรณีทดสอบอัตโนมัติครอบคลุม Solver ทั้ง 8 โมดูล ผ่านทั้งหมด
              </p>
            </div>
            <div class="academic-card" style="text-align:center;">
              <div style="font-size:2.6rem; font-weight:700; color:var(--primary-blue);">144</div>
              <div class="card-heading" style="justify-content:center;">Boundary</div>
              <p style="font-size:0.84rem; color:var(--text-secondary); margin-top:0.3rem;">
                กรณีขอบเขตวิกฤต เพื่อจำแนกว่าอะไรรองรับ และอะไรถูกปฏิเสธ
              </p>
            </div>
            <div class="academic-card" style="text-align:center;">
              <div style="font-size:2.6rem; font-weight:700; color:var(--primary-blue);">15</div>
              <div class="card-heading" style="justify-content:center;">หน้าจอ</div>
              <p style="font-size:0.84rem; color:var(--text-secondary); margin-top:0.3rem;">
                ทดสอบเสมือนจริงบนเบราว์เซอร์ ไม่พบ JavaScript error
              </p>
            </div>
          </div>
          <div class="academic-card highlight">
            <div class="card-heading">ข้อจำกัดของการตีความผลทดสอบนี้</div>
            <p style="font-size:0.88rem; color:var(--text-secondary); margin-top:0.35rem;">
              การทดสอบผ่านพิสูจน์ว่า <strong>กรณีที่ประกาศรองรับทำงานถูกต้อง</strong> และ
              <strong>กรณีที่อยู่นอกรองรับถูกปฏิเสธอย่างชัดเจน</strong>
              แต่ไม่ได้พิสูจน์ว่าถูกต้องสำหรับทุกอินพุตที่เป็นไปได้
              เราจึงไม่กล่าวอ้างความถูกต้องแบบสากล
            </p>
          </div>""",
)

# --- Act 3 -------------------------------------------------------------------

S10 = slide(
    "5. ผลการประเมิน · ระเบียบวิธี",
    "ประเมินกับผู้ใช้จริง 50 คน ด้วยเครื่องมือ 2 ชุด",
    """          <div class="grid-2">
            <div class="academic-card">
              <div class="card-heading">กลุ่มตัวอย่าง</div>
              <p style="font-size:0.86rem; color:var(--text-secondary); margin-top:0.4rem;">
                บันทึกผล ณ วันที่ 30 ตุลาคม 2569 เวลา 10:15 น. รวม <strong>$N = 50$ คน</strong>
                (แบบประเมินยังเปิดรับอยู่หลังวันตัดรอบ)
              </p>
              <ul style="font-size:0.84rem; color:var(--text-secondary); margin-top:0.4rem; padding-left:1.1rem; line-height:1.7;">
                <li>ปริญญาตรีปี 3–4 <strong>74%</strong> · ปี 1–2 16% · บัณฑิตศึกษา 6%</li>
                <li>กำลังเรียนแคลคูลัส 30% · เคยสอบผ่านแล้ว 46%</li>
                <li>อุปกรณ์: แท็บเล็ต 40% · คอมพิวเตอร์ 34% · สมาร์ตโฟน 26%</li>
                <li>สังกัด: มก. กำแพงแสน 36%, ศิลปากร 24%, มรภ.ธนบุรี 12%, อื่น ๆ 28%</li>
              </ul>
            </div>
            <div class="academic-card">
              <div class="card-heading">เครื่องมือวัด</div>
              <div style="font-size:0.86rem; color:var(--text-secondary); margin-top:0.4rem; line-height:1.7;">
                <p><strong>ชุดที่ 1 · ความพึงพอใจ 4 ด้าน</strong><br>
                มาตรประมาณค่า 5 ระดับ รวม 20 ข้อ ครอบคลุม UI/UX, ฟังก์ชันเชิงโต้ตอบ,
                เนื้อหาและมโนทัศน์, เจตคติและแรงจูงใจ</p>
                <p style="margin-top:0.5rem;"><strong>ชุดที่ 2 · System Usability Scale</strong><br>
                10 ข้อ ฉบับปรับปรุงข้อคำถามเป็นเชิงบวก (Positive-phrased SUS)
                ตามกรอบของ Sauro &amp; Lewis (2011) เพื่อลดความสับสนของผู้ตอบไทย</p>
              </div>
            </div>
          </div>
          <p style="font-size:0.85rem; color:var(--text-muted);">
            การเลือกกลุ่มตัวอย่างเป็นแบบบังเอิญ (Convenience Sampling) จากเครือข่ายของผู้จัดทำ
            ซึ่งเป็นข้อจำกัดที่ระบุไว้ในบทที่ 5
          </p>""",
)

S11 = slide(
    "5. ผลการประเมิน · ความพึงพอใจ",
    "ภาพรวมอยู่ในระดับมากที่สุด 4.63 จาก 5.00",
    """          <div class="grid-2">
            <table class="table-academic">
              <thead>
                <tr><th>ด้านการประเมิน</th><th>$\\bar{x}$</th><th>$S.D.$</th><th>ระดับ</th></tr>
              </thead>
              <tbody>
                <tr><td>1. การออกแบบส่วนประสานงาน (UI/UX)</td><td>4.62</td><td>0.60</td><td>มากที่สุด</td></tr>
                <tr><td>2. ฟังก์ชันเชิงโต้ตอบและการคำนวณ</td><td>4.60</td><td>0.61</td><td>มากที่สุด</td></tr>
                <tr><td>3. เนื้อหาและมโนทัศน์ทางคณิตศาสตร์</td><td>4.64</td><td>0.56</td><td>มากที่สุด</td></tr>
                <tr style="background:var(--accent-blue-light);"><td>4. เจตคติและแรงจูงใจในการเรียนรู้</td><td><strong>4.67</strong></td><td>0.56</td><td>มากที่สุด</td></tr>
                <tr style="font-weight:700;"><td>ภาพรวมทุกด้าน</td><td>4.63</td><td>0.58</td><td>มากที่สุด</td></tr>
              </tbody>
            </table>
            <div class="academic-card">
              <div class="card-heading">อ่านผลอย่างไรให้ไม่เกินจริง</div>
              <p style="font-size:0.86rem; color:var(--text-secondary); margin-top:0.35rem;">
                คะแนนสูงสุดคือด้าน <strong>เจตคติและแรงจูงใจ</strong> ซึ่งสอดคล้องกับสมมติฐานว่า
                การเห็นภาพและการทดลองลดความวิตกกังวลต่อวิชาแคลคูลัส
              </p>
              <p style="font-size:0.86rem; color:var(--text-secondary); margin-top:0.5rem;">
                แต่คะแนนนี้คือ <strong>การรับรู้ของผู้เรียน (Perceived)</strong>
                ไม่ใช่หลักฐานว่าผลสัมฤทธิ์ทางการเรียนสูงขึ้น
                ซึ่งต้องใช้การทดสอบก่อนและหลังเรียนจึงจะสรุปได้
              </p>
              <div class="math-box">$$\\bar{x} = 4.63,\\quad S.D. = 0.58,\\quad N = 50$$</div>
            </div>
          </div>""",
)

S12 = slide(
    "5. ผลการประเมิน · ความสะดวกในการใช้งาน",
    "SUS 82.15 (Grade A) และการอ่านผลอย่างโปร่งใส",
    """          <div class="grid-2">
            <div class="academic-card">
              <div class="card-heading">คะแนนรวม</div>
              <div style="font-size:2.8rem; font-weight:700; color:var(--primary-blue); margin-top:0.3rem;">82.15</div>
              <p style="font-size:0.85rem; color:var(--text-secondary);">
                $S.D. = 19.36$ · มัธยฐาน 87.50 · เกณฑ์มาตรฐานอุตสาหกรรม 68.0
              </p>
              <div class="math-box">$$\\text{SUS} = 2.5\\sum_{i=1}^{10} s_i,\\quad s_i = X_i - 1$$</div>
              <p style="font-size:0.82rem; color:var(--text-muted); margin-top:0.3rem;">
                จัดอยู่ในเกณฑ์ยอดเยี่ยม Grade A (Brooke, 1996; Sauro, 2011)
              </p>
            </div>
            <div class="academic-card">
              <div class="card-heading">ความลำเอียงที่พบ และวิธีจัดการ</div>
              <ul style="font-size:0.85rem; color:var(--text-secondary); margin-top:0.4rem; padding-left:1.1rem; line-height:1.75;">
                <li>พบการกาดิ่ง (ให้คะแนนเท่ากันทุกข้อ) <strong>21 คน คิดเป็น 42%</strong></li>
                <li>เมื่อแยกกลุ่มที่มีการกระจายคะแนนตามธรรมชาติ ($n=29$)
                    คะแนนเฉลี่ยอยู่ที่ <strong>73.53</strong> ($S.D.=15.95$)</li>
                <li>ยังคงอยู่ในระดับ <strong>Grade B (Good)</strong> และสูงกว่าเกณฑ์ 68.0</li>
              </ul>
              <p style="font-size:0.84rem; color:var(--text-secondary); margin-top:0.5rem;">
                เรารายงานทั้งสองค่า เพราะการรายงานเฉพาะ 82.15 จะทำให้ผลดูดีเกินจริง
                และปิดบังพฤติกรรมการตอบของผู้ใช้
              </p>
            </div>
          </div>""",
)

S13 = slide(
    "5. ผลการประเมิน · ข้อกังวลของผู้ใช้จริง",
    "สี่ข้อกังวลที่ผู้เรียนสะท้อน และเหตุผลเบื้องหลังการออกแบบ",
    """          <table class="table-academic">
            <thead>
              <tr><th style="width:26%;">ข้อกังวล</th><th style="width:37%;">คำตอบเชิงออกแบบ</th><th style="width:37%;">เหตุผล</th></tr>
            </thead>
            <tbody>
              <tr>
                <td>โดเมนเว็บไซต์ดูน่ากังวล</td>
                <td>ติดตั้งบน Streamlit Community Cloud ที่เข้ารหัส HTTPS ตลอดเวลา และผูกโดเมนย่อยของมหาวิทยาลัยได้</td>
                <td>ข้อจำกัดของแพลตฟอร์มฟรี ไม่ใช่ช่องโหว่ของระบบ</td>
              </tr>
              <tr>
                <td>ตัวหนังสือเยอะ อยากเห็นคำตอบก่อน</td>
                <td>ยืนยันว่าระบบเป็นห้องทดลองการเรียนรู้ ไม่ใช่เครื่องเฉลย</td>
                <td>การตัดขั้นตอนออกจะทำลายกลไกนั่งร้านทางปัญญาที่เป็นหัวใจของโครงงาน</td>
              </tr>
              <tr>
                <td>โทนสีดูไม่เป็นทางการ</td>
                <td>เลือกสไตล์ Playful Bauhaus Pop โดยเจตนา</td>
                <td>เพื่อลดความวิตกกังวลต่อวิชาคณิตศาสตร์ สอดคล้องกับคะแนนด้านเจตคติ 4.67</td>
              </tr>
              <tr>
                <td>เหมาะกับคอมพิวเตอร์มากกว่ามือถือ</td>
                <td>ระบุอุปกรณ์ที่แนะนำ และวางแผนปรับ Auto-scroll ในอนาคต</td>
                <td>การเรียนรู้ที่ต้องเทียบสมการกับกราฟพร้อมกันต้องใช้พื้นที่หน้าจอ</td>
              </tr>
            </tbody>
          </table>
          <p style="font-size:0.88rem; color:var(--text-secondary);">
            เราเลือกตอบข้อกังวลด้วยเหตุผลการออกแบบ ไม่ใช่การแก้ตามเสียงส่วนใหญ่ทุกข้อ
            เพราะบางข้อขัดกับวัตถุประสงค์ทาง pedagogy ของโครงงาน
          </p>""",
)

S14 = slide(
    "5. ผลการประเมิน · ความต้องการของผู้เรียน",
    "ผู้เรียนร้อยละ 58 ต้องการอินทิเกรตทีละส่วนเพิ่ม",
    """          <div class="grid-2">
            <table class="table-academic">
              <thead>
                <tr><th>หัวข้อที่ต้องการให้พัฒนาเพิ่ม</th><th>จำนวน</th><th>ร้อยละ</th></tr>
              </thead>
              <tbody>
                <tr><td>การอินทิเกรตทีละส่วน (Integration by Parts)</td><td>29</td><td>58.0%</td></tr>
                <tr><td>การแยกเป็นเศษส่วนย่อย (Partial Fractions)</td><td>25</td><td>50.0%</td></tr>
                <tr><td>การแทนค่าด้วยฟังก์ชันตรีโกณมิติ (Trig Sub)</td><td>22</td><td>44.0%</td></tr>
                <tr><td>การจำลอง 3 มิติสำหรับปริมาตรการหมุน</td><td>21</td><td>42.0%</td></tr>
              </tbody>
            </table>
            <div class="academic-card">
              <div class="card-heading">ตีความ Demand นี้อย่างไร</div>
              <p style="font-size:0.86rem; color:var(--text-secondary); margin-top:0.35rem;">
                ตัวเลขนี้เป็น <strong>สัญญาณความต้องการ</strong> ไม่ใช่ข้อบกพร่องของระบบ
                ผู้เรียนที่ผ่านการใช้งานแล้วอยากได้หัวข้อที่ต่อเนื่องขึ้น
                ซึ่งแปลว่าระบบถูกใช้จนถึงขีดจำกัดของขอบเขตที่ประกาศไว้
              </p>
              <p style="font-size:0.86rem; color:var(--text-secondary); margin-top:0.5rem;">
                จึงนำตัวเลขนี้ไปเขียนเป็นข้อเสนอแนะในบทที่ 5
                โดยเรียงตามลำดับความต้องการจริงของผู้ใช้ ไม่ใช่ตามความสะดวกของผู้พัฒนา
              </p>
            </div>
          </div>""",
)

S15 = slide(
    "6. อภิปรายผล",
    "เหตุใดการเห็นภาพจึงเปลี่ยนความเข้าใจ ไม่ใช่แค่ทำให้สนุก",
    """          <div class="grid-2">
            <div class="academic-card">
              <div class="card-heading">กรอบ APOS (Dubinsky, 1991)</div>
              <table class="table-academic" style="margin-top:0.4rem; font-size:0.82rem;">
                <tr><th style="width:26%;">ขั้น</th><th>สิ่งที่ระบบจัดให้</th></tr>
                <tr><td>Action</td><td>ผู้เรียนลากสไลเดอร์ ป้อนฟังก์ชัน เห็นผลทันที</td></tr>
                <tr><td>Process</td><td>เห็นรูปแบบซ้ำ ๆ ว่าค่า $h$ เล็กลงทำให้ความชันลู่เข้า</td></tr>
                <tr><td>Object</td><td>เข้าใจอนุพันธ์ในฐานะฟังก์ชัน ไม่ใช่การคำนวณครั้งเดียว</td></tr>
                <tr><td>Schema</td><td>เชื่อมลิมิต อนุพันธ์ และปริพันธ์เป็นโครงเดียวกัน</td></tr>
              </table>
            </div>
            <div class="academic-card">
              <div class="card-heading">เทียบกับสื่อเดิม</div>
              <p style="font-size:0.86rem; color:var(--text-secondary); margin-top:0.35rem;">
                ตำราอธิบายนิยามได้ครบ แต่ไม่มีที่ให้ผู้เรียน <em>ทดลองปรับตัวแปรแล้วล้มเหลวอย่างปลอดภัย</em>
                ซึ่งเป็นกลไกที่ทำให้ Concept Image ค่อย ๆ ขยับเข้าหา Concept Definition
                (Tall &amp; Vinner, 1981)
              </p>
              <div class="academic-card highlight" style="margin-top:0.6rem;">
                <p style="font-size:0.85rem; color:var(--text-secondary);">
                  นี่คือคำตอบว่าทำไมเครื่องมือที่ "ตอบถูก" ยังไม่พอ
                  เพราะสิ่งที่ขาดไม่ใช่คำตอบ แต่คือ <strong>พื้นที่ให้คิดก่อนได้คำตอบ</strong>
                </p>
              </div>
            </div>
          </div>""",
)

# --- Act 4 -------------------------------------------------------------------

S16 = slide(
    "7. ข้อจำกัด",
    "สิ่งที่ระบบยังทำไม่ได้ ระบุตรงไปตรงมา",
    """          <div class="grid-2">
            <div class="academic-card">
              <div class="card-heading">ข้อจำกัดทางคณิตศาสตร์</div>
              <ul style="font-size:0.85rem; color:var(--text-secondary); margin-top:0.4rem; padding-left:1.1rem; line-height:1.75;">
                <li>ฟังก์ชันที่ไม่มีปฏิยานุพันธ์ในรูปมูลฐาน เช่น $e^{-x^2}$, $\\frac{\\sin x}{x}$ ไม่สามารถแจกแจงวิธีทำแบบพีชคณิตได้</li>
                <li>ปริมาตรทรงตันรองรับเฉพาะการหมุนรอบแกน $x$ ยังไม่มีวิธีเปลือกทรงกระบอก</li>
                <li>การอินทิเกรตเทียบกับแกน $y$ ($x = f(y)$) ยังไม่รองรับ</li>
              </ul>
            </div>
            <div class="academic-card">
              <div class="card-heading">ข้อจำกัดทางเทคนิค</div>
              <ul style="font-size:0.85rem; color:var(--text-secondary); margin-top:0.4rem; padding-left:1.1rem; line-height:1.75;">
                <li>ฟังก์ชันกวัดแกว่งรุนแรง เช่น $\\sin\\frac{1}{x}$ เมื่อ $x \\to 0$ ตรวจจับ DNE ได้ถูกต้อง แต่กราฟอาจเกิดภาพลวงตาจากความละเอียดจุดพล็อต</li>
                <li>การสร้างกราฟบนเครื่องแม่ข่ายทำให้ช้าลงเมื่อมีผู้ใช้พร้อมกันมาก</li>
                <li>การตัดคำภาษาไทยขึ้นบรรทัดใหม่ยังไม่สมบูรณ์ในบางจุด</li>
              </ul>
            </div>
          </div>
          <div class="academic-card highlight">
            <p style="font-size:0.88rem; color:var(--text-secondary);">
              ข้อจำกัดเหล่านี้ถูกออกแบบให้ <strong>ตรวจพบและแจ้งเตือนได้</strong>
              ไม่ใช่ปล่อยให้ผู้เรียนเข้าใจผิดโดยไม่รู้ตัว
              การรู้ว่าอะไรทำไม่ได้คือส่วนหนึ่งของความน่าเชื่อถือของเครื่องมือการสอน
            </p>
          </div>""",
)

S17 = slide(
    "8. ข้อเสนอแนะ",
    "แนวทางต่อยอด 3 ด้าน เรียงตามหลักฐานจากผู้ใช้",
    """          <div class="grid-3">
            <div class="academic-card">
              <div class="card-heading">ด้านเนื้อหา</div>
              <ol style="font-size:0.84rem; color:var(--text-secondary); margin-top:0.4rem; padding-left:1.1rem; line-height:1.8;">
                <li>Partial Fractions และ Trig Substitution (50%, 44%)</li>
                <li>วิธีเปลือกทรงกระบอกและการหมุนรอบแกน $y$</li>
                <li>ต่อยอดสู่แคลคูลัสหลายตัวแปร</li>
              </ol>
            </div>
            <div class="academic-card">
              <div class="card-heading">ด้านประสบการณ์ผู้ใช้</div>
              <ol style="font-size:0.84rem; color:var(--text-secondary); margin-top:0.4rem; padding-left:1.1rem; line-height:1.8;">
                <li>ปรับการตัดคำภาษาไทยให้ถูกต้อง</li>
                <li>เลื่อนหน้าจอไปยังผลลัพธ์อัตโนมัติเมื่อคำนวณเสร็จ</li>
                <li>เพิ่มวิดีโอแนะนำการใช้งานสั้น 2&ndash;3 นาที</li>
              </ol>
            </div>
            <div class="academic-card">
              <div class="card-heading">ด้านการวิเคราะห์การเรียนรู้</div>
              <ol style="font-size:0.84rem; color:var(--text-secondary); margin-top:0.4rem; padding-left:1.1rem; line-height:1.8;">
                <li>ระบบบัญชีผู้ใช้และประวัติการเรียนรู้รายบุคคล</li>
                <li>แดชบอร์ดผู้สอนแสดงจุดที่ผู้เรียนเข้าใจผิดบ่อย</li>
                <li>เชื่อมผลกับ Pre-test / Post-test เพื่อวัดผลสัมฤทธิ์จริง</li>
              </ol>
            </div>
          </div>
          <p style="font-size:0.86rem; color:var(--text-secondary);">
            ลำดับความสำคัญอ้างอิงจากความต้องการจริงของผู้เรียน ($N=50$)
            ไม่ใช่จากความยากง่ายของการพัฒนา
          </p>""",
)

S18 = slide(
    "9. บทสรุป",
    "ตอบวัตถุประสงค์ทั้ง 5 ข้อ พร้อมหลักฐานประกอบ",
    """          <table class="table-academic">
            <thead>
              <tr><th style="width:36%;">วัตถุประสงค์</th><th style="width:34%;">ผลที่ได้</th><th style="width:30%;">หลักฐาน</th></tr>
            </thead>
            <tbody>
              <tr><td>1. พัฒนาเว็บแอปพลิเคชันด้วย Python และ Streamlit</td><td>ระบบ 15 หน้า ใช้งานได้จริงบนคลาวด์</td><td>ลิงก์แอปสาธารณะ</td></tr>
              <tr><td>2. รวบรวมเนื้อหาและแบบฝึกหัด 7 โมดูล</td><td>ครบ 7 โมดูล + Solver + ข้อสอบ 80 ข้อ</td><td>บทที่ 3, ภาคผนวก ข</td></tr>
              <tr><td>3. ระบบคำนวณเชิงสัญลักษณ์ที่ถูกต้อง</td><td>250 กรณีทดสอบผ่านทั้งหมด คงรูปเศษส่วนแท้</td><td>บทที่ 4 ตาราง 4.1</td></tr>
              <tr><td>4. กลไกป้องกันจุดเข้าใจผิด</td><td>Fail-safe 4 กรณี ตรวจจุดโปร่ง จุดมุมแหลม จุดเอกฐาน</td><td>ตาราง 4.3</td></tr>
              <tr style="background:var(--accent-blue-light);"><td>5. ประเมินความพึงพอใจและความสะดวก</td><td>$\\bar{x}=4.63/5.00$ และ SUS 82.15 (Grade A)</td><td>ตาราง 4.5, §4.3.2</td></tr>
            </tbody>
          </table>
          <p style="font-size:0.88rem; color:var(--text-secondary);">
            สรุปเชิงแนวคิด: ระบบนี้ไม่ได้ทำให้ผู้เรียนคำนวณเร็วขึ้น
            แต่ทำให้ <strong>ช่วงเวลาก่อนได้คำตอบ</strong> กลายเป็นส่วนหนึ่งของการเรียนรู้
          </p>""",
)

S19 = slide(
    "9. บทสรุป · สิ่งที่ได้จริง",
    "ผลผลิตที่ใช้งานได้ และสิ่งที่ยังต้องทำต่อ",
    f"""          <div class="grid-3">
            <div class="academic-card" style="text-align:center;">
              <div class="card-heading" style="justify-content:center;">เว็บแอปพลิเคชัน</div>
              <p style="font-size:0.84rem; color:var(--text-secondary); margin-top:0.4rem;">
                เปิดใช้ได้จริง ผ่านเบราว์เซอร์ ไม่ต้องติดตั้ง
              </p>
              <div style="margin-top:0.7rem; display:flex; flex-direction:column; gap:0.5rem; align-items:center;">
                <img src="../report/figures/calculus-app-qr.png" alt="QR code เว็บแอปพลิเคชัน"
                     style="width:110px; height:110px; border:1px solid var(--border-medium); border-radius:6px; background:#fff; padding:4px;">
                <a href="{APP_URL}" target="_blank" rel="noopener"
                   style="font-size:0.72rem; color:var(--primary-blue); word-break:break-all; text-align:center; text-decoration:none;">
                  เปิดเว็บแอป
                </a>
              </div>
            </div>
            <div class="academic-card" style="text-align:center;">
              <div class="card-heading" style="justify-content:center;">ชุดทดสอบอัตโนมัติ</div>
              <p style="font-size:0.84rem; color:var(--text-secondary); margin-top:0.4rem;">
                250 กรณี พร้อมใช้ต่อยอดเมื่อเพิ่มโมดูลใหม่
              </p>
              <div class="math-box" style="margin-top:0.6rem;">$$250 \\text{{ passed}}$$</div>
            </div>
            <div class="academic-card" style="text-align:center;">
              <div class="card-heading" style="justify-content:center;">ข้อมูลผลประเมินจริง</div>
              <p style="font-size:0.84rem; color:var(--text-secondary); margin-top:0.4rem;">
                $N=50$ พร้อมตารางสถิติที่ตรวจสอบย้อนกลับได้
              </p>
              <div style="margin-top:0.7rem; display:flex; flex-direction:column; gap:0.5rem; align-items:center;">
                <img src="../report/figures/calculus-survey-qr.png" alt="QR code แบบประเมิน"
                     style="width:110px; height:110px; border:1px solid var(--border-medium); border-radius:6px; background:#fff; padding:4px;">
                <span style="font-size:0.72rem; color:var(--text-muted);">แบบประเมินยังเปิดรับอยู่</span>
              </div>
            </div>
          </div>
          <div class="academic-card highlight">
            <p style="font-size:0.88rem; color:var(--text-secondary);">
              สิ่งที่ยังต้องทำต่อ: เพิ่มหัวข้อตามความต้องการของผู้เรียน, ปรับการแสดงผลภาษาไทย,
              และเชื่อมระบบเก็บข้อมูลการเรียนรู้เพื่อวัดผลสัมฤทธิ์อย่างเป็นระบบ
            </p>
          </div>""",
)

S20 = f"""      <div class="slide">
        <div class="slide-header">
          <div>
            <div class="section-label">ขอขอบพระคุณคณะกรรมการทุกท่าน</div>
            <div class="main-title" style="font-size:2.2rem; margin-top:0.5rem;">ขอบคุณครับ</div>
            <p style="font-size:1.05rem; color:var(--text-secondary); margin-top:0.8rem;">
              พร้อมรับฟังข้อซักถามและข้อเสนอแนะ
            </p>
          </div>
          <div class="slide-counter-chip">20 / 20</div>
        </div>
        <div class="slide-body">
          <div class="grid-3">
            <div class="academic-card">
              <div class="card-heading">เว็บแอปพลิเคชัน</div>
              <a href="{APP_URL}" target="_blank" rel="noopener"
                 style="font-size:0.78rem; color:var(--primary-blue); word-break:break-all;">
                calculus-integration-app.streamlit.app
              </a>
            </div>
            <div class="academic-card">
              <div class="card-heading">ซอร์สโค้ด</div>
              <a href="https://github.com/SubwatG/calculus-integration-app" target="_blank" rel="noopener"
                 style="font-size:0.86rem; color:var(--primary-blue);">
                github.com/SubwatG/calculus-integration-app
              </a>
            </div>
            <div class="academic-card">
              <div class="card-heading">เอกสารรายงาน</div>
              <p style="font-size:0.84rem; color:var(--text-secondary);">
                บทที่ 1&ndash;5, บรรณานุกรม และภาคผนวก ก&ndash;จ
              </p>
            </div>
          </div>
          <div class="academic-card highlight" style="text-align:center;">
            <p style="font-size:0.95rem; color:var(--text-secondary);">
              เวลาซักถามและตอบข้อเสนอแนะ <strong>ไม่น้อยกว่า 10 นาที</strong>
            </p>
          </div>
        </div>
      </div>"""

SLIDES = [S1, S2, S3, S4, S5, S6, S7, S8, S9, S10,
          S11, S12, S13, S14, S15, S16, S17, S18, S19, S20]

# ----------------------------------------------------------------------------
# 3. ประกอบไฟล์ HTML
# ----------------------------------------------------------------------------


def build() -> str:
    css, nav_js = extract_theme(PROPOSAL_DECK)
    nav_js = patch_nav_js(nav_js)
    slides_html = "\n\n".join(SLIDES)

    return f"""<!DOCTYPE html>
<html lang="th">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>การนำเสนอโครงงาน | Calculus Learning Sandbox (สอบปลายภาค)</title>

<!-- Fonts: ชุดเดียวกับเว็บแอป (Fredoka หัวเรื่อง / Mali เนื้อหาไทย / Outfit ตัวเลข) -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fredoka:wght@400;500;600;700&family=Mali:ital,wght@0,400;0,500;0,600;0,700;1,400&family=Outfit:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">

<!-- KaTeX Math Rendering -->
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.css">
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.js"></script>
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/contrib/auto-render.min.js"></script>

<style>{css}</style>
</head>
<body>

<!-- Top Navigation -->
<div class="top-nav">
  <div class="nav-title">
    <span class="ku-badge">KU</span>
    <span>สาขาวิชาคณิตศาสตร์ประยุกต์ &bull; คณะศิลปศาสตร์และวิทยาศาสตร์</span>
  </div>
  <div class="nav-actions">
    <a href="{APP_URL}" target="_blank" rel="noopener" class="btn-action" style="text-decoration:none; display:inline-flex; align-items:center;">
      เปิดแอปจริง
    </a>
    <button class="btn-action" onclick="toggleOverview()">ภาพรวมสไลด์</button>
    <button class="btn-primary-action" onclick="goToSlide(totalSlides - 1)">ไปหน้าสุดท้าย</button>
  </div>
</div>

<div class="progress-rail">
  <div class="progress-fill" id="progressFill"></div>
</div>

<div class="deck-canvas">
{slides_html}
</div>

<div class="bottom-footer">
  <div class="brand-meta">
    <span>Calculus Learning Sandbox</span>
    <span>&bull;</span>
    <span>รายงานโครงงานคณิตศาสตร์ประยุกต์ 2569</span>
  </div>
  <div id="slideCounterText" style="font-family:'JetBrains Mono', monospace; font-weight:600;">
    Slide 1 of 20
  </div>
</div>

<!-- Modal Overview Grid -->
<div class="modal-overlay" id="modalOverlay" onclick="toggleOverview()">
  <div class="grid-thumbs" onclick="event.stopPropagation()">
    <!-- Populated by JS -->
  </div>
</div>

<script>{nav_js}</script>

</body>
</html>
"""


def main() -> None:
    if not PROPOSAL_DECK.exists():
        sys.exit(f"[ERROR] ไม่พบ deck ต้นทาง: {PROPOSAL_DECK}")

    html = build()
    OUT_PATH.write_text(html, encoding="utf-8")

    slide_count = len(re.findall(r'<div class="slide">', html))
    print(f"[OK] เขียนไฟล์: {OUT_PATH}")
    print(f"     slides: {slide_count}")
    print(f"     size: {OUT_PATH.stat().st_size:,} bytes")

    if slide_count != 20:
        sys.exit(f"[ERROR] จำนวนสไลด์ไม่ครบ 20 (ได้ {slide_count})")


if __name__ == "__main__":
    main()
