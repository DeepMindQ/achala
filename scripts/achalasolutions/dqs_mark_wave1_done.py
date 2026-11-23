"""Mark all 100 Wave-1 items as Done in the Master Change List (after browser verification)."""
import openpyxl

PATH = "/home/z/my-project/download/achala_Website_Overhaul_Change_List.xlsx"
wb = openpyxl.load_workbook(PATH)
ws = wb["Master Change List"]

done = 0
for row in ws.iter_rows(min_row=5, min_col=2, max_col=12):
    id_cell = row[0]           # B: ID
    status_cell = row[10]      # L: Status
    wave_cell = row[1]         # C: Wave
    if id_cell.value and str(id_cell.value).startswith("CHG-") and wave_cell.value and str(wave_cell.value).startswith("Wave 1"):
        status_cell.value = "Done"
        done += 1

wb.save(PATH)
print(f"Marked {done} Wave-1 items as Done")
