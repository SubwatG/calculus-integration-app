#!/usr/bin/env python3
"""
build_defense_deck.py
---------------------
สร้างสไลด์นำเสนอสอบป้องกันปริญญานิพนธ์ (28–30 นาที) 34 หน้า เป็น single-file HTML
โดยต่อยอดจากสไลด์สอบโครงงานเดิมใน docs/defense/slide-deck-defense.html
ผสานเนื้อหาจากสไลด์นำเสนอหัวข้อ (Canva) ตารางเปรียบเทียบ AI/Wolfram/Desmos,
ไล่ลำดับบทที่ 1, สถาปัตยกรรม 3 ชั้น, ขั้นตอน 4 ขั้น,
และเน้นเนื้อหาบทที่ 2 ทุกหัวข้อ (7 โมดูล x 2 สไลด์: ทฤษฎี 1 + ตัวอย่าง 1)
พร้อมระบบนำทาง JS, ธีม Bauhaus Pop, และชิประบุชื่อผู้พูด (ขวัญเรือน / เบญจกัฬยาณี)

ใช้งาน:
    python3 build_defense_deck.py

ผลลัพธ์:
    slide-deck-defense.html  (เปิดในเบราว์เซอร์ได้ทันที ออฟไลน์ 100%)
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

import base64

def img_b64(filename: str) -> str:
    search_dirs = [
        HERE / "figures",
        REPORT_DIR / "figures",
        HERE,
    ]
    for d in search_dirs:
        p = d / filename
        if p.exists():
            mime = "image/png"
            if p.suffix.lower() in [".jpg", ".jpeg"]:
                mime = "image/jpeg"
            elif p.suffix.lower() == ".svg":
                mime = "image/svg+xml"
            b64 = base64.b64encode(p.read_bytes()).decode("ascii")
            return f"data:{mime};base64,{b64}"
    raise FileNotFoundError(f"Cannot find image: {filename}")

def web_frame_img(
    filename: str,
    alt: str,
    caption: str = "หน้าจอเว็บแอปจริง (เลื่อนดูด้านล่าง / คลิกเพื่อดูภาพเต็ม)",
    max_height: str = "360px"
) -> str:
    uri = img_b64(filename)
    safe_alt = alt.replace("'", "\\'")
    safe_cap = caption.replace("'", "\\'")
    return f"""<div class="web-preview-frame" style="max-height:{max_height}; overflow-y:auto; border:1.5px solid var(--ink); border-radius:8px; box-shadow:2px 2px 0 var(--ink); background:#ffffff; margin-top:0.35rem;">
  <div style="background:var(--canvas); padding:5px 9px; font-size:0.72rem; border-bottom:1px solid var(--border-medium); display:flex; justify-content:space-between; align-items:center; position:sticky; top:0; z-index:2;">
    <span style="font-weight:600; color:var(--ink);">🌐 {caption}</span>
    <span style="font-size:0.68rem; color:var(--text-muted); cursor:pointer;" onclick="openLightboxModal('{uri}', '{safe_alt}')">🔍 คลิกขยาย</span>
  </div>
  <img src="{uri}" alt="{alt}" style="width:100%; height:auto; display:block; cursor:zoom-in;" onclick="openLightboxModal('{uri}', '{safe_alt}')">
</div>"""


# ----------------------------------------------------------------------------
# 1. โหลดธีม Bauhaus Pop (mirror ของ utils/theme.py) + nav JS จาก deck เดิม
# ----------------------------------------------------------------------------


def extract_theme(deck_path: Path) -> tuple[str, str]:
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
    nav_js = nav_js.replace(
        "const isBackup = index >= 15;",
        "const isBackup = index >= DEFENSE_BACKUP_FROM;",
    )
    if "DEFENSE_BACKUP_FROM" in nav_js and "const DEFENSE_BACKUP_FROM" not in nav_js:
        nav_js = "const DEFENSE_BACKUP_FROM = 999;\n" + nav_js
    nav_js += """
