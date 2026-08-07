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
        "title": "บทเรียนแคลคูลัส",
        "subtitle": "เนื้อหาและทฤษฎีทีละบท",
        "btn_label": "เข้าสู่บทเรียน",
        "target": "pages/lessons.py",
        "key": "btn_card_lessons",
    },
    {
        "title": "แก้โจทย์ทีละขั้น",
        "subtitle": "ใส่โจทย์ คำนวณด้วย SymPy",
        "btn_label": "คำนวณโจทย์",
        "target": "pages/solver.py",
        "key": "btn_card_solver",
    },
    {
        "title": "พื้นที่ใต้กราฟ",
        "subtitle": "หัวข้อเลือกเรียน",
        "btn_label": "เลือกหัวข้อ",
        "target": "pages/topics.py",
        "key": "btn_card_topics",
    },
    {
        "title": "เกมทบทวน",
        "subtitle": "ตอบคำถามสะสมคะแนน",
        "btn_label": "เริ่มเกมทบทวน",
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
                    f"<p style='color: #5a6289; font-size: 14px; margin-top: -8px;'>{card['subtitle']}</p>",
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
