import sys
import re
import zipfile
from pathlib import Path

MATH_FONT = "Cambria Math"
MATH_SIZE = "24"  # 12pt (half-points)
MATH_RPR = (
    '<w:rPr>'
    f'<w:rFonts w:ascii="{MATH_FONT}" w:hAnsi="{MATH_FONT}"'
    f' w:eastAsia="{MATH_FONT}" w:cs="{MATH_FONT}" />'
    f'<w:sz w:val="{MATH_SIZE}" />'
    f'<w:szCs w:val="{MATH_SIZE}" />'
    '<w:i />'
    '</w:rPr>'
)

TABLE_BORDERS = (
    '<w:tblBorders>'
    '<w:top w:val="single" w:sz="8" w:space="0" w:color="000000"/>'
    '<w:left w:val="none"/>'
    '<w:bottom w:val="single" w:sz="8" w:space="0" w:color="000000"/>'
    '<w:right w:val="none"/>'
    '<w:insideH w:val="single" w:sz="4" w:space="0" w:color="CCCCCC"/>'
    '<w:insideV w:val="none"/>'
    '</w:tblBorders>'
)

def postprocess_docx(docx_path: str):
    path = Path(docx_path)
    if not path.exists():
        print(f"Error: {docx_path} not found")
        sys.exit(1)

    temp_out = path.with_suffix(".tmp.docx")
    math_count = 0

    with zipfile.ZipFile(path, "r") as zin, zipfile.ZipFile(temp_out, "w", compression=zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            data = zin.read(item.filename)

            if item.filename == "word/document.xml":
                xml = data.decode("utf-8")

                # 1. Remove all w:pBdr (paragraph borders)
                xml = re.sub(r"<w:pBdr>.*?</w:pBdr>", "", xml, flags=re.DOTALL)

                # 2. Inject Cambria Math into all math runs <m:r>
                def repl_math(match):
                    nonlocal math_count
                    body = match.group(1)
                    cleaned = re.sub(r"<w:rPr>.*?</w:rPr>", "", body, flags=re.DOTALL)
                    math_count += 1
                    return f"<m:r>{MATH_RPR}{cleaned}</m:r>"

                xml = re.sub(r"<m:r>(.*?)</m:r>", repl_math, xml, flags=re.DOTALL)

                # 3. Add table borders to tables missing tblBorders
                def repl_tbl(match):
                    tbl_pr = match.group(1)
                    if "<w:tblBorders" not in tbl_pr:
                        tbl_pr = tbl_pr + TABLE_BORDERS
                    return f"<w:tblPr>{tbl_pr}</w:tblPr>"

                xml = re.sub(r"<w:tblPr>(.*?)</w:tblPr>", repl_tbl, xml, flags=re.DOTALL)

                data = xml.encode("utf-8")

            elif item.filename == "word/styles.xml":
                xml = data.decode("utf-8")

                # Strip theme overrides so font falls back strictly to TH SarabunPSK
                xml = re.sub(r'w:asciiTheme="[^"]*"', '', xml)
                xml = re.sub(r'w:hAnsiTheme="[^"]*"', '', xml)
                xml = re.sub(r'w:eastAsiaTheme="[^"]*"', '', xml)
                xml = re.sub(r'w:cstheme="[^"]*"', '', xml)

                # Force TH SarabunPSK on all font attributes
                xml = re.sub(r'w:ascii="[^"]*"', 'w:ascii="TH SarabunPSK"', xml)
                xml = re.sub(r'w:hAnsi="[^"]*"', 'w:hAnsi="TH SarabunPSK"', xml)
                xml = re.sub(r'w:eastAsia="[^"]*"', 'w:eastAsia="TH SarabunPSK"', xml)
                xml = re.sub(r'w:cs="[^"]*"', 'w:cs="TH SarabunPSK"', xml)

                # Strip blue / theme colors from headings
                xml = re.sub(r'w:themeColor="[^"]*"', '', xml)
                xml = re.sub(r'w:themeShade="[^"]*"', '', xml)

                # Heading 1 & Title: 20pt (sz=40) Bold Black
                def fix_h1_title(m):
                    block = m.group(0)
                    block = re.sub(r'<w:sz\s+w:val="[^"]*"\s*/>', '<w:sz w:val="40"/>', block)
                    block = re.sub(r'<w:szCs\s+w:val="[^"]*"\s*/>', '<w:szCs w:val="40"/>', block)
                    if '<w:color' in block:
                        block = re.sub(r'<w:color\s+[^>]*/>', '<w:color w:val="000000"/>', block)
                    else:
                        block = re.sub(r'(<w:rPr[^>]*>)', r'\1<w:color w:val="000000"/>', block)
                    if "<w:b/>" not in block and "<w:b " not in block:
                        block = re.sub(r'(<w:rPr[^>]*>)', r'\1<w:b/><w:bCs/>', block)
                    return block

                xml = re.sub(r'<w:style[^>]*w:styleId="Heading1"[^>]*>.*?</w:style>', fix_h1_title, xml, flags=re.DOTALL)
                xml = re.sub(r'<w:style[^>]*w:styleId="Title"[^>]*>.*?</w:style>', fix_h1_title, xml, flags=re.DOTALL)
                xml = re.sub(r'<w:style[^>]*w:styleId="TitleChar"[^>]*>.*?</w:style>', fix_h1_title, xml, flags=re.DOTALL)
                xml = re.sub(r'<w:style[^>]*w:styleId="Heading1Char"[^>]*>.*?</w:style>', fix_h1_title, xml, flags=re.DOTALL)

                # Heading 2: 18pt (sz=36) Bold Black
                def fix_h2(m):
                    block = m.group(0)
                    block = re.sub(r'<w:sz w:val="[^"]*"/>', '<w:sz w:val="36"/>', block)
                    block = re.sub(r'<w:szCs w:val="[^"]*"/>', '<w:szCs w:val="36"/>', block)
                    block = re.sub(r'<w:color [^>]*/>', '<w:color w:val="000000"/>', block)
                    if "<w:b/>" not in block and "<w:b " not in block:
                        block = re.sub(r'(<w:rPr>)', r'\1<w:b/><w:bCs/>', block)
                    return block

                xml = re.sub(r'<w:style[^>]*w:styleId="Heading2"[^>]*>.*?</w:style>', fix_h2, xml, flags=re.DOTALL)

                # Heading 3: 16pt (sz=32) Bold Black
                def fix_h3(m):
                    block = m.group(0)
                    block = re.sub(r'<w:sz w:val="[^"]*"/>', '<w:sz w:val="32"/>', block)
                    block = re.sub(r'<w:szCs w:val="[^"]*"/>', '<w:szCs w:val="32"/>', block)
                    block = re.sub(r'<w:color [^>]*/>', '<w:color w:val="000000"/>', block)
                    if "<w:b/>" not in block and "<w:b " not in block:
                        block = re.sub(r'(<w:rPr>)', r'\1<w:b/><w:bCs/>', block)
                    return block

                xml = re.sub(r'<w:style[^>]*w:styleId="Heading3"[^>]*>.*?</w:style>', fix_h3, xml, flags=re.DOTALL)

                data = xml.encode("utf-8")

            zout.writestr(item, data)

    temp_out.replace(path)
    print(f"[SUCCESS] Post-processed {path.name}:")
    print(f"  - TH SarabunPSK 20pt Bold Black applied to Heading 1 and Title")
    print(f"  - TH SarabunPSK 18pt Bold Black applied to Heading 2")
    print(f"  - Theme fonts & colors stripped (no Tahoma / no Blue #0F4761)")
    print(f"  - All paragraph bottom borders (w:pBdr) removed")
    print(f"  - Table borders verified")
    print(f"  - Cambria Math 12pt applied to {math_count} math runs")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        postprocess_docx(sys.argv[1])