function openLightboxModal(src, caption) {
  const modal = document.getElementById('imageLightboxModal');
  const img = document.getElementById('lightboxImg');
  const cap = document.getElementById('lightboxCaption');
  if (modal && img) {
    img.src = src;
    if (cap) cap.textContent = caption || '';
    modal.style.display = 'flex';
  }
}
function closeLightboxModal() {
  const modal = document.getElementById('imageLightboxModal');
  if (modal) modal.style.display = 'none';
}
document.addEventListener('keydown', (e) => {
  if (e.key === 'Escape') {
    closeLightboxModal();
  }
});
"""
    return nav_js


# ----------------------------------------------------------------------------
# 2. ฟังก์ชันตัวช่วยนิยามสไลด์
# ----------------------------------------------------------------------------


def slide(label: str, title: str, body: str, counter: str = "", speaker: str = "") -> str:
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


def cover_slide(label: str, title: str, subtitle: str, meta_html: str, counter: str = "01 / 34") -> str:
    return f"""      <div class="slide">
        <div class="slide-header">
          <div>
            <div class="section-label">{label}</div>
            <div class="main-title" style="font-size:2.35rem; line-height:1.35; margin-top:0.5rem;">{title}</div>
            <p style="font-size:1.15rem; color:var(--text-secondary); margin-top:0.9rem; font-weight:500;">{subtitle}</p>
          </div>
          <div class="slide-counter-chip">{counter}</div>
        </div>
        <div class="slide-body">
{meta_html}
        </div>
      </div>"""


# ----------------------------------------------------------------------------
# 3. นิยามเนื้อหาสไลด์ 34 หน้า (Act 1 ถึง Act 6)
# ----------------------------------------------------------------------------

# ============================================================================
# ACT 1: บทนำ ที่มา และการวางตำแหน่งเครื่องมือ (สไลด์ 01–06, ~5 นาที)
# ============================================================================

S01 = cover_slide(
    "รายงานโครงงานคณิตศาสตร์ประยุกต์ ประจำปีการศึกษา 2569",
    "การพัฒนาเว็บแอปพลิเคชันช่วยเรียนคณิตศาสตร์<br>สำหรับแคลคูลัสเบื้องต้น",
    "Development of a Math Tutor Web Application for Introductory Calculus",
    """          <div class="grid-3">
            <div class="academic-card">
              <div class="card-heading">ผู้จัดทำ</div>
              <p style="font-size:0.92rem; color:var(--text-secondary); margin-top:0.4rem;">
                นางสาวขวัญเรือน สำเนียงดี (6621602928)<br>
                นางสาวเบญจกัฬยาณี พิทยากูล (6621602979)
              </p>
            </div>
            <div class="academic-card">
              <div class="card-heading">อาจารย์ที่ปรึกษา</div>
              <p style="font-size:0.92rem; color:var(--text-secondary); margin-top:0.4rem;">
                อาจารย์ ดร.กิตติพงศ์ ทรัพย์วัฒนาชัย
              </p>
            </div>
            <div class="academic-card">
              <div class="card-heading">ภาควิชา</div>
              <p style="font-size:0.92rem; color:var(--text-secondary); margin-top:0.4rem;">
                วิทยาการคำนวณและเทคโนโลยีดิจิทัล<br>คณะศิลปศาสตร์และวิทยาศาสตร์ มก.
              </p>
            </div>
          </div>
          <div class="academic-card highlight" style="margin-top:0.35rem;">
            <p style="font-size:0.9rem; color:var(--text-secondary);">
              <strong>โครงสร้างการนำเสนอ 28–30 นาที</strong> บทนำและเปรียบเทียบเครื่องมือ &rarr; สถาปัตยกรรม &rarr;
              เนื้อหาและตัวอย่างคำนวณบทที่ 2 (7 โมดูล x 2 สไลด์) &rarr; การทดสอบ 265 ข้อ &rarr; การประเมินผู้ใช้จริง &rarr; แถลง Errata
            </p>
          </div>""",
    "01 / 34"
)

S02 = slide(
    "1. ที่มาและความสำคัญ · สภาพปัญหาในการเรียนแคลคูลัส",
    "สามปัญหาสำคัญที่พบในการจัดการเรียนการสอนแคลคูลัสระดับมหาวิทยาลัย",
    """          <div class="grid-3">
            <div class="academic-card">
              <div class="card-heading">1. ความซับซ้อนของมโนทัศน์</div>
              <p style="font-size:0.86rem; color:var(--text-secondary); margin-top:0.35rem;">
                นิสิตส่วนใหญ่ประสบปัญหาในหัวข้อ <strong>ลิมิต อนุพันธ์ และปริพันธ์</strong> เนื่องจากเป็นแนวคิดเชิงนามธรรม
                ที่ต้องอาศัยการเชื่อมโยงอย่างแนบแน่นระหว่าง <strong>เรขาคณิตและพีชคณิต</strong>
              </p>
            </div>
            <div class="academic-card">
              <div class="card-heading">2. ขาดความเข้าใจเงื่อนไขและที่มา</div>
              <p style="font-size:0.86rem; color:var(--text-secondary); margin-top:0.35rem;">
                ผู้เรียนมักจดจำเฉพาะ <strong>สูตรสำเร็จในการคำนวณ</strong> แต่ขาดความเข้าใจในเงื่อนไขการใช้สูตร
                เช่น เงื่อนไขความต่อเนื่อง ขอบเขตการอินทิเกรต หรือพฤติกรรมของฟังก์ชัน ณ จุดวิกฤต
              </p>
            </div>
            <div class="academic-card">
              <div class="card-heading">3. สื่อการเรียนรู้กระจัดกระจาย</div>
              <p style="font-size:0.86rem; color:var(--text-secondary); margin-top:0.35rem;">
                เนื้อหา ตัวอย่าง และแบบฝึกหัดที่มีอยู่ทั่วไปมักกระจัดกระจาย ขาดการจัดหมวดหมู่อย่างเป็นระบบ
                และไม่มีระบบที่รวบรวมเครื่องมือคำนวณพร้อมคำอธิบายภาษาไทยไว้ในที่เดียว
              </p>
            </div>
          </div>
          <div class="academic-card highlight">
            <p style="font-size:0.9rem; color:var(--text-secondary);">
              <strong>แรงบันดาลใจในการวิจัย:</strong> พัฒนาสื่อการเรียนรู้ดิจิทัลภาษาไทยที่เป็นเสมือน "ห้องทดลองทางคณิตศาสตร์"
              ให้ผู้เรียนสามารถทดลองปรับค่า สังเกตพฤติกรรมกราฟ และทำความเข้าใจที่มาของสูตรด้วยตนเอง
            </p>
          </div>""",
    "02 / 34",
    "ขวัญเรือน"
)

S03 = slide(
    "1. ที่มาและความสำคัญ · ปัญหามโนทัศน์ที่มองไม่เห็น",
    "สามจุดบอดทางมโนทัศน์ที่ผู้เรียนคำนวณได้ แต่จินตนาการภาพไม่ออก",
    """          <div class="grid-3">
            <div class="academic-card">
              <div class="card-heading">จุดที่ 1 · ลิมิตเข้าใกล้จุด</div>
              <p style="font-size:0.86rem; color:var(--text-secondary); margin-top:0.35rem;">
                รูปแบบยังไม่กำหนด $\\frac{0}{0}$ ผู้เรียนมักท่องจำว่า "แยกตัวประกอบแล้วตัดทอน"
                แต่ไม่เคยเห็นว่าค่าฟังก์ชันวิ่งชนเข้าสู่ 4 จริงอย่างไร และทำไมกราฟจึงเกิดจุดโปร่ง
              </p>
              <div class="math-box">$$\\lim_{x\\to 2}\\frac{x^2-4}{x-2} = 4$$</div>
            </div>
            <div class="academic-card">
              <div class="card-heading">จุดที่ 2 · อนุพันธ์และเส้นสัมผัส</div>
              <p style="font-size:0.86rem; color:var(--text-secondary); margin-top:0.35rem;">
                คำว่า $h\\to 0$ ในนิยามอนุพันธ์เป็นนามธรรม ผู้เรียนไม่เห็นการหมุนของเส้นตัดโค้งเข้าทาบเส้นสัมผัส
                และไม่เข้าใจว่าทำไมจุดมุมแหลม $|x|$ จึงหาอนุพันธ์ไม่ได้
              </p>
              <div class="math-box">$$f'(a)=\\lim_{h\\to 0}\\frac{f(a+h)-f(a)}{h}$$</div>
            </div>
            <div class="academic-card">
              <div class="card-heading">จุดที่ 3 · ปริพันธ์ผลรวมรีมันน์</div>
              <p style="font-size:0.86rem; color:var(--text-secondary); margin-top:0.35rem;">
                ผลบวกของพื้นที่สี่เหลี่ยมผืนผ้ากลายเป็นพื้นที่ใต้เส้นโค้งได้อย่างไร
                ตัวเชื่อมโยงที่แท้จริงคือการลู่เข้าเมื่อ $n\\to\\infty$ ไม่ใช่การท่องจำสูตรอินทิเกรต
              </p>
              <div class="math-box">$$\\lim_{n\\to\\infty}\\sum_{i=1}^{n} f(x_i^*)\\,\\Delta x = \\int_a^b f(x)\\,dx$$</div>
            </div>
          </div>
          <div class="academic-card highlight">
            <p style="font-size:0.9rem; color:var(--text-secondary);">
              <strong>หลักการสำคัญ:</strong> ปัญหาไม่ได้อยู่ที่ผู้เรียนคิดเลขไม่เป็น แต่อยู่ที่ <strong>ไม่มีภาพจำลองทางเรขาคณิต (Concept Image)</strong> ที่สอดคล้องกับนิยามทางคณิตศาสตร์ (Concept Definition)
            </p>
          </div>""",
    "03 / 34",
    "ขวัญเรือน"
)

S04 = slide(
    "1. ที่มาและความสำคัญ · การวิเคราะห์เปรียบเทียบระบบ",
    "การวางตำแหน่งเครื่องมือ: AI Chat vs WolframAlpha vs GeoGebra/Desmos vs เรา",
    """          <table class="table-academic">
            <thead>
              <tr>
                <th style="width:20%;">มิติการเปรียบเทียบ</th>
                <th style="width:20%;">ปัญญาประดิษฐ์ (AI Chat)</th>
                <th style="width:20%;">WolframAlpha</th>
                <th style="width:20%;">GeoGebra / Desmos</th>
                <th style="width:20%; background:var(--accent-blue-light);">Calculus Sandbox (เรา)</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td><strong>1. รูปแบบการโต้ตอบ</strong></td>
                <td>ทางเดียว (ถามแล้วอ่านคำตอบยาว)</td>
                <td>ทางเดียว (ใส่โจทย์แล้วดูผลลัพธ์)</td>
                <td>ปรับกราฟอิสระ (ไม่มีโจทย์ในตัว)</td>
                <td><strong>โต้ตอบสองทาง มีโครงสร้างนำทาง</strong></td>
              </tr>
              <tr>
                <td><strong>2. บทบาทต่อผู้เรียน</strong></td>
                <td>บอกวิธีทำทั้งหมดในคราวเดียว</td>
                <td>แสดงคำตอบทันที (วิธีทำเสียเงิน)</td>
                <td>วาดกราฟ ไม่มีระบบสอนในตัว</td>
                <td><strong>ห้องทดลองฝึกคิด มีคำใบ้ 3 ระดับ</strong></td>
              </tr>
              <tr>
                <td><strong>3. การจัดการจุดเข้าใจผิด</strong></td>
                <td>ตอบตามฉลาดโมเดล (เสี่ยงหลอน)</td>
                <td>ตรวจไม่ได้ แจ้งแค่ไวยากรณ์ผิด</td>
                <td>ตรวจไม่ได้ วาดตามที่พิมพ์</td>
                <td><strong>ตรวจจับ Misconceptions แจ้งเตือนสด</strong></td>
              </tr>
              <tr>
                <td><strong>4. ต้นทุนและการเข้าถึง</strong></td>
                <td>โมเดลคิดวิเคราะห์มีค่าบริการ</td>
                <td>วิธีทำละเอียดมีค่าบริการสูง</td>
                <td>ฟรี แต่ต้องเชี่ยวชาญพิมพ์สูตร</td>
                <td><strong>โอเพนซอร์ส 100% ฟรีผ่านเว็บ</strong></td>
              </tr>
            </tbody>
          </table>
          <p style="font-size:0.86rem; color:var(--text-secondary); margin-top:0.4rem;">
            อ้างอิงตารางที่ 3 เล่มหน้า 26 และสไลด์นำเสนอหัวข้อ: ระบบของเราออกแบบขึ้นเพื่อเป็น <strong>นั่งร้านทางปัญญา (Scaffolding)</strong> สำหรับผู้เรียนไทยโดยเฉพาะ
          </p>""",
    "04 / 34",
    "ขวัญเรือน"
)

S05 = slide(
    "2. วัตถุประสงค์ของโครงงาน",
    "เป้าหมายเชิงพัฒนาระบบ การศึกษา และการประเมินผล 5 ข้อ",
    """          <div class="grid-2">
            <div class="academic-card">
              <div class="card-heading">วัตถุประสงค์ 5 ข้อหลัก</div>
              <ol style="font-size:0.86rem; color:var(--text-secondary); margin-top:0.45rem; padding-left:1.15rem; line-height:1.75;">
                <li><strong>พัฒนาเว็บแอปพลิเคชัน:</strong> ด้วยภาษา Python และ Streamlit เพื่อเป็นสื่อการเรียนรู้เชิงโต้ตอบสำหรับแคลคูลัสเบื้องต้น</li>
                <li><strong>รวบรวมเนื้อหาครบวงจร:</strong> รวบรวมทฤษฎี ตัวอย่างคำนวณทีละขั้น และแบบฝึกหัด 7 โมดูลไว้ในระบบเดียวอย่างเป็นหมวดหมู่</li>
                <li><strong>สร้างระบบคำนวณสัญลักษณ์ (CAS):</strong> ใช้ SymPy ประมวลผลและแสดงขั้นตอนวิธีทำทางคณิตศาสตร์อย่างถูกต้องแม่นยำ</li>
                <li><strong>พัฒนากลไกป้องกันข้อผิดพลาด:</strong> ตรวจจับและแจ้งเตือนจุดเข้าใจผิด (Misconceptions) ที่พบบ่อยในแต่ละหัวข้อ</li>
                <li><strong>ประเมินความพึงพอใจและ SUS:</strong> ประเมินความสะดวกในการใช้งานกับผู้เรียนจริงตามเกณฑ์มาตรฐานสากล</li>
              </ol>
            </div>
            <div class="academic-card">
              <div class="card-heading">ประโยชน์ที่คาดว่าจะได้รับ</div>
              <ul style="font-size:0.86rem; color:var(--text-secondary); margin-top:0.45rem; padding-left:1.15rem; line-height:1.75;">
                <li>ผู้เรียนมีเครื่องมือทบทวนมโนทัศน์และฝึกแก้โจทย์ด้วยตนเองได้ทุกที่ทุกเวลา</li>
                <li>ลดภาระการจดจำสูตรโดยไม่เข้าใจเงื่อนไข ผ่านการทดลองปรับค่าพารามิเตอร์บนกราฟ</li>
                <li>อาจารย์ผู้สอนมีสื่อสาธิตทางคณิตศาสตร์เชิงโต้ตอบภาษาไทยใช้ประกอบการบรรยาย</li>
                <li>เป็นต้นแบบเว็บแอปพลิเคชันเพื่อการศึกษาที่ต่อยอดในวิชาคณิตศาสตร์ขั้นสูงได้</li>
              </ul>
            </div>
          </div>""",
    "05 / 34",
    "ขวัญเรือน"
)

S06 = slide(
    "2. ขอบเขตการศึกษาและเทคโนโลยีที่ใช้",
    "กรอบเทคโนโลยี และขอบเขตเนื้อหา 7 โมดูลบทเรียน",
    """          <div class="grid-2">
            <div class="academic-card">
              <div class="card-heading">กรอบเทคโนโลยีที่เลือกใช้ (Technology Stack)</div>
              <ul style="font-size:0.85rem; color:var(--text-secondary); margin-top:0.4rem; padding-left:1.1rem; line-height:1.75;">
                <li><strong>ภาษาหลัก:</strong> Python 3.10+ ประสิทธิภาพสูง รองรับงานวิทยาศาสตร์ข้อมูล</li>
                <li><strong>ส่วนติดต่อผู้ใช้ (UI):</strong> Streamlit Framework สำหรับ Web App เชิงโต้ตอบ</li>
                <li><strong>ระบบคำนวณสัญลักษณ์:</strong> SymPy (Computer Algebra System) คำนวณตรงรูปแท้จริง</li>
                <li><strong>การพล็อตกราฟิก:</strong> Matplotlib + NumPy สำหรับวาดเส้นโค้งและพื้นที่เรขาคณิต 2D</li>
                <li><strong>การเรนเดอร์สมการ:</strong> KaTeX แสดงผลสูตรคณิตศาสตร์สวยงามตามมาตรฐาน LaTeX</li>
              </ul>
            </div>
            <div class="academic-card">
              <div class="card-heading">ขอบเขตเนื้อหา 7 โมดูลหลัก</div>
              <div class="grid-2" style="margin-top:0.4rem; gap:0.5rem; font-size:0.84rem; color:var(--text-secondary);">
                <div>
                  <div class="key-badge">M1</div> ลิมิตและความต่อเนื่อง<br>
                  <div class="key-badge">M2</div> เส้นสัมผัสและอนุพันธ์<br>
                  <div class="key-badge">M3</div> ผลรวมรีมันน์<br>
                  <div class="key-badge">M4</div> การแทนค่าตัวแปร $u$
                </div>
                <div>
                  <div class="key-badge">M5</div> พื้นที่ระหว่างเส้นโค้ง<br>
                  <div class="key-badge">M6</div> ปริมาตรทรงตันจากการหมุน<br>
                  <div class="key-badge">M7</div> ปริพันธ์ไม่ตรงแบบ<br>
                  <div class="key-badge">+</div> คลังข้อสอบมโนทัศน์ 80 ข้อ
                </div>
              </div>
              <p style="font-size:0.81rem; color:var(--text-muted); margin-top:0.5rem;">
                ขอบเขต: รองรับฟังก์ชันมูลฐานมาตรฐาน พหุนาม ตรีโกณ เอกซ์โพเนนเชียล ลอการิทึม หมุนรอบแกน $x$
              </p>
            </div>
          </div>""",
    "06 / 34",
    "ขวัญเรือน"
)

# ============================================================================
# ACT 2: สถาปัตยกรรมและระเบียบวิธีดำเนินงาน (สไลด์ 07–10, ~3 นาที)
# ============================================================================

S07 = slide(
    "3. วิธีดำเนินงาน · สถาปัตยกรรมระบบ 3 ชั้น",
    "จากเนื้อหาบทเรียน ผ่านการประมวลผล สู่การใช้งานบนเว็บ",
    """          <div class="grid-2" style="grid-template-columns:0.8fr 1.6fr; align-items:start;">
            <div style="display:flex; flex-direction:column; gap:0.65rem;">
              <div class="academic-card">
                <div class="card-heading">1. ส่วนติดต่อผู้ใช้ (Frontend)</div>
                <p style="font-size:0.84rem; color:var(--text-secondary); margin-top:0.3rem;">
                  <strong>Streamlit</strong> รับฟังก์ชันและพารามิเตอร์ แสดงบทเรียน วิธีทำ และกราฟโต้ตอบ
                </p>
              </div>
              <div class="academic-card">
                <div class="card-heading">2. บริการประมวลผล (Backend)</div>
                <p style="font-size:0.84rem; color:var(--text-secondary); margin-top:0.3rem;">
                  <strong>SymPy</strong> คำนวณเชิงสัญลักษณ์ ร่วมกับการตรวจเงื่อนไขและ <strong>Matplotlib</strong> สำหรับกราฟ
                </p>
              </div>
              <div class="academic-card">
                <div class="card-heading">3. จัดเก็บข้อมูล (Data &amp; Storage)</div>
                <p style="font-size:0.84rem; color:var(--text-secondary); margin-top:0.3rem;">
                  แยกเนื้อหาบทเรียน <strong>Markdown</strong> และคลังข้อสอบ <strong>JSON</strong> ออกจากตรรกะประมวลผล
                </p>
              </div>
            </div>
            <figure class="academic-card" style="margin:0; padding:0.75rem;">
              <div class="card-heading">ภาพรวมสถาปัตยกรรมและเส้นทางเผยแพร่</div>
              <button type="button" onclick="openLightboxModal(this.querySelector('img').src, 'ผังแนวคิดประกอบการนำเสนอ')" aria-label="ขยายภาพผังสถาปัตยกรรม" style="display:block; width:100%; padding:0; margin-top:0.5rem; border:0; background:transparent; cursor:zoom-in;">
                <img src='""" + img_b64("architecture-workflow-full.png") + """' alt="ผังแนวคิดแสดงเนื้อหา สถาปัตยกรรมสามชั้น และการเผยแพร่ผ่าน GitHub และ Streamlit Community Cloud" style="display:block; width:100%; height:auto; max-height:360px; object-fit:contain;">
              </button>
              <figcaption style="font-size:0.78rem; color:var(--text-secondary); margin-top:0.5rem; line-height:1.6;">
                คลิกภาพเพื่อขยาย &bull; ผังแนวคิดประกอบการนำเสนอ ไม่ใช่รายการความสามารถที่ทดสอบแล้วทั้งหมด<br>
                <strong>User Progress (Future)</strong> คือแนวทางพัฒนาต่อ ยังไม่ใช่ระบบบันทึกความก้าวหน้าถาวร
              </figcaption>
            </figure>
          </div>""",
    "07 / 34",
    "เบญจกัฬยาณี"
)

S08 = slide(
    "3. วิธีดำเนินงาน · นั่งร้านทางปัญญา 4 ระดับ",
    "การจัดลำดับการเรียนรู้ตามหลัก Cognitive Load (Sweller, 1988)",
    """          <div class="grid-4">
            <div class="academic-card">
              <div class="key-badge">ระดับ 1</div>
              <div class="card-heading" style="margin-top:0.5rem;">เห็นภาพ (Visualizing)</div>
              <p style="font-size:0.83rem; color:var(--text-secondary); margin-top:0.35rem;">
                ปรับค่าพารามิเตอร์ผ่านแถบเลื่อน (Slider) แล้วเห็นกราฟขยับตามทันที
              </p>
            </div>
            <div class="academic-card">
              <div class="key-badge">ระดับ 2</div>
              <div class="card-heading" style="margin-top:0.5rem;">เห็นโครงสร้าง (Structuring)</div>
              <p style="font-size:0.83rem; color:var(--text-secondary); margin-top:0.35rem;">
                คลี่ดูวิธีทำทีละขั้น พร้อมทฤษฎีบทกำกับในแต่ละขั้นตอนอย่างเป็นลำดับ
              </p>
            </div>
            <div class="academic-card">
              <div class="key-badge">ระดับ 3</div>
              <div class="card-heading" style="margin-top:0.5rem;">ลองทำเอง (Practicing)</div>
              <p style="font-size:0.83rem; color:var(--text-secondary); margin-top:0.35rem;">
                ทำแบบทดสอบมโนทัศน์ที่มีคำใบ้ 3 ระดับ ไม่บอกคำตอบสุดท้ายทันที
              </p>
            </div>
            <div class="academic-card">
              <div class="key-badge">ระดับ 4</div>
              <div class="card-heading" style="margin-top:0.5rem;">ตรวจจุดผิด (Self-Correcting)</div>
              <p style="font-size:0.83rem; color:var(--text-secondary); margin-top:0.35rem;">
                แจ้งเตือน $\\frac{0}{0}$, จุดโปร่ง, จุดมุมแหลม, จุดเอกฐาน, หรือพื้นที่ติดลบ
              </p>
            </div>
          </div>
          <div class="academic-card highlight">
            <p style="font-size:0.9rem; color:var(--text-secondary);">
              <strong>ทำไมต้องมีครบทั้ง 4 ระดับ:</strong> หากมีแต่กราฟ ผู้เรียนจะได้เพียงความเพลิดเพลินแต่เขียนวิธีทำไม่เป็น &bull; หากมีแต่เฉลย ผู้เรียนจะขาดการคิดวิเคราะห์ &bull; การผสาน 4 ระดับช่วยให้เกิด <strong>การตรวจสอบตนเอง (Metacognition)</strong>
            </p>
          </div>""",
    "08 / 34",
    "เบญจกัฬยาณี"
)

S09 = slide(
    "3. วิธีดำเนินงาน · ขั้นตอนการดำเนินงาน 4 ขั้นตอน",
    "วงจรการพัฒนาระบบ: Plan & Design &bull; Content &bull; Development &bull; Test & Deploy",
    """          <div class="grid-2">
            <div class="academic-card">
              <div class="card-heading">ขั้นตอนที่ 1 · Plan & Design</div>
              <p style="font-size:0.84rem; color:var(--text-secondary); margin-top:0.3rem;">
                กำหนดวัตถุประสงค์การเรียนรู้ตามหลักสูตร มก. จัดทำโครงสร้างบทเรียน และออกแบบ Wireframe / UI Mockup สไตล์ Bauhaus Pop
              </p>
              <div class="card-heading" style="margin-top:0.6rem;">ขั้นตอนที่ 2 · Content Synthesis</div>
              <p style="font-size:0.84rem; color:var(--text-secondary); margin-top:0.3rem;">
                สังเคราะห์เนื้อหาทฤษฎีแคลคูลัส 7 หัวข้อ จัดทำขั้นตอนวิธีทำตัวอย่างโจทย์ และเตรียมคลังข้อสอบมโนทัศน์ 80 ข้อพร้อมคำใบ้ 3 ระดับ
              </p>
            </div>
            <div class="academic-card">
              <div class="card-heading">ขั้นตอนที่ 3 · System Development</div>
              <p style="font-size:0.84rem; color:var(--text-secondary); margin-top:0.3rem;">
                พัฒนาเว็บแอปด้วย Python + Streamlit สร้างโมดูลคำนวณ SymPy Solver และโมดูลวาดกราฟิก Matplotlib Plotter
              </p>
              <div class="card-heading" style="margin-top:0.6rem;">ขั้นตอนที่ 4 · Test & Cloud Deployment</div>
              <p style="font-size:0.84rem; color:var(--text-secondary); margin-top:0.3rem;">
                ทดสอบความถูกต้องด้วย Pytest 265 ข้อ, ทดสอบขอบเขต 144 เคส นำขึ้น Streamlit Community Cloud และประเมินผู้ใช้จริง $N=50$ คน
              </p>
            </div>
          </div>""",
    "09 / 34",
    "เบญจกัฬยาณี"
)

S10 = slide(
    "3. วิธีดำเนินงาน · การเข้าถึงระบบจริง (Live Access)",
    "ช่องทางการเข้าใช้งานเว็บแอปพลิเคชันบน Streamlit Cloud และคลังรหัสต้นฉบับ",
    """          <div class="grid-2">
            <div class="academic-card">
              <div class="card-heading">ช่องทางการใช้งานระบบจริง</div>
              <p style="font-size:0.88rem; color:var(--text-secondary); margin-top:0.4rem;">
                ระบบได้รับการติดตั้งและเปิดให้ใช้งานสาธารณะผ่าน <strong>Streamlit Community Cloud</strong>:
              </p>
              <div class="math-box" style="font-size:0.88rem; font-family:'Outfit', sans-serif; word-break:break-all;">
                <a href='""" + APP_URL + """' target="_blank" rel="noopener" style="color:var(--primary-blue);">
                  """ + APP_URL + """
                </a>
              </div>
              <ul style="font-size:0.84rem; color:var(--text-secondary); margin-top:0.5rem; padding-left:1.15rem; line-height:1.7;">
                <li>รองรับการใช้งานผ่านเว็บเบราว์เซอร์ทุกแพลตฟอร์ม (PC, Tablet, Mobile)</li>
                <li>ไม่ต้องติดตั้งโปรแกรมหรือไลบรารีใดๆ เพิ่มเติมบนเครื่องผู้เรียน</li>
                <li>ซอร์สโค้ดเปิดเผยแบบ Open Source บน GitHub</li>
              </ul>
            </div>
            <div class="academic-card primary" style="text-align:center; display:flex; flex-direction:column; align-items:center; justify-content:center;">
              <div class="card-heading" style="justify-content:center;">สแกนเพื่อเปิดแอปพลิเคชันจริง</div>
              <img src='""" + img_b64('calculus-app-qr.png') + """' alt="QR Code เข้าใช้งานระบบ"
                   style="width:145px; height:145px; margin-top:0.6rem; border:2px solid var(--ink); border-radius:10px; padding:5px; background:#fff; box-shadow:3px 3px 0 var(--ink); cursor:zoom-in;"
                   onclick="openLightboxModal(this.src, 'QR Code เข้าใช้งานระบบ')">
              <p style="font-size:0.78rem; color:var(--text-muted); margin-top:0.5rem;">
                สแกนด้วยสมาร์ตโฟนหรือแท็บเล็ตเพื่อร่วมทดสอบพร้อมกัน
              </p>
            </div>
          </div>""",
    "10 / 34",
    "ขวัญเรือน"
)

# ============================================================================
# ACT 3: ทฤษฎีและเนื้อหาบทที่ 2 (สไลด์ 11–24: 7 โมดูล x 2 สไลด์, ~12 นาที)
# ============================================================================

# --- 2.1.1 ลิมิตและความต่อเนื่อง ---
S11 = slide(
    "2.1.1 ทฤษฎี · ลิมิตและความต่อเนื่อง",
    "นิยามลิมิตสองด้าน ความต่อเนื่อง 3 เงื่อนไข และกฎโลปิตาล",
    """          <div class="grid-2">
            <div class="academic-card">
              <div class="card-heading">นิยามลิมิตและความต่อเนื่อง</div>
              <p style="font-size:0.84rem; color:var(--text-secondary); margin-top:0.35rem;">
                ลิมิตของ $f(x)$ เมื่อ $x\\to a$ จะมีค่าเท่ากับ $L$ ก็ต่อเมื่อลิมิตซ้ายและขวามีค่าเท่ากัน:
              </p>
              <div class="math-box" style="font-size:0.82rem;">$$\\lim_{x\\to a^-} f(x) = \\lim_{x\\to a^+} f(x) = L$$</div>
              <p style="font-size:0.84rem; color:var(--text-secondary); margin-top:0.35rem;">
                ฟังก์ชันจะ <strong>ต่อเนื่อง ณ จุด $x = a$</strong> ก็ต่อเมื่อครบ 3 เงื่อนไข:
              </p>
              <ol style="font-size:0.82rem; color:var(--text-secondary); margin-top:0.25rem; padding-left:1.1rem; line-height:1.6;">
                <li>$f(a)$ นิยามและหาค่าได้ในโดเมน</li>
                <li>$\\lim_{x\\to a} f(x)$ หาค่าได้เป็นจำนวนจริง</li>
                <li>$\\lim_{x\\to a} f(x) = f(a)$</li>
              </ol>
            </div>
            <div class="academic-card">
              <div class="card-heading">รูปแบบยังไม่กำหนด และกฎโลปิตาล</div>
              <p style="font-size:0.84rem; color:var(--text-secondary); margin-top:0.35rem;">
                เมื่อแทนค่าแล้วได้รูปแบบยังไม่กำหนด $\\left[\\frac{0}{0}\\right]$ หรือ $\\left[\\frac{\\infty}{\\infty}\\right]$
                หาก $f$ และ $g$ หาอนุพันธ์ได้บนช่วงเปิดรอบจุด $a$ และ $g'(x) \\neq 0$ จะได้:
              </p>
              <div class="math-box" style="font-size:0.82rem;">$$\\lim_{x\\to a} \\frac{f(x)}{g(x)} = \\lim_{x\\to a} \\frac{f'(x)}{g'(x)}$$</div>
              <p style="font-size:0.82rem; color:var(--text-muted); margin-top:0.4rem;">
                ระบบของเรารองรับทั้งการแยกตัวประกอบพีชคณิต และการตรวจสอบด้วยอนุพันธ์โลปิตาล
              </p>
            </div>
          </div>""",
    "11 / 34",
    "ขวัญเรือน"
)

S12 = slide(
    "2.1.1 ตัวอย่าง · ลิมิตและการจัดการรูปแบบ 0/0",
    "ตัวอย่างที่ 2.2: การคำนวณลิมิต ตารางลู่เข้า และการพล๊อตจุดโปร่ง",
    """          <div class="grid-2">
            <div class="academic-card">
              <div class="card-heading">ตัวอย่างที่ 2.2 จากเล่มรายงาน (หน้า 8)</div>
              <p style="font-size:0.84rem; color:var(--text-secondary); margin-top:0.3rem;">
                จงหาค่าของ $\\lim_{x\\to 3}\\frac{x^2-9}{x-3}$ ซึ่งแทนค่าแล้วได้ $\\left[\\frac{0}{0}\\right]$
              </p>
              <div class="math-box" style="font-size:0.82rem;">
                $$\\lim_{x\\to 3}\\frac{(x-3)(x+3)}{x-3} = \\lim_{x\\to 3}(x+3) = 6$$
              </div>
              <p style="font-size:0.82rem; color:var(--text-secondary); margin-top:0.35rem;">
                <strong>ตารางจำลองค่าลู่เข้าเชิงตัวเลขของระบบ:</strong>
              </p>
              <table class="table-academic" style="font-size:0.78rem;">
                <thead><tr><th>$x$ ซ้าย</th><th>$f(x)$</th><th>$x$ ขวา</th><th>$f(x)$</th></tr></thead>
                <tbody>
                  <tr><td>2.9</td><td>5.900</td><td>3.1</td><td>6.100</td></tr>
                  <tr><td>2.99</td><td>5.990</td><td>3.01</td><td>6.010</td></tr>
                  <tr><td>2.999</td><td>5.999</td><td>3.001</td><td>6.001</td></tr>
                </tbody>
              </table>
              <div class="academic-card highlight" style="margin-top:0.4rem; padding:0.5rem;">
                <p style="font-size:0.82rem; color:var(--text-secondary);">
                  <strong>จุดเตือนของระบบ:</strong> แม้ $f(3)$ จะไม่นิยามในโดเมน แต่ลิมิตหาค่าได้ กราฟจะแสดง <strong>จุดโปร่ง (Hole)</strong> ที่พิกัด $(3, 6)$ อย่างชัดเจน ป้องกันการสับสนระหว่างค่าฟังก์ชันกับลิมิต
                </p>
              </div>
            </div>
            <div>
