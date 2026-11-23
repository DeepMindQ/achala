"""Polish print setup for the Achala change list workbook (content untouched)."""
import openpyxl

PATH = "/home/z/my-project/download/achala_Website_Overhaul_Change_List.xlsx"

wb = openpyxl.load_workbook(PATH)

for name in wb.sheetnames:
    ws = wb[name]
    # Landscape + fit all columns on one page width for sane printing/export
    ws.page_setup.orientation = "landscape"
    ws.page_setup.fitToWidth = 1
    ws.page_setup.fitToHeight = 0
    ws.sheet_properties.pageSetUpPr.fitToPage = True
    ws.print_options.horizontalCentered = True
    # Repeat header rows when printing multi-page sheets
    if name == "Master Change List":
        ws.print_title_rows = "4:4"
    elif name == "Audit Findings":
        ws.print_title_rows = "2:2"
    # Freeze panes on the remaining sheets for easier scrolling
    if name == "Audit Findings":
        ws.freeze_panes = "A3"
    elif name == "Roadmap":
        ws.freeze_panes = "A3"
    elif name == "Brand Reference":
        ws.freeze_panes = "A3"
    elif name == "Read Me":
        ws.freeze_panes = "A4"

wb.properties.creator = "Z.ai"
wb.save(PATH)
print("Print setup applied to:", wb.sheetnames)
