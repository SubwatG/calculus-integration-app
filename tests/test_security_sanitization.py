import pytest
from utils.sympy_solver import sanitize_math_input, integrate, differentiate


def test_sanitize_valid_math():
    valid_expressions = [
        "x^2 + 3*x - 5",
        "sin(x)*cos(x)",
        "exp(-x^2)",
        "ln(x+1)",
        "sqrt(4-x^2)",
        "1/(x^2 + 1)",
        "3*t^2 + 2*t",
        "cosh(x) + sinh(x)",
        "x^3 - 2*x",
    ]
    for expr in valid_expressions:
        assert sanitize_math_input(expr) == expr


def test_sanitize_blocks_quotes():
    payloads = [
        '__import__("os").getcwd()',
        "open('/etc/hostname').read()",
        "exec('y = 1')",
        "`cat /etc/passwd`",
    ]
    for p in payloads:
        with pytest.raises(ValueError, match="quotes|เซมิโคลอน"):
            sanitize_math_input(p)


def test_sanitize_blocks_dunder_and_builtins():
    payloads = [
        "__class__",
        "__subclasses__",
        "__builtins__",
        "builtins.open",
        "globals()",
        "locals()",
    ]
    for p in payloads:
        with pytest.raises(ValueError, match="ตรวจพบคีย์เวิร์ด"):
            sanitize_math_input(p)


def test_sanitize_blocks_dangerous_modules():
    payloads = [
        "import sys",
        "subprocess.call",
        "os.system",
        "requests.get",
        "urllib.request",
    ]
    for p in payloads:
        with pytest.raises(ValueError, match="ตรวจพบ"):
            sanitize_math_input(p)


def test_sanitize_blocks_excessive_length():
    huge_input = "x + " * 250 + "1"
    with pytest.raises(ValueError, match="ยาวเกินกำหนด"):
        sanitize_math_input(huge_input)


def test_integrate_safely_handles_payloads():
    payload = "__import__('os').system('id')"
    res = integrate(payload)
    assert res["ok"] is False
    assert res["result"] is None


def test_differentiate_safely_handles_payloads():
    payload = "open('/etc/hostname').read()"
    res = differentiate(payload)
    assert res["ok"] is False
    assert res["result"] is None