""" + web_frame_img("screenshot-limit-full.png", "โมดูลลิมิตเข้าใกล้จุด", "หน้าจอเว็บแอปจริง · ลิมิตเข้าใกล้จุดและการพล๊อตจุดโปร่ง (Hole)", max_height="390px") + """
            </div>
          </div>""",
    "12 / 34",
    "ขวัญเรือน"
)
# --- 2.1.2 เส้นสัมผัสและอนุพันธ์ ---
S13 = slide(
    "2.1.2 ทฤษฎี · เส้นสัมผัสและอนุพันธ์",
    "การแปลงจากเส้นตัดโค้งสู่เส้นสัมผัส และทฤษฎีบทการหาอนุพันธ์ได้",
    """          <div class="grid-2">
            <div class="academic-card">
              <div class="card-heading">นิยามอนุพันธ์ผ่านความชันเส้นตัดโค้ง</div>
              <p style="font-size:0.84rem; color:var(--text-secondary); margin-top:0.35rem;">
                ความชันของเส้นตัดโค้ง (Secant Line) ผ่านจุด $P(a, f(a))$ และ $Q(a+h, f(a+h))$ คือ:
              </p>
              <div class="math-box" style="font-size:0.82rem;">$$m_{\\text{sec}} = \\frac{f(a+h) - f(a)}{h}$$</div>
              <p style="font-size:0.84rem; color:var(--text-secondary); margin-top:0.35rem;">
                เมื่อ $h \\to 0$ จุด $Q$ เลื่อนเข้าทับจุด $P$ เส้นตัดโค้งจะกลายเป็น <strong>เส้นสัมผัส (Tangent Line)</strong>:
              </p>
              <div class="math-box" style="font-size:0.82rem;">$$f'(a) = \\lim_{h\\to 0} \\frac{f(a+h) - f(a)}{h}$$</div>
            </div>
            <div class="academic-card">
              <div class="card-heading">ทฤษฎีบทการหาอนุพันธ์ได้และความต่อเนื่อง</div>
              <div class="academic-card highlight" style="margin-top:0.35rem; padding:0.6rem;">
                <p style="font-size:0.85rem; color:var(--text-secondary);">
                  <strong>ทฤษฎีบท:</strong> ถ้า $f$ สามารถหาอนุพันธ์ได้ที่จุด $x = a$ แล้ว $f$ ย่อมมีความต่อเนื่องที่จุด $x = a$ เสมอ
                </p>
              </div>
              <p style="font-size:0.84rem; color:var(--text-secondary); margin-top:0.5rem;">
                <strong>บทกลับไม่เป็นจริง:</strong> ฟังก์ชันต่อเนื่องไม่จำเป็นต้องหาอนุพันธ์ได้ เช่น กรณี <strong>จุดมุมแหลม (Corner Point)</strong> หรือ <strong>เส้นสัมผัสแนวดิ่ง (Vertical Tangent)</strong>
              </p>
            </div>
          </div>""",
    "13 / 34",
    "ขวัญเรือน"
)

S14 = slide(
    "2.1.2 ตัวอย่าง · อนุพันธ์และกับดักจุดมุมแหลม",
    "ตัวอย่างที่ 2.3: หาสมการเส้นสัมผัส $x^2$ และการดักจับจุดมุมแหลม $|x|$",
    """          <div class="grid-2">
            <div class="academic-card">
              <div class="card-heading">ตัวอย่างที่ 2.3 จากเล่มรายงาน (หน้า 12)</div>
              <p style="font-size:0.84rem; color:var(--text-secondary); margin-top:0.3rem;">
                จงหาความชันและสมการเส้นสัมผัสของ $f(x) = x^2$ ที่จุด $x = 1$
              </p>
              <div class="math-box" style="font-size:0.8rem;">
                $$f'(1) = \\lim_{h\\to 0}\\frac{(1+h)^2 - 1^2}{h} = \\lim_{h\\to 0}\\frac{2h+h^2}{h} = 2$$
              </div>
              <p style="font-size:0.82rem; color:var(--text-secondary); margin-top:0.3rem;">
                จุดสัมผัสคือ $(1, 1)$ ความชัน $m = 2$ หาสมการเส้นสัมผัสได้คือ:
              </p>
              <div class="math-box" style="font-size:0.8rem;">
                $$y - 1 = 2(x - 1) \\implies y = 2x - 1$$
              </div>
              <div class="academic-card highlight" style="margin-top:0.4rem; padding:0.5rem;">
                <p style="font-size:0.81rem; color:var(--text-secondary);">
                  <strong>จุดเตือนของระบบ:</strong> ลิมิตความชันด้านซ้ายได้ $-1$ ด้านขวาได้ $+1$ ไม่เท่ากัน อนุพันธ์จึง **DNE** ระบบแจ้งเตือนว่าเป็นจุดมุมแหลมและปฏิเสธการวาดเส้นสัมผัสลวง
                </p>
              </div>
            </div>
            <div>
