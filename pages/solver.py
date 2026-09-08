import streamlit as st
from utils.math_render import preview_math_expr, render_syntax_guide
from utils.sympy_solver import compute_limit, differentiate, integrate
from utils.theme import render_hero


render_hero("แคลคูลัส", "เครื่องคิดเลขแก้โจทย์ทีละขั้นตอน")

op_options = ["อินทิเกรต", "อนุพันธ์", "ลิมิต"]
if hasattr(st, "segmented_control"):
    operation = st.segmented_control(
        "ประเภทการคำนวณ",
        op_options,
        default="อินทิเกรต",
    )
else:
    operation = st.selectbox("ประเภทการคำนวณ", op_options)

expr_input = st.text_input(
    "ใส่โจทย์",
    placeholder="เช่น x^2, sin(x), (x^2-4)/(x-2), e^x, 2x",
    key="solver_expr",
)
preview_math_expr(expr_input)
render_syntax_guide()

st.caption("ปุ่มลัดสำหรับใส่ฟังก์ชัน:")
btn_cols = st.columns(10)
tokens_data = [
    ("∫", ""),
    ("d/dx", ""),
    ("lim", ""),
    ("√", "sqrt(x)"),
    ("π", "pi"),
    ("sin", "sin(x)"),
    ("cos", "cos(x)"),
    ("tan", "tan(x)"),
    ("e", "exp(x)"),
    ("x^n", "x**2"),
]

for idx, (label, token) in enumerate(tokens_data):
    with btn_cols[idx]:
        if st.button(label, key=f"token_btn_{idx}"):
            if token:
                curr = st.session_state.get("solver_expr", "")
                st.session_state["solver_expr"] = curr + token if curr else token
                st.rerun()

point_val = 0.0
if operation == "ลิมิต":
    point_val = st.number_input("จุดที่ x เข้าใกล้", value=0.0, key="limit_point")

st.caption("ตัวอย่าง: x**2, sin(x), exp(x), (x**2-4)/(x-2) — ใช้ไวยากรณ์ Python/SymPy")

if st.button("คำนวณ", type="primary", key="btn_do_calc"):
    if not expr_input.strip():
        st.error("กรุณาใส่โจทย์ก่อนทำการคำนวณ")
    else:
        if operation == "อินทิเกรต":
            res = integrate(expr_input)
        elif operation == "อนุพันธ์":
            res = differentiate(expr_input)
        else:
            res = compute_limit(expr_input, point_val)

        if res["ok"]:
            st.markdown("### ผลลัพธ์")
            st.latex(res["latex"])

            st.markdown("### ขั้นตอนการคำนวณ")
            for step in res["steps"]:
                st.markdown(f"- {step}")
        else:
            st.error(res["error"])
