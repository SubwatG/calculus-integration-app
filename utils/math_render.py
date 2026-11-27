"""
Math rendering helpers for Streamlit (native KaTeX).

Streamlit rules:
- st.latex(expr): display math; expr must be pure LaTeX (no $...$, no Thai)
- st.markdown(text with $...$ or $$...$$): KaTeX via built-in engine
- unsafe_allow_html=True: KaTeX does not execute in raw HTML
- widget labels / selectbox options: do not support KaTeX; use Unicode instead

Pattern referenced from stat-distribution-solver/modules/math_render.py
"""

from __future__ import annotations

import re
from typing import Optional

import streamlit as st

_THAI_RE = re.compile(r"[\u0e00-\u0e7f]")
_WRAPPED_DISPLAY = re.compile(r"^\s*\$\$(.*)\$\$\s*$", re.DOTALL)
_WRAPPED_INLINE = re.compile(r"^\s*\$(.*)\$\s*$", re.DOTALL)


def format_inverse_trig(text: str) -> str:
    """Format inverse trigonometric functions and natural logarithm (\\log -> \\ln) to standard textbook notation."""
    if not text:
        return text
    # 0. Convert \log to \ln for natural logarithm
    s = re.sub(r"\\log(?![a-zA-Z0-9_])", r"\\ln", text)
    # 1. Handle \operatorname{asin}, \operatorname{acos}, \operatorname{atan}
    s = re.sub(r"\\operatorname\{a(sin|cos|tan)\}", r"\\arc\1", s)
    s = re.sub(r"\\operatorname\{arc(cot|sec|csc)\}", r"\\arc\1", s)
    # 2. Handle commands without leading backslash followed by parentheses e.g. asin(...) or asin{...}
    s = re.sub(r"(?<![a-zA-Z\\])a(sin|cos|tan)(?=\s*[\(\{\[_0-9]|\b)", r"\\arc\1", s)
    return s

_MATH_MACROS = [
    r"\\pi", r"\\infty", r"\\pm", r"\\mp", r"\\alpha", r"\\beta", r"\\gamma", 
    r"\\theta", r"\\lambda", r"\\mu", r"\\sigma", r"\\tau", r"\\phi", r"\\omega",
    r"\\Delta"
]
_MACROS_PATTERN = "|".join(_MATH_MACROS)

_BARE_LATEX_RE = re.compile(
    r"(\$\$.*?\$\$|\$.*?\$|"
    r"\\frac\{[^{}]*\}\{[^{}]*\}(?:\^[\w+-]+)?|"
    r"\\sqrt\{[^{}]*\}(?:\^[\w+-]+)?|"
    rf"(?:{_MACROS_PATTERN})(?![a-zA-Z])(?:\^[\w+-]+)?)"
)


def auto_wrap_bare_latex(text: str) -> str:
    """Wrap bare LaTeX commands or symbols not enclosed in $...$ so KaTeX can render them."""
    if not text or "\\" not in text:
        return text

    def replace_fn(match):
        token = match.group(0)
        if token.startswith("$"):
            return token
        return f"${token}$"

    return _BARE_LATEX_RE.sub(replace_fn, text)


def has_thai(text: str) -> bool:
    return bool(_THAI_RE.search(text or ""))


def strip_math_delimiters(expr: str) -> str:
    """Remove outer $...$ or $$...$$ if the whole string is wrapped."""
    s = format_inverse_trig((expr or "").strip())
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


def format_math_spacing(text: str) -> str:
    """Format spacing before and after math equations ($...$ or $$...$$) when adjacent to Thai text and wrap bare symbols."""
    if not text:
        return text
    # 0. Convert inverse trig functions and wrap bare LaTeX symbols
    text = format_inverse_trig(text)
    text = auto_wrap_bare_latex(text)
    if not has_thai(text):
        return text
    # 1. Thai character adjacent to opening $ (insert space)
    s = re.sub(r"([\u0e00-\u0e7f])(\$+)", r"\1 \2", text)
    # 2. Closing $ adjacent to Thai character (insert space)
    s = re.sub(r"(\$+)([\u0e00-\u0e7f])", r"\1 \2", s)
    return s


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
        st.markdown(format_math_spacing(s))
        return

    core = strip_math_delimiters(s)
    try:
        st.latex(core)
    except Exception:
        st.markdown(f"$${core}$$")