""" + web_frame_img("screenshot-tangent-full.png", "โมดูลเส้นสัมผัสและอนุพันธ์", "หน้าจอเว็บแอปจริง · เส้นสัมผัสและการดักจับจุดมุมแหลม", max_height="390px") + """
            </div>
          </div>""",
    "14 / 34",
    "ขวัญเรือน"
)

# --- 2.1.3 ผลรวมรีมันน์ ---
S15 = slide(
    "2.1.3 ทฤษฎี · ผลรวมรีมันน์และทฤษฎีบทหลักมูล",
    "นิยามผลรวมรีมันน์ 3 รูปแบบ และทฤษฎีบทหลักมูลของแคลคูลัส (FTC 1 & 2)",
    """          <div class="grid-2">
            <div class="academic-card">
              <div class="card-heading">นิยามผลรวมรีมันน์ (Riemann Sum)</div>
              <p style="font-size:0.84rem; color:var(--text-secondary); margin-top:0.35rem;">
                แบ่งช่วง $[a, b]$ ออกเป็น $n$ ช่วงย่อย ความกว้าง $\\Delta x = \\frac{b-a}{n}$
              </p>
              <ul style="font-size:0.82rem; color:var(--text-secondary); margin-top:0.3rem; padding-left:1.1rem; line-height:1.65;">
                <li><strong>ผลรวมซ้าย:</strong> $L_n = \\sum_{i=1}^n f(x_{i-1})\\Delta x$</li>
                <li><strong>ผลรวมขวา:</strong> $R_n = \\sum_{i=1}^n f(x_i)\\Delta x$</li>
                <li><strong>จุดกึ่งกลาง:</strong> $M_n = \\sum_{i=1}^n f(x_i^*)\\Delta x$ โดย $x_i^* = a + (i-0.5)\\Delta x$</li>
              </ul>
              <div class="math-box" style="font-size:0.8rem; margin-top:0.3rem;">
                $$\\int_a^b f(x)\\,dx = \\lim_{n\\to\\infty} \\sum_{i=1}^n f(x_i^*)\\,\\Delta x$$
              </div>
            </div>
            <div class="academic-card">
              <div class="card-heading">ทฤษฎีบทหลักมูลของแคลคูลัส (FTC)</div>
              <div class="academic-card highlight" style="margin-top:0.35rem; padding:0.55rem;">
                <p style="font-size:0.82rem; color:var(--text-secondary);">
                  <strong>FTC ส่วนที่ 1:</strong> ถ้า $f$ ต่อเนื่องบน $[a, b]$ และ $g(x) = \\int_a^x f(t)dt$ แล้ว $g'(x) = f(x)$
                </p>
              </div>
              <div class="academic-card highlight" style="margin-top:0.35rem; padding:0.55rem;">
                <p style="font-size:0.82rem; color:var(--text-secondary);">
                  <strong>FTC ส่วนที่ 2:</strong> ถ้า $F'(x) = f(x)$ แล้ว $\\int_a^b f(x)dx = F(b) - F(a)$
                </p>
              </div>
              <p style="font-size:0.82rem; color:var(--text-muted); margin-top:0.35rem;">
                FTC คือสะพานเชื่อมระหว่าง "พื้นที่จากการลู่เข้าของรีมันน์" กับ "ปฏิยานุพันธ์"
              </p>
            </div>
          </div>""",
    "15 / 34",
    "ขวัญเรือน"
)

S16 = slide(
    "2.1.3 ตัวอย่าง · ตรรกะขั้นตอนวิธีผลรวมรีมันน์",
    "ตัวอย่างที่ 2.7: การลู่เข้าของ $x^2$ บน $[0, 2]$ และความแม่นยำของจุดกึ่งกลาง",
    """          <div class="grid-2">
            <div>
              <table class="table-academic" style="font-size:0.75rem;">
                <thead>
                  <tr>
                    <th>จำนวนช่วง $n$</th>
                    <th>ผลรวมซ้าย $L_n$</th>
                    <th>Error ซ้าย</th>
                    <th>ผลรวมขวา $R_n$</th>
                    <th>Error ขวา</th>
                    <th>จุดกึ่งกลาง $M_n$</th>
                    <th>Error กึ่งกลาง</th>
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
              <p style="font-size:0.83rem; font-weight:600; margin-top:0.3rem;">
                ค่าจริงเชิงสัญลักษณ์: $\\int_0^2 x^2\\,dx = \\frac{8}{3} \\approx 2.6667$ ทั้งสามวิธีลู่เข้าหาค่านี้
              </p>
              <div style="display:flex; flex-direction:column; gap:0.4rem; margin-top:0.3rem;">
                <div class="academic-card" style="padding:0.5rem 0.7rem;">
                  <div class="card-heading" style="font-size:0.85rem;">เหตุผลที่จุดกึ่งกลางแม่นยำกว่า</div>
                  <p style="font-size:0.8rem; color:var(--text-secondary); margin-top:0.15rem;">
                    ที่ $n=4$ จุดกึ่งกลางคลาดเคลื่อนเพียง 1.56% เพราะพื้นที่ส่วนเกินด้านหนึ่งหักล้างกับส่วนขาดอีกด้านหนึ่งอย่างสมดุล
                  </p>
                </div>
                <div class="academic-card highlight" style="padding:0.5rem 0.7rem;">
                  <div class="card-heading" style="font-size:0.85rem;">สูตรตัวแทนในเล่มได้รับการแก้ไขแล้ว</div>
                  <p style="font-size:0.8rem; color:var(--text-secondary); margin-top:0.15rem;">
                    สูตรจุดกึ่งกลาง $x_i^* = a + (i-0.5)\\Delta x$ ในตัวอย่าง 2.7 หน้า 14 ของเล่มส่งกรรมการได้รับการแก้เป็นเครื่องหมายบวกถูกต้องแล้ว
                  </p>
                </div>
              </div>
            </div>
            <div>
