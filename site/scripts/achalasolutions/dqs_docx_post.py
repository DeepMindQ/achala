# -*- coding: utf-8 -*-
"""Post-process docx: patch footer PAGE fields with format switches (ROMAN/arabic),
remove empty pgNumType (docx skill WPS-compatibility rules)."""

import sys, zipfile, re, shutil, os, tempfile

def patch(path):
    tmpdir = tempfile.mkdtemp()
    try:
        with zipfile.ZipFile(path) as z:
            z.extractall(tmpdir)
        docx_xml_path = os.path.join(tmpdir, "word", "document.xml")
        with open(docx_xml_path, "r", encoding="utf-8") as f:
            doc = f.read()

        # remove empty pgNumType (cover section)
        doc = re.sub(r"<w:pgNumType/>", "", doc)

        # map footer rels
        rels_path = os.path.join(tmpdir, "word", "_rels", "document.xml.rels")
        with open(rels_path, "r", encoding="utf-8") as f:
            rels = f.read()
        rid_to_file = dict(re.findall(r'Id="(rId\d+)"[^>]*Target="(footer\d+\.xml)"', rels))

        # find sections: sectPr blocks with footerReference + pgNumType fmt
        footer_fmt = {}  # footer file -> ROMAN|arabic
        for sect in re.findall(r"<w:sectPr[^>]*>.*?</w:sectPr>", doc, re.S):
            fmt = None
            m = re.search(r'<w:pgNumType[^>]*w:fmt="([^"]+)"', sect)
            if m:
                fmt = m.group(1)
            for rid in re.findall(r'<w:footerReference[^>]*r:id="(rId\d+)"', sect):
                ffile = rid_to_file.get(rid)
                if ffile and fmt:
                    footer_fmt[ffile] = "ROMAN" if "oman" in fmt.lower() or "upperRoman" == fmt else "arabic"

        for ffile, fmt in footer_fmt.items():
            fpath = os.path.join(tmpdir, "word", ffile)
            if not os.path.exists(fpath):
                continue
            with open(fpath, "r", encoding="utf-8") as f:
                fx = f.read()
            fx = re.sub(r"(<w:instrText[^>]*>)\s*PAGE\s*(</w:instrText>)",
                        r"\1 PAGE \\* " + fmt + r" \\* MERGEFORMAT \2", fx)
            with open(fpath, "w", encoding="utf-8") as f:
                f.write(fx)

        with open(docx_xml_path, "w", encoding="utf-8") as f:
            f.write(doc)

        # rezip
        newpath = path + ".tmp"
        with zipfile.ZipFile(newpath, "w", zipfile.ZIP_DEFLATED) as z:
            for root, _, files in os.walk(tmpdir):
                for fn in files:
                    full = os.path.join(root, fn)
                    rel = os.path.relpath(full, tmpdir)
                    z.write(full, rel.replace(os.sep, "/"))
        shutil.move(newpath, path)
        print("patched", os.path.basename(path), "→", footer_fmt)
    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)

if __name__ == "__main__":
    for p in sys.argv[1:]:
        patch(p)
