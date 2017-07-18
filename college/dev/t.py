from openpyxl import load_workbook
wb = load_workbook(filename='学校标识码（整合）.xlsx', read_only=True)
ws = wb.active

for row in ws.rows:
    for cell in row:
        print(cell.value)