""" + web_frame_img("screenshot-riemann-full.png", "โมดูลผลรวมรีมันน์", "หน้าจอเว็บแอปจริง · การจำลองแท่งสี่เหลี่ยมและการลู่เข้าสู่ค่าปริพันธ์", max_height="390px") + """
            </div>
          </div>""",
    "16 / 34",
    "ขวัญเรือน"
)

# --- 2.1.4 เทคนิคการอินทิเกรต ---
S17 = slide(
    "2.1.4 ทฤษฎี · เทคนิคการอินทิเกรต",
    "การแทนค่าตัวแปร $u$ และการอินทิเกรตทีละส่วนด้วยหลักลำดับ LIATE",
    """          <div class="grid-2">
            <div class="academic-card">
              <div class="card-heading">1. การแทนค่าตัวแปร $u$ (Substitution)</div>
              <p style="font-size:0.83rem; color:var(--text-secondary); margin-top:0.35rem;">
                ใช้กฎลูกโซ่แบบย้อนกลับ: ให้ $u = g(x)$ จะได้ $du = g'(x)dx$
              </p>
              <div class="math-box" style="font-size:0.8rem;">$$\\int f(g(x))g'(x)\\,dx = \\int f(u)\\,du$$</div>
              <p style="font-size:0.83rem; color:var(--text-secondary); margin-top:0.35rem;">
                <strong>ปริพันธ์จำกัดเขตต้องเปลี่ยนขอบเขต:</strong> จาก $[a, b]$ สู่ $[g(a), g(b)]$ โดยไม่ต้องแปลงตัวแปรกลับ
              </p>
            </div>
            <div class="academic-card">
              <div class="card-heading">2. ลำดับการเลือก $u$ ตามกฎ LIATE (จากสไลด์หัวข้อ)</div>
              <p style="font-size:0.82rem; color:var(--text-secondary); margin-top:0.3rem;">
                สูตร By Parts: $\\int u\\,dv = uv - \\int v\\,du$ เรียงลำดับความสำคัญของ $u$:
              </p>
              <ul style="font-size:0.8rem; color:var(--text-secondary); margin-top:0.25rem; padding-left:1rem; line-height:1.6;">
                <li><strong>L (Logarithmic):</strong> $\\ln x$ &rarr; ควรเป็น $u$ เสมอ (ดิฟง่าย แต่อินทิเกรตยาก)</li>
                <li><strong>I (Inverse Trig):</strong> $\\arctan x$ &rarr; ควรเป็น $u$ เสมอ (ดิฟแล้วเป็นพีชคณิต)</li>
                <li><strong>A (Algebraic):</strong> $x^n$ &rarr; มักเป็น $u$ (ดิฟแล้วดีกรีลดลงเรื่อย ๆ)</li>
                <li><strong>T (Trigonometric):</strong> $\\sin x, \\cos x$ &rarr; มักเป็น $dv$ (อินทิเกรตแล้ววนลูป)</li>
                <li><strong>E (Exponential):</strong> $e^x$ &rarr; ควรเป็น $dv$ เสมอ (อินทิเกรตง่ายที่สุด)</li>
              </ul>
            </div>
          </div>""",
    "17 / 34",
    "ขวัญเรือน"
)

S18 = slide(
    "2.1.4 ตัวอย่าง · การแทนค่า $u$ และ By Parts",
    "ตัวอย่างที่ 2.8 และ 2.9: การคำนวณจริง และกับดักการเลือกตัวแปร By Parts",
    """          <div class="grid-2">
            <div style="display:flex; flex-direction:column; gap:0.5rem;">
              <div class="academic-card">
                <div class="card-heading">ตัวอย่างที่ 2.8: แทนค่า $u$ (เล่มหน้า 15)</div>
                <p style="font-size:0.82rem; color:var(--text-secondary); margin-top:0.25rem;">
                  จงหาค่าของ $\\int 2x\\cos(x^2)\\,dx$ ให้ $u = x^2 \\implies du = 2x\\,dx$
                </p>
                <div class="math-box" style="font-size:0.78rem;">
                  $$\\int \\cos(u)\\,du = \\sin(u) + C = \\sin(x^2) + C$$
                </div>
                <p style="font-size:0.8rem; color:var(--text-secondary); margin-top:0.25rem;">
                  ระบบจะตรวจสอบว่า $2x$ ตัดทอนกับ $dx$ ได้หมดจดหรือไม่ หากไม่หมดจะแจ้งเตือน
                </p>
              </div>
              <div class="academic-card">
                <div class="card-heading">ตัวอย่างที่ 2.9: กับดัก By Parts $\\int x e^x dx$</div>
                <p style="font-size:0.81rem; color:var(--text-secondary); margin-top:0.25rem;">
                  <strong>เลือกถูก (LIATE):</strong> $u = x, dv = e^x dx \\implies du = dx, v = e^x$<br>
                  $= x e^x - \\int e^x dx = xe^x - e^x + C$ (ดีกรีลดลง)
                </p>
                <div class="academic-card highlight" style="margin-top:0.3rem; padding:0.45rem;">
                  <p style="font-size:0.79rem; color:var(--text-secondary);">
                    <strong>จุดเตือนเมื่อเลือกสลับ:</strong> หากให้ $u = e^x, dv = x dx$ จะได้ $\\frac{1}{2}x^2 e^x - \\int \\frac{1}{2}x^2 e^x dx$ พจน์ใหม่ดีกรีเพิ่มเป็น $x^2$ ซับซ้อนกว่าเดิมและวนลูป!
                  </p>
                </div>
              </div>
            </div>
            <div>
""" + web_frame_img("screenshot-substitution-full.png", "โมดูลเทคนิคการอินทิเกรต", "หน้าจอเว็บแอปจริง · การแทนค่าตัวแปรและ By Parts", max_height="390px") + """
            </div>
          </div>""",
    "18 / 34",
    "ขวัญเรือน"
)

# --- 2.1.5 พื้นที่ระหว่างเส้นโค้ง ---
S19 = slide(
    "2.1.5 ทฤษฎี · พื้นที่ระหว่างเส้นโค้ง",
    "นิยามพื้นที่ปิดล้อม และขั้นตอนวิธีแยกอินทิเกรตตามจุดตัดสลับระนาบ",
    """          <div class="grid-2">
            <div class="academic-card">
              <div class="card-heading">นิยามพื้นที่ทางเรขาคณิต</div>
              <p style="font-size:0.84rem; color:var(--text-secondary); margin-top:0.35rem;">
                กำหนดให้ $f(x)$ และ $g(x)$ เป็นฟังก์ชันต่อเนื่องบน $[a, b]$ พื้นที่ของบริเวณปิดล้อมคือ:
              </p>
              <div class="math-box" style="font-size:0.82rem;">$$A = \\int_a^b |f(x) - g(x)|\\,dx$$</div>
              <p style="font-size:0.84rem; color:var(--text-secondary); margin-top:0.35rem;">
                <strong>ทำไมต้องมีค่าสัมบูรณ์:</strong> หากเส้นโค้งตัดกันสลับบน-ล่าง การอินทิเกรตตรง ๆ โดยไม่ใส่ค่าสัมบูรณ์จะทำให้พื้นที่ส่วนบวกและลบ <strong>หักล้างกันจนตอบ 0</strong>
              </p>
            </div>
            <div class="academic-card">
              <div class="card-heading">ขั้นตอนวิธีคำนวณ 4 ขั้นของระบบ</div>
              <ol style="font-size:0.82rem; color:var(--text-secondary); margin-top:0.35rem; padding-left:1.1rem; line-height:1.7;">
                <li><strong>หาจุดตัดทั้งหมด:</strong> แก้สมการ $f(x) - g(x) = 0$ บนช่วง $[a, b]$</li>
                <li><strong>แบ่งช่วงย่อย:</strong> ใช้จุดตัดแบ่งช่วงเพื่อระบุว่าช่วงใด $f \\ge g$ หรือ $g \\ge f$</li>
                <li><strong>คำนวณพื้นที่ย่อย:</strong> $\\int_{x_i}^{x_{i+1}} (y_{\\text{บน}} - y_{\\text{ล่าง}})\\,dx$</li>
                <li><strong>รวมผลลัพธ์สุทธิ:</strong> รวมพื้นที่ของทุกช่วงย่อยเข้าด้วยกัน</li>
              </ol>
            </div>
          </div>""",
    "19 / 34",
    "เบญจกัฬยาณี"
)

S20 = slide(
    "2.1.5 ตัวอย่าง · พื้นที่ปิดล้อมและจุดตัดสลับระนาบ",
    "ตัวอย่างที่ 2.10 และ 2.11: การคำนวณพื้นที่จริง และภาพกราฟิกแรเงา",
    """          <div class="grid-2">
            <div class="academic-card">
              <div class="card-heading">ตัวอย่างที่ 2.10: พาราโบลากับแกน $x$ (หน้า 17)</div>
              <p style="font-size:0.83rem; color:var(--text-secondary); margin-top:0.3rem;">
                หาพื้นที่ปิดล้อมด้วย $y = 2x - x^2$ และแกน $x$ ($y=0$) บน $[0, 2]$
              </p>
              <div class="math-box" style="font-size:0.8rem;">
                $$A = \\int_0^2 (2x - x^2)\\,dx = \\left[x^2 - \\frac{x^3}{3}\\right]_0^2 = 4 - \\frac{8}{3} = \\frac{4}{3}\\ \\text{ตร.หน่วย}$$
              </div>
              <p style="font-size:0.82rem; color:var(--text-secondary); margin-top:0.35rem;">
                <strong>ตัวอย่างที่ 2.11: เส้นตรง $y=2x$ กับ $y=x^2$</strong><br>
                จุดตัดคือ $x=0, 2$ ได้พื้นที่ $A = \\int_0^2 (2x - x^2)dx = \\frac{4}{3}$ ตร.หน่วย
              </p>
              <div class="academic-card highlight" style="margin-top:0.4rem; padding:0.5rem;">
                <p style="font-size:0.81rem; color:var(--text-secondary);">
                  <strong>ตัวอย่างซับซ้อน: $\\sin x$ กับ $\\cos x$ บน $[0, 2\\pi]$:</strong> ระบบแบ่งอินทิเกรต 3 ช่วงย่อยตามจุดตัด $\\frac{\\pi}{4}$ และ $\\frac{5\\pi}{4}$ แรเงาคนละสี ทำให้ได้พื้นที่รวม $4\\sqrt{2}$ อย่างถูกต้อง
                </p>
              </div>
            </div>
            <div>
