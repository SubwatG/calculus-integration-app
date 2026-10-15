import streamlit as st
from utils.theme import render_hero


render_hero("Math Tutor Web App", "เว็บช่วยเรียนคณิตศาสตร์ สำหรับแคลคูลัสเบื้องต้น")

search_query = st.text_input(
    label="ค้นหาสิ่งที่สอน...",
    placeholder="ค้นหาสิ่งที่สอน...",
    key="home_search",
)

cards_data = [
    {
        "title": "1. เส้นสัมผัสและอนุพันธ์",
        "subtitle": "สำรวจความชันเส้นสัมผัสและอนุพันธ์แบบโต้ตอบ",
        "btn_label": "เข้าสู่บทเรียนที่ 1",
        "target": "pages/tangent.py",
        "key": "btn_card_tangent",
    },
    {
        "title": "2. ลิมิตเข้าใกล้จุด",
        "subtitle": "สำรวจการลู่เข้า ลิมิตสองด้าน และรูปแบบไม่กำหนด",
        "btn_label": "เข้าสู่บทเรียนที่ 2",
        "target": "pages/limit_approach.py",
        "key": "btn_card_limit",
    },
    {
        "title": "3. ผลรวมรีมันน์ (Riemann)",
        "subtitle": "จำลองพื้นที่ใต้กราฟและการลู่เข้าสู่ค่าจริง",
        "btn_label": "เข้าสู่บทเรียนที่ 3",
        "target": "pages/riemann.py",
        "key": "btn_card_riemann",
    },
    {
        "title": "4. เทคนิคการอินทิเกรต",
        "subtitle": "ฝึกตัดสินใจเลือกตัวแปร u และ By Parts",
        "btn_label": "เข้าสู่บทเรียนที่ 4",
        "target": "pages/substitution.py",
        "key": "btn_card_sub",
    },
    {
        "title": "5. พื้นที่ระหว่างเส้นโค้ง",
        "subtitle": "คำนวณพื้นที่ปิดล้อมระหว่างสองฟังก์ชัน f(x) และ g(x)",
        "btn_label": "เข้าสู่บทเรียนที่ 5",
        "target": "pages/area_between.py",
        "key": "btn_card_area",
    },
    {
        "title": "6. ปริพันธ์ไม่ตรงแบบ",
        "subtitle": "สำรวจการลู่เข้าหรือลู่ออกบนช่วงอนันต์และจุดเอกฐาน",
        "btn_label": "เข้าสู่บทเรียนที่ 6",
        "target": "pages/improper_integrals.py",
        "key": "btn_card_improper",
    },
    {
        "title": "7. ปริมาตรของรูปทรงตัน",
        "subtitle": "คำนวณปริมาตรทรงตันที่เกิดจากการหมุน (Disk Method)",
        "btn_label": "เข้าสู่บทเรียนที่ 7",
        "target": "pages/volume_revolution.py",
        "key": "btn_card_volume",
    },
    {
        "title": "เครื่องคิดเลขสัญลักษณ์ SymPy",
        "subtitle": "แก้โจทย์แคลคูลัสแบบแจกแจงวิธีทำทีละขั้นตอน",
        "btn_label": "เปิดเครื่องคิดเลข",
        "target": "pages/solver.py",
        "key": "btn_card_solver",
    },
    {
        "title": "แบบทดสอบมโนทัศน์",
        "subtitle": "ฝึกคิด 80 ข้อ ครอบคลุม 8 บท พร้อมระบบคำใบ้และสุ่มตัวเลือก",
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
]

if filtered_cards:
    col1, col2 = st.columns(2)
    for idx, card in enumerate(filtered_cards):
        col = col1 if idx % 2 == 0 else col2
        with col:
            with st.container(border=True):
                st.markdown(f"### {card['title']}")
                st.markdown(
                    f"<p style='color: #475569; font-size: 14px; margin-top: -8px;'>{card['subtitle']}</p>",
                    unsafe_allow_html=True,
                )
                if st.button(card["btn_label"], key=card["key"], use_container_width=True):
                    st.switch_page(card["target"])
else:
    st.markdown("ไม่พบเมนูที่ค้นหา")

st.divider()

st.markdown("### ผลการทดสอบล่าสุด")
scores = st.session_state.get("quiz_scores", {})
basic_score = scores.get("basic_rules")

if basic_score and isinstance(basic_score, dict):
    s = basic_score.get("score", 0)
    t = basic_score.get("total", 5)
    st.metric("คะแนนเกมทบทวน (Basic Rules)", f"{s}/{t}")
    st.progress(s / t if t > 0 else 0)
else:
    st.markdown("ยังไม่มีคะแนน quiz — ไปลองเล่นเกมทบทวนได้เลย")

st.divider()

st.markdown(
    """
### วัตถุประสงค์การเรียนรู้

1. อธิบายภาพรวมว่าอินทิเกรตเกี่ยวข้องกับ ปฏิยานุพันธ์ (Antiderivative) และการสะสมปริมาณได้
2. แยกความแตกต่างระหว่าง Indefinite Integral และ Definite Integral ในระดับเบื้องต้น
3. เรียนรู้ขั้นตอนการคำนวณอินทิกรัล ปริมาตรของแข็ง และพื้นที่ใต้กราฟ
4. ทดสอบความรู้เบื้องต้นและทบทวนเฉลยอย่างเป็นระบบ
"""
)
