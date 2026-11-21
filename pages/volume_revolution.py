"""pages/volume_revolution.py : บทเรียน interactive: ปริมาตรของทรงตันที่เกิดจากการหมุน (Volume of Solids)

คำนวณปริมาตรแบบ Disk Method พร้อมพล็อตภาพตัดขวางและการหมุนรอบแกน
"""

import streamlit as st

from utils.math_render import preview_math_expr, render_latex, render_syntax_guide, render_steps
from utils.plotter import plot_volume, plot_volume_plotly
from utils.riemann_solver import X
from utils.theme import render_hero
from utils.theory import THEORY_CONTENT
from utils.volume_solver import compute_volume

render_hero("ปริมาตรของทรงตัน", "คำนวณปริมาตรแบบ disk และ washer")

if "volume_expr" not in st.session_state:
    st.session_state["volume_expr"] = "x"
if "volume_a" not in st.session_state:
    st.session_state["volume_a"] = 0.0
if "volume_b" not in st.session_state:
    st.session_state["volume_b"] = 2.0
if "volume_method" not in st.session_state:
    st.session_state["volume_method"] = "disk"
if "volume_inner" not in st.session_state:
    st.session_state["volume_inner"] = "x**2"

theory = THEORY_CONTENT["volume"]

# ---------------------------------------------------------------------------
# Concept Anchor & What to Observe (แนวคิดหลักและจุดสังเกต)
# ---------------------------------------------------------------------------
with st.container(border=True):
    col_badge, col_concept = st.columns([1, 4])
    with col_badge:
        st.markdown(
            """<span style="
                background-color: #FEF08A;
                border: 1.5px solid #18181B;
                border-radius: 8px;
                padding: 4px 10px;
                font-family: 'Fredoka', 'Mali', sans-serif;
                font-size: 13px;
                font-weight: 700;
                color: #18181B;
                display: inline-block;
            ">หลักการสำคัญ</span>""",
            unsafe_allow_html=True,
        )
    with col_concept:
        st.markdown("**ปริมาตรของรูปทรงตันจากการหมุน (Disk & Washer Methods)**")

    st.latex(r"V_{\text{Disk}} = \pi \int_a^b [R(x)]^2\,dx \qquad V_{\text{Washer}} = \pi \int_a^b \left([R(x)]^2 - [r(x)]^2\right)\,dx")

    st.markdown(
        """
| วิธีการคำนวณ | ลักษณะรูปทรงตัน | สูตรปริมาตรจากการหมุน |
| :---: | :--- | :--- |
| วิธีจาน (Disk) | พื้นที่แนบสนิทกับแกนหมุน (ไม่มีรูตรงกลาง) | $V = \\pi \\int_a^b [R(x)]^2\\,dx$ |
| วิธีวงแหวน (Washer) | มีช่องว่างระหว่างกราฟกับแกนหมุน (มีรูกลวง) | $V = \\pi \\int_a^b \\left([R(x)]^2 - [r(x)]^2\\right)\\,dx$ |
        """
    )

with st.expander("รายละเอียดทฤษฎี ข้อควรระวัง และการประยุกต์ใช้เพิ่มเติม", expanded=False):
    col_t1, col_t2 = st.columns(2)
    with col_t1:
        st.markdown("**เงื่อนไขการใช้งาน**")
        for item in theory["conditions"]:
            st.markdown(f"- {item}")
        st.markdown("**สมบัติสำคัญ**")
        for item in theory["properties"]:
            st.markdown(f"- {item}")
    with col_t2:
        st.markdown("**ข้อควรระวัง**")
        with st.container(border=True):
            for caution in theory["cautions"]:
                st.markdown(f"- {caution}")
        st.markdown("**การประยุกต์ใช้**")
        for item in theory["applications"]:
            st.markdown(f"- {item}")

st.divider()
st.markdown("### ลองคำนวณ")

st.markdown("**ตัวอย่างโจทย์ยอดนิยม:**")

def _set_vol_preset(r_val: str, a_val: float, b_val: float, method: str, inner_val: str | None = None) -> None:
    st.session_state["volume_expr"] = r_val
    st.session_state["volume_a"] = a_val
    st.session_state["volume_b"] = b_val
    st.session_state["volume_method"] = method
    if inner_val is not None:
        st.session_state["volume_inner"] = inner_val

