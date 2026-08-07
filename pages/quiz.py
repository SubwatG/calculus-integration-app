import streamlit as st
from utils.quiz_engine import load_quiz
from utils.theme import render_hero


QUIZ_TOPIC = "basic_rules"

render_hero("GAME", "เกมทบทวนความรู้ — ตอบคำถามให้ถูกเพื่อสะสมคะแนน")

questions = load_quiz(QUIZ_TOPIC)

if "quiz_q_index" not in st.session_state:
    st.session_state.quiz_q_index = 0
if "quiz_score" not in st.session_state:
    st.session_state.quiz_score = 0
if "quiz_user_answers" not in st.session_state:
    st.session_state.quiz_user_answers = {}
if "quiz_revealed" not in st.session_state:
    st.session_state.quiz_revealed = False
if "quiz_done" not in st.session_state:
    st.session_state.quiz_done = False
if "quiz_current_choice" not in st.session_state:
    st.session_state.quiz_current_choice = None
# self-contained init (app.py also initializes these; kept here so the page
# also works when run directly via `streamlit run pages/quiz.py`)
if "quiz_scores" not in st.session_state:
    st.session_state.quiz_scores = {}
if "quiz_answers" not in st.session_state:
    st.session_state.quiz_answers = {}
if "quiz_submitted" not in st.session_state:
    st.session_state.quiz_submitted = False


def reset_quiz() -> None:
    st.session_state.quiz_q_index = 0
    st.session_state.quiz_score = 0
    st.session_state.quiz_user_answers = {}
    st.session_state.quiz_revealed = False
    st.session_state.quiz_done = False
    st.session_state.quiz_current_choice = None


if st.session_state.quiz_done:
    final_score = st.session_state.quiz_score
    total_q = len(questions)

    st.markdown("### การทดสอบเสร็จสิ้น")
    st.metric("คะแนนสะสมของคุณ", f"{final_score}/{total_q}")
    st.progress(final_score / total_q if total_q > 0 else 0)

    st.divider()
    st.markdown("### สรุปคำตอบและคำอธิบาย")

    saved_answers = st.session_state.quiz_user_answers
    for idx, q in enumerate(questions):
        user_ans = saved_answers.get(idx, "ไม่ได้ตอบ")
        is_correct = user_ans == q["answer"]
        status_symbol = "✓ ถูกต้อง" if is_correct else "✗ ยังไม่ถูก"

        with st.expander(f"ข้อ {idx + 1}: {status_symbol}", expanded=True):
            st.markdown(f"**คำตอบของคุณ:** {user_ans}")
            st.markdown(f"**คำตอบที่ถูกต้อง:** {q['answer']}")
            st.markdown(f"**คำอธิบาย:** {q['explanation']}")

    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        if st.button("เล่นใหม่", key="btn_quiz_restart", use_container_width=True):
            reset_quiz()
            st.rerun()
    with col_btn2:
        if st.button("กลับหน้าหลัก", key="btn_quiz_home", use_container_width=True):
            st.switch_page("pages/home.py")
else:
    q_idx = st.session_state.quiz_q_index
    if q_idx >= len(questions):
        st.session_state.quiz_done = True
        st.session_state.quiz_scores[QUIZ_TOPIC] = {
            "score": st.session_state.quiz_score,
            "total": len(questions),
        }
        st.session_state.quiz_answers[QUIZ_TOPIC] = st.session_state.quiz_user_answers
        st.session_state.quiz_submitted = True
        st.rerun()
    else:
        q = questions[q_idx]
        col_h1, col_h2 = st.columns([2, 1])
        with col_h1:
            st.markdown(f"### ข้อที่ {q_idx + 1} / {len(questions)}")
        with col_h2:
            st.markdown(f"**คะแนนสะสม:** {st.session_state.quiz_score}")

        st.markdown(f"**คำถาม:** {q['question']}")

        choice_prefixes = ["A", "B", "C", "D"]
        revealed = st.session_state.quiz_revealed
        current_choice = st.session_state.quiz_current_choice

        col_a1, col_a2 = st.columns(2)
        for i, choice_text in enumerate(q["choices"]):
            prefix = choice_prefixes[i] if i < len(choice_prefixes) else str(i + 1)
            btn_label = f"{prefix}. {choice_text}"
            target_col = col_a1 if i % 2 == 0 else col_a2

            with target_col:
                if revealed:
                    if choice_text == q["answer"]:
                        st.markdown(f"**{btn_label}** — ✓ คำตอบที่ถูก")
                    elif choice_text == current_choice:
                        st.markdown(
                            f"<span style='color:#e0414d;'>**{btn_label}** — ✗ คำตอบของคุณ</span>",
                            unsafe_allow_html=True,
                        )
                    else:
                        st.markdown(btn_label)
                else:
                    if st.button(
                        btn_label,
                        key=f"choice_btn_{q_idx}_{i}",
                        use_container_width=True,
                    ):
                        st.session_state.quiz_current_choice = choice_text
                        st.session_state.quiz_user_answers[q_idx] = choice_text
                        if choice_text == q["answer"]:
                            st.session_state.quiz_score += 1
                        st.session_state.quiz_revealed = True
                        st.rerun()

        if revealed:
            st.divider()
            if current_choice == q["answer"]:
                st.markdown("✓ **ถูกต้อง**")
            else:
                st.markdown(f"✗ **ยังไม่ถูก** (คำตอบที่ถูกคือ: {q['answer']})")

            st.markdown(f"**คำอธิบาย:** {q['explanation']}")

            if st.button("ข้อถัดไป", type="primary", key=f"btn_next_q_{q_idx}"):
                if q_idx + 1 < len(questions):
                    st.session_state.quiz_q_index += 1
                    st.session_state.quiz_revealed = False
                    st.session_state.quiz_current_choice = None
                else:
                    st.session_state.quiz_done = True
                    st.session_state.quiz_scores[QUIZ_TOPIC] = {
                        "score": st.session_state.quiz_score,
                        "total": len(questions),
                    }
                    st.session_state.quiz_answers[QUIZ_TOPIC] = (
                        st.session_state.quiz_user_answers
                    )
                    st.session_state.quiz_submitted = True
                st.rerun()