""" + web_frame_img("screenshot-area-full.png", "โมดูลพื้นที่ปิดล้อม", "หน้าจอเว็บแอปจริง · พื้นที่ระหว่างเส้นโค้งและการแรเงา", max_height="390px") + """
            </div>
          </div>""",
    "20 / 34",
    "เบญจกัฬยาณี"
)

# --- 2.1.6 ปริมาตรทรงตัน ---
S21 = slide(
    "2.1.6 ทฤษฎี · ปริมาตรทรงตันจากการหมุน",
    "วิธีจานกลม (Disk Method) และวิธีวงแหวน (Washer Method) รอบแกน $x$",
    """          <div class="grid-2">
            <div class="academic-card">
              <div class="card-heading">1. วิธีจานกลม (Disk Method)</div>
              <p style="font-size:0.84rem; color:var(--text-secondary); margin-top:0.35rem;">
                ใช้เมื่อบริเวณที่หมุนแนบชิดกับแกนหมุน โดยหน้าตัดเป็นรูปวงกลมตัน รัศมี $R(x) = f(x)$:
              </p>
              <div class="math-box" style="font-size:0.82rem;">$$V = \\pi \\int_a^b [f(x)]^2\\,dx$$</div>
              <p style="font-size:0.82rem; color:var(--text-muted); margin-top:0.35rem;">
                ที่มา: ผลบวกปริมาตรแผ่นจานทรงกระบอกบางสะสม $\\sum \\pi [f(x_i)]^2 \\Delta x$
              </p>
            </div>
            <div class="academic-card">
              <div class="card-heading">2. วิธีวงแหวน (Washer Method)</div>
              <p style="font-size:0.84rem; color:var(--text-secondary); margin-top:0.35rem;">
                ใช้เมื่อบริเวณที่หมุนมีช่องว่าง/รูกลวง เกิดรัศมีนอก $R(x)$ และรัศมีใน $r(x)$:
              </p>
              <div class="math-box" style="font-size:0.82rem;">$$V = \\pi \\int_a^b \\left([R(x)]^2 - [r(x)]^2\\right)\\,dx$$</div>
              <div class="academic-card highlight" style="margin-top:0.35rem; padding:0.5rem;">
                <p style="font-size:0.81rem; color:var(--text-secondary);">
                  <strong>จุดที่มักจำผิด:</strong> สูตรต้องเป็น $\\pi(R^2 - r^2)$ เสมอ ห้ามนำรัศมีมาลบกันก่อนยกกำลังสอง $\\pi(R - r)^2$ เด็ดขาด
                </p>
              </div>
            </div>
          </div>""",
    "21 / 34",
    "เบญจกัฬยาณี"
)

S22 = slide(
    "2.1.6 ตัวอย่าง · ปริมาตรทรงตันจากการหมุนรอบแกน $x$",
    "ตัวอย่างที่ 2.12 (วิธีจาน) และ 2.13 (วิธีวงแหวน) พร้อมภาพหน้าตัดสะสม",
    """          <div class="grid-2">
            <div class="academic-card">
              <div class="card-heading">ตัวอย่างที่ 2.12: วิธีจาน (เล่มหน้า 19)</div>
              <p style="font-size:0.82rem; color:var(--text-secondary); margin-top:0.25rem;">
                หมุนบริเวณใต้กราฟ $y = \\sqrt{x}$ จาก $x = 0$ ถึง $4$ รอบแกน $x$
              </p>
              <div class="math-box" style="font-size:0.78rem;">
                $$V = \\pi \\int_0^4 (\\sqrt{x})^2\\,dx = \\pi \\int_0^4 x\\,dx = \\pi\\left[\\frac{x^2}{2}\\right]_0^4 = 8\\pi\\ \\text{ลบ.หน่วย}$$
              </div>
              <div class="card-heading" style="margin-top:0.4rem;">ตัวอย่างที่ 2.13: วิธีวงแหวน (เล่มหน้า 20)</div>
              <p style="font-size:0.82rem; color:var(--text-secondary); margin-top:0.25rem;">
                หมุนบริเวณปิดล้อมด้วย $y = x$ และ $y = x^2$ รอบแกน $x$ ($R=x, r=x^2$)
              </p>
              <div class="math-box" style="font-size:0.78rem;">
                $$V = \\pi \\int_0^1 (x^2 - x^4)\\,dx = \\pi\\left[\\frac{x^3}{3} - \\frac{x^5}{5}\\right]_0^1 = \\frac{2\\pi}{15}\\ \\text{ลบ.หน่วย}$$
              </div>
              <div class="academic-card highlight" style="margin-top:0.4rem; padding:0.5rem;">
                <p style="font-size:0.81rem; color:var(--text-secondary);">
                  ระบบจะวาดภาพแว่นวงแหวนโปร่งใสซ้อนทับกัน ช่วยให้ผู้เรียนมองเห็นมโนทัศน์ของความหนา $\\Delta x$ กลายเป็นปริมาตรทรงตัน 3 มิติ
                </p>
              </div>
            </div>
            <div>
""" + web_frame_img("screenshot-volume-full.png", "โมดูลปริมาตรทรงตัน", "หน้าจอเว็บแอปจริง · ปริมาตรทรงตันจากการหมุนรอบแกน x", max_height="390px") + """
            </div>
          </div>""",
    "22 / 34",
    "เบญจกัฬยาณี"
)

# --- 2.1.7 ปริพันธ์ไม่ตรงแบบ ---
S23 = slide(
    "2.1.7 ทฤษฎี · ปริพันธ์ไม่ตรงแบบ",
    "การจำแนกชนิดที่ 1 (ขอบเขตอนันต์) และชนิดที่ 2 (จุดเอกฐาน/หารด้วยศูนย์)",
    """          <div class="grid-2">
            <div class="academic-card">
              <div class="card-heading">ชนิดที่ 1 · ขอบเขตเป็นอนันต์ (Infinite Interval)</div>
              <p style="font-size:0.83rem; color:var(--text-secondary); margin-top:0.35rem;">
                ช่วงของการอินทิเกรตยาวถึงอนันต์ นิยามผ่านลิมิตของตัวแปร $t$:
              </p>
              <div class="math-box" style="font-size:0.8rem;">$$\\int_a^\\infty f(x)\\,dx = \\lim_{t\\to\\infty} \\int_a^t f(x)\\,dx$$</div>
              <p style="font-size:0.82rem; color:var(--text-muted); margin-top:0.3rem;">
                หากลิมิตหาค่าเป็นจำนวนจริงได้ เรียกว่า <strong>ลู่เข้า (Converges)</strong> หากหาค่าไม่ได้ เรียกว่า <strong>ลู่ออก (Diverges)</strong>
              </p>
            </div>
            <div class="academic-card">
              <div class="card-heading">ชนิดที่ 2 · มีจุดเอกฐาน (Discontinuous Integrand)</div>
              <p style="font-size:0.83rem; color:var(--text-secondary); margin-top:0.35rem;">
                ฟังก์ชันมีค่าพุ่งสู่อนันต์ ณ จุด $c \\in [a, b]$ ต้องแยกช่วงออกเป็น 2 ส่วน:
              </p>
              <div class="math-box" style="font-size:0.8rem;">$$\\int_a^b f(x)\\,dx = \\lim_{t\\to c^-}\\int_a^t f(x)\\,dx + \\lim_{s\\to c^+}\\int_s^b f(x)\\,dx$$</div>
              <div class="academic-card highlight" style="margin-top:0.35rem; padding:0.5rem;">
                <p style="font-size:0.81rem; color:var(--text-secondary);">
                  <strong>กฎความเข้มงวด:</strong> ปริพันธ์จะลู่เข้าก็ต่อเมื่อลิมิตทั้งสองส่วนหาค่าได้พร้อมกัน ห้ามนำ $\\pm\\infty$ มาหักล้างกันให้เป็นศูนย์
                </p>
              </div>
            </div>
          </div>""",
    "23 / 34",
    "เบญจกัฬยาณี"
)

S24 = slide(
    "2.1.7 ตัวอย่าง · การตรวจสอบการลู่เข้าและจุดเอกฐาน",
    "ตัวอย่างที่ 2.14 และ 2.15: ปริพันธ์ลู่เข้า vs กรณีลู่ออกที่ห้ามหักล้าง",
    """          <div class="grid-2">
            <div class="academic-card">
              <div class="card-heading">ตัวอย่างที่ 2.14: ชนิดที่ 1 (ลู่เข้าสู่ 1)</div>
              <p style="font-size:0.82rem; color:var(--text-secondary); margin-top:0.25rem;">
                จงตรวจสอบการลู่เข้าของ $\\int_1^\\infty \\frac{1}{x^2}\\,dx$
              </p>
              <div class="math-box" style="font-size:0.78rem;">
                $$\\lim_{t\\to\\infty}\\int_1^t x^{-2}dx = \\lim_{t\\to\\infty}\\left[-\\frac{1}{x}\\right]_1^t = \\lim_{t\\to\\infty}\\left(-\\frac{1}{t} + 1\\right) = 1$$
              </div>
              <div class="card-heading" style="margin-top:0.35rem;">ตัวอย่างที่ 2.15: ชนิดที่ 2 (ลู่เข้าสู่ 2)</div>
              <p style="font-size:0.82rem; color:var(--text-secondary); margin-top:0.25rem;">
                จงหาค่าของ $\\int_0^1 \\frac{1}{\\sqrt{x}}\\,dx$ (จุดเอกฐานที่ $x=0$)
              </p>
              <div class="math-box" style="font-size:0.78rem;">
                $$\\lim_{t\\to 0^+}\\int_t^1 x^{-1/2}dx = \\lim_{t\\to 0^+}\\left[2\\sqrt{x}\\right]_t^1 = 2 - 0 = 2$$
              </div>
              <div class="academic-card highlight" style="margin-top:0.4rem; padding:0.5rem;">
                <p style="font-size:0.81rem; color:var(--text-secondary);">
                  <strong>กรณี $\\int_{-1}^1 \\frac{1}{x}dx$ ลู่ออก:</strong> มีจุดเอกฐานที่ $x=0$ ลิมิตด้านซ้ายได้ $-\\infty$ ลู่ออกทันที ระบบปฏิเสธการตอบ 0 เด็ดขาด
                </p>
              </div>
            </div>
            <div>
""" + web_frame_img("screenshot-improper-full.png", "โมดูลปริพันธ์ไม่ตรงแบบ", "หน้าจอเว็บแอปจริง · ปริพันธ์ไม่ตรงแบบและการตรวจสอบการลู่เข้า", max_height="390px") + """
            </div>
          </div>""",
    "24 / 34",
    "เบญจกัฬยาณี"
)

# ============================================================================
# ACT 4: การทำงานจริง คลังแบบทดสอบ และการประกันคุณภาพ (สไลด์ 25–27, ~3 นาที)
# ============================================================================

S25 = slide(
    "4. ผลการดำเนินงาน · ความซื่อสัตย์เชิงสัญลักษณ์",
    "ระบบเลือกที่จะบอกว่า \"ทำไม่ได้\" ดีกว่าคำนวณค่าลวงออกมา",
    """          <div class="grid-2">
            <div style="display:flex; flex-direction:column; gap:0.5rem;">
              <div class="academic-card">
                <div class="card-heading">ความแม่นยำเชิงสัญลักษณ์ (SymPy CAS)</div>
                <p style="font-size:0.85rem; color:var(--text-secondary); margin-top:0.3rem;">
                  ผลลัพธ์คงรูปเศษส่วนและค่าคงตัวทางคณิตศาสตร์อย่างแท้จริง ไม่แปลงเป็นทศนิยม จึงไม่เกิดความคลาดเคลื่อนสะสมจากการปัดเศษ (Floating-point error)
                </p>
                <div class="math-box">$$\\int_0^2 (2x - x^2)\\,dx = \\frac{4}{3}\\ \\text{ตารางหน่วย}$$</div>
              </div>
              <div class="academic-card">
                <div class="card-heading">Fail-safe 4 กรณีที่ระบบปฏิเสธอย่างถูกต้อง</div>
                <ul style="font-size:0.82rem; color:var(--text-secondary); margin-top:0.3rem; padding-left:1.1rem; line-height:1.65;">
                  <li>ลิมิตซ้ายและขวาไม่เท่ากัน &rarr; รายงานสถานะ $\\text{DNE}$</li>
                  <li>จุดมุมแหลม $|x|$ ที่ $x=0$ &rarr; ปฏิเสธการวาดเส้นสัมผัสลวง</li>
                  <li>ปริพันธ์ลู่ออก &rarr; ระบุสถานะชัดเจน ไม่คืนค่าตัวเลขหักล้าง</li>
                  <li>ไม่มีปฏิยานุพันธ์ในรูปฟังก์ชันมูลฐาน &rarr; แจ้งเตือนข้อจำกัดและหยุด</li>
                </ul>
              </div>
            </div>
            <div>
