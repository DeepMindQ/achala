#!/usr/bin/env python3
"""Post-process the audit docx: patch footer PAGE fields with format switches
(ROMAN for front-matter section, arabic for body) and strip empty <w:pgNumType/>."""
import re
import shutil
import sys
import zipfile

DOC = "/home/z/my-project/download/Achala_Content_Audit_Change_Register.docx"
TMP = DOC + ".tmp"


def main():
    zin = zipfile.ZipFile(DOC, "r")
    names = zin.namelist()
    docxml = zin.read("word/document.xml").decode("utf-8")

    # 1. strip empty pgNumType (cover section)
    docxml_new = docxml.replace("<w:pgNumType/>", "")

    # 2. map sections -> footer rels. Find sectPr blocks in order.
    sects = re.findall(r"<w:sectPr[\s\S]*?</w:sectPr>", docxml_new)
    info = []
    for i, s in enumerate(sects):
        fmt = None
        m = re.search(r'<w:pgNumType[^>]*w:fmt="([^"]+)"', s)
        if m:
            fmt = m.group(1)
        foots = re.findall(r'<w:footerReference[^>]*r:id="([^"]+)"', s)
        info.append((i, fmt, foots))
    print("sections:", info)

    rels = zin.read("word/_rels/document.xml.rels").decode("utf-8")
    relmap = dict(re.findall(r'<Relationship Id="([^"]+)"[^>]*Target="([^"]+)"', rels))

    footer_fmt = {}
    for i, fmt, foots in info:
        for rid in foots:
            target = relmap.get(rid, "")
            fname = "word/" + target.lstrip("/")
            if fmt == "upperRoman" or fmt == "lowerRoman":
                footer_fmt[fname] = "ROMAN"
            elif fmt in ("decimal", None):
                footer_fmt.setdefault(fname, "arabic")

    zout = zipfile.ZipFile(TMP, "w", zipfile.ZIP_DEFLATED)
    for item in names:
        data = zin.read(item)
        if item == "word/document.xml":
            data = docxml_new.encode("utf-8")
        elif item in footer_fmt:
            xml = data.decode("utf-8")
            switch = footer_fmt[item]
            xml, n = re.subn(
                r"(<w:instrText[^>]*>)\s*PAGE\s*(</w:instrText>)",
                r"\g<1> PAGE \\* " + switch + r" \\* MERGEFORMAT \g<2>",
                xml,
            )
            print(f"patched {item}: {n} field(s) -> {switch}")
            data = xml.encode("utf-8")
        zout.writestr(item, data)
    zout.close()
    zin.close()
    shutil.move(TMP, DOC)
    print("done")


if __name__ == "__main__":
    main()
