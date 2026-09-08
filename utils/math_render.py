"""
Math rendering helpers for Streamlit (native KaTeX).

กฎของ Streamlit:
- st.latex(expr)  → display math; expr ต้องเป็น pure LaTeX (ไม่มี $...$, ไม่มีภาษาไทย)
- st.markdown(text with $...$ or $$...$$) → KaTeX ผ่าน built-in engine
- unsafe_allow_html=True → KaTeX ไม่ทำงานใน raw HTML
- widget labels / selectbox options → ไม่รองรับ KaTeX ใช้ Unicode แทน

อ้างอิง pattern จาก stat-distribution-solver/modules/math_render.py
"""

from __future__ import annotations

import re
from typing import Optional

import streamlit as st

_THAI_RE = re.compile(r"[\u0e00-\u0e7f]")
_WRAPPED_DISPLAY = re.compile(r"^\s*\$\$(.*)\$\$\s*$", re.DOTALL)
_WRAPPED_INLINE = re.compile(r"^\s*\$(.*)\$\s*$", re.DOTALL)


def has_thai(text: str) -> bool:
    return bool(_THAI_RE.search(text or ""))


def strip_math_delimiters(expr: str) -> str:
    """Remove outer $...$ or $$...$$ if the whole string is wrapped."""
    s = (expr or "").strip()
    m = _WRAPPED_DISPLAY.match(s)
    if m:
        return m.group(1).strip()
    m = _WRAPPED_INLINE.match(s)
    if m and s.count("$") == 2:
        return m.group(1).strip()
    return s


def is_pure_latex(expr: str) -> bool:
    """True if string looks like pure LaTeX (safe for st.latex)."""
    s = (expr or "").strip()
    if not s or has_thai(s):
        return False
    if "$" in s:
        return False
    return ("\\" in s) or any(ch in s for ch in "=^_{}()[]")


def render_latex(expr: str, *, label: Optional[str] = None) -> None:
    """Render pure LaTeX with st.latex; fall back to markdown if mixed."""
    if expr is None:
        return
    s = str(expr).strip()
    if not s:
        return
    if label:
        st.markdown(f"**{label}**")

    if has_thai(s) or "$" in s:
        st.markdown(s)
        return

    core = strip_math_delimiters(s)
    try:
        st.latex(core)
    except Exception:
        st.markdown(f"$${core}$$")


def render_steps(steps) -> None:
    """Display step-by-step solution cleanly like an academic worksheet."""
    if not steps:
        return
    st.markdown("### วิธีทำทีละขั้นตอน")
    for i, step in enumerate(steps, 1):
        s = str(step)
        try:
            render_latex(s, label=f"ขั้นที่ {i}")
        except Exception:
            # สูตรเดียวพังไม่ควรซ่อนขั้นอื่น
            st.markdown(f"**ขั้นที่ {i}** (แสดงสูตรไม่สำเร็จ)")
            st.code(s, language=None)


def preview_math_expr(expr_str: str, label: str = "สมการที่ระบบเข้าใจ") -> bool:
    """พรีวิวสมการ LaTeX แบบสด และแจ้งเตือนไวยากรณ์ที่เป็นมิตร"""
    clean = (expr_str or "").strip()
    if not clean:
        return False
    try:
        import sympy as sp
        from sympy.parsing.sympy_parser import (
            convert_xor,
            implicit_multiplication_application,
            parse_expr,
            standard_transformations,
        )

        transformations = standard_transformations + (
            implicit_multiplication_application,
            convert_xor,
        )
        local_dict = {"e": sp.E, "E": sp.E, "pi": sp.pi, "ln": sp.log}
        parsed = parse_expr(clean, transformations=transformations, local_dict=local_dict)
        latex_str = sp.latex(parsed)
        st.caption(f"{label}:")
        st.latex(f"f(x) = {latex_str}")
        return True
    except Exception:
        st.caption("[คำแนะนำ] ตรวจสอบวงเล็บและรูปแบบฟังก์ชัน เช่น x^2, 2x, sin(x), e^x, sqrt(x)")
        return False


def render_syntax_guide() -> None:
    """แสดงการ์ดคำแนะนำไวยากรณ์การป้อนสมการสำหรับผู้เริ่มต้น"""
    with st.expander("คำแนะนำการป้อนสมการ (สำหรับผู้เริ่มต้น)", expanded=False):
        st.markdown(
            """
            * **ยกกำลัง:** พิมพ์ `x^2` หรือ `x**2` (เช่น `x^3 - 2x`)
            * **การคูณ:** พิมพ์ `2x` หรือ `2*x` (ระบบรองรับการละเครื่องหมายคูณ)
            * **เอกซ์โพเนนเชียล:** พิมพ์ `e^x` หรือ `exp(x)`
            * **ลอการิทึมธรรมชาติ:** พิมพ์ `ln(x)` หรือ `log(x)`
            * **สแควร์รูท:** พิมพ์ `sqrt(x)` (เช่น `sqrt(x^2 + 1)`)
            * **ฟังก์ชันตรีโกณมิติ:** พิมพ์ `sin(x)`, `cos(x)`, `tan(x)`
            * **เศษส่วน:** ให้ใส่วงเล็บกำกับ เช่น `1/(x+1)` หรือ `(x^2-4)/(x-2)`
            """
        )

