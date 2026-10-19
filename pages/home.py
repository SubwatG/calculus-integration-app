import streamlit as st
from utils.theme import render_hero

render_hero(
    "Calculus Learning Sandbox",
    "เว็บแอปพลิเคชันสำหรับฝึกมโนทัศน์แคลคูลัสผ่านกราฟเชิงโต้ตอบและการคำนวณทีละขั้น",
)

st.markdown(
    """
    <style>
    .home-hero-banner {
        background: linear-gradient(135deg, #FFF1F2 0%, #FEF08A 50%, #E0F2FE 100%);
        border: 2.5px solid #18181B;
        border-radius: 14px;
        padding: 12px 18px;
        box-shadow: 4px 4px 0px #18181B;
        margin-bottom: 20px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        flex-wrap: wrap;
        gap: 10px;
    }
    .home-stat-pill {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background-color: #FFFFFF;
        border: 1.5px solid #18181B;
        border-radius: 999px;
        padding: 4px 12px;
        font-family: 'Fredoka', 'Mali', sans-serif;
        font-size: 13px;
        font-weight: 700;
        color: #18181B;
        box-shadow: 2px 2px 0px #18181B;
    }
    .card-category-badge {
        display: inline-block;
        border: 1.5px solid #18181B;
        border-radius: 999px;
        padding: 3px 10px;
        font-family: 'Fredoka', 'Mali', sans-serif;
        font-size: 11.5px;
        font-weight: 700;
        color: #18181B;
        box-shadow: 1.5px 1.5px 0px #18181B;
        margin-bottom: 8px;
    }
    .obj-card {
        background: #FFFFFF;
        border: 2px solid #18181B;
        border-radius: 12px;
        padding: 14px 16px;
        box-shadow: 3px 3px 0px #18181B;
        height: 100%;
        transition: transform 0.15s ease;
    }
    .obj-card:hover {
        transform: translate(-2px, -2px);
        box-shadow: 4.5px 4.5px 0px #18181B;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Highlight Banner
st.markdown(
    """
    <div class="home-hero-banner">
        <div style="display: flex; align-items: center; gap: 8px;">
            <span class="material-symbols-rounded" style="font-size: 24px; color: #D97706;">lightbulb</span>
            <span style="font-family: 'Fredoka', 'Mali', sans-serif; font-size: 14px; font-weight: 700; color: #18181B;">
                สำรวจมโนทัศน์แคลคูลัสผ่านกราฟแบบอินเทอร์แอ็กทิฟและการแก้โจทย์ทีละขั้น
            </span>
        </div>
        <div style="display: flex; gap: 8px; flex-wrap: wrap;">
            <span class="home-stat-pill">7 โมดูลจำลอง</span>
            <span class="home-stat-pill">SymPy CAS</span>
            <span class="home-stat-pill">80 ข้อสอบ</span>
            <span class="home-stat-pill">KU KPS</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

search_query = st.text_input(
    label="ค้นหาบทเรียนหรือเครื่องมือ...",
    placeholder="พิมพ์เพื่อค้นหา เช่น ลิมิต, รีมันน์, ปริมาตร, u-sub...",
    key="home_search",
)

cards_data = [
    {
        "title": "1. ลิมิตเข้าใกล้จุด",
        "subtitle": "สำรวจการลู่เข้า ลิมิตสองด้าน และรูปแบบไม่กำหนด (Indeterminate Forms)",
        "badge": "บทเรียนที่ 1 • แคลคูลัส 1",
        "badge_color": "#FECDD3",
        "btn_label": "เข้าสู่บทเรียนที่ 1",
        "target": "pages/limit_approach.py",
        "key": "btn_card_limit",
    },
    {
        "title": "2. เส้นสัมผัสและอนุพันธ์",
        "subtitle": "สำรวจความชันเส้นสัมผัส อนุพันธ์แบบโต้ตอบ และอัตราการเปลี่ยนแปลง",
        "badge": "บทเรียนที่ 2 • อนุพันธ์",
        "badge_color": "#FEF08A",
        "btn_label": "เข้าสู่บทเรียนที่ 2",
        "target": "pages/tangent.py",
        "key": "btn_card_tangent",
    },
    {
        "title": "3. ผลรวมรีมันน์ (Riemann Sum)",
        "subtitle": "จำลองพื้นที่ใต้กราฟด้วยแท่งสี่เหลี่ยมและการลู่เข้าสู่ค่าอินทิกรัลจริง",
        "badge": "บทเรียนที่ 3 • ปริพันธ์",
        "badge_color": "#BAE6FD",
        "btn_label": "เข้าสู่บทเรียนที่ 3",
        "target": "pages/riemann.py",
        "key": "btn_card_riemann",
    },
    {
        "title": "4. เทคนิคการอินทิเกรต",
        "subtitle": "ฝึกตัดสินใจเลือกตัวแปร u-Substitution และ Integration by Parts",
        "badge": "บทเรียนที่ 4 • เทคนิคอินทิเกรต",
        "badge_color": "#BBF7D0",
        "btn_label": "เข้าสู่บทเรียนที่ 4",
        "target": "pages/substitution.py",
        "key": "btn_card_sub",
    },
    {
        "title": "5. พื้นที่ระหว่างเส้นโค้ง",
        "subtitle": "คำนวณพื้นที่ปิดล้อมระหว่างสองฟังก์ชัน f(x) และ g(x) พร้อมกราฟแรเงา",
        "badge": "บทเรียนที่ 5 • การประยุกต์",
        "badge_color": "#FED7AA",
        "btn_label": "เข้าสู่บทเรียนที่ 5",
        "target": "pages/area_between.py",
        "key": "btn_card_area",
    },
    {
        "title": "6. ปริมาตรของรูปทรงตัน",
        "subtitle": "คำนวณปริมาตรทรงตันที่เกิดจากการหมุนรอบแกนด้วยวิธีจาน (Disk Method)",
        "badge": "บทเรียนที่ 6 • ปริมาตรหมุน",
        "badge_color": "#E9D5FF",
        "btn_label": "เข้าสู่บทเรียนที่ 6",
        "target": "pages/volume_revolution.py",
        "key": "btn_card_volume",
    },
    {
        "title": "7. ปริพันธ์ไม่ตรงแบบ",
        "subtitle": "สำรวจการลู่เข้าหรือลู่ออกบนช่วงอนันต์และจุดเอกฐาน (Singularities)",
        "badge": "บทเรียนที่ 7 • ปริพันธ์ขั้นสูง",
        "badge_color": "#FBCFE8",
        "btn_label": "เข้าสู่บทเรียนที่ 7",
        "target": "pages/improper_integrals.py",
        "key": "btn_card_improper",
    },
    {
        "title": "เครื่องคิดเลขสัญลักษณ์ SymPy",
        "subtitle": "แก้โจทย์แคลคูลัสพร้อมแสดงวิธีทำทีละขั้น",
        "badge": "เครื่องมือคำนวณ • CAS",
        "badge_color": "#FEF08A",
        "btn_label": "เปิดเครื่องคิดเลข",
        "target": "pages/solver.py",
        "key": "btn_card_solver",
    },
    {
        "title": "แบบทดสอบมโนทัศน์ (80 ข้อ)",
        "subtitle": "ฝึกคิด 80 ข้อ ครอบคลุม 8 บทเรียน พร้อมระบบคำใบ้และสุ่มตัวเลือก",
        "badge": "วัดระดับทักษะ • มีคำใบ้",
        "badge_color": "#BAE6FD",
        "btn_label": "เริ่มทำแบบทดสอบ",
        "target": "pages/quiz.py",
        "key": "btn_card_quiz",
    },
]

filtered_cards = [
    card
    for card in cards_data
    if not search_query
    or search_query.lower() in card["title"].lower()
    or search_query.lower() in card["subtitle"].lower()
    or search_query.lower() in card["badge"].lower()
]

if filtered_cards:
    col1, col2 = st.columns(2)
    for idx, card in enumerate(filtered_cards):
        col = col1 if idx % 2 == 0 else col2
        with col:
            with st.container(border=True):
                st.markdown(
                    f"<span class='card-category-badge' style='background-color: {card.get('badge_color', '#FEF08A')};'>{card.get('badge', 'บทเรียน')}</span>",
                    unsafe_allow_html=True,
                )
                st.markdown(f"### {card['title']}")
                st.markdown(
                    f"<p style='color: #475569; font-size: 14px; margin-top: -6px; line-height: 1.5;'>{card['subtitle']}</p>",
                    unsafe_allow_html=True,
                )
                if st.button(card["btn_label"], icon=":material/arrow_forward:", key=card["key"], use_container_width=True):
                    st.switch_page(card["target"])
else:
    st.info("ไม่พบเมนูหรือบทเรียนที่ตรงกับคำค้นหา ลองใช้คำอื่น", icon=":material/search:")

st.divider()

st.markdown("### ผลการทดสอบล่าสุด (Your Recent Progress)")
scores = st.session_state.get("quiz_scores", {})
basic_score = scores.get("basic_rules")

if basic_score and isinstance(basic_score, dict):
    s = basic_score.get("score", 0)
    t = basic_score.get("total", 5)
    st.metric("คะแนนเกมทบทวน (Basic Rules)", f"{s}/{t}")
    st.progress(s / t if t > 0 else 0)
    if s == t:
        st.balloons()
        st.success("ทำคะแนนเต็มในหมวดนี้", icon=":material/check_circle:")
else:
    col_sc1, col_sc2 = st.columns([3, 1])
    with col_sc1:
        st.markdown(
            """
            <div style="background-color: #FFFFFF; border: 2px dashed #94A3B8; border-radius: 12px; padding: 12px 18px;">
                <span style="font-family: 'Fredoka', 'Mali', sans-serif; font-size: 14px; font-weight: 600; color: #475569;">
                    ยังไม่มีบันทึกคะแนนในเซสชันนี้ ทำแบบทดสอบมโนทัศน์เพื่อบันทึกผล
                </span>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col_sc2:
        if st.button("ไปทำแบบทดสอบ", icon=":material/quiz:", key="btn_home_to_quiz", use_container_width=True):
            st.switch_page("pages/quiz.py")

st.divider()

st.markdown("### วัตถุประสงค์การเรียนรู้ (Learning Goals)")

ocol1, ocol2, ocol3, ocol4 = st.columns(4)

with ocol1:
    st.markdown(
        """
        <div class="obj-card" style="background: linear-gradient(180deg, #FFFFFF 0%, #FFF1F2 100%);">
            <div style="margin-bottom: 6px;"><span class="material-symbols-rounded" style="font-size: 26px; color: #E11D48;">square_foot</span></div>
            <h4 style="font-family: 'Fredoka', 'Mali', sans-serif; font-size: 14px; font-weight: 700; margin: 0 0 6px 0; color: #E11D48;">
                1. เชื่อมโยงแนวคิด
            </h4>
            <p style="font-family: 'Mali', sans-serif; font-size: 12.5px; color: #4B5563; margin: 0; line-height: 1.5;">
                เข้าใจความสัมพันธ์ระหว่างปฏิยานุพันธ์และการสะสมปริมาณใต้กราฟ
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with ocol2:
    st.markdown(
        """
        <div class="obj-card" style="background: linear-gradient(180deg, #FFFFFF 0%, #FEF9C3 100%);">
            <div style="margin-bottom: 6px;"><span class="material-symbols-rounded" style="font-size: 26px; color: #D97706;">balance</span></div>
            <h4 style="font-family: 'Fredoka', 'Mali', sans-serif; font-size: 14px; font-weight: 700; margin: 0 0 6px 0; color: #D97706;">
                2. แยกแยะปริพันธ์
            </h4>
            <p style="font-family: 'Mali', sans-serif; font-size: 12.5px; color: #4B5563; margin: 0; line-height: 1.5;">
                แยกความแตกต่างระหว่าง Indefinite และ Definite Integral ได้อย่างแม่นยำ
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with ocol3:
    st.markdown(
        """
        <div class="obj-card" style="background: linear-gradient(180deg, #FFFFFF 0%, #F0FDF4 100%);">
            <div style="margin-bottom: 6px;"><span class="material-symbols-rounded" style="font-size: 26px; color: #16A34A;">rotate_right</span></div>
            <h4 style="font-family: 'Fredoka', 'Mali', sans-serif; font-size: 14px; font-weight: 700; margin: 0 0 6px 0; color: #16A34A;">
                3. ประยุกต์เรขาคณิต
            </h4>
            <p style="font-family: 'Mali', sans-serif; font-size: 12.5px; color: #4B5563; margin: 0; line-height: 1.5;">
                คำนวณพื้นที่ใต้กราฟ พื้นที่ระหว่างเส้นโค้ง และปริมาตรทรงตันจากการหมุน
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with ocol4:
    st.markdown(
        """
        <div class="obj-card" style="background: linear-gradient(180deg, #FFFFFF 0%, #EFF6FF 100%);">
            <div style="margin-bottom: 6px;"><span class="material-symbols-rounded" style="font-size: 26px; color: #2563EB;">assignment</span></div>
            <h4 style="font-family: 'Fredoka', 'Mali', sans-serif; font-size: 14px; font-weight: 700; margin: 0 0 6px 0; color: #2563EB;">
                4. วัดผลอย่างเป็นระบบ
            </h4>
            <p style="font-family: 'Mali', sans-serif; font-size: 12.5px; color: #4B5563; margin: 0; line-height: 1.5;">
                ทดสอบความรู้ ทบทวนเฉลยอย่างมีเหตุผล พร้อมระบบคำใบ้ฝึกกระบวนการคิด
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
