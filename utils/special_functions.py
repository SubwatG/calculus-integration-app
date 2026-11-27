"""Detect special functions that are outside the Calculus 1 syllabus.

The app relies on SymPy, which happily returns erf, Si, li and friends for
integrals that have no elementary antiderivative. Showing those symbols without
explanation makes students think the app computed something wrong, so every page
that renders an antiderivative asks this module first.
"""

from __future__ import annotations

import sympy as sp

# SymPy function class name -> (Thai name, one-line meaning, LaTeX name)
SPECIAL_FUNCTIONS: dict[str, tuple[str, str, str]] = {
    "erf": (
        "ฟังก์ชันความคลาดเคลื่อน",
        r"$\operatorname{erf}(x)=\frac{2}{\sqrt{\pi}}\int_0^x e^{-t^2}\,dt$ ใช้ในความน่าจะเป็นและการแพร่",
        r"\operatorname{erf}",
    ),
    "erfc": (
        "ฟังก์ชันความคลาดเคลื่อนส่วนเติมเต็ม",
        r"$\operatorname{erfc}(x)=1-\operatorname{erf}(x)$",
        r"\operatorname{erfc}",
    ),
    "erfi": (
        "ฟังก์ชันความคลาดเคลื่อนจินตภาพ",
        r"$\operatorname{erfi}(x)=-i\,\operatorname{erf}(ix)$",
        r"\operatorname{erfi}",
    ),
    "Si": (
        "ฟังก์ชันไซน์อินทิกรัล",
        r"$\operatorname{Si}(x)=\int_0^x \frac{\sin t}{t}\,dt$",
        r"\operatorname{Si}",
    ),
    "Ci": (
        "ฟังก์ชันโคไซน์อินทิกรัล",
        r"$\operatorname{Ci}(x)=-\int_x^\infty \frac{\cos t}{t}\,dt$",
        r"\operatorname{Ci}",
    ),
    "li": (
        "ฟังก์ชันลอการิทึมอินทิกรัล",
        r"$\operatorname{li}(x)=\int_0^x \frac{dt}{\ln t}$",
        r"\operatorname{li}",
    ),
    "Li": (
        "ฟังก์ชันโพลีลอการิทึม",
        r"$\operatorname{Li}(x)$ นิยามผ่านผลบวกอนันต์ ใช้ในทฤษฎีจำนวน",
        r"\operatorname{Li}",
    ),
    "Ei": (
        "ฟังก์ชันเอกซ์โพเนนเชียลอินทิกรัล",
        r"$\operatorname{Ei}(x)=\int_{-\infty}^{x} \frac{e^{t}}{t}\,dt$",
        r"\operatorname{Ei}",
    ),
    "gamma": (
        "ฟังก์ชันแกมมา",
        r"$\Gamma(x)=\int_0^\infty t^{x-1}e^{-t}\,dt$ ขยายแฟกทอเรียลไปยังจำนวนจริง",
        r"\Gamma",
    ),
    "lowergamma": (
        "ฟังก์ชันแกมมาไม่สมบูรณ์",
        r"$\gamma(a,x)$ คืออินทิกรัลของ $t^{a-1}e^{-t}$ บางช่วง",
        r"\gamma",
    ),
    "uppergamma": (
        "ฟังก์ชันแกมมาไม่สมบูรณ์",
        r"$\Gamma(a,x)$ คืออินทิกรัลของ $t^{a-1}e^{-t}$ บางช่วง",
        r"\Gamma",
    ),
    "hyper": (
        "ฟังก์ชันไฮเปอร์จีโอเมตริก",
        r"${}_pF_q$ เขียนอนุกรมกำลังทั่วไปในรูปเดียว",
        r"{}_pF_q",
    ),
    "zeta": (
        "ฟังก์ชันซีตา",
        r"$\zeta(s)=\sum_{n=1}^{\infty} n^{-s}$",
        r"\zeta",
    ),
    "LambertW": (
        "ฟังก์ชันแลมเบิร์ตดับเบิลยู",
        r"$W(x)$ คือคำตอบของ $We^{W}=x$",
        r"W",
    ),
    "besselj": (
        "ฟังก์ชันเบสเซล",
        r"$J_n(x)$ เป็นคำตอบของสมการเชิงอนุพันธ์แบบเบสเซล",
        r"J_n",
    ),
    "bessely": (
        "ฟังก์ชันเบสเซลชนิดที่สอง",
        r"$Y_n(x)$ เป็นคำตอบอิสระอีกตัวของสมการเบสเซล",
        r"Y_n",
    ),
}


def special_functions_in(expr) -> list[str]:
    """Return the special-function names used by a SymPy expression, in order."""
    if expr is None:
        return []
    if isinstance(expr, str):
        return []
    try:
        atoms = expr.atoms(sp.Function)
    except AttributeError:
        return []
    found: list[str] = []
    for atom in atoms:
        name = atom.func.__name__
        if name in SPECIAL_FUNCTIONS and name not in found:
            found.append(name)
    return found


def has_special_function(expr) -> bool:
    """True when the expression needs a special function to be written exactly."""
    return bool(special_functions_in(expr))


def describe_special_functions(names: list[str]) -> str:
    """One short Thai sentence naming the functions, their meaning and the scope."""
    if not names:
        return ""
    parts = []
    for name in names:
        thai_name, _, _ = SPECIAL_FUNCTIONS[name]
        parts.append(f"{thai_name} ({name})")
    details = " ".join(SPECIAL_FUNCTIONS[name][1] for name in names)
    return (
        "คำตอบนี้ต้องใช้ฟังก์ชันพิเศษ " + " และ ".join(parts)
        + " ซึ่งอยู่นอกหลักสูตร Calculus 1 โดย " + details
    )


def latex_names(names: list[str]) -> str:
    """Comma-separated LaTeX names for a compact inline notice."""
    return ", ".join(SPECIAL_FUNCTIONS[name][2] for name in names)


def numeric_approximation(expr, digits: int = 10):
    """Return a numeric approximation of an exact value, or None when impossible."""
    if expr is None or isinstance(expr, str):
        return None
    try:
        return sp.N(expr, digits)
    except Exception:
        return None