""" + web_frame_img("screenshot-solver-full.png", "เครื่องคำนวณสัญลักษณ์", "หน้าจอเว็บแอปจริง · เครื่องคำนวณแคลคูลัสขั้นสูงเชิงสัญลักษณ์", max_height="390px") + """
            </div>
          </div>""",
    "25 / 34",
    "ขวัญเรือน"
)

S26 = slide(
    "4. ผลการดำเนินงาน · คลังข้อสอบและระบบคำใบ้",
    "คลังข้อสอบมโนทัศน์ 80 ข้อ พร้อมคำใบ้ 3 ระดับที่ไม่เฉลยคำตอบ",
    """          <div class="grid-2">
            <div style="display:flex; flex-direction:column; gap:0.5rem;">
              <div class="academic-card">
                <div class="card-heading">โครงสร้างแบบทดสอบมโนทัศน์</div>
                <ul style="font-size:0.83rem; color:var(--text-secondary); margin-top:0.35rem; padding-left:1.15rem; line-height:1.7;">
                  <li>ข้อสอบครอบคลุมทั้ง 7 โมดูล + Solver รวม 80 ข้อ (โมดูลละ 10 ข้อ)</li>
                  <li>ข้อคำถามเน้น **ความเข้าใจเชิงมโนทัศน์** ไม่ใช่การคิดเลขถึก</li>
                  <li>ระบบคำใบ้ 3 ระดับ: ทบทวนนิยาม &rarr; จัดรูปโจทย์ &rarr; ชี้จุดลวง</li>
                  <li>สุ่มสลับตำแหน่งตัวเลือก (Shuffle) ทุกครั้งที่ทำ</li>
                </ul>
              </div>
              <div class="academic-card">
                <div class="card-heading">การดักจับจุดเข้าใจผิด (Distractor Analysis)</div>
                <ul style="font-size:0.81rem; color:var(--text-secondary); margin-top:0.3rem; padding-left:1.1rem; line-height:1.65;">
                  <li>ลืมใส่ค่าสัมบูรณ์ใน $\\int \\frac{1}{x}dx = \\ln|x| + C$</li>
                  <li>จำสูตรวงแหวนผิดเป็น $\\pi(R - r)^2$</li>
                  <li>ลืมเปลี่ยนขอบเขตตัวแปรในการแทนค่า $u$</li>
                  <li>คิดว่า $\\frac{0}{0}$ ตอบ 0 หรือ 1 หรือหาค่าไม่ได้ทันที</li>
                </ul>
              </div>
            </div>
            <div>
""" + web_frame_img("screenshot-quiz-full.png", "หน้าจอแบบทดสอบ", "หน้าจอเว็บแอปจริง · คลังแบบทดสอบมโนทัศน์ 80 ข้อและระบบคำใบ้ 3 ระดับ", max_height="390px") + """
            </div>
          </div>""",
    "26 / 34",
    "เบญจกัฬยาณี"
)

S27 = slide(
    "4. ผลการดำเนินงาน · ความถูกต้องทางเทคนิค",
    "หลักฐานการทดสอบ: 265 กรณีหน่วยย่อย, 144 กรณีขอบเขต, 15 หน้าจอ",
    """          <div class="grid-3">
            <div class="academic-card" style="text-align:center;">
              <div style="font-size:2.6rem; font-weight:700; color:var(--primary-blue);">265</div>
              <div class="card-heading" style="justify-content:center;">Pytest (ผ่าน 100%)</div>
              <p style="font-size:0.84rem; color:var(--text-secondary); margin-top:0.3rem;">
                ทดสอบอัตโนมัติคลุมทุก Solver และตัวแปลงทางคณิตศาสตร์
              </p>
            </div>
            <div class="academic-card" style="text-align:center;">
              <div style="font-size:2.6rem; font-weight:700; color:var(--primary-blue);">144</div>
              <div class="card-heading" style="justify-content:center;">Boundary Cases</div>
              <p style="font-size:0.84rem; color:var(--text-secondary); margin-top:0.3rem;">
                กรณีขอบเขตวิกฤต จำแนกสิ่งที่รองรับและสิ่งที่ปฏิเสธ
              </p>
            </div>
            <div class="academic-card" style="text-align:center;">
              <div style="font-size:2.6rem; font-weight:700; color:var(--primary-blue);">15</div>
              <div class="card-heading" style="justify-content:center;">หน้าจอระบบ</div>
              <p style="font-size:0.84rem; color:var(--text-secondary); margin-top:0.3rem;">
                ทดสอบเสมือนจริงบนเบราว์เซอร์ ไม่พบ JavaScript error
              </p>
            </div>
          </div>
          <div class="academic-card highlight">
            <div class="card-heading">ข้อจำกัดของการตีความผลทดสอบนี้</div>
            <p style="font-size:0.88rem; color:var(--text-secondary); margin-top:0.35rem;">
              การทดสอบผ่านพิสูจน์ว่า <strong>กรณีที่ประกาศรองรับทำงานถูกต้อง</strong> และ
              <strong>กรณีที่อยู่นอกขอบเขตถูกปฏิเสธอย่างชัดเจน</strong>
              แต่ไม่ได้พิสูจน์ว่าถูกต้องสำหรับทุกอินพุตที่เป็นไปได้ เราจึงไม่กล่าวอ้างความถูกต้องแบบสากล
            </p>
          </div>""",
    "27 / 34",
    "ขวัญเรือน"
)

# ============================================================================
# ACT 5: ผลการประเมินและการวิเคราะห์ผู้ใช้จริง (สไลด์ 28–31, ~3.5 นาที)
# ============================================================================

S28 = slide(
    "5. ผลการประเมิน · ระเบียบวิธีและกลุ่มตัวอย่าง",
    "ประเมินกับผู้ใช้จริง 50 คน ด้วยเครื่องมือมาตรฐาน 2 ชุด",
    """          <div class="grid-2">
            <div class="academic-card">
              <div class="card-heading">กลุ่มตัวอย่าง ($N = 50$)</div>
              <p style="font-size:0.86rem; color:var(--text-secondary); margin-top:0.4rem;">
                บันทึกผล ณ วันที่ 30 ตุลาคม 2569 เวลา 10:15 น. รวม <strong>$N = 50$ คน</strong>
              </p>
              <ul style="font-size:0.84rem; color:var(--text-secondary); margin-top:0.4rem; padding-left:1.1rem; line-height:1.7;">
                <li>ปริญญาตรีปี 3–4 <strong>74%</strong> · ปี 1–2 16% · บัณฑิตศึกษา 6%</li>
                <li>กำลังเรียนแคลคูลัส 30% · เคยสอบผ่านแล้ว 46%</li>
                <li>อุปกรณ์: แท็บเล็ต 40% · คอมพิวเตอร์ 34% · สมาร์ตโฟน 26%</li>
                <li>สังกัด: มก. กำแพงแสน 36%, ศิลปากร 24%, มรภ.ธนบุรี 12%, อื่น ๆ 28%</li>
              </ul>
            </div>
            <div class="academic-card">
              <div class="card-heading">เครื่องมือวัด 2 ชุด</div>
              <div style="font-size:0.86rem; color:var(--text-secondary); margin-top:0.4rem; line-height:1.7;">
                <p><strong>ชุดที่ 1 · ความพึงพอใจ 4 ด้าน (20 ข้อ)</strong><br>
                มาตรประมาณค่า 5 ระดับ: UI/UX, ฟังก์ชันโต้ตอบ, เนื้อหามโนทัศน์, เจตคติและแรงจูงใจ</p>
                <p style="margin-top:0.5rem;"><strong>ชุดที่ 2 · System Usability Scale (10 ข้อ)</strong><br>
                ฉบับปรับปรุงข้อคำถามเป็นเชิงบวก (Sauro &amp; Lewis, 2011) เพื่อลดความสับสนของผู้ตอบไทย</p>
              </div>
            </div>
          </div>
          <p style="font-size:0.85rem; color:var(--text-muted); margin-top:0.3rem;">
            การเลือกกลุ่มตัวอย่างเป็นแบบตามสะดวก (Convenience Sampling) ซึ่งเป็นข้อจำกัดที่ระบุไว้ในบทที่ 5
          </p>""",
    "28 / 34",
    "เบญจกัฬยาณี"
)

S29 = slide(
    "5. ผลการประเมิน · ความพึงพอใจของผู้ใช้งาน",
    "ภาพรวมอยู่ในระดับมากที่สุด 4.63 จาก 5.00 ($S.D. = 0.58$)",
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
                คะแนนสูงสุดคือด้าน <strong>เจตคติและแรงจูงใจ (4.67)</strong> ซึ่งสอดคล้องกับสมมติฐานว่า
                การเห็นภาพและการทดลองช่วยลดความวิตกกังวลต่อวิชาแคลคูลัส
              </p>
              <p style="font-size:0.86rem; color:var(--text-secondary); margin-top:0.5rem;">
                แต่คะแนนนี้คือ <strong>การรับรู้ของผู้เรียน (Perceived)</strong>
                ไม่ใช่หลักฐานว่าผลสัมฤทธิ์ทางการเรียนสูงขึ้น ซึ่งต้องใช้การทดลอง Pre/Post-test ในงานวิจัยขั้นต่อไป
              </p>
              <div class="math-box">$$\\bar{x} = 4.63,\\quad S.D. = 0.58,\\quad N = 50$$</div>
            </div>
          </div>""",
    "29 / 34",
    "เบญจกัฬยาณี"
)

S30 = slide(
    "5. ผลการประเมิน · ความสะดวกในการใช้งาน (SUS)",
    "SUS 82.15 (Grade A) และการอ่านผลอย่างโปร่งใส ($n=29$ ได้ 73.53)",
    """          <div class="grid-2">
            <div class="academic-card">
              <div class="card-heading">คะแนนรวม ($N = 50$)</div>
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
                <li>พบการกาดิ่ง (ตอบคะแนนเท่ากันทุกข้อ) <strong>21 คน คิดเป็น 42%</strong></li>
                <li>เมื่อแยกกลุ่มที่มีการกระจายคะแนนตามธรรมชาติ ($n=29$)
                    คะแนนเฉลี่ยอยู่ที่ <strong>73.53</strong> ($S.D.=15.95$)</li>
                <li>ยังคงอยู่ในระดับ <strong>Grade B (Good)</strong> และสูงกว่าเกณฑ์ 68.0</li>
              </ul>
              <p style="font-size:0.84rem; color:var(--text-secondary); margin-top:0.5rem;">
                เรารายงานทั้งสองค่าในบทที่ 4 และบทคัดย่อ เพื่อความโปร่งใสทางวิชาการ
              </p>
            </div>
          </div>""",
    "30 / 34",
    "เบญจกัฬยาณี"
)

S31 = slide(
    "6. ข้อคิดเห็นและ Demand ของผู้เรียน",
    "สี่ข้อกังวลที่ผู้เรียนสะท้อน และความต้องการหัวข้อเพิ่มเติม",
    """          <div class="grid-2">
            <table class="table-academic">
              <thead>
                <tr><th>หัวข้อที่ต้องการเพิ่ม</th><th>จำนวน</th><th>ร้อยละ</th></tr>
              </thead>
              <tbody>
                <tr><td>อินทิเกรตทีละส่วน (By Parts)</td><td>29</td><td>58.0%</td></tr>
                <tr><td>แยกเศษส่วนย่อย (Partial Fractions)</td><td>25</td><td>50.0%</td></tr>
                <tr><td>แทนค่าฟังก์ชันตรีโกณมิติ</td><td>22</td><td>44.0%</td></tr>
                <tr><td>แบบจำลอง 3 มิติสำหรับการหมุน</td><td>21</td><td>42.0%</td></tr>
              </tbody>
            </table>
            <div class="academic-card">
              <div class="card-heading">ข้อกังวลที่ผู้เรียนสะท้อน</div>
              <ul style="font-size:0.84rem; color:var(--text-secondary); margin-top:0.4rem; padding-left:1.15rem; line-height:1.7;">
                <li><strong>โทนสีสดใส:</strong> เลือกใช้สไตล์ Bauhaus เพื่อลดความเครียด สอดคล้องกับเจตคติ 4.67</li>
                <li><strong>ตัวหนังสือเยอะ:</strong> ยืนยันว่าระบบเป็นห้องทดลอง ไม่ใช่เครื่องแจกคำตอบ</li>
                <li><strong>จอมือถือ:</strong> วางแผนปรับ Responsive สำหรับมือถือในรุ่นถัดไป</li>
              </ul>
            </div>
          </div>""",
    "31 / 34",
    "เบญจกัฬยาณี"
)

