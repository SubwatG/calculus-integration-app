import streamlit as st
from utils.theme import render_hero

render_hero(
    "👩‍🎓 ประวัติคณะผู้จัดทำและอาจารย์ที่ปรึกษา (Creators & Advisor) ✨",
    "✨ คณะผู้พัฒนาเว็บแอปพลิเคชันช่วยเรียนรู้แคลคูลัสแบบมีปฏิสัมพันธ์ (Calculus Learning Sandbox) • ภาควิชาวิทยาการคำนวณและเทคโนโลยีดิจิทัล มก. กำแพงแสน 🌾",
)

st.markdown(
    """
    <style>
    .creators-intro-banner {
        background: linear-gradient(135deg, #FEF08A 0%, #FBCFE8 50%, #BAE6FD 100%);
        border: 2.5px solid #18181B;
        border-radius: 14px;
        padding: 14px 20px;
        box-shadow: 4px 4px 0px #18181B;
        margin-bottom: 24px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        flex-wrap: wrap;
        gap: 12px;
    }
    .creators-tag {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background-color: #FFFFFF;
        border: 1.5px solid #18181B;
        border-radius: 999px;
        padding: 5px 14px;
        font-family: 'Fredoka', 'Mali', sans-serif;
        font-size: 13px;
        font-weight: 700;
        color: #18181B;
        box-shadow: 2px 2px 0px #18181B;
    }
    .creator-card-unified {
        background: linear-gradient(150deg, #FFFFFF 0%, #FEFCE8 100%);
        border: 2.5px solid #18181B;
        border-radius: 16px;
        padding: 22px 24px;
        box-shadow: 4px 4px 0px #18181B;
        margin-bottom: 20px;
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        transition: all 0.18s cubic-bezier(0.34, 1.56, 0.64, 1);
    }
    .creator-card-unified:hover {
        transform: translate(-3px, -3px);
        box-shadow: 6px 6px 0px #18181B;
    }
    .avatar-badge-unified {
        width: 52px;
        height: 52px;
        background: #FFFFFF;
        border: 2px solid #18181B;
        box-shadow: 2px 2px 0px #18181B;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 26px;
        flex-shrink: 0;
    }
    .creator-badge {
        display: inline-block;
        background-color: #FEF08A;
        border: 1.5px solid #18181B;
        border-radius: 999px;
        padding: 4px 14px;
        font-family: 'Fredoka', 'Mali', sans-serif;
        font-size: 13px;
        font-weight: 700;
        color: #18181B;
        box-shadow: 1.5px 1.5px 0px #18181B;
    }
    .creator-name {
        font-family: 'Fredoka', 'Mali', sans-serif;
        font-size: 1.25rem;
        font-weight: 700;
        color: #18181B;
        margin: 0 0 4px 0;
        line-height: 1.35;
    }
    .creator-sub {
        font-family: 'Mali', sans-serif;
        font-size: 0.95rem;
        font-weight: 600;
        color: #D97706;
        margin: 0 0 10px 0;
    }
    .creator-desc {
        font-family: 'Mali', sans-serif;
        font-size: 0.92rem;
        color: #374151;
        line-height: 1.65;
        margin: 0;
    }
    .advisor-card {
        background: linear-gradient(150deg, #FFFFFF 0%, #FEFCE8 100%);
        border: 2.5px solid #18181B;
        border-radius: 16px;
        padding: 22px 26px;
        box-shadow: 4px 4px 0px #18181B;
        margin-top: 8px;
        margin-bottom: 24px;
        transition: all 0.18s cubic-bezier(0.34, 1.56, 0.64, 1);
    }
    .advisor-card:hover {
        transform: translate(-3px, -3px);
        box-shadow: 6px 6px 0px #18181B;
    }
    .skill-pill {
        display: inline-flex;
        align-items: center;
        gap: 5px;
        background-color: #FFFFFF;
        border: 1.5px solid #18181B;
        border-radius: 999px;
        padding: 3px 11px;
        font-family: 'Fredoka', 'Mali', sans-serif;
        font-size: 12px;
        font-weight: 700;
        color: #18181B;
        box-shadow: 1.5px 1.5px 0px #18181B;
        margin: 2px 3px 2px 0;
    }
    .pill-pink { background-color: #FCE7F3; }
    .pill-yellow { background-color: #FEF08A; }
    .pill-blue { background-color: #BAE6FD; }
    .pill-green { background-color: #BBF7D0; }
    .pill-purple { background-color: #E9D5FF; }
    .pill-orange { background-color: #FED7AA; }

    .bento-card {
        background: #FFFFFF;
        border: 2.5px solid #18181B;
        border-radius: 14px;
        padding: 18px 20px;
        box-shadow: 3.5px 3.5px 0px #18181B;
        height: 100%;
        transition: all 0.18s cubic-bezier(0.34, 1.56, 0.64, 1);
    }
    .bento-card:hover {
        transform: translate(-2px, -2px);
        box-shadow: 5px 5px 0px #18181B;
    }
    .github-link-btn {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background-color: #FEF08A !important;
        color: #18181B !important;
        border: 2px solid #18181B !important;
        padding: 9px 18px;
        border-radius: 12px;
        font-family: 'Fredoka', 'Mali', sans-serif !important;
        font-size: 13.5px;
        font-weight: 700 !important;
        text-decoration: none !important;
        box-shadow: 3px 3px 0px #18181B !important;
        transition: all 0.15s ease;
    }
    .github-link-btn:hover {
        background-color: #FDE047 !important;
        transform: translate(-2px, -2px);
        box-shadow: 4.5px 4.5px 0px #18181B !important;
        color: #18181B !important;
    }
    .github-link-btn * {
        color: #18181B !important;
        font-weight: 700 !important;
    }
    .stat-chip {
        background: #FFFFFF;
        border: 2px solid #18181B;
        border-radius: 14px;
        padding: 12px 14px;
        box-shadow: 2.5px 2.5px 0px #18181B;
        display: flex;
        align-items: center;
        gap: 12px;
        transition: all 0.15s ease;
    }
    .stat-chip:hover {
        transform: translate(-2px, -2px);
        box-shadow: 4px 4px 0px #18181B;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Cheerful Welcome Ribbon
st.markdown(
    """
    <div class="creators-intro-banner">
        <div style="display: flex; align-items: center; gap: 10px;">
            <span style="font-size: 28px;">🌾</span>
            <div>
                <span style="font-family: 'Fredoka', 'Mali', sans-serif; font-size: 15px; font-weight: 700; color: #18181B;">
                    โครงงานวิจัยระดับปริญญาตรี (Senior Capstone Project)
                </span>
                <div style="font-family: 'Mali', sans-serif; font-size: 13px; color: #4B5563; font-weight: 600;">
                    มหาวิทยาลัยเกษตรศาสตร์ วิทยาเขตกำแพงแสน
                </div>
            </div>
        </div>
        <div style="display: flex; gap: 8px; flex-wrap: wrap;">
            <span class="creators-tag">✨ Open-Access</span>
            <span class="creators-tag">📐 Interactive Calculus</span>
            <span class="creators-tag">💖 Made with Love</span>
        </div>
    </div>

    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 12px; margin-bottom: 24px;">
        <div class="stat-chip">
            <span style="font-size: 26px;">📐</span>
            <div>
                <div style="font-family: 'Outfit', 'Fredoka', sans-serif; font-size: 15.5px; font-weight: 800; color: #18181B;">7 โมดูลจำลอง</div>
                <div style="font-family: 'Mali', sans-serif; font-size: 12px; color: #4B5563;">Interactive Geometry</div>
            </div>
        </div>
        <div class="stat-chip">
            <span style="font-size: 26px;">💡</span>
            <div>
                <div style="font-family: 'Outfit', 'Fredoka', sans-serif; font-size: 15.5px; font-weight: 800; color: #18181B;">80 ข้อแบบทดสอบ</div>
                <div style="font-family: 'Mali', sans-serif; font-size: 12px; color: #4B5563;">มีคำใบ้ 2 ระดับ & สุ่มตัวเลือก</div>
            </div>
        </div>
        <div class="stat-chip">
            <span style="font-size: 26px;">🧮</span>
            <div>
                <div style="font-family: 'Outfit', 'Fredoka', sans-serif; font-size: 15.5px; font-weight: 800; color: #18181B;">SymPy CAS Engine</div>
                <div style="font-family: 'Mali', sans-serif; font-size: 12px; color: #4B5563;">แจกแจงวิธีทำทีละขั้น</div>
            </div>
        </div>
        <div class="stat-chip">
            <span style="font-size: 26px;">💖</span>
            <div>
                <div style="font-family: 'Outfit', 'Fredoka', sans-serif; font-size: 15.5px; font-weight: 800; color: #18181B;">100% Open Access</div>
                <div style="font-family: 'Mali', sans-serif; font-size: 12px; color: #4B5563;">เพื่อการศึกษาไทยทุกคน</div>
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("### 👩‍🎓 คณะผู้จัดทำโครงงาน (Project Creators)")

col1, col2 = st.columns(2)

with col1:
    st.markdown(
        """
        <div class="creator-card-unified">
            <div>
                <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 12px;">
                    <span class="creator-badge" style="margin-bottom: 0;">💻 ผู้พัฒนาโครงงาน</span>
                    <div class="avatar-badge-unified">👩🏻‍💻</div>
                </div>
                <h4 class="creator-name">นางสาวเบญจกัฬยาณี พิทยากูล</h4>
                <div class="creator-sub">นิสิตระดับปริญญาตรี • สาขาวิชาคณิตศาสตร์ประยุกต์</div>
                <div style="height: 1.5px; background: #E4E4E7; margin: 10px 0 12px 0;"></div>
                <p class="creator-desc">
                    • <b>ภาควิชา:</b> วิทยาการคำนวณและเทคโนโลยีดิจิทัล<br>
                    • <b>คณะ:</b> ศิลปศาสตร์และวิทยาศาสตร์<br>
                    • <b>สถาบัน:</b> มหาวิทยาลัยเกษตรศาสตร์ วิทยาเขตกำแพงแสน
                </p>
                <div style="display: flex; flex-wrap: wrap; gap: 6px; margin-top: 12px;">
                    <span class="skill-pill pill-yellow">🌾 KU KPS</span>
                    <span class="skill-pill pill-blue">💻 วท.บ. คณิตศาสตร์ประยุกต์</span>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col2:
    st.markdown(
        """
        <div class="creator-card-unified">
            <div>
                <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 12px;">
                    <span class="creator-badge" style="margin-bottom: 0;">🌸 ผู้พัฒนาโครงงาน</span>
                    <div class="avatar-badge-unified">👩🏻‍💻</div>
                </div>
                <h4 class="creator-name">นางสาวขวัญเรือน สำเนียงดี</h4>
                <div class="creator-sub">นิสิตระดับปริญญาตรี • สาขาวิชาคณิตศาสตร์ประยุกต์</div>
                <div style="height: 1.5px; background: #E4E4E7; margin: 10px 0 12px 0;"></div>
                <p class="creator-desc">
                    • <b>ภาควิชา:</b> วิทยาการคำนวณและเทคโนโลยีดิจิทัล<br>
                    • <b>คณะ:</b> ศิลปศาสตร์และวิทยาศาสตร์<br>
                    • <b>สถาบัน:</b> มหาวิทยาลัยเกษตรศาสตร์ วิทยาเขตกำแพงแสน
                </p>
                <div style="display: flex; flex-wrap: wrap; gap: 6px; margin-top: 12px;">
                    <span class="skill-pill pill-yellow">🌾 KU KPS</span>
                    <span class="skill-pill pill-pink">📐 วท.บ. คณิตศาสตร์ประยุกต์</span>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("### 👨‍🏫 อาจารย์ที่ปรึกษาโครงงาน (Project Advisor)")

st.markdown(
    """
    <div class="advisor-card">
        <div style="display: flex; align-items: center; gap: 20px; flex-wrap: wrap;">
            <div class="avatar-badge-unified" style="width: 60px; height: 60px; font-size: 30px; background: #FFFFFF;">👨🏻‍🏫</div>
            <div style="flex: 1; min-width: 250px;">
                <span class="creator-badge" style="background-color: #FEF08A; margin-bottom: 6px;">🎓 อาจารย์ที่ปรึกษาโครงงาน (Project Advisor)</span>
                <h4 class="creator-name" style="font-size: 1.35rem; margin: 4px 0 6px 0;">
                    อาจารย์กิตติพงษ์ ทรัพย์วัฒนาชัย
                </h4>
                <p style="font-family: 'Mali', sans-serif; font-size: 0.95rem; color: #4B5563; margin: 0; line-height: 1.6;">
                    อาจารย์ที่ปรึกษาโครงงาน • ภาควิชาวิทยาการคำนวณและเทคโนโลยีดิจิทัล<br>
                    คณะศิลปศาสตร์และวิทยาศาสตร์ มหาวิทยาลัยเกษตรศาสตร์ วิทยาเขตกำแพงแสน
                </p>
                <div style="display: flex; flex-wrap: wrap; gap: 6px; margin-top: 10px;">
                    <span class="skill-pill pill-yellow">🌾 มหาวิทยาลัยเกษตรศาสตร์</span>
                    <span class="skill-pill pill-green">💻 วิทยาการคำนวณและเทคโนโลยีดิจิทัล</span>
                </div>
            </div>
        </div>
    </div>

    <div style="
        background: linear-gradient(135deg, #FEF9C3 0%, #FFFFFF 50%, #FEF08A 100%);
        border: 2px solid #18181B;
        border-radius: 14px;
        padding: 14px 18px;
        box-shadow: 3.5px 3.5px 0px #18181B;
        margin-top: 8px;
        margin-bottom: 24px;
        display: flex;
        align-items: center;
        gap: 12px;
    ">
        <span style="font-size: 28px;">🌟</span>
        <div style="font-family: 'Mali', sans-serif; font-size: 13.5px; color: #18181B; line-height: 1.55;">
            <b>วิสัยทัศน์โครงงาน:</b> เปลี่ยนนิยามและทฤษฎีแคลคูลัสที่ซับซ้อนให้กลายเป็นภาพจำลองที่สัมผัสได้จริง เพื่อส่งเสริมความเข้าใจในระดับมโนทัศน์ (Conceptual Understanding) อย่างยั่งยืน ✨
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("### 🏛️ ข้อมูลโครงงานและวัตถุประสงค์ (Project Overview)")

bcol1, bcol2, bcol3 = st.columns(3)

with bcol1:
    st.markdown(
        """
        <div class="bento-card" style="background: linear-gradient(180deg, #FFFFFF 0%, #FFF1F2 100%);">
            <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 10px;">
                <span style="font-size: 24px;">🎯</span>
                <h4 style="font-family: 'Fredoka', 'Mali', sans-serif; font-size: 1.05rem; font-weight: 700; margin: 0; color: #E11D48;">
                    3 วัตถุประสงค์หลัก
                </h4>
            </div>
            <ul style="font-family: 'Mali', sans-serif; font-size: 0.88rem; color: #374151; line-height: 1.65; padding-left: 18px; margin: 0;">
                <li><b>1. สื่อการเรียนรู้แบบเปิด:</b> เพื่อเป็นเครื่องมือเรียนเสริมแคลคูลัสฟรี (Open-Access) ทุกที่ทุกเวลา</li>
                <li><b>2. เสริมสร้างมโนทัศน์:</b> เข้าใจแนวคิดลึกซึ้งผ่านภาพและกราฟจำลองเชิงเรขาคณิต</li>
                <li><b>3. แจกแจงวิธีทำเป็นระบบ:</b> ยกระดับทักษะการแก้โจทย์อย่างถูกต้องตามหลักคณิตศาสตร์</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )

with bcol2:
    st.markdown(
        """
        <div class="bento-card" style="background: linear-gradient(180deg, #FFFFFF 0%, #F0FDF4 100%);">
            <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 10px;">
                <span style="font-size: 24px;">🚀</span>
                <h4 style="font-family: 'Fredoka', 'Mali', sans-serif; font-size: 1.05rem; font-weight: 700; margin: 0; color: #16A34A;">
                    จุดเด่นของระบบ
                </h4>
            </div>
            <ul style="font-family: 'Mali', sans-serif; font-size: 0.88rem; color: #374151; line-height: 1.65; padding-left: 18px; margin: 0;">
                <li><b>7 โมดูลจำลองแคลคูลัส:</b> ลิมิต, เส้นสัมผัส, ผลรวมรีมันน์, u-Sub & By Parts, พื้นที่, ปริมาตรหมุน และปริพันธ์ไม่ตรงแบบ</li>
                <li><b>เครื่องคิดเลขสัญลักษณ์ SymPy:</b> ถอดขั้นตอนการอินทิเกรตและอนุพันธ์แบบสมบูรณ์</li>
                <li><b>แบบทดสอบมโนทัศน์ 80 ข้อ:</b> ครอบคลุม 8 บทเรียน พร้อมคำใบ้และสุ่มตัวเลือก</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )

with bcol3:
    st.markdown(
        """
        <div class="bento-card" style="background: linear-gradient(180deg, #FFFFFF 0%, #EFF6FF 100%);">
            <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 10px;">
                <span style="font-size: 24px;">🛠️</span>
                <h4 style="font-family: 'Fredoka', 'Mali', sans-serif; font-size: 1.05rem; font-weight: 700; margin: 0; color: #2563EB;">
                    เครื่องมือและเทคโนโลยี
                </h4>
            </div>
            <div style="display: flex; flex-wrap: wrap; gap: 4px; margin-top: 6px;">
                <span class="skill-pill pill-yellow">🐍 Python 3.12+</span>
                <span class="skill-pill pill-pink">🎈 Streamlit Framework</span>
                <span class="skill-pill pill-blue">⚡ SymPy CAS</span>
                <span class="skill-pill pill-purple">📊 Plotly Dynamic Graphs</span>
                <span class="skill-pill pill-green">📐 KaTeX Mathematical Typography</span>
                <span class="skill-pill pill-orange">🎨 Neo-Brutalism Pop UI</span>
                <span class="skill-pill pill-pink">🧪 Pytest Automated Testing</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)

with st.container(border=True):
    st.markdown(
        """
        <div style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 14px;">
            <div style="display: flex; align-items: center; gap: 14px;">
                <span style="font-size: 34px;">🐙</span>
                <div>
                    <h4 style="font-family: 'Fredoka', 'Mali', sans-serif; margin: 0 0 2px 0; font-size: 1.15rem; color: #18181B; font-weight: 700;">
                        คลังซอร์สโค้ดโครงงาน (Open-Source Repository)
                    </h4>
                    <p style="font-family: 'Mali', sans-serif; margin: 0; font-size: 0.92rem; color: #4B5563;">
                        โครงการนี้เปิดเป็นโอเพ่นซอร์สเพื่อประโยชน์ทางการศึกษา สามารถศึกษาโค้ดหรือร่วมต่อยอดได้ที่ GitHub
                    </p>
                </div>
            </div>
            <a href="https://github.com/SubwatG/calculus-integration-app" target="_blank" class="github-link-btn">
                <span>⭐ SubwatG/calculus-integration-app ↗</span>
            </a>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.write("")
col_nav1, col_nav2 = st.columns(2)
with col_nav1:
    if st.button("📝 ร่วมทำแบบประเมินความพึงพอใจ (SUS)", type="primary", use_container_width=True):
        st.switch_page("pages/survey.py")
with col_nav2:
    if st.button("🏠 กลับสู่หน้าหลัก", use_container_width=True):
        st.switch_page("pages/home.py")
