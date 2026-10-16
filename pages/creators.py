import streamlit as st
from utils.theme import render_hero

render_hero("ประวัติคณะผู้จัดทำ", "คณะผู้พัฒนาเว็บแอปพลิเคชันช่วยเรียนรู้แคลคูลัสแบบมีปฏิสัมพันธ์ (Calculus Learning Sandbox)")

st.markdown(
    """
    <style>
    .creator-card {
        background-color: #FFFFFF;
        border: 2.5px solid #18181B;
        border-radius: 14px;
        padding: 22px 24px;
        box-shadow: 4px 4px 0px #18181B;
        margin-bottom: 20px;
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
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
        margin-bottom: 12px;
    }
    .creator-name {
        font-family: 'Fredoka', 'Mali', sans-serif;
        font-size: 1.3rem;
        font-weight: 700;
        color: #18181B;
        margin: 0 0 6px 0;
    }
    .creator-sub {
        font-family: 'Mali', sans-serif;
        font-size: 0.95rem;
        font-weight: 600;
        color: #F43F5E;
        margin: 0 0 12px 0;
    }
    .creator-desc {
        font-family: 'Mali', sans-serif;
        font-size: 0.95rem;
        color: #374151;
        line-height: 1.65;
        margin: 0;
    }
    .advisor-card {
        background: linear-gradient(135deg, #FFF0F5 0%, #FEF9C3 100%);
        border: 2.5px solid #18181B;
        border-radius: 14px;
        padding: 22px 26px;
        box-shadow: 4px 4px 0px #18181B;
        margin-top: 8px;
        margin-bottom: 24px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown("### 👩‍🎓 คณะผู้จัดทำโครงงาน (Project Creators)")

col1, col2 = st.columns(2)

with col1:
    st.markdown(
        """
        <div class="creator-card">
            <div>
                <span class="creator-badge">👩‍💻 ผู้พัฒนาโครงงาน</span>
                <h4 class="creator-name">นางสาวขวัญเรือน สำเนียงดี</h4>
                <div class="creator-sub">นิสิตระดับปริญญาตรี • สาขาวิชาคณิตศาสตร์ประยุกต์</div>
                <p class="creator-desc">
                    • <b>ภาควิชา:</b> วิทยาการคำนวณและเทคโนโลยีดิจิทัล<br>
                    • <b>คณะ:</b> ศิลปศาสตร์และวิทยาศาสตร์<br>
                    • <b>สถาบัน:</b> มหาวิทยาลัยเกษตรศาสตร์ วิทยาเขตกำแพงแสน
                </p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col2:
    st.markdown(
        """
        <div class="creator-card">
            <div>
                <span class="creator-badge">👩‍💻 ผู้พัฒนาโครงงาน</span>
                <h4 class="creator-name">นางสาวเบญจกัฬยาณี พิทยากูล</h4>
                <div class="creator-sub">นิสิตระดับปริญญาตรี • สาขาวิชาคณิตศาสตร์ประยุกต์</div>
                <p class="creator-desc">
                    • <b>ภาควิชา:</b> วิทยาการคำนวณและเทคโนโลยีดิจิทัล<br>
                    • <b>คณะ:</b> ศิลปศาสตร์และวิทยาศาสตร์<br>
                    • <b>สถาบัน:</b> มหาวิทยาลัยเกษตรศาสตร์ วิทยาเขตกำแพงแสน
                </p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("### 👨‍🏫 อาจารย์ที่ปรึกษาโครงงาน (Project Advisor)")

st.markdown(
    """
    <div class="advisor-card">
        <div style="display: flex; align-items: center; gap: 16px; flex-wrap: wrap;">
            <span style="font-size: 38px; line-height: 1;">🎓</span>
            <div>
                <h4 style="font-family: 'Fredoka', 'Mali', sans-serif; font-size: 1.25rem; font-weight: 700; color: #18181B; margin: 0 0 4px 0;">
                    อาจารย์กิตติพงษ์ ทรัพย์วัฒนาชัย
                </h4>
                <p style="font-family: 'Mali', sans-serif; font-size: 0.95rem; color: #4B5563; margin: 0; line-height: 1.55;">
                    อาจารย์ที่ปรึกษาโครงงาน • ภาควิชาวิทยาการคำนวณและเทคโนโลยีดิจิทัล<br>
                    คณะศิลปศาสตร์และวิทยาศาสตร์ มหาวิทยาลัยเกษตรศาสตร์ วิทยาเขตกำแพงแสน
                </p>
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("### 🏛️ ข้อมูลโครงงานและวัตถุประสงค์ (Project Overview)")

with st.container(border=True):
    st.markdown(
        """
        * **ชื่อโครงงาน:** การพัฒนาเว็บแอปพลิเคชันช่วยเรียนคณิตศาสตร์สำหรับแคลคูลัสเบื้องต้น (*Development of an Interactive Web Application for Calculus Learning*)
        * **หน่วยงาน:** ภาควิชาวิทยาการคำนวณและเทคโนโลยีดิจิทัล คณะศิลปศาสตร์และวิทยาศาสตร์ มหาวิทยาลัยเกษตรศาสตร์ วิทยาเขตกำแพงแสน
        * **วัตถุประสงค์หลัก:**
          1. เพื่อเป็นสื่อช่วยสอนเสริมและเครื่องมือการเรียนรู้แคลคูลัสแบบเปิด (Open-Access Educational Tool)
          2. เพื่อเสริมสร้างมโนทัศน์ทางคณิตศาสตร์ (Conceptual Understanding) ผ่านกราฟจำลองเชิงเรขาคณิตแบบอินเทอร์แอ็กทิฟ
          3. เพื่อยกระดับความเข้าใจขั้นตอนการแก้โจทย์อย่างเป็นระบบตามหลักคณิตศาสตร์ (Step-by-Step Worked Solutions)
        * **เครื่องมือและเทคโนโลยี:** Python, Streamlit, SymPy CAS, Plotly Dynamic Visualizations, KaTeX Typography
        * **ซอร์สโค้ดโครงงาน:** [GitHub: SubwatG/calculus-integration-app](https://github.com/SubwatG/calculus-integration-app)
        """
    )

st.write("")
col_nav1, col_nav2 = st.columns(2)
with col_nav1:
    if st.button("📝 ร่วมทำแบบประเมินความพึงพอใจ (SUS)", type="primary", use_container_width=True):
        st.switch_page("pages/survey.py")
with col_nav2:
    if st.button("🏠 กลับสู่หน้าหลัก", use_container_width=True):
        st.switch_page("pages/home.py")