# ============================================================================
# ACT 6: ข้อจำกัด แถลง Errata บทสรุป และถาม-ตอบ (สไลด์ 32–34, ~2 นาที)
# ============================================================================

S32 = slide(
    "7. ข้อจำกัดและการแถลง Errata เล่มส่งกรรมการ",
    "การตรวจสอบตนเองอย่างซื่อสัตย์ และรายการ Errata",
    """          <div class="grid-2">
            <div class="academic-card">
              <div class="card-heading">ข้อจำกัดทางคณิตศาสตร์ที่ค้นพบ</div>
              <ul style="font-size:0.84rem; color:var(--text-secondary); margin-top:0.4rem; padding-left:1.1rem; line-height:1.75;">
                <li>ฟังก์ชันไม่มีปฏิยานุพันธ์มูลฐาน ($e^{-x^2}, \\frac{\\sin x}{x}$) ระบบแจ้งเตือนหยุดคำนวณ</li>
                <li>ปริมาตรทรงตันรองรับการหมุนรอบแกน $x$ เท่านั้น</li>
                <li>ฟังก์ชันกวัดแกว่งรุนแรง ($\\sin\\frac{1}{x}$) แสดงสถานะ DNE ถูกต้องแต่กราฟอาจเกิด Aliasing</li>
              </ul>
            </div>
            <div class="academic-card">
              <div class="card-heading">ใบบันทึก Errata เล่มส่งกรรมการ (120 หน้า)</div>
              <ul style="font-size:0.84rem; color:var(--text-secondary); margin-top:0.4rem; padding-left:1.1rem; line-height:1.75;">
                <li><strong>ภาคผนวก ง (หน้า 95–104):</strong> เฉลยเป็น ก ทั้ง 16 ข้อ เกิดจาก JSON dump สล็อตแรก (มีตารางเฉลยสลับ 4:4:4:4 แนบมาด้วย)</li>
                <li><strong>สารบัญภาพ:</strong> เลขหน้าภาพที่ 12 คลาดเคลื่อน 2 หน้าจากการแทรก QR Code เว็บจริง</li>
                <li><strong>บรรณานุกรม [6]–[14]:</strong> เป็นเอกสารเครื่องมือ จะเติม In-text ในบทที่ 2 หลังสอบ</li>
              </ul>
            </div>
          </div>""",
    "32 / 34",
    "นำเสนอร่วมกัน"
)

S33 = slide(
    "8. ข้อเสนอแนะและบทสรุป",
    "แนวทางต่อยอด 3 ด้าน และการตอบโจทย์วัตถุประสงค์ทั้ง 5 ข้อ",
    """          <div class="grid-3">
            <div class="academic-card">
              <div class="card-heading">ด้านเนื้อหา</div>
              <p style="font-size:0.84rem; color:var(--text-secondary); margin-top:0.4rem;">
                เพิ่ม By Parts (58%) และ Partial Fractions (50%) พร้อมวิธีเปลือกทรงกระบอก (Cylindrical Shells)
              </p>
            </div>
            <div class="academic-card">
              <div class="card-heading">ด้านประสบการณ์ผู้ใช้</div>
              <p style="font-size:0.84rem; color:var(--text-secondary); margin-top:0.4rem;">
                ปรับระบบ Responsive ให้ลื่นไหลบนมือถือ 100% และเพิ่มโมเดล 3D WebGL สำหรับการหมุนทรงตัน
              </p>
            </div>
            <div class="academic-card">
              <div class="card-heading">ด้านการวิเคราะห์การเรียนรู้</div>
              <p style="font-size:0.84rem; color:var(--text-secondary); margin-top:0.4rem;">
                เชื่อมต่อฐานข้อมูลเก็บ Log การทำแบบทดสอบเพื่อวัดผลสัมฤทธิ์ Pre/Post-test อย่างเป็นทางการ
              </p>
            </div>
          </div>
          <div class="academic-card highlight" style="margin-top:0.5rem;">
            <p style="font-size:0.9rem; color:var(--text-secondary);">
              <strong>ตอบวัตถุประสงค์ครบ 5 ข้อ:</strong> เว็บแอป 15 หน้าใช้งานได้จริง &bull; ครบ 7 โมดูล &bull; SymPy คำนวณถูกต้องผ่านการทดสอบ 265 ข้อ &bull; ป้องกัน Misconceptions ด้วยคำใบ้ &bull; ประเมินความพึงพอใจ 4.63 และ SUS 73.53 (Good)
            </p>
          </div>""",
    "33 / 34",
    "เบญจกัฬยาณี"
)

S34 = """      <div class="slide">
        <div class="slide-header">
          <div>
            <div class="section-label">ขอขอบพระคุณคณะกรรมการทุกท่าน</div>
            <div class="main-title" style="font-size:2.2rem; margin-top:0.5rem;">ขอบพระคุณค่ะ / พร้อมรับฟังข้อซักถาม</div>
            <p style="font-size:1.05rem; color:var(--text-secondary); margin-top:0.8rem;">
              Calculus Learning Sandbox &bull; โครงงานคณิตศาสตร์ประยุกต์ 2569
            </p>
          </div>
          <div class="slide-counter-chip">34 / 34</div>
        </div>
        <div class="slide-body">
          <div class="grid-3">
            <div class="academic-card" style="text-align:center;">
              <div class="card-heading" style="justify-content:center;">เว็บแอปพลิเคชันจริง</div>
              <a href='""" + APP_URL + """' target="_blank" rel="noopener"
                 style="font-size:0.78rem; color:var(--primary-blue); word-break:break-all; display:block; margin-top:0.4rem;">
                calculus-integration-app.streamlit.app
              </a>
              <img src='""" + img_b64('calculus-app-qr.png') + """' alt="QR Code" style="width:110px; height:110px; margin-top:0.5rem; border:1.5px solid var(--ink); border-radius:8px; padding:3px; background:#fff; cursor:zoom-in;" onclick="openLightboxModal(this.src, 'QR Code เข้าใช้งานระบบ')">
            </div>
            <div class="academic-card">
              <div class="card-heading">ซอร์สโค้ดและรายงาน</div>
              <p style="font-size:0.84rem; color:var(--text-secondary); margin-top:0.4rem; line-height:1.7;">
                <strong>GitHub:</strong> SubwatG/calculus-integration-app<br>
                <strong>เล่มรายงาน:</strong> ฉบับส่งกรรมการ (120 หน้า)<br>
                <strong>เอกสารประกอบ:</strong> ใบบันทึก Errata, สเปกสไลด์ 34 หน้า, คู่มือ Q&A 22 ข้อ, ชีตสรุปโค้ดดิ้ง
              </p>
            </div>
            <div class="academic-card">
              <div class="card-heading">คณะผู้วิจัย</div>
              <p style="font-size:0.84rem; color:var(--text-secondary); margin-top:0.4rem; line-height:1.7;">
                ขวัญเรือน สำเนียงดี (แอร์)<br>
                เบญจกัฬยาณี พิทยากูล (ชิชา)<br>
                อ.ดร.กิตติพงศ์ ทรัพย์วัฒนาชัย (ที่ปรึกษา)
              </p>
            </div>
          </div>
          <div class="academic-card highlight" style="text-align:center; margin-top:0.5rem;">
            <p style="font-size:0.95rem; color:var(--text-secondary);">
              ช่วงตอบข้อซักถามและรับฟังข้อเสนอแนะจากคณะกรรมการ
            </p>
          </div>
        </div>
      </div>"""

SLIDES = [
    S01, S02, S03, S04, S05, S06,
    S07, S08, S09, S10,
    S11, S12, S13, S14, S15, S16, S17, S18, S19, S20, S21, S22, S23, S24,
    S25, S26, S27,
    S28, S29, S30, S31,
    S32, S33, S34
]

# ----------------------------------------------------------------------------
# 4. ประกอบไฟล์ HTML
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
<title>การนำเสนอโครงงาน | Calculus Learning Sandbox (สอบป้องกันโครงงาน)</title>

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
    <span>สาขาวิชาคณิตศาสตร์ประยุกต์ &bull; ภาควิชาวิทยาการคำนวณและเทคโนโลยีดิจิทัล</span>
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
    Slide 1 of 34
  </div>
</div>

<!-- Modal Overview Grid -->
<div class="modal-overlay" id="modalOverlay" onclick="toggleOverview()">
  <div class="grid-thumbs" onclick="event.stopPropagation()">
    <!-- Populated by JS -->
  </div>
</div>


<!-- Lightbox Image Modal -->
<div id="imageLightboxModal" class="modal-overlay" onclick="closeLightboxModal()" style="display:none; z-index:1000; align-items:center; justify-content:center;">
  <div style="position:relative; max-width:94vw; max-height:94vh; display:flex; flex-direction:column; align-items:center;" onclick="event.stopPropagation()">
    <div style="display:flex; justify-content:space-between; align-items:center; width:100%; margin-bottom:8px;">
      <div id="lightboxCaption" style="color:#ffffff; font-size:1.05rem; font-weight:600; text-shadow:0 1px 4px rgba(0,0,0,0.8);"></div>
      <button onclick="closeLightboxModal()" style="background:var(--rose); color:#ffffff; border:1.5px solid #000; border-radius:6px; padding:6px 14px; font-weight:700; cursor:pointer; font-family:'Outfit', sans-serif;">✕ ปิด (Close)</button>
    </div>
    <div style="max-height:85vh; overflow:auto; background:#ffffff; border:2px solid #000; border-radius:8px; box-shadow:0 10px 40px rgba(0,0,0,0.6);">
      <img id="lightboxImg" src="" style="width:100%; height:auto; display:block;">
    </div>
  </div>
</div>

<script>{nav_js}</script>

</body>
</html>
"""


OUT_PDF_PATH = HERE / "slide-deck-defense.pdf"


def export_pdf(html_path: Path, pdf_path: Path) -> bool:
    import shutil
    import subprocess

    browser_candidates = [
        Path(r"C:\Program Files\Google\Chrome\Application\chrome.exe"),
        Path(r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"),
        Path(r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"),
        Path(r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"),
        Path("/usr/bin/google-chrome"),
        Path("/usr/bin/chromium"),
        Path("/usr/bin/chromium-browser"),
    ]
    browser = None
    for cand in browser_candidates:
        if cand.exists():
            browser = cand
            break
    if not browser:
        for name in ["google-chrome", "chrome", "chromium", "msedge"]:
            found = shutil.which(name)
            if found:
                browser = Path(found)
                break

    if not browser:
        print("[INFO] ข้ามการสร้าง PDF (ไม่พบ Chrome/Edge หรือ Chromium)")
        return False

    cmd = [
        str(browser),
        "--headless=new",
        "--disable-gpu",
        "--no-pdf-header-footer",
        f"--print-to-pdf={pdf_path.resolve()}",
        str(html_path.resolve()),
    ]
    try:
        subprocess.run(cmd, capture_output=True, text=True, timeout=40)
        if pdf_path.exists():
            print(f"[OK] สร้าง PDF: {pdf_path}")
            print(f"     size: {pdf_path.stat().st_size:,} bytes")
            return True
    except Exception as e:
        print(f"[WARN] เกิดข้อผิดพลาดในการสร้าง PDF: {e}")
    return False


def main() -> None:
    if not PROPOSAL_DECK.exists():
        sys.exit(f"[ERROR] ไม่พบ deck ต้นทาง: {PROPOSAL_DECK}")

    html = build()
    OUT_PATH.write_text(html, encoding="utf-8")

    slide_count = len(re.findall(r'<div class="slide">', html))
    print(f"[OK] เขียนไฟล์: {OUT_PATH}")
    print(f"     slides: {slide_count}")
    print(f"     size: {OUT_PATH.stat().st_size:,} bytes")

    if slide_count != 34:
        sys.exit(f"[ERROR] จำนวนสไลด์ไม่ครบ 34 (ได้ {slide_count})")

    export_pdf(OUT_PATH, OUT_PDF_PATH)


if __name__ == "__main__":
    main()
