import streamlit as st


st.title("Calculus Tutor: Integration")

st.markdown(
    """
เว็บแอปนี้ช่วยผู้เรียนเริ่มต้นหัวข้ออินทิเกรต (integration) ผ่านบทเรียนสั้น
ตัวอย่างที่เห็นขั้นตอน และแบบทดสอบพร้อมคำอธิบายหลังส่งคำตอบ

## Learning objectives

เมื่อใช้หน้าแรกนี้แล้ว ผู้เรียนควรสามารถ

1. อธิบายภาพรวมว่าอินทิเกรตเกี่ยวข้องกับ antiderivative และการสะสมได้
2. แยกความแตกต่างระหว่าง indefinite integral และ definite integral ได้ในระดับเบื้องต้น
3. เห็นเส้นทางการเรียนจากภาพรวม ไปสู่กฎพื้นฐาน และแบบทดสอบท้ายบท
"""
)

st.markdown(
    r"""
## ภาพรวมแนวคิด

อินทิเกรตเป็นหนึ่งในแกนหลักของแคลคูลัส ใช้ได้ทั้งในความหมายของ
ปฏิยานุพันธ์ (antiderivative) และความหมายของการสะสม (accumulation)
เช่น พื้นที่ใต้กราฟหรือปริมาณรวมที่เกิดจากอัตราการเปลี่ยนแปลง

สมการพื้นฐานที่ควรจำคือ ถ้า $F'(x)=f(x)$ แล้ว

$$
\int f(x)\,dx = F(x)+C
$$
"""
)

st.latex(r"\int_a^b f(x)\,dx = F(b)-F(a)")

col1, col2 = st.columns(2)

with col1:
    st.subheader("เส้นทางการเรียน")
    st.markdown(
        """
1. อ่านภาพรวมของ integration
2. เรียนกฎพื้นฐาน เช่น constant rule, power rule, sum rule
3. ทำแบบทดสอบ Basic Rules
4. อ่านคำอธิบายของข้อที่ตอบผิด แล้วกลับไปทบทวน
"""
    )

with col2:
    st.subheader("คะแนนล่าสุด")
    score = st.session_state.get("quiz_scores", {}).get("basic_rules")
    if score is None:
        st.info("ยังไม่มีคะแนน quiz")
    else:
        st.metric("Basic Rules Quiz", f"{score['score']}/{score['total']}")
        st.progress(score["score"] / score["total"])
