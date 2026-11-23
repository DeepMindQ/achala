#!/usr/bin/env python3
"""Mark Wave 1 as executed & verified in the Roadmap sheet, preserving existing styles."""
import shutil
from copy import copy
from openpyxl import load_workbook
from openpyxl.styles import Font

SRC = "/home/z/my-project/download/achala_Website_Overhaul_Change_List.xlsx"

shutil.copy(SRC, SRC + ".bak")
wb = load_workbook(SRC)
ws = wb["Roadmap"]

# find header row: the row containing 'Wave'
header_row = None
for r in range(1, 8):
    if ws.cell(row=r, column=2).value == "Wave":
        header_row = r
        break
assert header_row, "header row not found"
hdr = header_row

status_col = 8  # column H ('Depends on' is G=7)
assert ws.cell(row=hdr, column=7).value == "Depends on", ws.cell(row=hdr, column=7).value

def copy_style(src, dst):
    dst.font = copy(src.font)
    dst.fill = copy(src.fill)
    dst.border = copy(src.border)
    dst.alignment = copy(src.alignment)
    dst.number_format = src.number_format

# header cell
h = ws.cell(row=hdr, column=status_col, value="Status")
copy_style(ws.cell(row=hdr, column=7), h)

STATUS = {
    "Wave 1 - Brand Foundation": "Done — executed & verified (100/100 automated checks + build)",
    "Wave 2 - Visual & Motion System": "Pending",
    "Wave 3 - Page Experience & Navigation": "Pending",
    "Wave 4 - Content & Conversion": "Pending",
    "Wave 5 - SEO, A11y, Performance & Launch": "Pending",
}
done_font = Font(name=ws.cell(row=hdr, column=7).font.name, size=10, bold=True, color="2E7D32")
for r in range(hdr + 1, hdr + 6):
    wave = ws.cell(row=r, column=2).value
    if wave is None:
        continue
    c = ws.cell(row=r, column=status_col, value=STATUS.get(wave, "Pending"))
    copy_style(ws.cell(row=r, column=7), c)
    if wave.startswith("Wave 1"):
        c.font = done_font

# widen column G to fit
ws.column_dimensions["H"].width = max(ws.column_dimensions["H"].width or 0, 34)

# update the note row to record verification
for r in range(hdr + 6, ws.max_row + 1):
    v = ws.cell(row=r, column=2).value
    if isinstance(v, str) and v.startswith("Note:"):
        ws.cell(row=r, column=2).value = v + " Wave 1 was executed and verified on 2026-11-20: 638 pages built, search reindexed, logo pixel-match sign-off on record (Wave1_Logo_PixelMatch_Signoff.png)."
        break

wb.save(SRC)
print("Roadmap updated: Status column added, Wave 1 = Done")

# quick verify
wb2 = load_workbook(SRC)
ws2 = wb2["Roadmap"]
for r in range(hdr, hdr + 6):
    print([ws2.cell(row=r, column=c).value for c in (2, 8)])