def render_steps(steps, title: Optional[str] = "### วิธีทำทีละขั้นตอน") -> None:
    """Render step-by-step worked solutions cleanly using st.latex and KaTeX."""
    if not steps:
        return

    if title:
        st.markdown(title)

    for i, step in enumerate(steps, 1):
        if isinstance(step, dict):
            raw_title = step.get("title", f"ขั้นตอนที่ {i}")
            clean_title = re.sub(r"^(?:ขั้น(?:ตอน)?ที่\s*\d+\s*[:.]?\s*)", "", raw_title).strip() or raw_title
            latex_expr = step.get("latex", "")
            desc = step.get("desc", "")
            st.markdown(f"**ขั้นที่ {i}: {format_math_spacing(clean_title)}**")
            if desc:
                st.markdown(format_math_spacing(desc))
            if latex_expr:
                core_lex = strip_math_delimiters(latex_expr)
                if is_pure_latex(core_lex):
                    st.latex(core_lex)
                else:
                    st.markdown(format_math_spacing(latex_expr))
            continue

        s = str(step).strip()
        if not s:
            continue

        # Strip step prefix to avoid redundant numbering like "Step 2: Step 1"
        clean_s = re.sub(r"^(?:ขั้น(?:ตอน)?ที่\s*\d+\s*[:.]?\s*)", "", s).strip()

        # Check format "Thai description: LaTeX equation"
        if ":" in clean_s:
            parts = clean_s.split(":", 1)
            title_text = parts[0].strip()
            math_part = parts[1].strip()

            st.markdown(f"**ขั้นที่ {i}: {format_math_spacing(title_text)}**")

            # If multi-line, separate markdown explanations from LaTeX equations
            if "\n" in math_part:
                sub_lines = [line.strip() for line in math_part.split("\n") if line.strip()]
                for sub_line in sub_lines:
                    core_sub = strip_math_delimiters(sub_line)
                    if has_thai(core_sub) or not is_pure_latex(core_sub):
                        st.markdown(format_math_spacing(sub_line))
                    elif core_sub:
                        try:
                            st.latex(core_sub)
                        except Exception:
                            st.markdown(f"$${core_sub}$$")
            else:
                core_math = strip_math_delimiters(math_part)

                # If containing Thai or not pure LaTeX, always render as markdown, never pass to st.latex
                if has_thai(core_math) or not is_pure_latex(core_math):
                    st.markdown(format_math_spacing(math_part))
                elif core_math:
                    try:
                        st.latex(core_math)
                    except Exception:
                        st.markdown(f"$${core_math}$$")
        else:
            # Case without colon (:)
            if "$" in clean_s:
                st.markdown(f"**ขั้นที่ {i}**")
                st.markdown(format_math_spacing(clean_s))
            elif is_pure_latex(clean_s) or ("\\" in clean_s) or ("=" in clean_s):
                st.markdown(f"**ขั้นที่ {i}**")
                try:
                    st.latex(strip_math_delimiters(clean_s))
                except Exception:
                    st.markdown(f"$${clean_s}$$")
            else:
                st.markdown(f"**ขั้นที่ {i}:** {format_math_spacing(clean_s)}")


def preview_math_expr(expr_str: str, label: str = "สมการที่ระบบเข้าใจ", var_name: Optional[str] = None) -> bool:
    """Live preview of parsed LaTeX equation with syntax validation feedback."""
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
        latex_str = format_inverse_trig(sp.latex(parsed, inv_trig_style="full", ln_notation=True))

        # Define function names e.g. f(x), g(x), R(x), r(x)
        if var_name is None:
            if "g(x)" in label:
                var_name = "g"
            elif "R(x)" in label:
                var_name = "R"
            elif "r(x)" in label:
                var_name = "r"
            else:
                var_name = "f"

        st.caption(f"{label}:")
        st.latex(f"{var_name}(x) = {latex_str}")
        return True
    except Exception:
        st.caption("[คำแนะนำ] ตรวจสอบวงเล็บและรูปแบบฟังก์ชัน เช่น x^2, 2x, sin(x), e^x, sqrt(x), ln(x), arctan(x)")
        return False


def render_syntax_guide() -> None:
    """Render beginner-friendly mathematical input syntax guidance expander."""
    with st.expander("คำแนะนำการป้อนสมการ (สำหรับผู้เริ่มต้น)", expanded=False):
        st.markdown(
            """
            * **ยกกำลัง:** พิมพ์ `x^2` หรือ `x**2` (เช่น `x^3 - 2x`)
            * **การคูณ:** พิมพ์ `2x` หรือ `2*x` (ระบบรองรับการละเครื่องหมายคูณ)
            * **เอกซ์โพเนนเชียล:** พิมพ์ `e^x` หรือ `exp(x)`
            * **ลอการิทึมธรรมชาติ:** พิมพ์ `ln(x)` หรือ `log(x)`
            * **สแควร์รูท:** พิมพ์ `sqrt(x)` (เช่น `sqrt(x^2 + 1)`)
            * **ฟังก์ชันตรีโกณมิติ:** พิมพ์ `sin(x)`, `cos(x)`, `tan(x)`
            * **ฟังก์ชันตรีโกณมิติผกผัน:** พิมพ์ `arcsin(x)` หรือ `asin(x)`, `arccos(x)` หรือ `acos(x)`, `arctan(x)` หรือ `atan(x)`
            * **เศษส่วน:** ให้ใส่วงเล็บกำกับ เช่น `1/(x+1)` หรือ `(x^2-4)/(x-2)`
            """
        )

