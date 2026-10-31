#!/usr/bin/env python3
"""
fix_math_cambria.py
-------------------
Post-processor สำหรับปรับแต่งสมการคณิตศาสตร์ (OMML) ที่ Pandoc/Quarto สร้างขึ้น
ให้เป็นฟอนต์ Cambria Math ขนาด 12pt อย่างชัดเจน

เหตุผล: Pandoc สร้างแท็ก m:r โดยไม่มี w:rPr ฝังอยู่ ทำให้โปรแกรม Word/LibreOffice
เลือกขนาดและฟอนต์ตามเอกสารแวดล้อม (ซึ่งอาจเป็น TH SarabunPSK 16pt)
สคริปต์นี้จะเติม w:rPr ที่ระบุ Cambria Math + sz 24 half-points (12pt) ลงไป

ใช้งาน:
    python3 fix_math_cambria.py path/to/file.docx [path/to/another.docx ...]
"""

import re
import shutil
import sys
import zipfile
from pathlib import Path

MATH_FONT = "Cambria Math"
MATH_SIZE = "24"  # 24 half-points = 12pt

MATH_RPR = (
    '<w:rPr>'
    f'<w:rFonts w:ascii="{MATH_FONT}" w:hAnsi="{MATH_FONT}"'
    f' w:eastAsia="{MATH_FONT}" w:cs="{MATH_FONT}" />'
    f'<w:sz w:val="{MATH_SIZE}" />'
    f'<w:szCs w:val="{MATH_SIZE}" />'
    '<w:i />'
    '</w:rPr>'
)


def inject_math_rpr(xml_content: str) -> tuple[str, int]:
    """
    เติม <w:rPr> (Cambria Math 12pt) ให้ทุก m:r ที่ยังไม่มี
    m:r ที่มีอยู่แล้วจะถูกแทนที่ด้วย MATH_RPR เพื่อให้ทั้งเอกสารมีขนาดเดียวกัน
    """
    count = 0

    def repl(match):
        nonlocal count
        run_body = match.group(1)
        # ลบ w:rPr เดิม (ถ้ามี)
        cleaned = re.sub(r"<w:rPr>.*?</w:rPr>", "", run_body, flags=re.DOTALL)
        count += 1
        return f"<m:r>{MATH_RPR}{cleaned}</m:r>"

    new_xml = re.sub(r"<m:r>(.*?)</m:r>", repl, xml_content, flags=re.DOTALL)
    return new_xml, count


def set_math_defaults(styles_xml: str) -> str:
    """
    กำหนด default font ใน docDefaults เพื่อให้สมการที่ไม่มี w:rPr
    (หรือสมการที่สร้างจาก OMML อื่น) แสดงเป็น Cambria Math 12pt
    """
    math_defaults = (
        f'<w:rFonts w:ascii="{MATH_FONT}" w:hAnsi="{MATH_FONT}"'
        f' w:eastAsia="{MATH_FONT}" w:cs="{MATH_FONT}" />'
        f'<w:sz w:val="{MATH_SIZE}" />'
        f'<w:szCs w:val="{MATH_SIZE}" />'
    )

    def repl(match):
        return (
            "<w:rPrDefault><w:rPr>"
            + match.group(1)
            + math_defaults
            + "</w:rPr></w:rPrDefault>"
        )

    # แทนที่ rPrDefault เดิม (ถ้ามี)
    result, n = re.subn(
        r"<w:rPrDefault>\s*<w:rPr>(.*?)</w:rPr>\s*</w:rPrDefault>",
        repl,
        styles_xml,
        count=1,
        flags=re.DOTALL,
    )
    if n == 0:
        # ไม่มี rPrDefault → แทรกใหม่
        result = re.sub(
            r"(<w:docDefaults>)",
            r"\1<w:rPrDefault><w:rPr>" + math_defaults + "</w:rPr></w:rPrDefault>",
            styles_xml,
            count=1,
        )
    return result


def process_docx(docx_path: Path) -> None:
    if not docx_path.exists():
        print(f"[SKIP] ไม่พบไฟล์: {docx_path}")
        return

    temp_out = docx_path.with_suffix(".tmp.docx")
    math_count = 0

    with zipfile.ZipFile(docx_path, "r") as zin, zipfile.ZipFile(
        temp_out, "w", zipfile.ZIP_DEFLATED
    ) as zout:
        for item in zin.infolist():
            data = zin.read(item.filename)

            if item.filename == "word/document.xml":
                xml = data.decode("utf-8")
                xml, math_count = inject_math_rpr(xml)
                data = xml.encode("utf-8")

            elif item.filename == "word/styles.xml":
                xml = data.decode("utf-8")
                xml = set_math_defaults(xml)
                data = xml.encode("utf-8")

            zout.writestr(item, data)

    temp_out.replace(docx_path)
    print(f"[OK] {docx_path.name}: Cambria Math 12pt applied to {math_count} math runs")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 fix_math_cambria.py path/to/file.docx ...")
        sys.exit(1)

    for path_str in sys.argv[1:]:
        process_docx(Path(path_str))
