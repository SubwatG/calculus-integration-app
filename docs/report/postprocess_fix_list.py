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

                # 3. Ensure Heading 1 / Title runs have TH SarabunPSK 20pt (sz=40) Bold Black
                # Pandoc applies pStyle Heading1
                data = xml.encode("utf-8")

            elif item.filename == "word/styles.xml":
                xml = data.decode("utf-8")

                # Force TH SarabunPSK on all styles
                xml = re.sub(r'w:ascii="[^"]*"', 'w:ascii="TH SarabunPSK"', xml)
                xml = re.sub(r'w:hAnsi="[^"]*"', 'w:hAnsi="TH SarabunPSK"', xml)
                xml = re.sub(r'w:eastAsia="[^"]*"', 'w:eastAsia="TH SarabunPSK"', xml)
                xml = re.sub(r'w:cs="[^"]*"', 'w:cs="TH SarabunPSK"', xml)

                # Set Heading 1 & Title to sz=40 (20pt) Bold Black
                def fix_heading1_style(m):
                    style_block = m.group(0)
                    # Replace or insert sz=40
                    style_block = re.sub(r'<w:sz w:val="[^"]*"/>', '<w:sz w:val="40"/>', style_block)
                    style_block = re.sub(r'<w:szCs w:val="[^"]*"/>', '<w:szCs w:val="40"/>', style_block)
                    style_block = re.sub(r'<w:color w:val="[^"]*"/>', '<w:color w:val="000000"/>', style_block)
                    return style_block

                xml = re.sub(r'<w:style[^>]*w:styleId="Heading1"[^>]*>.*?</w:style>', fix_heading1_style, xml, flags=re.DOTALL)
                xml = re.sub(r'<w:style[^>]*w:styleId="Title"[^>]*>.*?</w:style>', fix_heading1_style, xml, flags=re.DOTALL)

                data = xml.encode("utf-8")

            zout.writestr(item, data)

    temp_out.replace(path)
    print(f"[SUCCESS] Post-processed {path.name}:")
    print(f"  - TH SarabunPSK 20pt Bold Black applied to Heading 1 and Title")
    print(f"  - All paragraph bottom borders (w:pBdr) removed")
    print(f"  - Cambria Math 12pt applied to {math_count} math runs")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        postprocess_docx(sys.argv[1])
