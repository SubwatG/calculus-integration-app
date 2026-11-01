import sys
import re
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path

W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
ET.register_namespace('w', W_NS)
ET.register_namespace('m', 'http://schemas.openxmlformats.org/officeDocument/2006/math')
ET.register_namespace('r', 'http://schemas.openxmlformats.org/officeDocument/2006/relationships')
ET.register_namespace('v', 'urn:schemas-microsoft-com:vml')
ET.register_namespace('wp', 'http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing')
ET.register_namespace('a', 'http://schemas.openxmlformats.org/drawingml/2006/main')
ET.register_namespace('pic', 'http://schemas.openxmlformats.org/drawingml/2006/picture')

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
MATH_RPR_RED = (
    '<w:rPr>'
    f'<w:rFonts w:ascii="{MATH_FONT}" w:hAnsi="{MATH_FONT}"'
    f' w:eastAsia="{MATH_FONT}" w:cs="{MATH_FONT}" />'
    f'<w:sz w:val="{MATH_SIZE}" />'
    f'<w:szCs w:val="{MATH_SIZE}" />'
    '<w:color w:val="C00000" />'
    '<w:b /><w:bCs />'
    '<w:i />'
    '</w:rPr>'
)

TABLE_BORDERS = (
    '<w:tblBorders>'
    '<w:top w:val="single" w:sz="8" w:space="0" w:color="000000"/>'
    '<w:left w:val="none"/>'
    '<w:bottom w:val="single" w:sz="8" w:space="0" w:color="000000"/>'
    '<w:right w:val="none"/>'
    '<w:insideH w:val="single" w:sz="4" w:space="0" w:color="D3D3D3"/>'
    '<w:insideV w:val="none"/>'
    '</w:tblBorders>'
)
TABLE_CELL_MAR = (
    '<w:tblCellMar>'
    '<w:top w:w="60" w:type="dxa"/>'
    '<w:bottom w:w="60" w:type="dxa"/>'
    '<w:left w:w="100" w:type="dxa"/>'
    '<w:right w:w="100" w:type="dxa"/>'
    '</w:tblCellMar>'
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

                # 2. Inject Cambria Math into all math runs <m:r> (with red math support for RedText paragraphs)
                def fix_p_math(p_match):
                    p_xml = p_match.group(0)
                    is_red_p = 'w:val="RedText"' in p_xml
                    def repl_math(m_match):
                        nonlocal math_count
                        body = m_match.group(1)
                        cleaned = re.sub(r"<w:rPr>.*?</w:rPr>", "", body, flags=re.DOTALL)
                        math_count += 1
                        rpr = MATH_RPR_RED if is_red_p else MATH_RPR
                        return f"<m:r>{rpr}{cleaned}</m:r>"
                    return re.sub(r"<m:r>(.*?)</m:r>", repl_math, p_xml, flags=re.DOTALL)

                xml = re.sub(r"<w:p\b.*?</w:p>", fix_p_math, xml, flags=re.DOTALL)

                # 3. Add table borders and compact margins to tables
                def repl_tbl(match):
                    tbl_pr = match.group(1)
                    if "<w:tblBorders" not in tbl_pr:
                        tbl_pr = tbl_pr + TABLE_BORDERS
                    if "<w:tblCellMar" not in tbl_pr:
                        tbl_pr = tbl_pr + TABLE_CELL_MAR
                    return f"<w:tblPr>{tbl_pr}</w:tblPr>"

                xml = re.sub(r"<w:tblPr>(.*?)</w:tblPr>", repl_tbl, xml, flags=re.DOTALL)

                # 3b. Make paragraphs inside table cells compact
                def repl_tc(match):
                    tc_xml = match.group(0)
                    def repl_tc_p(p_match):
                        p_xml = p_match.group(0)
                        if "<w:pPr>" in p_xml:
                            p_xml = re.sub(r"<w:spacing[^>]*/>", '<w:spacing w:after="20" w:line="240" w:lineRule="auto"/>', p_xml)
                            if "<w:spacing" not in p_xml:
                                p_xml = p_xml.replace("<w:pPr>", '<w:pPr><w:spacing w:after="20" w:line="240" w:lineRule="auto"/>')
                        else:
                            p_xml = f'<w:p><w:pPr><w:spacing w:after="20" w:line="240" w:lineRule="auto"/></w:pPr>{p_xml[5:]}'
                        return p_xml
                    return re.sub(r"<w:p\b.*?</w:p>", repl_tc_p, tc_xml, flags=re.DOTALL)

                xml = re.sub(r"<w:tc\b.*?</w:tc>", repl_tc, xml, flags=re.DOTALL)

                # 4. Inject crimson red color (#C00000) and bold into any run with RedText
                def repl_red_run(m):
                    r_pr = m.group(1)
                    if 'w:val="RedText"' in r_pr:
                        if '<w:color' not in r_pr:
                            r_pr += '<w:color w:val="C00000"/>'
                        else:
                            r_pr = re.sub(r'<w:color\s+[^>]*/>', '<w:color w:val="C00000"/>', r_pr)
                        if '<w:b/>' not in r_pr:
                            r_pr += '<w:b/><w:bCs/>'
                    return f'<w:rPr>{r_pr}</w:rPr>'

                xml = re.sub(r"<w:rPr>(.*?)</w:rPr>", repl_red_run, xml, flags=re.DOTALL)

                # 5. Proportionate column widths for tables
                try:
                    dtree = ET.fromstring(xml.encode("utf-8"))
                    tables_resized = 0
                    for tbl in dtree.iter(f"{{{W_NS}}}tbl"):
                        first_tr = tbl.find(f"{{{W_NS}}}tr")
                        if first_tr is None:
                            continue
                        cells = list(first_tr.iter(f"{{{W_NS}}}tc"))
                        n_cols = len(cells)

                        col_widths = None
                        if n_cols == 4:
                            # Col 0: ID (1100 dxa ~ 1.9 cm)
                            # Col 1: Expr & Condition (2500 dxa ~ 4.4 cm)
                            # Col 2: Status (1100 dxa ~ 1.9 cm)
                            # Col 3: Justification & Math details (4500 dxa ~ 7.9 cm)
                            col_widths = [1100, 2500, 1100, 4500]
                        elif n_cols == 6:
                            c0_text = "".join(cells[0].itertext())
                            if "ลำดับ" in c0_text or "test_" in c0_text:
                                col_widths = [700, 2200, 3700, 800, 800, 1000]
                            else:
                                col_widths = [2000, 2600, 1100, 1300, 900, 1300]

                        if col_widths:
                            tables_resized += 1
                            tbl_pr = tbl.find(f"{{{W_NS}}}tblPr")
                            if tbl_pr is not None:
                                tbl_w = tbl_pr.find(f"{{{W_NS}}}tblW")
                                if tbl_w is None:
                                    tbl_w = ET.SubElement(tbl_pr, f"{{{W_NS}}}tblW")
                                tbl_w.set(f"{{{W_NS}}}w", "9200")
                                tbl_w.set(f"{{{W_NS}}}type", "dxa")

                            grid = tbl.find(f"{{{W_NS}}}tblGrid")
                            if grid is not None:
                                tbl.remove(grid)
                            new_grid = ET.Element(f"{{{W_NS}}}tblGrid")
                            for w in col_widths:
                                gc = ET.SubElement(new_grid, f"{{{W_NS}}}gridCol")
                                gc.set(f"{{{W_NS}}}w", str(w))
                            idx = list(tbl).index(tbl_pr) + 1 if tbl_pr is not None else 0
                            tbl.insert(idx, new_grid)

                            for tr in tbl.iter(f"{{{W_NS}}}tr"):
                                r_cells = list(tr.iter(f"{{{W_NS}}}tc"))
                                if len(r_cells) == len(col_widths):
                                    for tc, w in zip(r_cells, col_widths):
                                        tcpr = tc.find(f"{{{W_NS}}}tcPr")
                                        if tcpr is None:
                                            tcpr = ET.Element(f"{{{W_NS}}}tcPr")
                                            tc.insert(0, tcpr)
                                        tcw = tcpr.find(f"{{{W_NS}}}tcW")
                                        if tcw is None:
                                            tcw = ET.SubElement(tcpr, f"{{{W_NS}}}tcW")
                                        tcw.set(f"{{{W_NS}}}w", str(w))
                                        tcw.set(f"{{{W_NS}}}type", "dxa")

                    xml = ET.tostring(dtree, encoding="utf-8").decode("utf-8")
                except Exception as e:
                    print(f"Warning: Table resizing skipped due to: {e}")

                data = xml.encode("utf-8")

            elif item.filename == "word/styles.xml":
                xml = data.decode("utf-8")

                # Define RedText character style if not present
                if 'w:styleId="RedText"' not in xml:
                    red_style = (
                        '<w:style w:type="character" w:customStyle="1" w:styleId="RedText">'
                        '<w:name w:val="RedText"/>'
                        '<w:basedOn w:val="DefaultParagraphFont"/>'
                        '<w:uiPriority w:val="1"/>'
                        '<w:qFormat/>'
                        '<w:rPr>'
                        '<w:color w:val="C00000"/>'
                        '<w:b/>'
                        '<w:bCs/>'
                        '</w:rPr>'
                        '</w:style>'
                    )
                    xml = xml.replace('</w:styles>', f'{red_style}</w:styles>')

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
                xml = re.sub(r'<w:style[^>]*w:styleId="Heading4"[^>]*>.*?</w:style>', fix_h3, xml, flags=re.DOTALL)
                xml = re.sub(r'<w:style[^>]*w:styleId="Heading3Char"[^>]*>.*?</w:style>', fix_h3, xml, flags=re.DOTALL)
                xml = re.sub(r'<w:style[^>]*w:styleId="Heading4Char"[^>]*>.*?</w:style>', fix_h3, xml, flags=re.DOTALL)

                # VerbatimChar & SourceCode: 16pt (sz=32) TH SarabunPSK
                def fix_verbatim(m):
                    block = m.group(0)
                    block = re.sub(r'<w:sz\s+w:val="[^"]*"\s*/>', '<w:sz w:val="32"/>', block)
                    block = re.sub(r'<w:szCs\s+w:val="[^"]*"\s*/>', '<w:szCs w:val="32"/>', block)
                    block = re.sub(r'<w:szCs\s*/>', '<w:szCs w:val="32"/>', block)
                    if '<w:sz ' not in block and '<w:sz/' not in block:
                        block = re.sub(r'(<w:rPr[^>]*>)', r'\1<w:sz w:val="32"/><w:szCs w:val="32"/>', block)
                    block = re.sub(r'w:ascii="[^"]*"', 'w:ascii="TH SarabunPSK"', block)
                    block = re.sub(r'w:hAnsi="[^"]*"', 'w:hAnsi="TH SarabunPSK"', block)
                    block = re.sub(r'w:cs="[^"]*"', 'w:cs="TH SarabunPSK"', block)
                    return block

                xml = re.sub(r'<w:style[^>]*w:styleId="VerbatimChar"[^>]*>.*?</w:style>', fix_verbatim, xml, flags=re.DOTALL)
                xml = re.sub(r'<w:style[^>]*w:styleId="SourceCode"[^>]*>.*?</w:style>', fix_verbatim, xml, flags=re.DOTALL)

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