p_cols = st.columns(4)
with p_cols[0]:
    st.button("ทรงกรวย $R(x) = x$ บน $[0, 2]$", key="pre_vol_1", use_container_width=True, on_click=_set_vol_preset, args=("x", 0.0, 2.0, "disk"))
with p_cols[1]:
    st.button("พาราโบลอยด์ $R(x) = \\sqrt{x}$ บน $[0, 4]$", key="pre_vol_2", use_container_width=True, on_click=_set_vol_preset, args=("sqrt(x)", 0.0, 4.0, "disk"))
with p_cols[2]:
    st.button("ทรงระฆังคว่ำ $R(x) = 4 - x^2$ บน $[0, 2]$", key="pre_vol_3", use_container_width=True, on_click=_set_vol_preset, args=("4 - x**2", 0.0, 2.0, "disk"))
with p_cols[3]:
    st.button("วงแหวน $R=\\sqrt{x}, r=x^2$ บน $[0, 1]$", key="pre_vol_4", use_container_width=True, on_click=_set_vol_preset, args=("sqrt(x)", 0.0, 1.0, "washer", "x**2"))

expr_input = st.text_input(
    "ฟังก์ชันรัศมี R(x) (หรือรัศมีนอกสำหรับ Washer)",
    value=st.session_state.get("volume_expr", "x"),
    placeholder="เช่น x, sqrt(x), x**2",
    key="volume_expr",
)
preview_math_expr(expr_input, label="พรีวิว R(x)")
render_syntax_guide()

from utils.keypad import render_math_keypad
render_math_keypad(target_key="volume_expr", key_prefix="vol_kp", expanded=False)

col_a, col_b = st.columns(2)
with col_a:
    a_val = st.number_input("ขอบล่าง a", key="volume_a")
with col_b:
    b_val = st.number_input("ขอบบน b", key="volume_b")

method_label = st.selectbox(
    "วิธีคำนวณ",
    ["disk", "washer"],
    key="volume_method",
)

inner_input = None
if method_label == "washer":
    inner_input = st.text_input(
        "ฟังก์ชันรัศมีวงใน r(x)",
        placeholder="เช่น x**2, 1, x",
        key="volume_inner",
    )
    preview_math_expr(inner_input, label="พรีวิว r(x)")

st.caption("[คำแนะนำ] รองรับการคำนวณทั้งแบบ Disk Method และ Washer Method รอบแกน x (y = 0)")

if not expr_input.strip():
    st.info("กรุณาระบุฟังก์ชัน R(x) หรือคลิกเลือกตัวอย่างด้านบน")
else:
    res = compute_volume(expr_input, a_val, b_val, method_label, inner_expr_str=inner_input)
    if res["ok"]:
        v_name = res.get("variable", "x")
        if v_name != "x":
            st.info(f"ตรวจพบตัวแปร **${v_name}$**: ระบบคำนวณและวาดกราฟเทียบกับตัวแปร ${v_name}$ อัตโนมัติ")

        st.markdown("### ผลลัพธ์")
        render_latex(res["latex"])
        st.divider()

        st.markdown("### ภาพตัดขวางทรงตันและการหมุนรอบแกน")
        st.caption("กราฟแบบ Interactive: ใช้ลูกกลิ้งเมาส์เพื่อซูมเข้า/ออก ลากเพื่อเลื่อนดูกราฟ หรือดับเบิลคลิกเพื่อรีเซ็ตมุมมอง")
        try:
            fig_plotly = plot_volume_plotly(res["expr"], a_val, b_val, method_label, inner_expr=res.get("inner_expr"))
            st.plotly_chart(fig_plotly, use_container_width=True, config={"scrollZoom": True, "displayModeBar": True})
        except Exception as e:
            st.warning(f"แสดงผลกราฟ interactive ขัดข้อง: {e} กำลังสลับไปใช้กราฟสำรอง")
            try:
                fig, ax = plot_volume(res["expr"], a_val, b_val, method_label, inner_expr=res.get("inner_expr"))
                st.pyplot(fig)
            except Exception as e2:
                st.warning(f"ไม่สามารถวาดกราฟได้: {e2}")

        render_steps(res["steps"])
    else:
        st.error(res["error"])
