"""Dump Menu Map sheet + representative URLs from the inventory for the proposal."""
import openpyxl

wb = openpyxl.load_workbook(
    "/home/z/my-project/download/achalasolutions-website-content/achala_Soft_Page_Inventory.xlsx",
    read_only=True, data_only=True,
)

print("=== MENU MAP ===")
ws = wb["Menu Map"]
for row in ws.iter_rows(values_only=True):
    vals = [v for v in row if v is not None]
    if vals:
        print(vals)

print("\n=== SAMPLE URLS ===")
ws = wb["Sitemap Inventory"]
rows = []
header = None
for row in ws.iter_rows(values_only=True):
    if header is None:
        header = row
        continue
    if row[1] is None:
        continue
    rows.append(row)

# columns: 1=ID, 2=Section, 3..6=Menu L1..L4, 7=Page Title, 8=URL Path, 9=Template
wanted_ids = {"HOME", "SERVICES-HUB", "INDUSTRIES-HUB", "SOLUTIONS-HUB", "PLATFORMS-HUB",
              "CASE-STUDIES-HUB", "COMPANY-HUB", "APPROACH-HUB", "INSIGHTS-HUB", "CONTACT-HUB"}
seen = set()
for r in rows:
    rid = str(r[1])
    if rid in wanted_ids and rid not in seen:
        seen.add(rid)
        print(f"{rid:20s} | L1={r[3]} | {r[7]} | {r[8]} | tmpl={r[9]}")

# one example per template type
print("\n=== ONE ROW PER TEMPLATE ===")
tmpl_seen = set()
for r in rows:
    t = str(r[9])
    if t not in tmpl_seen:
        tmpl_seen.add(t)
        print(f"{t:28s} | {str(r[2]):12s} | {str(r[7])[:60]} | {r[8]}")
