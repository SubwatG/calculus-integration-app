import streamlit as st

from utils.quiz_engine import grade_quiz, load_quiz


QUIZ_TOPIC = "basic_rules"


st.title("Basic Rules Quiz")

st.markdown(
    """
## Learning objectives

เมื่อทำแบบทดสอบนี้แล้ว ผู้เรียนควรสามารถ

1. เลือกใช้กฎพื้นฐานของอินทิเกรตกับโจทย์พหุนามได้
2. ตรวจจับคำตอบที่ลืมเพิ่มเลขชี้กำลังหรือหารค่าสัมประสิทธิ์ผิดได้
3. อ่านคำอธิบายเฉลยเพื่อทบทวนเหตุผลของแต่ละข้อได้
"""
)

questions = load_quiz(QUIZ_TOPIC)

with st.form("basic_rules_quiz"):
    answers = {}

    for index, question in enumerate(questions):
        st.markdown(f"### ข้อ {index + 1}")
        st.markdown(question["question"])
        answers[index] = st.radio(
            "เลือกคำตอบ",
            question["choices"],
            index=None,
            key=f"{QUIZ_TOPIC}_q_{index}",
        )

    submitted = st.form_submit_button("ส่งคำตอบ")

if submitted:
    result = grade_quiz(questions, answers)
    st.session_state.quiz_answers[QUIZ_TOPIC] = answers
    st.session_state.quiz_scores[QUIZ_TOPIC] = result
    st.session_state.quiz_submitted = True

if st.session_state.get("quiz_submitted") and QUIZ_TOPIC in st.session_state.quiz_scores:
    result = st.session_state.quiz_scores[QUIZ_TOPIC]
    st.success(f"คะแนน: {result['score']}/{result['total']}")
    st.progress(result["score"] / result["total"])

    st.divider()
    st.subheader("เฉลยและคำอธิบาย")

    saved_answers = st.session_state.quiz_answers.get(QUIZ_TOPIC, {})
    for index, question in enumerate(questions):
        user_answer = saved_answers.get(index)
        is_correct = user_answer == question["answer"]
        status = "ถูก" if is_correct else "ยังไม่ถูก"

        with st.expander(f"ข้อ {index + 1}: {status}", expanded=True):
            st.markdown(f"คำตอบของคุณ: {user_answer or 'ยังไม่ได้เลือก'}")
            st.markdown(f"คำตอบที่ถูกต้อง: {question['answer']}")
            st.markdown(question["explanation"])
