"""Count exact pages per section from the Page Inventory workbook."""
import openpyxl

wb = openpyxl.load_workbook(
    "/home/z/my-project/download/achalasolutions-website-content/achala_Soft_Page_Inventory.xlsx",
    read_only=True, data_only=True,
)
print("SHEETS:", wb.sheetnames)

# Find the sitemap sheet
for name in wb.sheetnames:
    ws = wb[name]
    print(f"\n--- {name} (dims={ws.calculate_dimension()}) ---")
    rows = ws.iter_rows(values_only=True)
    for i, row in enumerate(rows):
        if i > 4:
            break
        print(row)

# Deeper: parse the sitemap sheet, group by Section/Type column
for name in wb.sheetnames:
    ws = wb[name]
    headers = None
    data = []
    for row in ws.iter_rows(values_only=True):
        if headers is None:
            headers = [str(c) if c is not None else "" for c in row]
            continue
        if all(c is None for c in row):
            continue
        data.append(row)
    if any("URL" in h or "Page" in h for h in headers):
        print(f"\n=== PARSING {name}: headers={headers} rows={len(data)}")
        # Group by first column that looks like a section
        from collections import Counter
        col_section = None
        for j, h in enumerate(headers):
            if h.lower() in ("section", "area", "category", "type", "page type", "group"):
                col_section = j
                break
        if col_section is not None:
            c = Counter(r[col_section] for r in data)
            for k, v in c.most_common():
                print(f"  {k}: {v}")
        else:
            print("  No section column found; first 3 rows:")
            for r in data[:3]:
                print("   ", r)
