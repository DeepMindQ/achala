# -*- coding: utf-8 -*-
"""Remove the stale cached first paragraph inside a TOC field that duplicates the
first injected placeholder entry (docx-js field cache + placeholder injection).

Strategy: find the first TOC1 paragraph that contains the field begin+instrText+separate
runs followed by a cached <w:hyperlink>; delete that whole paragraph; re-inject the three
field-start runs at the top of the next paragraph so the field structure stays valid.
"""

import sys, zipfile, re, shutil, os, tempfile

PARA_PAT = re.compile(
    r'<w:p><w:pPr><w:pStyle w:val="TOC1"/>'
    r'(?:(?!</w:p>).)*?<w:fldChar w:fldCharType="begin"[^>]*/></w:r>'
    r'<w:r><w:instrText[^>]*>(?:(?!</w:instrText>).)*?</w:instrText></w:r>'
    r'<w:r><w:fldChar w:fldCharType="separate"/></w:r>'
    r'<w:hyperlink(?:(?!</w:hyperlink>).)*?</w:hyperlink></w:p>',
    re.S,
)
RUNS_PAT = re.compile(
    r'<w:r><w:fldChar w:fldCharType="begin"[^>]*/></w:r>'
    r'<w:r><w:instrText[^>]*>.*?</w:instrText></w:r>'
    r'<w:r><w:fldChar w:fldCharType="separate"/></w:r>',
    re.S,
)


def patch(path):
    tmpdir = tempfile.mkdtemp()
    try:
        with zipfile.ZipFile(path) as z:
            z.extractall(tmpdir)
        doc_path = os.path.join(tmpdir, "word", "document.xml")
        with open(doc_path, encoding="utf-8") as f:
            doc = f.read()

        m = PARA_PAT.search(doc)
        if not m:
            print("no stale cached TOC paragraph found - nothing to do")
            return
        para = m.group(0)
        runs_m = RUNS_PAT.search(para)
        if not runs_m:
            print("ERROR: could not extract field-start runs; aborting without change")
            sys.exit(1)
        runs = runs_m.group(0)

        rest = doc[m.end():]
        nxt = re.match(r"\s*<w:p><w:pPr>", rest)
        if not nxt:
            print("ERROR: no following TOC entry paragraph; aborting without change")
            sys.exit(1)
        # insert runs right after the next paragraph's closing </w:pPr>
        ppr_end = rest.find("</w:pPr>", nxt.end() - 1)
        if ppr_end < 0:
            print("ERROR: cannot find </w:pPr>; aborting without change")
            sys.exit(1)
        insert_at = ppr_end + len("</w:pPr>")

        new_doc = doc[: m.start()] + rest[:insert_at] + runs + rest[insert_at:]

        with open(doc_path, "w", encoding="utf-8") as f:
            f.write(new_doc)

        newpath = path + ".tmp"
        with zipfile.ZipFile(newpath, "w", zipfile.ZIP_DEFLATED) as z:
            for root, _, files in os.walk(tmpdir):
                for fn in files:
                    full = os.path.join(root, fn)
                    rel = os.path.relpath(full, tmpdir)
                    z.write(full, rel.replace(os.sep, "/"))
        shutil.move(newpath, path)
        print("deduped stale cached TOC entry in", os.path.basename(path))
    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)


if __name__ == "__main__":
    for p in sys.argv[1:]:
        patch(p)
